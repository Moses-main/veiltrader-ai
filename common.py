"""Shared helpers and network constants for VeilTrader."""
from __future__ import annotations

import base64
import json
import os
import time
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

load_dotenv()
BASE_CHAIN_ID = 8453
BASESCAN = "https://basescan.org"
IDENTITY_REGISTRY = Web3.to_checksum_address("0x8004A169FB4a3325136EB29fA0ceB6D2e539a432")
REPUTATION_REGISTRY = Web3.to_checksum_address("0x8004BAa17C55a88189AE136b182e5fdA19dE9b63")
UNISWAP_V3_ROUTER = Web3.to_checksum_address("0x2626664c2603336E57B271c5C0b26F421741e481")
WETH = Web3.to_checksum_address("0x4200000000000000000000000000000000000006")
USDC = Web3.to_checksum_address("0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913")
TOKENS = {
    "ETH": {"address": None, "decimals": 18},
    "WETH": {"address": WETH, "decimals": 18},
    "USDC": {"address": USDC, "decimals": 6},
}
ERC20_ABI = [
    {"name": "balanceOf", "type": "function", "stateMutability": "view", "inputs": [{"name": "owner", "type": "address"}], "outputs": [{"type": "uint256"}]},
    {"name": "allowance", "type": "function", "stateMutability": "view", "inputs": [{"type": "address"}, {"type": "address"}], "outputs": [{"type": "uint256"}]},
    {"name": "approve", "type": "function", "stateMutability": "nonpayable", "inputs": [{"type": "address"}, {"type": "uint256"}], "outputs": [{"type": "bool"}]},
]


def env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def env_bool(name: str, default: bool = False) -> bool:
    return env(name, str(default)).lower() in {"1", "true", "yes", "on"}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(value, high))


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def basescan_tx(tx_hash: str) -> str:
    return f"{BASESCAN}/tx/{tx_hash}"


def load_json(path: str, default: Any) -> Any:
    p = Path(path)
    return default if not p.exists() else json.loads(p.read_text())


def save_json(path: str, payload: Any) -> None:
    Path(path).write_text(json.dumps(payload, indent=2) + "\n")


def data_uri(payload: dict[str, Any]) -> str:
    blob = json.dumps(payload, separators=(",", ":")).encode()
    return "data:application/json;base64," + base64.b64encode(blob).decode()


def http_json(method: str, url: str, *, headers: dict[str, str] | None = None, json_body: dict[str, Any] | None = None, retries: int = 4, timeout: int = 30) -> dict[str, Any]:
    """Simple retry helper for rate-limits and flaky gateways."""
    for attempt in range(1, retries + 1):
        try:
            response = requests.request(method, url, headers=headers, json=json_body, timeout=timeout)
            if response.status_code in {429, 500, 502, 503, 504} and attempt < retries:
                time.sleep(min(2**attempt, 10))
                continue
            response.raise_for_status()
            return response.json() if response.text else {}
        except Exception:
            if attempt == retries:
                raise
            time.sleep(min(2**attempt, 10))
    return {}


def w3() -> Web3:
    client = Web3(Web3.HTTPProvider(env("BASE_RPC_URL", "https://mainnet.base.org")))
    client.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    if not client.is_connected():
        raise RuntimeError("Base RPC unavailable")
    return client


def account_from_key(client: Web3, key_env: str = "PRIVATE_KEY"):
    key = env(key_env)
    if not key:
        raise RuntimeError(f"Missing {key_env}")
    return client.eth.account.from_key(key)


def gas_price_gwei(client: Web3) -> float:
    return float(client.from_wei(client.eth.gas_price, "gwei"))


def send_tx(client: Web3, built: dict[str, Any], key_env: str = "PRIVATE_KEY") -> str:
    acct = account_from_key(client, key_env)
    tx = {
        **built,
        "from": built.get("from", acct.address),
        "chainId": BASE_CHAIN_ID,
        "nonce": client.eth.get_transaction_count(acct.address),
        "gasPrice": client.eth.gas_price,
    }
    tx.setdefault("gas", int(client.eth.estimate_gas(tx) * 1.15))
    signed = acct.sign_transaction(tx)
    return client.eth.send_raw_transaction(signed.raw_transaction).hex()
