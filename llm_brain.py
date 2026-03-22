"""Privacy-first LLM routing with a deterministic fallback policy."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any
from dotenv import load_dotenv

load_dotenv()

from common import clamp, env, http_json

PROMPT = (
    "You are VeilTrader, a private Base DeFi trading agent. Never ask for wallet addresses, raw dumps, "
    "or secrets. You only receive a redacted portfolio summary. Return strict JSON with keys: action, token_in, "
    "token_out, amount_pct, fee, confidence, rationale. Only trade with confidence >= 70, amount_pct <= 5, "
    "slippage <= 1%, and a single direct USDC/WETH swap. If uncertain, return HOLD."
)


def _extract_message(data: dict[str, Any]) -> dict[str, Any]:
    content = data["choices"][0]["message"]["content"]
    return json.loads(content[content.find("{") : content.rfind("}") + 1])


def _chat(url: str, key: str, model: str, summary: str) -> dict[str, Any]:
    return _extract_message(
        http_json(
            "POST",
            url,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            json_body={
                "model": model,
                "temperature": 0.2,
                "messages": [
                    {"role": "system", "content": PROMPT},
                    {"role": "user", "content": summary},
                ],
                "response_format": {"type": "json_object"},
            },
        )
    )


def _normalize(raw: dict[str, Any], provider: str) -> dict[str, Any]:
    action = str(raw.get("action", "HOLD")).upper()
    token_in = str(raw.get("token_in", "USDC")).upper()
    token_out = str(raw.get("token_out", "WETH")).upper()
    confidence = int(float(raw.get("confidence", 0)))
    return {
        "provider": provider,
        "action": action if action in {"BUY", "SELL", "HOLD"} else "HOLD",
        "token_in": token_in,
        "token_out": token_out,
        "amount_pct": clamp(
            float(raw.get("amount_pct", 0)), 0.0, float(env("MAX_TRADE_PCT", "5"))
        ),
        "fee": int(raw.get("fee", 500))
        if int(raw.get("fee", 500)) in {100, 500, 3000, 10000}
        else 500,
        "confidence": max(0, min(confidence, 100)),
        "rationale": str(raw.get("rationale", "No rationale provided."))[:280],
    }


def _local_policy(summary: str) -> dict[str, Any]:
    # If no LLM is configured, fail closed unless one asset concentration is extreme.
    if "USDC" in summary and "WETH" not in summary:
        return {
            "action": "BUY",
            "token_in": "USDC",
            "token_out": "WETH",
            "amount_pct": 1.0,
            "fee": 500,
            "confidence": 72,
            "rationale": "Failsafe rebalance from all-cash tracked portfolio.",
        }
    if "WETH" in summary and "USDC" not in summary:
        return {
            "action": "SELL",
            "token_in": "WETH",
            "token_out": "USDC",
            "amount_pct": 1.0,
            "fee": 500,
            "confidence": 72,
            "rationale": "Failsafe rebalance from all-WETH tracked portfolio.",
        }
    return {
        "action": "HOLD",
        "token_in": "USDC",
        "token_out": "WETH",
        "amount_pct": 0.0,
        "fee": 500,
        "confidence": 0,
        "rationale": "No safe edge detected; holding.",
    }


def decide(summary: str) -> dict[str, Any]:
    providers = [
        (
            "groq",
            env("GROQ_API_KEY"),
            env("GROQ_MODEL", "llama-3.3-70b-versatile"),
            "https://api.groq.com/openai/v1/chat/completions",
        ),
        (
            "venice",
            env("VENICE_API_KEY"),
            env("VENICE_MODEL", "llama-3.3-70b"),
            env("VENICE_API_URL", "https://api.venice.ai/api/v1/chat/completions"),
        ),
        (
            "bankr",
            env("BANKR_API_KEY"),
            env("BANKR_MODEL", "gpt-4.1-mini"),
            env("BANKR_API_URL", "https://api.bankr.bot/v1/chat/completions"),
        ),
    ]
    last_error = None
    for name, key, model, url in providers:
        if not key:
            continue
        try:
            return _normalize(_chat(url, key, model, summary), name)
        except Exception as exc:
            last_error = f"{name}: {exc}"
    local = _normalize(_local_policy(summary), "local_failsafe")
    if last_error:
        local["rationale"] = (
            f"{local['rationale']} Gateway fallback after {last_error}"[:280]
        )
    return local
