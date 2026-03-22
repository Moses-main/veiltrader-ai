#!/usr/bin/env python3
"""
VeilTrader AI - Professional Trading Dashboard
Real-time portfolio monitoring and trading control.
"""

import streamlit as st
import json
import time
import os
import requests
from datetime import datetime

st.set_page_config(
    page_title="VeilTrader | Trading Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Professional dark theme CSS
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp { background: #0a0e17; }
    
    /* Hide default streamlit elements */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #1a1f2e; }
    ::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 3px; }
    
    /* Main cards */
    .main-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #141824 100%);
        border: 1px solid #2d3748;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }
    
    /* Portfolio card */
    .portfolio-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
    }
    
    /* Token balance */
    .token-balance {
        display: flex;
        align-items: center;
        padding: 16px;
        background: rgba(59, 130, 246, 0.05);
        border-radius: 12px;
        margin: 8px 0;
    }
    
    .token-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        margin-right: 16px;
    }
    
    .token-name {
        font-size: 14px;
        color: #94a3b8;
        font-weight: 500;
    }
    
    .token-value {
        font-size: 24px;
        font-weight: 700;
        color: #f1f5f9;
    }
    
    .token-usd {
        font-size: 14px;
        color: #64748b;
    }
    
    /* Price change indicators */
    .price-up { color: #22c55e; }
    .price-down { color: #ef4444; }
    
    /* Status indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .status-active {
        background: rgba(34, 197, 94, 0.15);
        color: #22c55e;
    }
    
    .status-inactive {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Trade signal card */
    .signal-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #0c1929 100%);
        border: 1px solid #1e40af;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
    }
    
    .signal-action {
        font-size: 48px;
        font-weight: 800;
        margin: 16px 0;
    }
    
    .signal-buy { color: #22c55e; }
    .signal-sell { color: #ef4444; }
    .signal-hold { color: #f59e0b; }
    
    .confidence-bar {
        height: 8px;
        background: #1e293b;
        border-radius: 4px;
        overflow: hidden;
        margin: 16px 0;
    }
    
    .confidence-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    
    /* Transaction history */
    .tx-item {
        background: #1a1f2e;
        border-left: 3px solid #3b82f6;
        padding: 16px;
        margin: 12px 0;
        border-radius: 0 8px 8px 0;
    }
    
    .tx-hash {
        font-family: 'Monaco', monospace;
        font-size: 12px;
        color: #64748b;
    }
    
    .tx-link {
        color: #3b82f6;
        text-decoration: none;
        font-size: 12px;
    }
    
    /* Stats grid */
    .stat-box {
        background: #1a1f2e;
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    
    .stat-value {
        font-size: 32px;
        font-weight: 700;
        color: #f1f5f9;
    }
    
    .stat-label {
        font-size: 12px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 8px;
    }
    
    .stat-change {
        font-size: 14px;
        margin-top: 8px;
    }
    
    /* Chart placeholder */
    .chart-container {
        background: #1a1f2e;
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 20px;
        height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Header */
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 24px;
        background: #0f172a;
        border-bottom: 1px solid #1e293b;
        margin: -1rem -1rem 24px -1rem;
    }
    
    .logo {
        font-size: 20px;
        font-weight: 700;
        color: #f1f5f9;
    }
    
    .network-badge {
        background: #1e293b;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        color: #94a3b8;
    }
    
    /* Wallet address */
    .wallet-address {
        font-family: 'Monaco', monospace;
        font-size: 11px;
        color: #64748b;
        background: #1a1f2e;
        padding: 8px 12px;
        border-radius: 8px;
    }
</style>
""",
    unsafe_allow_html=True,
)


def load_logs():
    """Load agent logs from file."""
    try:
        if os.path.exists("agent_log.json"):
            return json.load(open("agent_log.json")).get("logs", [])
    except:
        pass
    return []


def load_agent_info():
    """Load agent configuration."""
    try:
        if os.path.exists("agent.json"):
            return json.load(open("agent.json"))
    except:
        pass
    return {}


def format_timestamp(ts):
    """Format Unix timestamp to readable time."""
    if ts:
        return datetime.fromtimestamp(ts).strftime("%H:%M:%S")
    return "--:--:--"


def get_token_icon(token):
    """Return emoji icon for token."""
    icons = {"ETH": "⟐", "WETH": "Ξ", "USDC": "$", "USDT": "₮", "DAI": "◈"}
    return icons.get(token.upper(), "◯")


def load_portfolio_from_api(wallet):
    """Load portfolio data from API or return mock data."""
    try:
        # Try to fetch from a running instance
        r = requests.get(f"http://localhost:8000/portfolio/{wallet}", timeout=2)
        if r.ok:
            return r.json()
    except:
        pass

    # Return mock data for display purposes
    return {"eth": 0.225, "weth": 0.1, "usdc": 0, "total_usd": 220.0}


# Header
st.markdown(
    """
<div class="header">
    <div class="logo">📊 VeilTrader</div>
    <div style="display: flex; align-items: center; gap: 16px;">
        <span class="network-badge">Base Sepolia</span>
        <span class="wallet-address">0xe81e...A11C</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Load data
logs = load_logs()
portfolio = load_portfolio_from_api(os.getenv("WALLET_ADDRESS", ""))

# Top stats row
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
        f"""
    <div class="stat-box">
        <div class="stat-value">${portfolio.get("total_usd", 0):,.2f}</div>
        <div class="stat-label">Portfolio Value</div>
        <div class="stat-change price-up">↑ 2.4%</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    trades = len([l for l in logs if l.get("event") == "trade_executed"])
    st.markdown(
        f"""
    <div class="stat-box">
        <div class="stat-value">{trades}</div>
        <div class="stat-label">Total Trades</div>
        <div class="stat-change">All time</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col3:
    pnl = sum(l.get("pnlUSD", 0) for l in logs if l.get("event") == "trade_executed")
    color = "price-up" if pnl >= 0 else "price-down"
    st.markdown(
        f"""
    <div class="stat-box">
        <div class="stat-value {color}">${pnl:+.2f}</div>
        <div class="stat-label">Total P&L</div>
        <div class="stat-change">Since launch</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col4:
    wins = len([l for l in logs if l.get("pnlUSD", 0) > 0])
    win_rate = (wins / trades * 100) if trades > 0 else 0
    st.markdown(
        f"""
    <div class="stat-box">
        <div class="stat-value">{win_rate:.0f}%</div>
        <div class="stat-label">Win Rate</div>
        <div class="stat-change">{wins}W / {trades - wins}L</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col5:
    status = (
        "Active" if os.getenv("EMERGENCY_STOP", "false").lower() != "true" else "Paused"
    )
    st.markdown(
        f"""
    <div class="stat-box">
        <div style="padding: 20px;">
            <span class="status-indicator {"status-active" if status == "Active" else "status-inactive"}">
                <span class="status-dot" style="background: {"#22c55e" if status == "Active" else "#ef4444"}"></span>
                {status}
            </span>
        </div>
        <div class="stat-label">Agent Status</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# Main content - two columns
left_col, right_col = st.columns([1.2, 0.8])

with left_col:
    # Portfolio section
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("💼 Portfolio Holdings")

    # Token balances
    tokens = [
        ("ETH", portfolio.get("eth", 0), portfolio.get("eth", 0) * 2000, "#627eea"),
        ("WETH", portfolio.get("weth", 0), portfolio.get("weth", 0) * 2000, "#627eea"),
        ("USDC", portfolio.get("usdc", 0), portfolio.get("usdc", 0), "#2775ca"),
    ]

    for token, amount, usd, color in tokens:
        st.markdown(
            f"""
        <div class="token-balance">
            <div class="token-icon" style="background: {color};">{get_token_icon(token)}</div>
            <div style="flex: 1;">
                <div class="token-name">{token}</div>
                <div class="token-value">{amount:.4f}</div>
            </div>
            <div style="text-align: right;">
                <div class="token-usd">${usd:,.2f}</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Chart placeholder
    st.markdown(
        '<div class="chart-container"><span style="color: #64748b;">📈 Portfolio chart coming soon</span></div>',
        unsafe_allow_html=True,
    )

with right_col:
    # Latest Signal
    recent_trades = [l for l in logs if l.get("event") == "trade_executed"]

    if recent_trades:
        last = recent_trades[-1]
        action = last.get("decision", "HOLD")
        confidence = last.get("confidence", 0)
        action_class = f"signal-{action.lower()}"

        st.markdown(
            f"""
        <div class="signal-card">
            <div style="color: #64748b; font-size: 12px; text-transform: uppercase;">Latest Signal</div>
            <div class="signal-action {action_class}">{action}</div>
            <div style="color: #94a3b8;">Confidence: {confidence}%</div>
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: {confidence}%; background: {"#22c55e" if action == "BUY" else "#ef4444" if action == "SELL" else "#f59e0b"};"></div>
            </div>
            <div style="color: #64748b; font-size: 12px;">{last.get("rationale", "No rationale")[:50]}...</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
        <div class="signal-card">
            <div style="color: #64748b; font-size: 12px;">No trades yet</div>
            <div class="signal-action signal-hold">HOLD</div>
            <div style="color: #94a3b8;">Agent initializing...</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Stats
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("📈 Performance")

    perf_col1, perf_col2 = st.columns(2)
    with perf_col1:
        st.metric(
            "Best Trade", f"${max([l.get('pnlUSD', 0) for l in logs], default=0):+.2f}"
        )
    with perf_col2:
        st.metric(
            "Worst Trade", f"${min([l.get('pnlUSD', 0) for l in logs], default=0):+.2f}"
        )

    st.markdown("</div>", unsafe_allow_html=True)

# Transaction History
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📋 Recent Transactions")

if logs:
    for log in reversed(logs[-5:]):
        event = log.get("event", "")
        ts = format_timestamp(log.get("timestamp"))
        tx = log.get("txHash", "")

        if event == "trade_executed":
            decision = log.get("decision", "")
            token_in = log.get("tokenIn", "")
            token_out = log.get("tokenOut", "")
            pnl = log.get("pnlUSD", 0)

            st.markdown(
                f"""
            <div class="tx-item" style="border-left-color: {"#22c55e" if pnl >= 0 else "#ef4444"};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: #f1f5f9;">{decision}</strong>
                        <span style="color: #94a3b8;"> {token_in} → {token_out}</span>
                    </div>
                    <div style="text-align: right;">
                        <span class="{"price-up" if pnl >= 0 else "price-down"}" style="font-weight: 600;">${pnl:+.2f}</span>
                        <div class="tx-hash">{ts} • {tx[:10]}...{tx[-8:]}</div>
                    </div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        elif event == "error":
            st.markdown(
                f"""
            <div class="tx-item" style="border-left-color: #ef4444;">
                <div style="color: #ef4444;">❌ Error</div>
                <div class="tx-hash">{ts} • {log.get("error", "Unknown error")[:60]}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
else:
    st.info("No transactions yet. The agent will begin trading automatically.")

# Auto refresh
time.sleep(10)
st.rerun()
