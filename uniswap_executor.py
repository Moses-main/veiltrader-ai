"""Uniswap quote + exactInputSingle execution with hard safety rails."""
from __future__ import annotations

import time
from typing import Any

from common import BASE_CHAIN_ID, ERC20_ABI, TOKENS, UNISWAP_V3_ROUTER, USDC, WETH, basescan_tx, clamp, env, env_bool, gas_price_gwei, http_json, send_tx, w3

ROUTER_ABI = [{"name": "exactInputSingle", "type": "function", "stateMutability": "payable", "inputs": [{"components": [{"name": "tokenIn", "type": "address"}, {"name": "tokenOut", "type": "address"}, {"name": "fee", "type": "uint24"}, {"name": "recipient", "type": "address"}, {"name": "deadline", "type": "uint256"}, {"name": "amountIn", "type": "uint256"}, {"name": "amountOutMinimum", "type": "uint256"}, {"name": "sqrtPriceLimitX96", "type": "uint160"}], "name": "params", "type": "tuple"}], "outputs": [{"type": "uint256"}]}]
PAIR = {"USDC": USDC, "WETH": WETH}


def _quote(wallet: str, token_in: str, token_out: str, amount: int) -> dict[str, Any]:
    api_key = env("UNISWAP_API_KEY")
    if not api_key:
        raise RuntimeError("Missing UNISWAP_API_KEY")
    return http_json(
        "POST",
        env("UNISWAP_QUOTE_URL", "https://trade-api.gateway.uniswap.org/v1/quote"),
        headers={"x-api-key": api_key, "Content-Type": "application/json"},
        json_body={
            "type": "EXACT_INPUT",
            "amount": str(amount),
            "tokenInChainId": BASE_CHAIN_ID,
            "tokenOutChainId": BASE_CHAIN_ID,
            "tokenIn": token_in,
            "tokenOut": token_out,
            "swapper": wallet,
            "generatePermitAsTransaction": False,
            "slippageTolerance": int(env("MAX_SLIPPAGE_BPS", "100")),
            "routingPreference": "BEST_PRICE",
            "protocols": ["V3"],
            "urgency": "urgent",
        },
    )


def _pick_quote_amount(quote: dict[str, Any]) -> int:
    for path in [("quote", "output", "amount"), ("quote", "output", "endAmount"), ("quote", "quote", "amountOut"), ("quote", "outAmount"), ("amountOut",)]:
        node: Any = quote
        for key in path:
            node = node.get(key) if isinstance(node, dict) else None
        if node not in (None, ""):
            return int(str(node))
    raise RuntimeError("Unrecognized Uniswap quote payload")


def execute_trade(decision: dict[str, Any], portfolio: dict[str, Any]) -> dict[str, Any]:
    if decision.get("action") == "HOLD" or decision.get("confidence", 0) < 70:
        return {"status": "skipped", "reason": "No high-confidence trade."}
    token_in, token_out = decision.get("token_in", "USDC").upper(), decision.get("token_out", "WETH").upper()
    if token_in not in PAIR or token_out not in PAIR or token_in == token_out:
        return {"status": "skipped", "reason": "Only direct USDC/WETH swaps are enabled."}
    pct = clamp(float(decision.get("amount_pct", 0.0)), 0.0, float(env("MAX_TRADE_PCT", "5"))) / 100
    amount = portfolio["holdings"].get(token_in, {}).get("amount", 0.0) * pct
    amount_raw = int(amount * (10 ** TOKENS[token_in]["decimals"]))
    if amount_raw <= 0:
        return {"status": "skipped", "reason": f"No {token_in} available."}
    client, wallet = w3(), portfolio["wallet"]
    quote = _quote(wallet, PAIR[token_in], PAIR[token_out], amount_raw)
    quoted_out = _pick_quote_amount(quote)
    min_out = int(quoted_out * (1 - int(env("MAX_SLIPPAGE_BPS", "100")) / 10_000))
    if env_bool("DRY_RUN"):
        return {"status": "dry_run", "quote_id": quote.get("requestId"), "amount_in": round(amount, 6), "min_out_raw": str(min_out)}
    token = client.eth.contract(address=PAIR[token_in], abi=ERC20_ABI)
    if token.functions.allowance(wallet, UNISWAP_V3_ROUTER).call() < amount_raw:
        approval = send_tx(client, token.functions.approve(UNISWAP_V3_ROUTER, amount_raw).build_transaction({"from": wallet}))
        client.eth.wait_for_transaction_receipt(approval, timeout=600)
    router = client.eth.contract(address=UNISWAP_V3_ROUTER, abi=ROUTER_ABI)
    params = (PAIR[token_in], PAIR[token_out], int(decision.get("fee", 500)), wallet, int(time.time()) + 600, amount_raw, min_out, 0)
    built = router.functions.exactInputSingle(params).build_transaction({"from": wallet})
    gas_eth = float(client.from_wei(client.eth.estimate_gas(built) * client.eth.gas_price, "ether"))
    if gas_eth > float(env("MAX_GAS_ETH", "0.005")):
        return {"status": "skipped", "reason": f"Gas {gas_eth:.6f} ETH too high at {gas_price_gwei(client):.3f} gwei."}
    tx_hash = send_tx(client, built)
    return {"status": "submitted", "tx_hash": tx_hash, "basescan": basescan_tx(tx_hash), "quote_id": quote.get("requestId"), "amount_in": round(amount, 6), "min_out_raw": str(min_out)}
