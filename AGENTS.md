# AGENTS.md

> Instructions for AI coding agents working on VeilTrader AI.

## Project Overview

VeilTrader AI is a privacy-first autonomous DeFi trading agent on Base (Ethereum L2). It uses LLMs for decision-making, executes Uniswap V3 swaps, and posts reputation to ERC-8004.

## Setup Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Run tests
pytest tests/

# Start the agent
python main.py

# Start dashboard
streamlit run streamlit_app.py
```

## Environment Variables

Required secrets (see `.env.example`):
- `BASE_NETWORK` - "mainnet" or "sepolia"
- `GROQ_API_KEY` - Groq API key for LLM
- `WALLET_ADDRESS` - Wallet address for portfolio reading
- `PRIVATE_KEY` - Wallet private key (NEVER commit this)
- `UNISWAP_API_KEY` - Uniswap Developer Platform API key

## Network Configuration

Networks are defined in `common.py` under the `NETWORKS` dict:
- Mainnet: Chain ID 8453, uses production addresses
- Sepolia: Chain ID 84532, uses testnet addresses

To add a new network, add to the `NETWORKS` dict with:
- `chain_id`
- `rpc`
- `basescan`
- `uniswap_router`
- `identity_registry`
- `reputation_registry`
- `usdc`, `weth`, `wsteth` addresses

## Architecture

### Core Modules

| File | Purpose |
|------|---------|
| `main.py` | Entry point, FastAPI server, hourly trading loop |
| `core.py` | Business logic, coordinates LLM + portfolio |
| `llm_brain.py` | LLM routing with Groq → Venice → Bankr fallback |
| `portfolio_reader.py` | On-chain balance reading, data redaction |
| `uniswap_executor.py` | Uniswap V3 swap execution |
| `reputation_manager.py` | ERC-8004 reputation posting |
| `register_agent.py` | Agent identity registration |
| `common.py` | Shared utilities, network config |

### Key Patterns

1. **LLM Fallback Chain**: Try Groq first, then Venice, then Bankr, then demo mode
2. **Privacy**: Always redact wallet addresses before LLM analysis
3. **Safety**: 70% min confidence, 5% max trade size, 1% slippage
4. **Multi-network**: Use `NETWORK` dict for all addresses

## Code Style

- Python 3.12+
- Single quotes for strings
- Type hints where possible
- docstrings for functions
- Max line length: 100

## Testing

```bash
# Run all tests
pytest tests/ -v

# Test specific module
pytest tests/test_llm_brain.py -v

# Test with coverage
pytest tests/ --cov=. --cov-report=term-missing
```

## Adding New Features

### New LLM Provider

1. Add provider to `llm_brain.py` `providers` list
2. Follow pattern: `(name, api_key_env, model, url)`
3. Update `_normalize()` if response format differs

### New Token Support

1. Add to `uniswap_executor.py` `TOKENS` dict
2. Add decimals to `DECIMALS` dict
3. Update fee tiers in `FEES` dict if needed

### New Network

1. Add entry to `common.py` `NETWORKS` dict
2. Get contract addresses for the new network
3. Update `.env.example` with new network options

## Security Considerations

- NEVER log wallet addresses or private keys
- NEVER commit `.env` files
- Always validate transaction parameters before signing
- Use testnet for development
- Review all swap amounts before execution

## Trade Execution Flow

1. Read portfolio balances
2. Redact sensitive data
3. Query LLM for decision
4. Validate confidence >= 70%
5. Execute swap on Uniswap
6. Post reputation to ERC-8004
7. Log activity

## Common Tasks

### Update LLM Model

Edit `llm_brain.py` `decide()` function, change model in providers tuple.

### Add Safety Check

Edit `uniswap_executor.py` before transaction signing.

### Debug LLM Responses

Add `print()` in `_chat()` function or check `agent_log.json`.

## File Structure

```
veiltrader-ai/
├── main.py                 # Entry point
├── core.py                 # Business logic
├── llm_brain.py            # LLM routing
├── portfolio_reader.py     # Balance reading
├── uniswap_executor.py     # Swap execution
├── reputation_manager.py   # ERC-8004
├── register_agent.py       # Registration
├── common.py               # Utilities
├── streamlit_app.py        # Dashboard
├── agent.json              # Agent manifest
├── agent_log.json          # Activity log
├── docs/                   # Documentation
│   └── ARCHITECTURE.md
├── dist/                   # Frontend build
└── tests/                  # Test suite
```
