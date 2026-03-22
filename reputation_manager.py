#!/usr/bin/env python3
"""
VeilTrader AI - ERC-8004 Reputation Manager
Posts real feedback to the on-chain Reputation Registry after trades.
"""

import os, json, time
from web3 import Web3
from dotenv import load_dotenv

from common import CHAIN_ID, NETWORK

load_dotenv()

ERC8004_REPUTATION = NETWORK["reputation_registry"]
ABI = [
    {
        "inputs": [
            {"name": "agentId", "type": "uint256"},
            {"name": "rating", "type": "uint8"},
            {"name": "feedback", "type": "string"},
            {"name": "proof", "type": "bytes"},
        ],
        "name": "postFeedback",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    }
]


class ReputationManager:
    def __init__(self):
        rpc_url = os.getenv("BASE_RPC_URL", NETWORK["rpc"])
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not self.w3.is_connected():
            raise ConnectionError(f"Base RPC connection failed at {rpc_url}")
        self.contract = self.w3.eth.contract(
            Web3.to_checksum_address(ERC8004_REPUTATION), abi=ABI
        )
        self.account = self._get_account()
        with open("agent.json") as f:
            self.agent_id = json.load(f).get("agentId", 123456789)

    def _get_account(self):
        key = os.getenv("PRIVATE_KEY")
        if not key:
            raise ValueError("PRIVATE_KEY not set")
        return self.w3.eth.account.from_key(key)

    def post_feedback(
        self, trade_success=True, profit_loss_usd=0, tx_hash="", block_number=0
    ):
        """Post feedback to ERC-8004 Reputation Registry"""
        rating = (
            5 if (trade_success and profit_loss_usd > 0) else 4 if trade_success else 2
        )
        feedback = f"Agent {self.agent_id} trade | P&L: {'+' if profit_loss_usd >= 0 else ''}${profit_loss_usd:.2f} | Tx: {tx_hash[:10]}..."
        proof = b""

        tx = self.contract.functions.postFeedback(
            self.agent_id, rating, feedback, proof
        ).build_transaction(
            {
                "from": self.account.address,
                "nonce": self.w3.eth.get_transaction_count(self.account.address),
                "gas": 100000,
                "gasPrice": self.w3.eth.gas_price,
                "chainId": CHAIN_ID,
            }
        )

        signed = self.account.sign_transaction(tx)
        sent = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        print(f"Reputation feedback tx: {sent.hex()}")

        receipt = self.w3.eth.wait_for_transaction_receipt(sent, timeout=60)
        self._log_feedback(rating, feedback, tx_hash, block_number)
        return receipt.status == 1

    def _log_feedback(self, rating, feedback, tx_hash, block_number):
        try:
            entry = {
                "timestamp": int(time.time()),
                "event": "reputation_feedback_posted",
                "agentId": self.agent_id,
                "rating": rating,
                "feedback": feedback,
                "txHash": tx_hash,
                "blockNumber": block_number,
            }
            data = (
                json.load(open("agent_log.json"))
                if os.path.exists("agent_log.json")
                else {"logs": []}
            )
            data["logs"].append(entry)
            json.dump(data, open("agent_log.json", "w"), indent=2)
        except:
            pass


def post_trade_reputation(
    trade_success=True, profit_loss_usd=0, tx_hash="", block_number=0
):
    return ReputationManager().post_feedback(
        trade_success, profit_loss_usd, tx_hash, block_number
    )


if __name__ == "__main__":
    print(f"Agent ID: {ReputationManager().agent_id}")
