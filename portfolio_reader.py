"""Reads a Base wallet and returns a redacted summary for the private LLM."""
from __future__ import annotations

from common import ERC20_ABI, TOKENS, env, w3


def read_portfolio() -> dict:
    client, wallet = w3(), env("TRADER_ADDRESS")
    if not wallet:
        raise RuntimeError("Missing TRADER_ADDRESS")
    holdings = {"ETH": {"amount": float(client.from_wei(client.eth.get_balance(wallet), "ether")), "address": None}}
    for symbol, meta in TOKENS.items():
        if not meta["address"]:
            continue
        raw = client.eth.contract(address=meta["address"], abi=ERC20_ABI).functions.balanceOf(wallet).call()
        holdings[symbol] = {"amount": raw / (10 ** meta["decimals"]), "address": meta["address"]}
    tracked = {symbol: round(item["amount"], 6) for symbol, item in holdings.items() if item["amount"] > 0}
    total = sum(tracked.values()) or 1.0
    weights = {symbol: round((amount / total) * 100, 2) for symbol, amount in tracked.items()}
    summary = "Tracked Base assets: " + (", ".join(f"{s} {weights[s]}% ({tracked[s]})" for s in tracked) if tracked else "none")
    return {"wallet": wallet, "holdings": holdings, "tracked": tracked, "weights": weights, "summary": summary}


if __name__ == "__main__":
    print(read_portfolio()["summary"])
