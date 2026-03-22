#!/usr/bin/env python3
"""
VeilTrader AI - Uniswap V3 Executor
Executes real swaps on Base via Uniswap Developer Platform API.
"""

import os, time, requests
from web3 import Web3
from dotenv import load_dotenv

from common import CHAIN_ID, NETWORK, TOKENS as COMMON_TOKENS

load_dotenv()


class UniswapExecutor:
    ROUTER = NETWORK["uniswap_router"]
    ABI = [
        {
            "inputs": [
                {
                    "components": [
                        {"name": "tokenIn", "type": "address"},
                        {"name": "tokenOut", "type": "address"},
                        {"name": "fee", "type": "uint24"},
                        {"name": "amountIn", "type": "uint256"},
                        {"name": "amountOutMinimum", "type": "uint256"},
                        {"name": "sqrtPriceLimitX96", "type": "uint160"},
                    ],
                    "name": "params",
                    "type": "tuple",
                }
            ],
            "name": "exactInputSingle",
            "outputs": [{"name": "amountOut", "type": "uint256"}],
            "stateMutability": "payable",
            "type": "function",
        }
    ]
    TOKENS = {
        "USDC": NETWORK["usdc"],
        "WETH": NETWORK["weth"],
        "USDT": "0xDcEF968D448955473Cd7Cb1cFf81EB52e43FA5CE",
        "DAI": "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
        "WSTETH": NETWORK.get("wsteth") or "0x0000000000000000000000000000000000000000",
        "STETH": "0xc58d696aBd4633fC27Dd9D5C338242Cc62dC82A7",
    }
    DECIMALS = {"USDC": 6, "USDT": 6, "DAI": 18, "WETH": 18, "STETH": 18, "WSTETH": 18}
    FEES = {("USDC", "USDT"): 500, ("USDT", "USDC"): 500, "default": 3000}

    def __init__(self):
        rpc_url = os.getenv("BASE_RPC_URL", NETWORK["rpc"])
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not self.w3.is_connected():
            raise ConnectionError(f"Base RPC connection failed at {rpc_url}")
        self.api_key = os.getenv("UNISWAP_API_KEY")
        self.contract = self.w3.eth.contract(
            Web3.to_checksum_address(self.ROUTER), abi=self.ABI
        )
        self.account = self._get_account()

    def _get_account(self):
        key = os.getenv("PRIVATE_KEY")
        if not key:
            raise ValueError("PRIVATE_KEY not set")
        return self.w3.eth.account.from_key(key)

    def _quote(self, token_in, token_out, amount_wei):
        if not self.api_key:
            raise ValueError("UNISWAP_API_KEY not set")
        dec_in, dec_out = (
            self.DECIMALS.get(token_in, 18),
            self.DECIMALS.get(token_out, 18),
        )
        params = {
            "inputToken": token_in,
            "outputToken": token_out,
            "amount": str(amount_wei / (10**dec_in)),
        }
        for attempt in range(3):
            try:
                r = requests.get(
                    "https://api.uniswap.org/v1/quote",
                    params=params,
                    headers={"X-API-KEY": self.api_key},
                    timeout=15,
                )
                r.raise_for_status()
                data = r.json()
                return {
                    "amountOut": int(float(data["amountOut"]) * (10**dec_out)),
                    "priceImpact": data.get("priceImpact", 0),
                }
            except Exception as e:
                if attempt == 2:
                    raise Exception(f"Uniswap API failed: {e}")
                time.sleep(2**attempt)

    def execute_swap(self, token_in, token_out, amount_wei, slippage=0.01):
        """Execute swap and return receipt dict"""
        token_in_addr = self.TOKENS.get(token_in.upper()) or Web3.to_checksum_address(
            token_in
        )
        token_out_addr = self.TOKENS.get(token_out.upper()) or Web3.to_checksum_address(
            token_out
        )
        fee = self.FEES.get((token_in.upper(), token_out.upper()), self.FEES["default"])

        # Get quote
        quote = self._quote(token_in_addr, token_out_addr, amount_wei)
        amount_out_min = int(quote["amountOut"] * (1 - slippage))

        # Build tx
        params = (token_in_addr, token_out_addr, fee, amount_wei, amount_out_min, 0)
        data = self.contract.encodeABI("exactInputSingle", [params])

        tx = {
            "to": self.ROUTER,
            "data": data,
            "value": 0,
            "gas": 200000,
            "gasPrice": self.w3.eth.gas_price,
            "nonce": self.w3.eth.get_transaction_count(self.account.address),
            "chainId": CHAIN_ID,
        }

        signed = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        print(f"Swap tx sent: {tx_hash.hex()}")

        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
        if receipt.status == 1:
            return {
                "transactionHash": tx_hash.hex(),
                "blockNumber": receipt.blockNumber,
                "status": "success",
                "amountOut": quote["amountOut"],
                "priceImpact": quote["priceImpact"],
            }
        return {"status": "failed", "error": "Transaction reverted"}


if __name__ == "__main__":
    e = UniswapExecutor()
    print(f"Connected: {e.w3.is_connected()}, Account: {e.account.address}")
