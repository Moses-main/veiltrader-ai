#!/usr/bin/env python3
"""
VeilTrader AI - Minimal Streamlit Dashboard
Clean, modern UI for demo and monitoring.
"""

import streamlit as st
import json
import time
import os

st.set_page_config(page_title="VeilTrader AI", page_icon="🛡️", layout="wide")

# Dark theme CSS
st.markdown(
    """
<style>
    .stApp { background: #0d1117; }
    .metric-card {
        background: linear-gradient(135deg, #161b22 0%, #21262d 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #58a6ff; }
    .metric-label { font-size: 0.875rem; color: #8b949e; text-transform: uppercase; letter-spacing: 0.05em; }
    .trade-buy { color: #3fb950; font-size: 1.5rem; font-weight: 600; }
    .trade-sell { color: #f85149; font-size: 1.5rem; font-weight: 600; }
    .trade-hold { color: #d29922; font-size: 1.5rem; font-weight: 600; }
    .status-dot { height: 10px; width: 10px; border-radius: 50%; display: inline-block; margin-right: 8px; }
    .status-online { background: #3fb950; box-shadow: 0 0 8px #3fb950; }
    .status-offline { background: #f85149; }
    .status-warning { background: #d29922; }
    .log-item {
        background: #161b22;
        border-left: 3px solid #58a6ff;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        font-family: 'SF Mono', Monaco, monospace;
        font-size: 0.85rem;
    }
    .prize-bar { height: 6px; background: #21262d; border-radius: 3px; margin-top: 4px; }
    .prize-fill { height: 100%; border-radius: 3px; transition: width 0.3s ease; }
    h1, h2, h3 { color: #c9d1d9 !important; }
    .stMetric { background: transparent !important; }
    .stMetric > div { background: transparent !important; }
</style>
""",
    unsafe_allow_html=True,
)


def load_logs():
    try:
        if os.path.exists("agent_log.json"):
            return json.load(open("agent_log.json")).get("logs", [])
    except:
        pass
    return []


def load_agent_info():
    try:
        if os.path.exists("agent.json"):
            return json.load(open("agent.json"))
    except:
        pass
    return {}


def format_time(ts):
    return time.strftime("%H:%M:%S", time.localtime(ts))


def get_status_color(event):
    if "executed" in event or "success" in event:
        return "#3fb950"
    if "failed" in event or "error" in event:
        return "#f85149"
    return "#58a6ff"


# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="font-size: 2.5rem; margin: 0;">🛡️ VeilTrader AI</h1>
            <p style="color: #8b949e; font-size: 1.1rem; margin-top: 0.5rem;">
                Autonomous Privacy-First DeFi Trading Agent
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

# Status bar
agent_info = load_agent_info()
logs = load_logs()

status_col1, status_col2, status_col3, status_col4, status_col5 = st.columns(5)

with status_col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Network</div>
            <div class="metric-value" style="font-size: 1rem;">{agent_info.get("network", "Base")}</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

with status_col2:
    trades = len([l for l in logs if l.get("event") == "trade_executed"])
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Total Trades</div>
            <div class="metric-value">{trades}</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

with status_col3:
    revenue = sum(
        l.get("usdc_amount", 0) for l in logs if l.get("event") == "x402_request_served"
    )
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">x402 Revenue</div>
            <div class="metric-value">${revenue:.2f}</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

with status_col4:
    status = (
        "Online"
        if os.getenv("EMERGENCY_STOP", "false").lower() != "true"
        else "Stopped"
    )
    color = "#3fb950" if status == "Online" else "#f85149"
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Status</div>
            <div style="color: {color}; font-weight: 600;">
                <span class="status-dot {"status-online" if status == "Online" else "status-offline"}"></span>
                {status}
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

with status_col5:
    lido = "Active" if os.getenv("LIDO_MODE", "false").lower() == "true" else "Off"
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">LIDO Mode</div>
            <div style="color: #a371f7; font-weight: 600;">{lido}</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# Main content
main_col, side_col = st.columns([2, 1])

with main_col:
    st.subheader("📊 Live Activity")

    # Recent activity
    recent = logs[-10:] if logs else []

    if recent:
        for log in reversed(recent):
            event = log.get("event", "")
            ts = format_time(log.get("timestamp", 0))
            color = get_status_color(event)

            # Format content based on event type
            if event == "trade_executed":
                content = f"**{log.get('decision', 'N/A')}** {log.get('tokenIn', '')} → {log.get('tokenOut', '')}"
                tx = log.get("txHash", "")
                if tx:
                    content += f" • [View Tx](https://sepolia.basescan.org/tx/{tx})"
            elif event == "x402_request_served":
                content = f"Signal served: **{log.get('recommendation', 'N/A')}** ({log.get('confidence', 0)}%)"
            elif event == "reputation_feedback_posted":
                content = f"Rating: **{log.get('rating', 0)}/5** • {log.get('feedback', '')[:50]}"
            elif event == "error":
                content = f"❌ {log.get('error', 'Unknown error')[:80]}"
            else:
                content = str(log)[:100]

            st.markdown(
                f"""
                <div class="log-item" style="border-left-color: {color};">
                    <div style="display: flex; justify-content: space-between; color: #8b949e;">
                        <span style="text-transform: uppercase; font-size: 0.75rem; font-weight: 600;">{event.replace("_", " ")}</span>
                        <span>{ts}</span>
                    </div>
                    <div style="margin-top: 4px; color: #c9d1d9;">{content}</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No activity yet. Start the agent to see live updates.")

with side_col:
    st.subheader("🎯 Prize Tracks")

    prizes = [
        ("Venice: Private Agents", "$3,000", 0.9, "#a371f7"),
        ("Uniswap: Agentic Finance", "$2,500", 0.8, "#58a6ff"),
        ("Protocol Labs: ERC-8004", "$4,000", 0.85, "#3fb950"),
        ("Synthesis Open Track", "$25k+", 0.8, "#f0883e"),
        ("OpenServ: Ship Something Real", "$2,500", 0.7, "#db61a2"),
    ]

    for name, amount, progress, color in prizes:
        st.markdown(
            f"""
            <div style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #c9d1d9; font-size: 0.875rem;">{name}</span>
                    <span style="color: #8b949e; font-size: 0.75rem;">{amount}</span>
                </div>
                <div class="prize-bar">
                    <div class="prize-fill" style="width: {progress * 100}%; background: {color};"></div>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.subheader("⚙️ Quick Actions")

    if st.button("🧪 Request Signal (Demo)", use_container_width=True):
        signals = [
            ("BUY", "Accumulation pattern detected", 85),
            ("SELL", "Profit taking recommended", 78),
            ("HOLD", "Awaiting clearer signals", 72),
        ]
        sig = signals[int(time.time()) % 3]
        st.success(f"**{sig[0]}** - {sig[1]} (Confidence: {sig[2]}%)")

    lido_toggle = st.toggle(
        "🔐 LIDO Mode", os.getenv("LIDO_MODE", "false").lower() == "true"
    )
    if lido_toggle:
        st.success("LIDO Mode enabled - Yield-preserving strategy active")
    else:
        st.info("Standard trading mode")

# Footer
st.markdown("---")
st.markdown(
    """
<div style="text-align: center; color: #8b949e; padding: 1rem;">
    <span>🛡️ VeilTrader AI</span> • 
    <span>Built for Synthesis Hackathon 2026</span> • 
    <span>Autonomous • Privacy-First • On-Chain</span>
</div>
""",
    unsafe_allow_html=True,
)

# Auto-refresh
time.sleep(5)
st.rerun()
