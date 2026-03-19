# VeilTrader

> "VeilTrader is a fully autonomous, privacy-first AI trading agent on Base (Ethereum). It privately analyzes any user’s DeFi portfolio using a no-data-retention LLM (Venice/Groq/Bankr fallback), makes risk-aware trade decisions, executes real Uniswap V3 swaps using the official Uniswap Developer Platform API + on-chain router, posts reputation updates to the ERC-8004 Reputation Registry, and only publishes verifiable transaction proofs. After one-time setup it runs forever with zero human intervention. Built to win Venice 'Private Agents, Trusted Actions', Uniswap 'Agentic Finance', Bankr 'Best LLM Gateway', Protocol Labs 'Agents With Receipts — ERC-8004' + 'Let the Agent Cook', and Synthesis Open Track."

## Prize targeting table

| Prize | Implementation in this repo |
|---|---|
| Venice - Private Agents, Trusted Actions | `llm_brain.py` uses Groq default, Venice fallback, and avoids raw portfolio logging. |
| Uniswap - Agentic Finance | `uniswap_executor.py` requests quotes from the official Uniswap Developer Platform Trade API, then signs a real Base Uniswap V3 `exactInputSingle` swap. |
| Bankr - Best LLM Gateway | Bankr is the third fallback provider and `main.py` tracks a rolling Bankr budget from estimated trading profits. |
| Protocol Labs - Agents With Receipts / Let the Agent Cook | `register_agent.py` writes ERC-8004 identity data and `reputation_manager.py` publishes verifiable trade proofs to the reputation registry. |
| MetaMask Delegation Framework | The repo is EOA-native today; session-key / EIP-7702 extension points are called out in code comments and deployment docs. |
| Synthesis Open Track | The app is autonomous, privacy-first, Python-only, and ready for Base mainnet deployment. |

## What is included

- ERC-8004 identity registration on Base via `register_agent.py`.
- `agent.json` and append-only `agent_log.json` for judges.
- Private LLM routing with Groq → Venice → Bankr fallback.
- Base portfolio reads with no raw-balance persistence.
- Uniswap quote + route discovery via official Trade API.
- Real on-chain Uniswap V3 swap execution via router calldata.
- ERC-8004 reputation posting after successful trades.
- Hourly autonomy loop plus emergency stop protections.
- Streamlit dashboard for a 60-second demo.

## Safety model

- Never trades more than `MAX_TRADE_PCT` (default 5%) in a cycle.
- Rejects any LLM recommendation below 70 confidence.
- Caps slippage at 1% (`MAX_SLIPPAGE_BPS=100`).
- Skips trades when gas exceeds `MAX_GAS_ETH`.
- Supports `.emergency_stop` file or `EMERGENCY_STOP=true`.
- Only publishes transaction proofs, not raw portfolio state.

## Real transaction workflow

1. Copy `.env.example` to `.env` and fill Base/LLM/Uniswap secrets.
2. Run `python register_agent.py` to mint the ERC-8004 identity NFT and update `agent.json`.
3. Run `python main.py --once` for a single dry operating cycle.
4. Run `python main.py` for the forever loop.
5. Run `streamlit run streamlit_app.py` for the demo dashboard.

> This environment did not include funded Base credentials or API keys, so the repo ships with pending placeholders rather than fabricated “real” hashes. After you run the commands above, replace placeholder links in your submission package with the generated BaseScan URLs.

## Submission checklist

- [ ] `agent.json` updated with real `agentId` and registration tx hash.
- [ ] At least one swap tx hash captured in `agent_log.json`.
- [ ] At least one ERC-8004 feedback tx hash captured in `agent_log.json`.
- [ ] BaseScan links pasted into the final submission form.
- [ ] 60-second video recorded using the Streamlit dashboard.

## 60-second demo video script

1. Show `agent.json` with the official description and ERC-8004 registry address.
2. Open the Streamlit dashboard and point out agent ID, cycle count, and latest decision.
3. Run `python main.py --once` in a terminal.
4. Show the new `agent_log.json` row with trade / no-trade output.
5. Open BaseScan for the registration tx and the swap tx.
6. Finish on the reputation tx proving on-chain receipts.

## Example links to populate after mainnet execution

- Registration: `https://basescan.org/tx/<REGISTRATION_TX_HASH>`
- Swap: `https://basescan.org/tx/<SWAP_TX_HASH>`
- Reputation: `https://basescan.org/tx/<REPUTATION_TX_HASH>`

## Replit / Render / Railway

See `DEPLOYMENT GUIDE.md` for step-by-step deployment instructions.
