"""Autonomous VeilTrader runtime loop."""
from __future__ import annotations

import argparse
import os
import time

from common import env, env_bool, load_json, now_iso, save_json
from llm_brain import decide
from portfolio_reader import read_portfolio
from reputation_manager import post_trade_feedback
from uniswap_executor import execute_trade

DESCRIPTION = "VeilTrader is a fully autonomous, privacy-first AI trading agent on Base (Ethereum). It privately analyzes any user’s DeFi portfolio using a no-data-retention LLM (Venice/Groq/Bankr fallback), makes risk-aware trade decisions, executes real Uniswap V3 swaps using the official Uniswap Developer Platform API + on-chain router, posts reputation updates to the ERC-8004 Reputation Registry, and only publishes verifiable transaction proofs. After one-time setup it runs forever with zero human intervention. Built to win Venice 'Private Agents, Trusted Actions', Uniswap 'Agentic Finance', Bankr 'Best LLM Gateway', Protocol Labs 'Agents With Receipts — ERC-8004' + 'Let the Agent Cook', and Synthesis Open Track."


def emergency_stop() -> bool:
    return env_bool("EMERGENCY_STOP") or os.path.exists(env("EMERGENCY_STOP_FILE", ".emergency_stop"))


def append_log(entry: dict) -> None:
    history = load_json("agent_log.json", [])
    history.append(entry)
    save_json("agent_log.json", history[-250:])


def bankr_budget() -> float:
    budget = float(env("BANKR_BUDGET_USD", "0"))
    for item in load_json("agent_log.json", []):
        budget += max(float(item.get("estimated_profit_usd", 0) or 0), 0) * 0.05
    return round(budget, 2)


def agent_id() -> int:
    return int(load_json("agent.json", {}).get("registrations", [{}])[0].get("agentId", 0))


def run_cycle() -> dict:
    if emergency_stop():
        return {"timestamp": now_iso(), "reasoning_summary": "Emergency stop active.", "decision": "HALT", "trade_status": "blocked", "trade_tx": None, "reputation_status": "skipped", "reputation_tx": None, "bankr_budget_usd": bankr_budget()}
    portfolio = read_portfolio()
    decision = decide(portfolio["summary"] + " Keep the answer private and conservative.")
    trade = execute_trade(decision, portfolio)
    reputation = {"status": "skipped"}
    if trade.get("status") == "submitted" and agent_id() > 0:
        reputation = post_trade_feedback(agent_id(), trade["tx_hash"])
    return {
        "timestamp": now_iso(),
        "reasoning_summary": decision.get("rationale", "No rationale provided."),
        "decision": decision.get("action", "HOLD"),
        "llm_provider": decision.get("provider"),
        "trade_status": trade.get("status"),
        "trade_tx": trade.get("tx_hash"),
        "trade_basescan": trade.get("basescan"),
        "reputation_status": reputation.get("status"),
        "reputation_tx": reputation.get("tx_hash"),
        "reputation_basescan": reputation.get("basescan"),
        "bankr_budget_usd": bankr_budget(),
    }


def main(run_once: bool = False) -> None:
    print(DESCRIPTION)
    while True:
        try:
            append_log(run_cycle())
        except Exception as exc:
            append_log({"timestamp": now_iso(), "reasoning_summary": f"Cycle error: {exc}", "decision": "ERROR", "trade_status": "error", "trade_tx": None, "reputation_status": "skipped", "reputation_tx": None, "bankr_budget_usd": bankr_budget()})
        if run_once:
            break
        time.sleep(int(env("SLEEP_SECONDS", "3600")))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="run one autonomous cycle")
    parser.add_argument("--dry-run", action="store_true", help="quote-only cycle; do not submit swaps")
    args = parser.parse_args()
    if args.dry_run:
        os.environ["DRY_RUN"] = "true"
    main(args.once or args.dry_run)
