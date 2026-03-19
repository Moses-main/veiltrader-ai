# DEPLOYMENT GUIDE

## Replit

1. Create a new Python Repl and import this repository.
2. Add every variable from `.env.example` to Replit Secrets.
3. Run `pip install -r requirements.txt`.
4. Run `python register_agent.py` once after funding the Base wallet.
5. Start the worker with `python main.py`.
6. Start the demo UI with `streamlit run streamlit_app.py --server.port 3000 --server.address 0.0.0.0`.
7. Rerun `python register_agent.py --write-only` after you know the final public URLs.

## Railway

1. Create a project from this repo.
2. Add `.env.example` variables in Railway's Variables tab.
3. Create a worker service using `python main.py`.
4. Create a web service using `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`.
5. Run `python register_agent.py` once from Railway's shell after funding the wallet.

## Render

1. Create a Background Worker for `python main.py`.
2. Create a Web Service for the Streamlit command above.
3. Reuse the same environment variables on both services.
4. Run `python register_agent.py` from the Render shell after wallet funding.

## MetaMask delegation note

If you want the MetaMask delegation prize path, replace the EOA signer with a session key / delegation signer. The reasoning, Uniswap quote flow, and ERC-8004 proof pipeline remain the same.
