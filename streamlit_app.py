"""Simple judge-facing dashboard for VeilTrader."""
from __future__ import annotations

import streamlit as st

from common import load_json

st.set_page_config(page_title="VeilTrader", page_icon="🕶️", layout="wide")
agent = load_json("agent.json", {})
log = load_json("agent_log.json", [])
registration = (agent.get("registrations") or [{}])[0]

st.title("🕶️ VeilTrader")
st.caption(agent.get("description", ""))
left, mid, right = st.columns(3)
left.metric("Agent ID", registration.get("agentId", 0))
mid.metric("Cycles", len(log))
right.metric("Latest decision", log[-1].get("decision", "N/A") if log else "N/A")
if registration.get("chainExplorer") and "PENDING" not in str(registration.get("chainExplorer")):
    st.link_button("Open ERC-8004 registration on BaseScan", registration["chainExplorer"])
if log:
    st.subheader("Autonomous log")
    st.dataframe(log[::-1], use_container_width=True)
else:
    st.info("No cycles logged yet. Run `python main.py --once` first.")
