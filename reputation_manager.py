"""Post ERC-8004 trade feedback after successful swaps."""
from __future__ import annotations
import json
from common import REPUTATION_REGISTRY, account_from_key, basescan_tx, data_uri, env, send_tx, w3
from web3 import Web3

ABI = [{"name": "giveFeedback", "type": "function", "stateMutability": "nonpayable", "inputs": [
    {"name": "agentId", "type": "uint256"}, {"name": "value", "type": "int128"}, {"name": "valueDecimals", "type": "uint8"},
    {"name": "tag1", "type": "string"}, {"name": "tag2", "type": "string"}, {"name": "endpoint", "type": "string"},
    {"name": "feedbackURI", "type": "string"}, {"name": "feedbackHash", "type": "bytes32"}], "outputs": []}]

def post_trade_feedback(agent_id: int, trade_tx: str, pnl_bps: int = 100) -> dict:
    client = w3(); reviewer = account_from_key(client, "REPUTATION_PRIVATE_KEY" if env("REPUTATION_PRIVATE_KEY") else "PRIVATE_KEY")
    proof = {"agentId": agent_id, "tradeTx": trade_tx, "proofOfPayment": {"chainId": "8453", "txHash": trade_tx}, "note": "Verifiable trade proof only; no raw portfolio data retained."}
    uri = data_uri(proof); feedback_hash = Web3.keccak(text=json.dumps(proof, separators=(",", ":"))).hex()
    contract = client.eth.contract(address=REPUTATION_REGISTRY, abi=ABI)
    tx_hash = send_tx(client, contract.functions.giveFeedback(agent_id, pnl_bps, 0, "successRate", "swap", basescan_tx(trade_tx), uri, feedback_hash).build_transaction({"from": reviewer.address}), "REPUTATION_PRIVATE_KEY" if env("REPUTATION_PRIVATE_KEY") else "PRIVATE_KEY")
    return {"tx_hash": tx_hash, "basescan": basescan_tx(tx_hash), "reviewer": reviewer.address}
