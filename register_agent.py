#!/usr/bin/env python3
"""
VeilTrader AI - ERC-8004 Agent Registration
Performs real on-chain agent identity registration on Base.
"""

import json, os, time
from web3 import Web3
from dotenv import load_dotenv

from common import CHAIN_ID, NETWORK, REPUTATION_REGISTRY

load_dotenv()

ERC8004_IDENTITY_REGISTRY = NETWORK["identity_registry"]

IDENTITY_ABI = [
    {
        "inputs": [
            {"name": "agentId", "type": "uint256"},
            {"name": "metadataURI", "type": "string"},
        ],
        "name": "register",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"name": "agentId", "type": "uint256"}],
        "name": "resolve",
        "outputs": [{"name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
]


def register_agent():
    rpc_url = os.getenv("BASE_RPC_URL", NETWORK["rpc"])
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        print(f"ERROR: Failed to connect to Base RPC at {rpc_url}")
        return None

    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        print("ERROR: PRIVATE_KEY not set in .env")
        return None

    if ERC8004_IDENTITY_REGISTRY == "0x0000000000000000000000000000000000000000":
        print(
            "WARNING: Identity registry not deployed on testnet - skipping registration"
        )
        return {"agentId": 123456789, "address": "TESTNET_MODE"}

    account = w3.eth.account.from_key(private_key)
    contract = w3.eth.contract(
        Web3.to_checksum_address(ERC8004_IDENTITY_REGISTRY), abi=IDENTITY_ABI
    )

    try:
        existing = contract.functions.resolve(123456789).call()
        if existing != "0x0000000000000000000000000000000000000000":
            print(f"Agent already registered at: {existing}")
            return {"agentId": 123456789, "address": existing}
    except:
        pass

    with open("agent.json", "r") as f:
        metadata_uri = f"data:application/json,{f.read()}"

    tx = contract.functions.register(123456789, metadata_uri).build_transaction(
        {
            "from": account.address,
            "nonce": w3.eth.get_transaction_count(account.address),
            "gas": 200000,
            "gasPrice": w3.eth.gas_price,
            "chainId": CHAIN_ID,
        }
    )

    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"Registration tx sent: {tx_hash.hex()}")

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    if receipt.status == 1:
        print(f"SUCCESS: Agent registered in block {receipt.blockNumber}")
        with open("agent.json", "r") as f:
            data = json.load(f)
        data.update(
            {
                "agentId": 123456789,
                "registrationTxn": tx_hash.hex(),
                "identityRegistry": ERC8004_IDENTITY_REGISTRY,
                "reputationRegistry": REPUTATION_REGISTRY,
                "network": os.getenv("BASE_NETWORK", "mainnet"),
            }
        )
        with open("agent.json", "w") as f:
            json.dump(data, f, indent=2)
        return {
            "agentId": 123456789,
            "txHash": tx_hash.hex(),
            "block": receipt.blockNumber,
        }
    else:
        print("ERROR: Registration failed")
        return None


if __name__ == "__main__":
    result = register_agent()
    if result:
        print(f"Agent ID: {result['agentId']}, Tx: {result.get('txHash', 'N/A')}")
