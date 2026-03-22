#!/usr/bin/env python3
"""
VeilTrader AI - Core Module
Combines LLM Brain + Portfolio Reader into a single compact module.
Privacy-first: never logs raw portfolio data.
"""

import os, json, time, random, requests
from web3 import Web3
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


# ============ LLM BRAIN ============
class LLMBrain:
    SYSTEM_PROMPT = """You are VeilTrader's private AI brain. Make risk-aware DeFi trading decisions.
    PRIVACY RULE: Never log, retain, or reveal portfolio data, addresses, or balances.
    Output format:
    DECISION: [BUY/SELL/HOLD]
    CONFIDENCE: [0-100] (≥70 to execute)
    REASONING: [brief explanation]
    RISK: [LOW/MEDIUM/HIGH]"""

    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.venice_key = os.getenv("VENICE_API_KEY")
        self.bankr_key = os.getenv("BANKR_API_KEY")
        self.demo = os.getenv("DEMO_MODE", "false").lower() == "true"
        self.groq = Groq(api_key=self.groq_key) if self.groq_key else None

    def query(self, prompt):
        for provider in ["_groq", "_venice", "_bankr", "_demo"]:
            try:
                resp = getattr(self, provider)(prompt)
                return self._parse(resp)
            except:
                continue
        raise Exception("All LLM providers failed")

    def _groq(self, prompt):
        return (
            self.groq.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=500,
            )
            .choices[0]
            .message.content
        )

    def _venice(self, prompt):
        r = requests.post(
            "https://api.venice.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.venice_key}"},
            json={
                "model": "llama-3.3-70b",
                "messages": [
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.3,
                "max_tokens": 500,
            },
            timeout=10,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

    def _bankr(self, prompt):
        r = requests.post(
            "https://api.bankr.ai/v1/llm/generate",
            headers={"Authorization": f"Bearer {self.bankr_key}"},
            json={
                "prompt": f"{self.SYSTEM_PROMPT}\n\nUser: {prompt}\nAssistant:",
                "max_tokens": 500,
                "temperature": 0.3,
            },
            timeout=10,
        )
        r.raise_for_status()
        return r.json()["text"]

    def _demo(self, prompt):
        print("DEMO_MODE: Using simulated decision")
        decisions = ["BUY", "HOLD", "SELL"]
        d = random.choice(decisions)
        c = random.randint(65, 92)
        return f"DECISION: {d}\nCONFIDENCE: {c}\nREASONING: Market conditions {'favorable' if d == 'BUY' else 'neutral'}.\nRISK: MEDIUM"

    def _parse(self, response):
        lines = {
            k.split(":")[0].strip().upper(): k.split(":", 1)[1].strip()
            for k in response.split("\n")
            if ":" in k
        }
        d = lines.get("DECISION", "HOLD")
        c = int(lines.get("CONFIDENCE", 70))
        return {
            "decision": d if d in ["BUY", "SELL", "HOLD"] else "HOLD",
            "confidence": c,
            "reasoning": lines.get("REASONING", ""),
            "risk": lines.get("RISK", "MEDIUM"),
        }


def get_trading_decision(portfolio_summary):
    return LLMBrain().query(f"Analyze: {portfolio_summary}\nProvide trading decision.")


# ============ PORTFOLIO READER ============
TOKENS = {
    "USDC": {
        "addr": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "dec": 6,
        "cg": "usd-coin",
    },
    "WETH": {
        "addr": "0x4200000000000000000000000000000000000006",
        "dec": 18,
        "cg": "weth",
    },
    "USDT": {
        "addr": "0xDcEF968D448955473Cd7Cb1cFf81EB52e43FA5CE",
        "dec": 6,
        "cg": "tether",
    },
    "DAI": {
        "addr": "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
        "dec": 18,
        "cg": "dai",
    },
    "WSTETH": {
        "addr": "0x1F32b1C2345538c0c6f582fCB022739c4A194Ebb",
        "dec": 18,
        "cg": "wrapped-steth",
    },
    "STETH": {
        "addr": "0xc58d696aBd4633fC27Dd9D5C338242Cc62dC82A7",
        "dec": 18,
        "cg": "staked-ether",
    },
}


def get_portfolio_summary(address):
    if not address:
        return "No wallet address"
    try:
        w3 = Web3(
            Web3.HTTPProvider(os.getenv("BASE_RPC_URL", "https://mainnet.base.org"))
        )
        if not w3.is_connected():
            return "RPC connection failed"

        prices = {
            s: requests.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids={v['cg']}&vs_currencies=usd",
                timeout=5,
            )
            .json()
            .get(v["cg"], {})
            .get("usd", 1 if s in ["USDC", "USDT", "DAI"] else 3000)
            for s, v in TOKENS.items()
        }

        total = sum(
            w3.eth.contract(
                Web3.to_checksum_address(v["addr"]),
                abi=[
                    {
                        "inputs": [{"name": "_o", "type": "address"}],
                        "name": "balanceOf",
                        "outputs": [{"name": "", "type": "uint256"}],
                        "type": "function",
                    }
                ],
            )
            .functions.balanceOf(Web3.to_checksum_address(address))
            .call()
            / (10 ** v["dec"])
            * prices[s]
            for s, v in TOKENS.items()
        )

        ranges = [
            (0, 1000, "$0-$1k"),
            (1000, 5000, "$1k-$5k"),
            (5000, 10000, "$5k-$10k"),
            (10000, 50000, "$10k-$50k"),
            (50000, 100000, "$50k-$100k"),
            (100000, float("inf"), "$100k+"),
        ]
        val_label = next((r for mn, mx, r in ranges if mn <= total < mx), "$0-$1k")

        steth_bal = sum(
            w3.eth.contract(
                Web3.to_checksum_address(TOKENS[s]["addr"]),
                abi=[
                    {
                        "inputs": [{"name": "_o", "type": "address"}],
                        "name": "balanceOf",
                        "outputs": [{"name": "", "type": "uint256"}],
                        "type": "function",
                    }
                ],
            )
            .functions.balanceOf(Web3.to_checksum_address(address))
            .call()
            / (10 ** TOKENS[s]["dec"])
            for s in ["STETH", "WSTETH"]
            if s in TOKENS
        )
        lido_info = (
            f"\nLIDO: ~${steth_bal * prices.get('WETH', 3000) * 0.05 / 365:.2f}/day yield from {steth_bal:.4f} stETH"
            if steth_bal > 0 and os.getenv("LIDO_MODE") == "true"
            else ""
        )

        return f"Portfolio: Value {val_label}, {len(TOKENS)} tokens tracked{lido_info}"
    except Exception as e:
        return f"Portfolio error: {type(e).__name__}"


if __name__ == "__main__":
    addr = os.getenv("WALLET_ADDRESS", "0x0")
    print(f"Summary: {get_portfolio_summary(addr)}")
    print(f"Decision: {get_trading_decision(get_portfolio_summary(addr))}")
