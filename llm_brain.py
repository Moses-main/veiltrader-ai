"""Privacy-first LLM decision engine with Groq -> Venice -> Bankr fallback."""
from __future__ import annotations
import json
from typing import Any
from common import env, http_json

PROMPT = (
    "You are VeilTrader, a private Base DeFi trading agent. Never request wallet addresses, "
    "private keys, or raw ledger dumps. Use only the provided high-level portfolio summary. "
    "Return compact JSON with action in {BUY,SELL,HOLD}, token_in, token_out, amount_pct, fee, confidence, rationale. "
    "Only propose a trade if confidence is >= 70, amount_pct <= 5, slippage <= 1%, and exactly one trade is enough. "
    "If uncertain, return HOLD."
)

def _chat(url: str, key: str, model: str, summary: str) -> dict[str, Any]:
    data = http_json("POST", url, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, json_body={
        "model": model,
        "temperature": 0.2,
        "messages": [{"role": "system", "content": PROMPT}, {"role": "user", "content": summary}],
        "response_format": {"type": "json_object"},
    })
    content = data["choices"][0]["message"]["content"]
    return json.loads(content)

def decide(summary: str) -> dict[str, Any]:
    providers = [
        ("groq", env("GROQ_API_KEY"), env("GROQ_MODEL", "openai/gpt-oss-20b"), "https://api.groq.com/openai/v1/chat/completions"),
        ("venice", env("VENICE_API_KEY"), env("VENICE_MODEL", "llama-3.3-70b"), env("VENICE_API_URL", "https://api.venice.ai/api/v1/chat/completions")),
        ("bankr", env("BANKR_API_KEY"), env("BANKR_MODEL", "gpt-4.1-mini"), env("BANKR_API_URL", "https://api.bankr.bot/v1/chat/completions")),
    ]
    last_error = None
    for name, key, model, url in providers:
        if not key: continue
        try:
            out = _chat(url, key, model, summary)
            out["provider"] = name
            out["action"] = str(out.get("action", "HOLD")).upper()
            out["confidence"] = int(float(out.get("confidence", 0)))
            out["amount_pct"] = min(float(out.get("amount_pct", 0)), float(env("MAX_TRADE_PCT", "5")))
            out["fee"] = int(out.get("fee", 500)) if int(out.get("fee", 500)) in (100, 500, 3000, 10000) else 500
            return out if out["action"] in {"BUY", "SELL", "HOLD"} else {"action": "HOLD", "provider": name, "rationale": "invalid action"}
        except Exception as exc:
            last_error = f"{name}: {exc}"
    return {"action": "HOLD", "provider": "local_failsafe", "confidence": 0, "amount_pct": 0, "fee": 500, "rationale": last_error or "No LLM configured."}
