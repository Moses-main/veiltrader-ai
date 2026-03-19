"""Autonomous VeilTrader loop: read portfolio, reason privately, trade once, then publish proof."""
from __future__ import annotations
import argparse, os, time
from common import env, load_json, now_iso, save_json
from llm_brain import decide
from portfolio_reader import read_portfolio
from reputation_manager import post_trade_feedback
from uniswap_executor import execute_trade

DESCRIPTION = "VeilTrader is a fully autonomous, privacy-first AI trading agent on Base (Ethereum). It privately analyzes any user’s DeFi portfolio using a no-data-retention LLM (Venice/Groq/Bankr fallback), makes risk-aware trade decisions, executes real Uniswap V3 swaps using the official Uniswap Developer Platform API + on-chain router, posts reputation updates to the ERC-8004 Reputation Registry, and only publishes verifiable transaction proofs. After one-time setup it runs forever with zero human intervention. Built to win Venice 'Private Agents, Trusted Actions', Uniswap 'Agentic Finance', Bankr 'Best LLM Gateway', Protocol Labs 'Agents With Receipts — ERC-8004' + 'Let the Agent Cook', and Synthesis Open Track."

def emergency_stop() -> bool:
    return env("EMERGENCY_STOP", "false").lower() == "true" or os.path.exists(env("EMERGENCY_STOP_FILE", ".emergency_stop"))

def append_log(entry: dict) -> None:
    log = load_json("agent_log.json", [])
    log.append(entry)
    save_json("agent_log.json", log[-250:])

def bankr_budget(log: list[dict]) -> float:
    budget = float(env("BANKR_BUDGET_USD", "0"))
    for row in log:
        budget += max(float(row.get("estimated_profit_usd", 0)), 0) * 0.05
    return round(budget, 2)

def run_cycle() -> dict:
    if emergency_stop(): return {"timestamp": now_iso(), "reasoning_summary": "Emergency stop active.", "decision": "HALT", "trade_tx": None, "reputation_tx": None, "bankr_budget_usd": bankr_budget(load_json("agent_log.json", []))}
    portfolio = read_portfolio()
    decision = decide(portfolio["summary"] + " Only output one safe action.")
    trade = execute_trade(decision, portfolio)
    rep = None
    if trade.get("status") == "submitted":
        agent_id = int(load_json("agent.json", {}).get("registrations", [{}])[0].get("agentId", 0))
        if agent_id > 0:
            rep = post_trade_feedback(agent_id, trade["tx_hash"])
    return {
        "timestamp": now_iso(),
        "reasoning_summary": decision.get("rationale", "No rationale."),
        "decision": decision.get("action", "HOLD"),
        "trade_tx": trade.get("tx_hash"),
        "trade_basescan": trade.get("basescan"),
        "reputation_tx": None if not rep else rep.get("tx_hash"),
        "reputation_basescan": None if not rep else rep.get("basescan"),
        "llm_provider": decision.get("provider"),
        "bankr_budget_usd": bankr_budget(load_json("agent_log.json", [])),
    }

def main(run_once: bool = False) -> None:
    print(DESCRIPTION)
    while True:
        try: append_log(run_cycle())
        except Exception as exc: append_log({"timestamp": now_iso(), "reasoning_summary": f"Cycle error: {exc}", "decision": "ERROR", "trade_tx": None, "reputation_tx": None, "bankr_budget_usd": bankr_budget(load_json("agent_log.json", []))})
        if run_once: break
        time.sleep(int(env("SLEEP_SECONDS", "3600")))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="run one cycle for smoke tests")
    main(parser.parse_args().once)
