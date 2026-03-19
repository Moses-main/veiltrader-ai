# VeilTrader

> "VeilTrader is a fully autonomous, privacy-first AI trading agent on Base (Ethereum). It privately analyzes any user’s DeFi portfolio using a no-data-retention LLM (Venice/Groq/Bankr fallback), makes risk-aware trade decisions, executes real Uniswap V3 swaps using the official Uniswap Developer Platform API + on-chain router, posts reputation updates to the ERC-8004 Reputation Registry, and only publishes verifiable transaction proofs. After one-time setup it runs forever with zero human intervention. Built to win Venice 'Private Agents, Trusted Actions', Uniswap 'Agentic Finance', Bankr 'Best LLM Gateway', Protocol Labs 'Agents With Receipts — ERC-8004' + 'Let the Agent Cook', and Synthesis Open Track."

## Prize mapping

| Prize | How this repo targets it |
|---|---|
| Venice | `llm_brain.py` keeps reasoning private, never logs raw balances, and prefers Groq → Venice → Bankr fallback. |
| Uniswap | `uniswap_executor.py` gets official Trade API quotes and signs a Base Uniswap V3 `exactInputSingle` swap. |
| Bankr | Bankr is the tertiary LLM gateway, and `main.py` tracks a rolling Bankr budget sourced from profitable cycles. |
| Protocol Labs / ERC-8004 | `register_agent.py`, `agent.json`, `agent_log.json`, and `reputation_manager.py` provide identity + receipts. |
| MetaMask Delegation | The code is ready for a session-key signer swap without changing the reasoning or receipt flow. |
| Synthesis Open Track | The stack is Python 3.12, autonomous, Base-native, and submission-ready. |

## Included phases

1. **Setup + ERC-8004**: `requirements.txt`, `.env.example`, `agent.json`, `register_agent.py`.
2. **Private LLM brain**: `llm_brain.py` with deterministic safe fallback.
3. **Portfolio reader**: `portfolio_reader.py` for Base ETH/WETH/USDC balances.
4. **Uniswap execution**: `uniswap_executor.py` with quote + exactInputSingle flow.
5. **Reputation**: `reputation_manager.py` posts verifiable trade proofs.
6. **Autonomy**: `main.py` runs forever with one trade max per cycle.
7. **Dashboard + submission**: `streamlit_app.py`, this README, and `DEPLOYMENT GUIDE.md`.

## Safety rails

- `MAX_TRADE_PCT` defaults to 5% and is hard-clamped.
- `MAX_SLIPPAGE_BPS` defaults to 100 (1%).
- Gas is checked against `MAX_GAS_ETH` before submitting swaps.
- `EMERGENCY_STOP=true` or a `.emergency_stop` file halts trading immediately.
- `DRY_RUN=true` or `python main.py --dry-run` performs quote-only testing.
- `agent_log.json` stores summaries and tx proofs only, never raw addresses or full prompts.

## Mainnet flow

1. Copy `.env.example` to `.env`.
2. Fund the Base trader wallet.
3. Run `python register_agent.py`.
4. Run `python main.py --dry-run` to verify quotes/logging.
5. Run `python main.py --once` for one live cycle.
6. Run `python main.py` for the hourly loop.
7. Run `streamlit run streamlit_app.py` for the demo dashboard.

> This environment did not provide funded Base keys or API credentials, so the repo intentionally keeps `agent.json` and `agent_log.json` on safe placeholders rather than fabricating “real” tx hashes.

## Submission checklist

- [ ] Replace the placeholder registration entry in `agent.json` with a live Base registration.
- [ ] Capture at least one swap tx hash in `agent_log.json`.
- [ ] Capture at least one reputation tx hash in `agent_log.json`.
- [ ] Paste BaseScan links into the Synthesis submission.
- [ ] Record the 60-second walkthrough below.

## 60-second demo video script

1. Open `agent.json` and show the official project description.
2. Run `python main.py --dry-run` to show autonomous reasoning without spending funds.
3. Open `agent_log.json` and point out the redacted summary + trade status.
4. Show the Streamlit dashboard.
5. Show the ERC-8004 registration BaseScan page.
6. Show the swap and reputation BaseScan pages.

## BaseScan links to populate after live execution

- Registration: `https://basescan.org/tx/<REGISTRATION_TX_HASH>`
- Swap: `https://basescan.org/tx/<SWAP_TX_HASH>`
- Reputation: `https://basescan.org/tx/<REPUTATION_TX_HASH>`

See `DEPLOYMENT GUIDE.md` for Replit, Railway, and Render steps.
