# VeilTrader AI

> **Privacy-First Autonomous DeFi Trading Agent on Base**

VeilTrader AI is a fully autonomous, privacy-first AI trading agent that operates on Base (Ethereum L2). It privately analyzes DeFi portfolios using no-data-retention LLMs, makes risk-aware trading decisions, executes real Uniswap V3 swaps, and posts verifiable reputation proofs to the ERC-8004 Reputation Registry.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Base Network](https://img.shields.io/badge/Network-Base%20Sepolia-855DCD.svg)](https://base.org/)
[![Moltbook](https://img.shields.io/badge/Moltbook-Post-FF6B35)](https://www.moltbook.com/posts/b2aba4ce-eac8-48af-9516-0002216f28de)
[![Synthesis](https://img.shields.io/badge/Synthesis-Hackathon-9B5DEC)](https://synthesis.devfolio.co/)

### Links

- **Live Demo:** https://veiltrader-ai--moseschizaram.replit.app/
- **Presentation:** https://gamma.app/docs/Privacy-First-Autonomous-Trading-Agent-on-Base-0nlla4rzqaftvs4
- **Moltbook Post:** https://www.moltbook.com/posts/b2aba4ce-eac8-48af-9516-0002216f28de
- **Project Page:** https://synthesis.devfolio.co/projects/0eba8f11aa224a1d90206505e9dff60b

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Security](#security)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

VeilTrader AI is designed for hackathons and real-world DeFi trading scenarios where:

- **Privacy is paramount** - Portfolio data is redacted before LLM analysis
- **Autonomy is essential** - Runs 24/7 with zero human intervention
- **Transparency is required** - All trades are verifiable on-chain
- **Cost efficiency matters** - Operates on Base L2 for low gas fees

### Supported Networks

| Network | Chain ID | Status | RPC URL |
|---------|----------|--------|---------|
| Base Mainnet | 8453 | Production | `https://mainnet.base.org` |
| Base Sepolia | 84532 | Testnet | `https://sepolia.base.org` |

---

## Features

### Core Features

- **LLM-Powered Decision Making**
  - Privacy-first LLM with Groq → Venice → Bankr fallback chain
  - Risk-aware trading decisions with confidence scoring
  - No data retention policies from provider chain

- **Uniswap V3 Trading**
  - Real swap execution on Base
  - Support for USDC, WETH, USDT, DAI, wstETH
  - Configurable slippage tolerance and fees

- **ERC-8004 Reputation System**
  - On-chain identity registration
  - Post-trade reputation updates
  - Verifiable transaction proofs

- **x402 Payment Service**
  - Agent-to-agent commerce
  - 0.1 USDC per trade signal
  - Bearer token authentication

### Safety Features

- **70% Minimum Confidence Threshold** - Only executes trades with high confidence
- **5% Max Trade Size** - Limits exposure per trade
- **1% Slippage Protection** - Protects against front-running
- **Emergency Stop** - Instant halt flag
- **LIDO Treasury Mode** - Yield-preserving strategies
- **Single Trade Per Cycle** - No compounding risk

---

## Synthesis Hackathon Tracks

VeilTrader AI implements **7+ tracks** from the Synthesis hackathon, demonstrating comprehensive integration with partner infrastructure:

---

### 1. Synthesis Open Track

The Open Track is a shared prize across the whole event, focused on projects that align with all agentic judge values.

**Implementation:**
- Fully autonomous DeFi trading agent that operates 24/7 without human intervention
- Complete trade execution pipeline: portfolio analysis → LLM decision → Uniswap swap → reputation posting
- Verifiable on-chain transaction proofs for all actions
- Privacy-preserving design with data redaction before LLM analysis

---

### 2. Uniswap — Agentic Finance Track

**Track Focus:** Build AI agents that leverage Uniswap infrastructure for autonomous financial operations.

**Implementation:**
```python
# From uniswap_executor.py - Official Uniswap Developer Platform integration
- Uses trade-api.gateway.uniswap.org for quote generation
- Supports USDC, WETH, USDT, DAI, wstETH tokens
- Configurable fee tiers: 0.01%, 0.05%, 0.3%, 1%
- Real swap execution via on-chain router: 0x2626664c2603336E57B271c5C0b26F421741e481
- Multi-network support: Base Mainnet (8453) and Sepolia (84532)
```

**Key Features:**
- Direct API integration for price quotes
- Transaction building and signing
- Slippage protection (1% max)
- Single direct swap execution per cycle

---

### 3. Venice — Private Agents, Trusted Actions Track

**Track Focus:** Build agents that leverage Venice's privacy-first LLM infrastructure.

**Implementation:**
```python
# From llm_brain.py - Venice as secondary LLM provider
providers = [
    ("groq", env("GROQ_API_KEY"), ...),
    ("venice", env("VENICE_API_KEY"), env("VENICE_MODEL", "llama-3.3-70b")),
    ...
]
```

**Privacy Features:**
- Portfolio data redacted before LLM analysis (wallet addresses masked)
- No raw wallet addresses logged
- Session-based processing only
- Venice as fallback with no-data-retention policy

---

### 4. Bankr — Best LLM Gateway Track

**Track Focus:** Build agents with intelligent LLM routing and fallback mechanisms.

**Implementation:**
```python
# Multi-provider fallback chain
providers = [
    ("groq", env("GROQ_API_KEY"), ...),      # Primary
    ("venice", env("VENICE_API_KEY"), ...),  # Secondary
    ("bankr", env("BANKR_API_KEY"), ...),    # Tertiary
]
```

**Gateway Features:**
- Automatic failover when primary provider fails
- Error collection and reporting
- Graceful degradation
- Consistent response normalization across providers

---

### 5. Protocol Labs — Agents With Receipts (ERC-8004) Track

**Track Focus:** Build agents that post verifiable receipts/proofs to ERC-8004 Reputation Registry.

**Implementation:**
```python
# From reputation_manager.py - ERC-8004 integration
- Identity Registration: register_agent.py
- Reputation Updates: reputation_manager.py
- Rating System: 2-5 scale with P&L tracking
- Transaction Proofs: Hash verification on-chain
```

**ERC-8004 Features:**
- On-chain identity registration
- Post-trade feedback posting
- Reputation score tracking
- Verifiable transaction receipts
- Identity Registry: `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
- Reputation Registry: `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63`

---

### 6. Protocol Labs — Let the Agent Cook Track

**Track Focus:** Build agents that demonstrate autonomous capability and "living forever" infrastructure.

**Implementation:**
- Self-sustaining autonomous operation after one-time setup
- Hourly trading cycle with no human intervention
- Emergency stop flag for safety
- LIDO Treasury Mode for yield-preserving strategies
- Agent registration with unique identity
- Continuous operation framework

---

### 7. Base — Self-Sustaining Autonomous Agents Track

**Track Focus:** Build autonomous agents native to Base network.

**Implementation:**
```python
# Network Configuration from common.py
NETWORKS = {
    "mainnet": {"chain_id": 8453, "rpc": "https://mainnet.base.org", ...},
    "sepolia": {"chain_id": 84532, "rpc": "https://sepolia.base.org", ...}
}
```

**Base-Native Features:**
- Built on Base L2 for low gas fees
- Ethereum-equivalent EVM for compatibility
- Native USDC and WETH support
- Sepolia testnet for development
- Coinbase-backed infrastructure

---

### 8. x402 — Agent Commerce Track

**Track Focus:** Enable agent-to-agent payments and micropayments.

**Implementation:**
```python
# From main.py - x402 payment service
@app.post("/trade-signal")
async def trade_signal(authorization: str = Header(None)):
    # Bearer token authentication
    # $0.1 USDC per trade signal
    # Revenue tracking and logging
```

**Commerce Features:**
- Paid `/trade-signal` endpoint with x402 authentication
- Revenue logging for agent earnings
- Bearer token validation
- Paid client access to trade recommendations

---

### Track Implementation Matrix

| Track | Implementation | Files |
|-------|----------------|-------|
| Synthesis Open | Full autonomous agent | `main.py`, `core.py` |
| Uniswap Agentic Finance | Swap execution | `uniswap_executor.py` |
| Venice Privacy | LLM provider | `llm_brain.py` |
| Bankr LLM Gateway | Fallback routing | `llm_brain.py` |
| ERC-8004 Receipts | Reputation posting | `reputation_manager.py`, `register_agent.py` |
| Let Agent Cook | Self-sustaining ops | `main.py` (hourly loop) |
| Base Native | Network integration | `common.py` |
| x402 Commerce | Payment endpoint | `main.py` |

---

### Technical Architecture for Tracks

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SYNTHESIS HACKATHON TRACKS                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐                                                        │
│  │  Open Track     │─────────────────────────────────────────────────────┐  │
│  └────────┬────────┘                                                     │  │
│           │                                                              │  │
│  ┌────────┴────────┐   ┌─────────────────┐   ┌───────────────────────┐   │  │
│  │  Uniswap        │   │  Venice         │   │  Bankr                 │   │  │
│  │  Agentic Finance│   │  Private Agents │   │  Best LLM Gateway      │   │  │
│  └────────┬────────┘   └────────┬────────┘   └───────────┬───────────┘   │  │
│           │                      │                       │               │  │
│  ┌────────┴────────┐   ┌────────┴────────┐   ┌───────────┴───────────┐   │  │
│  │  Protocol Labs   │   │  Protocol Labs │   │  Base                  │   │  │
│  │  ERC-8004       │   │  Let Agent Cook│   │  Self-Sustaining       │   │  │
│  └────────┬────────┘   └────────┬────────┘   └───────────┬───────────┘   │  │
│           │                      │                       │               │  │
│  ┌────────┴────────┐                                     │               │  │
│  │  x402           │─────────────────────────────────────┘               │  │
│  │  Agent Commerce │                                                     │  │
│  └────────┬────────┘                                                     │  │
│           │                                                              │  │
└───────────┼──────────────────────────────────────────────────────────────┘  │
            │                                                               │
            ▼                                                               │
┌───────────────────────────────────────────────────────────────────────────┐
│                        IMPLEMENTATION LAYER                                │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│   ┌─────────────────────────────────────────────────────────────────┐    │
│   │                         main.py                                  │    │
│   │              FastAPI Server + Hourly Loop + x402                 │    │
│   └─────────────────────────────┬───────────────────────────────────┘    │
│                                 │                                         │
│   ┌─────────────────────────────┴───────────────────────────────────┐    │
│   │                         core.py                                 │    │
│   │                   Business Logic & Decision Engine               │    │
│   └─────────────────────────────┬───────────────────────────────────┘    │
│                                 │                                         │
│   ┌─────────────┬───────────────┼───────────────┬─────────────────┐      │
│   │             │               │               │                 │      │
│   ▼             ▼               ▼               ▼                 ▼      │
│ ┌────────┐  ┌──────────┐  ┌────────────┐  ┌────────────────┐  ┌────────┐ │
│ │llm_   │  │portfolio │  │ uniswap_   │  │reputation_    │  │register│ │
│ │brain  │  │_reader   │  │ executor   │  │manager        │  │_agent  │ │
│ │       │  │          │  │            │  │               │  │        │ │
│ │ -Groq │  │ -USDC   │  │ -Uniswap  │  │ -ERC-8004    │  │ -Id    │ │
│ │ -Venice│ │ -WETH   │  │ V3 Swap   │  │ -Identity    │  │ -Reg   │ │
│ │ -Bankr│  │ -Redact │  │ -Quote    │  │ -Reputation  │  │        │ │
│ └────────┘  └──────────┘  └────────────┘  └────────────────┘  └────────┘ │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          VELTRADER AI                                  │
│                  Privacy-First Autonomous Trading Agent                  │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER                                  │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐    ┌─────────────────────────────────────┐   │
│  │   Web Dashboard     │    │        Paid API Clients             │   │
│  │  (Streamlit/Replit)│    │     (x402 @trade-signal)            │   │
│  └─────────┬───────────┘    └──────────────────┬──────────────────┘   │
└────────────┼───────────────────────────────────┼──────────────────────┘
             │                                   │
             ▼                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          MAIN.PY                                       │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────┐   │
│  │  FastAPI Server │  │  Hourly Loop   │  │   x402 Payment Svc    │   │
│  │  - /health     │  │  - Portfolio   │  │   - Bearer Token      │   │
│  │  - /trade-signal│  │  - Decision    │  │   - $0.1 USDC         │   │
│  └───────┬────────┘  └───────┬────────┘  └───────────┬────────────┘   │
└──────────┼───────────────────┼────────────────────────┼────────────────┘
           │                   │                        │
           ▼                   ▼                        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           CORE.PY                                       │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Trading Decision Engine                       │   │
│  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │   │
│  │   │ LLM Brain  │  │ Portfolio   │  │  Trade Validator        │ │   │
│  │   │ - Groq     │  │ Reader      │  │  - Confidence >= 70%   │ │   │
│  │   │ - Venice   │  │ - USDC/WETH │  │  - Amount <= 5%        │ │   │
│  │   │ - Bankr    │  │ - Redacted  │  │  - Slippage <= 1%      │ │   │
│  │   └──────┬──────┘  └──────┬──────┘  └────────────┬────────────┘ │   │
│  └──────────┼─────────────────┼─────────────────────┼───────────────┘   │
└─────────────┼─────────────────┼─────────────────────┼──────────────────┘
              │                 │                     │
              ▼                 ▼                     ▼
┌─────────────────────┐  ┌─────────────────┐  ┌──────────────────────────┐
│    LLM PROVIDERS    │  │  BLOCKCHAIN     │  │   EXECUTION LAYER        │
├─────────────────────┤  ├─────────────────┤  ├──────────────────────────┤
│                     │  │                 │  │                          │
│  ┌────────────────┐ │  │  Base Network   │  │  ┌────────────────────┐  │
│  │ 1. Groq (Pri)  │ │  │  - Mainnet 8453│  │  │  Uniswap Executor  │  │
│  │ 2. Venice      │ │  │  - Sepolia 84532│  │  │  - Get Quote      │  │
│  │ 3. Bankr       │ │  │                 │  │  │  - Sign & Execute │  │
│  └────────────────┘ │  │  Tokens:        │  │  │  - USDC/WETH Swap │  │
│                     │  │  - USDC         │  │  └─────────┬──────────┘  │
│  LLM FALLBACK CHAIN │  │  - WETH         │  │            │             │
│                     │  │  - wstETH       │  │            ▼             │
└─────────────────────┘  └─────────────────┘  │  ┌────────────────────┐  │
                                               │  │ ERC-8004 Manager  │  │
                                               │  │ - Post Reputation │  │
                                               │  │ - Identity Reg    │  │
                                               │  └────────────────────┘  │
                                               └────────────────────────────┘
```

### Component Data Flow

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ Portfolio │ ──▶ │ Redact   │ ──▶ │ LLM      │ ──▶ │ Validate │ ──▶ │ Execute  │
│  Reader   │     │  Data    │     │ Decision │     │  Trade   │     │  Swap    │
└──────────┘     └──────────┘     └──────────┘     └──────────┘     └────┬─────┘
                                                                        │
                    ┌────────────────────────────────────────────────────┘
                    ▼
              ┌──────────┐     ┌──────────┐     ┌──────────┐
              │ Reputation│ ──▶ │  Log    │ ──▶ │  Sleep   │
              │  Update   │     │ Activity│     │  1 Hour  │
              └──────────┘     └──────────┘     └──────────┘
```

### LLM Provider Fallback Chain

```
Request ──▶ Groq Available? ──▶ YES ──▶ Process with Groq ──▶ Return Decision
              │
              ▼ NO
         Venice Available? ──▶ YES ──▶ Process with Venice ──▶ Return Decision
              │
              ▼ NO
         Bankr Available? ──▶ YES ──▶ Process with Bankr ──▶ Return Decision
              │
              ▼ NO
         Error: No LLM Provider Available
```

### Trade Execution Flow

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TRADE EXECUTION CYCLE                           │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  1. READ PORTFOLIO                                                     │
│     └─▶ Query USDC balance, WETH balance on Base                       │
│                                                                        │
│  2. REDACT DATA                                                        │
│     └─▶ Mask wallet addresses before LLM analysis                      │
│                                                                        │
│  3. LLM DECISION                                                       │
│     └─▶ Groq/Venice/Bankr returns: {action, confidence, rationale}     │
│                                                                        │
│  4. VALIDATE TRADE                                                     │
│     ├─▶ Confidence >= 70%?                                             │
│     ├─▶ Amount <= 5% of portfolio?                                    │
│     └─▶ Slippage <= 1%?                                                │
│                                                                        │
│  5. EXECUTE (if valid)                                                 │
│     ├─▶ Get quote from Uniswap API                                     │
│     ├─▶ Sign transaction with wallet                                    │
│     ├─▶ Execute swap on Base                                           │
│     └─▶ Wait for confirmation                                           │
│                                                                        │
│  6. POST REPUTATION                                                    │
│     ├─▶ Rate trade 2-5 stars                                           │
│     ├─▶ Record P&L                                                     │
│     └─▶ Post to ERC-8004 Registry                                      │
│                                                                        │
│  7. LOG & SLEEP                                                        │
│     └─▶ Log to agent_log.json, sleep 1 hour, repeat                    │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### System Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TRADING CYCLE SEQUENCE                              │
└─────────────────────────────────────────────────────────────────────────────┘

 Hour 0: Trading Cycle Begins
 │
 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Agent ───────────────▶ Chain: Read Portfolio Balances                        │
│                              ◀─────────────── USDC: $500, WETH: 0.1        │
└─────────────────────────────────────────────────────────────────────────────┘
 │
 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Agent ───────────────▶ LLM: Get Trading Decision (redacted)                │
│                              ◀─────────────── BUY WETH, 85% confidence     │
└─────────────────────────────────────────────────────────────────────────────┘
 │
 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CONFIDENCE >= 70%?                                   │
└─────────────────────────────────────────────────────────────────────────────┘
         │
    ┌────┴────┐
    │YES      │NO
    ▼         ▼
┌────────────────┐  ┌────────────────┐
│ Execute Swap   │  │ Skip Trade     │
│ Agent─────────▶│  │ Log HOLD       │
│    Uniswap     │  │                │
└───────┬────────┘  └────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Swap 25 USDC ───────────▶ Chain: Execute on Uniswap V3                      │
│                        ◀─────────────── Transaction Receipt                 │
└─────────────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Agent ───────────────▶ Registry: Post Feedback (Rating: 5, P&L: +$2.50)    │
│                              ◀─────────────── Confirmation                   │
└─────────────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Agent: Log Activity                                                          │
│                                                                              │
│ Sleep 1 Hour ────────────▶ (Repeat Cycle)                                    │
└─────────────────────────────────────────────────────────────────────────────┘

 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
                              x402 PAYMENT REQUEST
 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

 User ───▶ Agent: POST /trade-signal (Bearer token + 0.1 USDC)
              │
              ▼
         Validate Token
              │
              ▼
         ┌────────┐
         │ Valid? │
         └────┬───┘
         ┌────┴────┐
         │YES      │NO
         ▼         ▼
   ┌──────────┐  ┌──────────────┐
   │Get Decision│  │ 402 Error    │
   │from LLM   │  │ Returned      │
   └─────┬────┘  └──────────────┘
         │
         ▼
   ┌──────────────────────────────────────┐
   │ Return {recommendation, confidence}  │
   └──────────────────────────────────────┘
```

### Trading Decision Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      TRADING DECISION FLOWCHART                             │
└─────────────────────────────────────────────────────────────────────────────┘

                           ┌─────────────────┐
                           │  Start Trading  │
                           │     Cycle       │
                           └────────┬────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │  Read Portfolio │
                           │ Get USDC/WETH   │
                           └────────┬────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │ Redact Sensitive│
                           │     Data        │
                           └────────┬────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │  Query LLM      │
                           │    Provider     │
                           └────────┬────────┘
                                    │
                          ┌─────────┴─────────┐
                          │                   │
                          ▼                   ▼
                    ┌───────────┐       ┌───────────┐
                    │Groq?      │       │Venice?    │
                    │ Available │NO     │ Available │
                    └─────┬─────┘       └─────┬─────┘
                    ┌─────┴─────┐             │
                    │YES        │             ▼
                    ▼           │       ┌───────────┐
              ┌───────────┐     │       │Bankr?     │
              │Process    │     │       │ Available │
              │with Groq  │     │       └─────┬─────┘
              └─────┬─────┘     │       ┌─────┴─────┐
                    │           │       │YES        │NO
                    │           │       ▼           ▼
                    │     ┌─────┴───┐ ┌─────────┐ ┌──────────────┐
                    │     │Process  │ │Process  │ │Error: No     │
                    │     │with     │ │with     │ │LLM Provider  │
                    │     │Venice   │ │Bankr    │ │Available     │
                    │     └────┬────┘ └────┬────┘ └──────────────┘
                    │          │          │
                    └──────────┴──────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │ Parse Decision │
                           │ {action, conf} │
                           └────────┬────────┘
                                    │
                          ┌─────────┴─────────┐
                          │                   │
                          ▼                   ▼
                   ┌────────────┐      ┌────────────┐
                   │Conf >= 70%?│NO    │ Conf >= 70%│YES
                   └─────┬──────┘      └─────┬──────┘
                         │                    │
                         ▼                    ▼
                  ┌────────────┐      ┌─────────────┐
                  │ HOLD       │      │ Valid Trade?│
                  │ Log & Skip │      └──────┬──────┘
                  └─────┬──────┘             │
                        │            ┌────────┴────────┐
                        │            │                 │
                        │       ┌────┴────┐    ┌──────┴─────┐
                        │       │BUY?      │NO  │SELL?        │YES
                        │       └────┬─────┘    └──────┬─────┘
                        │            │                 │
                        │            ▼                 ▼
                        │      ┌───────────┐    ┌───────────┐
                        │      │ Check if │    │ Swap WETH │
                        │      │ SELL?    │    │  ▶ USDC   │
                        │      └─────┬─────┘    └─────┬─────┘
                        │            │YES              │
                        │            ▼                 │
                        │      ┌───────────┐           │
                        │      │ Swap USDC│           │
                        │      │  ▶ WETH  │           │
                        │      └─────┬─────┘           │
                        │            │                 │
                        └────────────┴─────────────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │ Execute on      │
                           │   Uniswap       │
                           └────────┬────────┘
                                    │
                          ┌─────────┴─────────┐
                          │                   │
                          ▼                   ▼
                   ┌────────────┐      ┌────────────┐
                   │   Success? │YES   │   Success? │NO
                   │            │      │            │
                   └─────┬──────┘      └─────┬──────┘
                         │                    │
                         ▼                    ▼
                  ┌────────────┐      ┌────────────┐
                  │ Post ERC-  │      │  Log Error │
                  │ 8004 Rep.  │      │            │
                  └─────┬──────┘      └─────┬──────┘
                        │                    │
                        └──────────┬─────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  Log Activity   │
                          └────────┬────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │  Sleep 1 Hour   │
                          └────────┬────────┘
                                   │
                                   └────────▶ (Repeat Cycle)
```

---

## Quick Start

### Prerequisites

- Python 3.12+
- MetaMask or compatible wallet
- API keys (optional for demo mode)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/veiltrader-ai.git
cd veiltrader-ai

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### Configuration

Edit `.env` with your settings:

```env
# Network: "mainnet" or "sepolia"
BASE_NETWORK="sepolia"

# RPC URL (leave empty for default)
BASE_RPC_URL=""

# Wallet Configuration
WALLET_ADDRESS="0x..."
PRIVATE_KEY="0x..."

# LLM Providers (optional - demo mode works without)
GROQ_API_KEY="your_groq_key"
VENICE_API_KEY="your_venice_key"
BANKR_API_KEY="your_bankr_key"

# Demo Mode (for testing without real trades)
DEMO_MODE="true"
```

### Running

```bash
# Start the agent (FastAPI + autonomous loop)
python main.py

# Or run the dashboard separately
streamlit run streamlit_app.py
```

---

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `BASE_NETWORK` | Network to use | `sepolia` | No |
| `BASE_RPC_URL` | Base RPC endpoint | Auto | No |
| `PRIVATE_KEY` | Wallet private key | - | Yes |
| `WALLET_ADDRESS` | Wallet address | - | Yes |
| `UNISWAP_API_KEY` | Uniswap API key | - | Recommended |
| `GROQ_API_KEY` | Groq API key | - | No |
| `VENICE_API_KEY` | Venice API key | - | No |
| `BANKR_API_KEY` | Bankr API key | - | No |
| `DEMO_MODE` | Simulated trading | `true` | No |
| `EMERGENCY_STOP` | Stop all trading | `false` | No |
| `MAX_TRADE_PERCENTAGE` | Max trade size | `0.05` | No |
| `SLIPPAGE_TOLERANCE` | Max slippage | `0.01` | No |

### Network Addresses

#### Base Mainnet (8453)

| Contract | Address |
|----------|---------|
| Uniswap V3 Router | `0x2626664c2603336E57B271c5C0b26F421741e481` |
| USDC | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| WETH | `0x4200000000000000000000000000000000000006` |
| ERC-8004 Identity | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |
| ERC-8004 Reputation | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` |

#### Base Sepolia (84532)

| Contract | Address |
|----------|---------|
| Uniswap V3 Router | `0x2626664c2603336E57B271c5C0b26F421741e481` |
| USDC | `0x036aB6B98c8a4e5b5b4606C28F6966Ce73C80C7D` |
| WETH | `0x4200000000000000000000000000000000000006` |
| ERC-8004 | Not deployed |

---

## How It Works

### Trading Cycle State Machine

```
┌───────────────┐
│ Start         │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Read Portfolio │
└───────┬───────┘
        │
        ▼
┌───────────────────────┐
│ Analyze & Get Decision│
└───────┬───────────────┘
        │
        ▼
    ┌───────────────────────┐
    │ Confidence >= 70%?    │
    └───────┬───────────────┘
            │
    ┌───────┴───────┐
    │YES           │NO
    ▼              ▼
┌──────────┐  ┌──────────┐
│ BUY/SELL │  │  HOLD    │
└─────┬────┘  └────┬─────┘
      │            │
      ▼            │
┌──────────┐      │
│Execute   │      │
│Trade     │      │
└─────┬────┘      │
      │            │
┌─────┴────┐      │
│Tx Success│      │
│or Failed │      │
└─────┬────┘      │
      │            │
      ▼            ▼
┌──────────────────────┐
│ Post ERC-8004        │
│ Reputation (if OK)   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Log Activity         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Sleep 1 Hour        │
└──────────┬───────────┘
           │
           └──────▶ (Repeat)
```

### x402 Payment Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │     │  FastAPI    │     │     LLM     │
│             │     │   Server    │     │  Provider   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │ POST /trade-signal│                   │
       │ + Bearer Token    │                   │
       │ + 0.1 USDC        │                   │
       │──────────────────▶│                   │
       │                   │                   │
       │                   │ Validate Token    │
       │                   │─ ─ ─ ─ ─ ─ ─ ─ ─ │
       │                   │                   │
       │              ┌────┴────┐              │
       │              │         │              │
       │         Valid         Invalid         │
       │              │         │              │
       │              ▼         ▼              │
       │       ┌──────────┐ ┌────────────┐     │
       │       │ Request  │ │ 402 Error  │     │
       │       │ Decision │ │ Returned   │     │
       │       └────┬─────┘ └───────────┘     │
       │            │                        │
       │            │  GET Decision          │
       │            │───────────────────────▶│
       │            │                        │
       │            │  {recommendation,     │
       │            │   confidence}          │
       │            │◀──────────────────────│
       │            │                        │
       │      200 OK Response                │
       │◀───────────────────────────────────│
       │            │                        │
```

### LLM Fallback Chain Flow

```
                    ┌─────────────────────┐
                    │  Trade Decision     │
                    │     Request         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Groq Available?    │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │YES                 │NO
                    ▼                     ▼
           ┌────────────────┐    ┌─────────────────────┐
           │ Process with   │    │Venice Available?    │
           │    Groq        │    └──────────┬──────────┘
           └───────┬────────┘               │
                   │            ┌───────────┴───────────┐
                   │            │YES                   │NO
                   │            ▼                       ▼
                   │   ┌────────────────┐    ┌─────────────────────┐
                   │   │ Process with   │    │ Bankr Available?     │
                   │   │   Venice       │    └──────────┬──────────┘
                   │   └───────┬────────┘               │
                   │           │            ┌─────────────┴────────────┐
                   │           │            │YES                     │NO
                   │           │            ▼                         ▼
                   │           │   ┌────────────────┐    ┌────────────────────┐
                   │           │   │ Process with   │    │ Raise RuntimeError │
                   │           │   │    Bankr       │    │ "No LLM Provider"  │
                   │           │   └───────┬────────┘    └────────────────────┘
                   │           │           │
                   │           │           │
                   └───────────┼───────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Return Decision     │
                    │  to Caller          │
                    └─────────────────────┘
```

---

## Security

### Best Practices

1. **Never commit private keys** - Use environment variables only
2. **Start with testnet** - Always test on Sepolia first
3. **Set trade limits** - Keep `MAX_TRADE_PERCENTAGE` low
4. **Monitor logs** - Review `agent_log.json` regularly
5. **Enable emergency stop** - Use `EMERGENCY_STOP=true` during issues

### Privacy Features

- Portfolio data is redacted before LLM analysis
- No raw wallet addresses logged
- Session-based processing only
- No data retention from LLM providers

### Risk Management

```
┌─────────────────────────────────────────────────────────┐
│                    RISK CONTROLS                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │ 70% Min     │    │ 5% Max       │    │ 1% Slippage │ │
│  │ Confidence  │    │ Trade Size   │    │ Protection  │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │ Emergency   │    │ Single       │    │ LIDO Mode   │ │
│  │ Stop Flag   │    │ Trade/Cycle  │    │ Protection  │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Development

### Project Structure

```
veiltrader-ai/
├── main.py                 # Entry point + FastAPI server
├── core.py                  # LLM brain + portfolio reader
├── llm_brain.py             # Privacy-first LLM routing
├── portfolio_reader.py       # On-chain balance reader
├── uniswap_executor.py      # Uniswap V3 swap executor
├── reputation_manager.py    # ERC-8004 integration
├── register_agent.py        # Agent registration
├── common.py                # Shared utilities
├── streamlit_app.py         # Dashboard UI
│
├── docs/
│   ├── ARCHITECTURE.md      # System architecture
│   ├── API.md               # API documentation
│   └── DEPLOYMENT.md        # Deployment guide
│
├── dist/                    # Frontend build
├── public/                  # Static assets
├── tests/                   # Test suite
│
├── .env.example             # Environment template
├── requirements.txt         # Dependencies
├── agent.json              # Agent metadata
├── agent_log.json          # Activity logs
├── README.md               # This file
├── CONTRIBUTING.md         # Contribution guide
├── LICENSE                 # MIT License
└── ARCHITECTURE.md         # Detailed architecture
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/test_uniswap_executor.py -v
```

### Code Style

```bash
# Format code
black .

# Lint code
ruff .

# Type check
mypy .
```

---

## Testing

### Testnet Setup

1. **Get test ETH:** https://www.coinbase.com/faucets/base-ethereum-sepolia-faucet
2. **Get test USDC:** Mint from Base Sepolia USDC contract
3. **Set environment:**
   ```bash
   BASE_NETWORK=sepolia
   DEMO_MODE=false
   ```

### Demo Mode

When `DEMO_MODE=true`, the agent uses simulated decisions without real trades:

```python
# Simulated response
{
    "decision": random.choice(["BUY", "SELL", "HOLD"]),
    "confidence": random.randint(60, 95),
    "reasoning": "Demo mode - simulated decision"
}
```

### Manual Testing

```bash
# Test portfolio reader
python -c "from portfolio_reader import get_portfolio_summary; print(get_portfolio_summary('0x...'))"

# Test Uniswap executor
python -c "from uniswap_executor import UniswapExecutor; e = UniswapExecutor(); print('Connected:', e.w3.is_connected())"

# Test LLM
python -c "from llm_brain import LLMBrain; b = LLMBrain(); print(b.get_response('Should I buy ETH?'))"
```

---

## Deployment

### Replit

1. Import project to Replit
2. Add secrets in Secrets panel:
   ```
   BASE_NETWORK=sepolia
   PRIVATE_KEY=your_key
   WALLET_ADDRESS=your_address
   GROQ_API_KEY=your_key
   DEMO_MODE=false
   ```
3. Click Run

### Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

```bash
# Build and run
docker build -t veiltrader-ai .
docker run -d --env-file .env veiltrader-ai
```

### VPS/Raspberry Pi

```bash
# SSH into server
ssh user@your-server

# Clone and setup
git clone https://github.com/yourusername/veiltrader-ai.git
cd veiltrader-ai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create systemd service
sudo nano /etc/systemd/system/veiltrader.service

# Start service
sudo systemctl start veiltrader
sudo systemctl enable veiltrader
```

### Cloud Platforms

| Platform | Instructions |
|----------|--------------|
| Railway | Connect repo → Add secrets → Deploy |
| Render | Create Python app → Connect repo → Add env vars |
| Fly.io | `fly launch` → `fly deploy` |
| Heroku | `heroku create` → `git push heroku main` |

---

## Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Detailed system architecture with diagrams |
| [API.md](docs/API.md) | API endpoints and schemas |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Deployment guides for various platforms |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |

---

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our development workflow.

### Quick Guide

```bash
# Fork the repository
# Clone your fork
git clone https://github.com/yourusername/veiltrader-ai.git
cd veiltrader-ai

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes and commit
git commit -m "Add amazing feature"

# Push and create PR
git push origin feature/amazing-feature
```

---

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- **Uniswap Labs** - V3 swap infrastructure
- **ERC-8004 Protocol** - Reputation registry standard
- **Base** - Low-cost L2 infrastructure
- **Groq, Venice, Bankr** - LLM inference providers

---

<p align="center">
  <strong>Built for Privacy-First DeFi Trading</strong>
  <br>
  <sub>Powered by Base • Secured by ERC-8004 • Intelligent by LLMs</sub>
</p>
