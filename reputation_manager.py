"""ERC-8004 feedback posting for verifiable trade receipts."""
from __future__ import annotations

import json

from web3 import Web3

from common import REPUTATION_REGISTRY, account_from_key, basescan_tx, data_uri, env, send_tx, w3

ABI = [{"name": "giveFeedback", "type": "function", "stateMutability": "nonpayable", "inputs": [
    {"name": "agentId", "type": "uint256"}, {"name": "value", "type": "int128"}, {"name": "valueDecimals", "type": "uint8"},
    {"name": "tag1", "type": "string"}, {"name": "tag2", "type": "string"}, {"name": "endpoint", "type": "string"},
    {"name": "feedbackURI", "type": "string"}, {"name": "feedbackHash", "type": "bytes32"}], "outputs": []}]


def post_trade_feedback(agent_id: int, trade_tx: str, score_bps: int = 100) -> dict:
    client = w3()
    key_env = "REPUTATION_PRIVATE_KEY" if env("REPUTATION_PRIVATE_KEY") else "PRIVATE_KEY"
    reviewer = account_from_key(client, key_env)
    proof = {"agentId": agent_id, "tradeTx": trade_tx, "proofOfPayment": {"chainId": "8453", "txHash": trade_tx}, "note": "Verifiable trade proof only; no portfolio state retained."}
    proof_json = json.dumps(proof, separators=(",", ":"))
    contract = client.eth.contract(address=REPUTATION_REGISTRY, abi=ABI)
    tx_hash = send_tx(
        client,
        contract.functions.giveFeedback(agent_id, score_bps, 0, "successRate", "swap", basescan_tx(trade_tx), data_uri(proof), Web3.keccak(text=proof_json).hex()).build_transaction({"from": reviewer.address}),
        key_env,
    )
    return {"status": "submitted", "tx_hash": tx_hash, "basescan": basescan_tx(tx_hash), "reviewer": reviewer.address}
