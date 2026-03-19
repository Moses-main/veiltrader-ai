# DEPLOYMENT GUIDE

## Replit one-click flow

1. Create a new Python Repl and import this repository.
2. Open **Secrets** and paste every key from `.env.example`.
3. In the shell, run `pip install -r requirements.txt`.
4. Run `python register_agent.py` once to mint the ERC-8004 identity.
5. Run `python main.py` as the always-on worker.
6. Add a second Replit tab for `streamlit run streamlit_app.py --server.port 3000 --server.address 0.0.0.0`.
7. Use the Replit URL for `PUBLIC_APP_URL` / `STREAMLIT_URL` in `.env`, then rerun `python register_agent.py --write-only` to refresh `agent.json`.

## Railway alternative

1. Create a new Railway project from this repo.
2. Add all `.env.example` variables in the Railway Variables panel.
3. Add a worker service using `python main.py`.
4. Add a web service using `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`.
5. Run a one-off shell command `python register_agent.py` after funding the Base wallet.

## Render alternative

1. Create a **Background Worker** for `python main.py`.
2. Create a **Web Service** for the Streamlit command above.
3. Set the same environment variables on both services.
4. Run `python register_agent.py` from the Render shell after wallet funding.

## MetaMask Delegation Framework note

To extend this repo for the MetaMask delegation prize, swap the signer in `common.py` for a session-key signer and optionally migrate the swap path to Uniswap's `swap_7702` flow. The portfolio, reasoning, and ERC-8004 proof pipeline remain unchanged.
