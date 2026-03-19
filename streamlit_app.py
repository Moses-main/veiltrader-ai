"""Minimal submission dashboard for judges and demo videos."""
from __future__ import annotations
import streamlit as st
from common import load_json

st.set_page_config(page_title="VeilTrader", page_icon="🕶️", layout="wide")
agent = load_json("agent.json", {})
log = load_json("agent_log.json", [])
reg = (agent.get("registrations") or [{}])[0]
st.title("🕶️ VeilTrader")
st.write(agent.get("description", ""))
col1, col2, col3 = st.columns(3)
col1.metric("Agent ID", reg.get("agentId", 0))
col2.metric("Cycles Logged", len(log))
col3.metric("Latest Decision", log[-1]["decision"] if log else "N/A")
if reg.get("chainExplorer") and "PENDING" not in str(reg.get("chainExplorer")): st.link_button("ERC-8004 registration", reg["chainExplorer"])
if log:
    st.subheader("Recent autonomous cycles")
    st.dataframe(log[::-1], use_container_width=True)
