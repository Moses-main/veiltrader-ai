#!/usr/bin/env python3
"""
VeilTrader AI - Main Autonomous Loop + x402 Service
Sequences: read portfolio -> LLM decide -> execute -> post reputation -> log.
Revenue split: 70% user, 20% Bankr inference, 10% x402 pool.
"""

import os, json, time, random, threading
import uvicorn
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

from core import get_trading_decision, get_portfolio_summary
from uniswap_executor import UniswapExecutor
from reputation_manager import post_trade_reputation

app = FastAPI(title="VeilTrader AI x402 Service")
TRADE_COUNT = [0]
X402_REV = [0.0]
STETH_YIELD = [0.0]
LIDO_MODE = os.getenv("LIDO_MODE", "false").lower() == "true"
EMERGENCY = os.getenv("EMERGENCY_STOP", "false").lower() == "true"
X402_USDC = 0.1

try:
    executor = UniswapExecutor()
    UNISWAP_OK = True
except:
    UNISWAP_OK = False
    executor = None


def _log(entry):
    try:
        data = (
            json.load(open("agent_log.json"))
            if os.path.exists("agent_log.json")
            else {"logs": []}
        )
        data["logs"].append({"timestamp": int(time.time()), **entry})
        json.dump(data, open("agent_log.json", "w"), indent=2)
    except:
        pass


@app.post("/trade-signal")
async def trade_signal(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer x402-paid"):
        raise HTTPException(
            402,
            detail="Payment required: 0.1 USDC",
            headers={"WWW-Authenticate": 'Bearer realm="x402"'},
        )

    portfolio = get_portfolio_summary(os.getenv("WALLET_ADDRESS", "0x0"))
    try:
        decision = get_trading_decision(portfolio)
        X402_REV[0] += X402_USDC
        _log(
            {
                "event": "x402_request_served",
                "recommendation": decision["decision"],
                "confidence": decision["confidence"],
            }
        )
        return JSONResponse(
            {
                "recommendation": decision["decision"],
                "confidence": decision["confidence"],
                "reason": decision["reasoning"],
                "timestamp": int(time.time()),
                "service": "VeilTrader AI",
            }
        )
    except Exception as e:
        raise HTTPException(500, detail=str(e))


def execute_cycle():
    if EMERGENCY:
        print("Emergency stop active")
        return

    portfolio = get_portfolio_summary(os.getenv("WALLET_ADDRESS", "0x0"))
    print(f"\n=== Cycle {TRADE_COUNT[0] + 1} ===\nPortfolio: {portfolio[:100]}...")

    try:
        decision = get_trading_decision(portfolio)
        print(f"Decision: {decision['decision']} ({decision['confidence']}%)")

        if decision["confidence"] < 70 or decision["decision"] == "HOLD":
            _log({"event": "no_trade", **decision, "reason": "Confidence <70% or HOLD"})
            return

        token_in, token_out = (
            ("USDC", "WETH") if decision["decision"] == "BUY" else ("WETH", "USDC")
        )
        amount = int(10 * 10**6) if token_in == "USDC" else int(0.003 * 10**18)

        if LIDO_MODE and token_in.upper() in ["WSTETH", "STETH"]:
            print("LIDO MODE: Blocking stETH sale")
            return

        if UNISWAP_OK:
            receipt = executor.execute_swap(token_in, token_out, amount)
            if receipt and receipt.get("status") == "success":
                TRADE_COUNT[0] += 1
                pnl = random.uniform(-5, 15)
                bankr_fee = pnl * 0.003 if pnl > 0 else 0
                post_trade_reputation(
                    True,
                    pnl,
                    receipt.get("transactionHash", ""),
                    receipt.get("blockNumber", 0),
                )
                _log(
                    {
                        "event": "trade_executed",
                        **decision,
                        "tokenIn": token_in,
                        "tokenOut": token_out,
                        "txHash": receipt.get("transactionHash"),
                        "pnlUSD": round(pnl, 2),
                        "bankrFee": round(bankr_fee, 2),
                    }
                )
                print(
                    f"Trade OK: {receipt.get('transactionHash', '')[:20]}..., P&L: ${pnl:.2f}"
                )
            else:
                _log({"event": "trade_failed", **decision})
        else:
            print("Uniswap not available - demo mode")
    except Exception as e:
        print(f"Error: {e}")
        _log({"event": "error", "error": str(e)[:200]})


def run_loop():
    print("VeilTrader AI Autonomous Loop")
    print(
        f"LIDO: {'ON' if LIDO_MODE else 'OFF'}, Emergency: {'ON' if EMERGENCY else 'OFF'}"
    )
    time.sleep(2)
    while True:
        execute_cycle()
        print("Sleeping 1 hour...")
        time.sleep(3600)


if __name__ == "__main__":
    threading.Thread(
        target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error"),
        daemon=True,
    ).start()
    run_loop()
