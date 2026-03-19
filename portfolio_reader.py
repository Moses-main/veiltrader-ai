"""Read a Base wallet portfolio without logging raw balances."""
from __future__ import annotations
from common import ERC20_ABI, TOKENS, env, w3

def read_portfolio() -> dict:
    client = w3(); wallet = env("TRADER_ADDRESS")
    if not wallet: raise RuntimeError("Missing TRADER_ADDRESS")
    holdings = {}
    eth = float(client.from_wei(client.eth.get_balance(wallet), "ether"))
    holdings["ETH"] = {"amount": eth, "address": None}
    for symbol, meta in TOKENS.items():
        if not meta["address"]: continue
        token = client.eth.contract(address=meta["address"], abi=ERC20_ABI)
        raw = token.functions.balanceOf(wallet).call()
        holdings[symbol] = {"amount": raw / (10 ** meta["decimals"]), "address": meta["address"]}
    liquid = {k: round(v["amount"], 6) for k, v in holdings.items() if v["amount"] > 0}
    summary = "Portfolio summary only: " + ", ".join(f"{k}={v}" for k, v in liquid.items()) if liquid else "Portfolio summary only: no tracked balances."
    return {"wallet": wallet, "holdings": holdings, "summary": summary}

if __name__ == "__main__":
    print(read_portfolio()["summary"])
