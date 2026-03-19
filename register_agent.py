"""Register VeilTrader in the ERC-8004 Identity Registry on Base."""
from __future__ import annotations

import argparse

from common import IDENTITY_REGISTRY, account_from_key, basescan_tx, data_uri, env, load_json, now_iso, save_json, send_tx, w3

ABI = [
    {"name": "register", "type": "function", "stateMutability": "nonpayable", "inputs": [{"name": "agentURI", "type": "string"}], "outputs": [{"type": "uint256"}]},
    {"anonymous": False, "type": "event", "name": "Registered", "inputs": [{"indexed": True, "name": "agentId", "type": "uint256"}, {"indexed": False, "name": "agentURI", "type": "string"}, {"indexed": True, "name": "owner", "type": "address"}]},
]


def build_payload() -> dict:
    payload = load_json("agent.json", {})
    payload["wallets"] = {"base": env("TRADER_ADDRESS") or payload.get("wallets", {}).get("base", "0x0000000000000000000000000000000000000000")}
    for service, key in (("web", "PUBLIC_APP_URL"), ("A2A", "A2A_URL"), ("MCP", "MCP_URL"), ("dashboard", "STREAMLIT_URL")):
        for item in payload.get("services", []):
            if item.get("name") == service and env(key):
                item["endpoint"] = env(key)
    return payload


def main(write_only: bool = False, print_uri: bool = False) -> None:
    payload = build_payload()
    uri = data_uri(payload)
    if print_uri:
        print(uri)
        return
    if write_only:
        save_json("agent.json", payload)
        print("Updated agent.json without chain write.")
        return
    client = w3()
    acct = account_from_key(client)
    registry = client.eth.contract(address=IDENTITY_REGISTRY, abi=ABI)
    tx_hash = send_tx(client, registry.functions.register(uri).build_transaction({"from": acct.address}))
    receipt = client.eth.wait_for_transaction_receipt(tx_hash, timeout=600)
    agent_id = int(registry.events.Registered().process_receipt(receipt)[0]["args"]["agentId"])
    payload["registrations"] = [{"agentId": agent_id, "agentRegistry": f"eip155:8453:{IDENTITY_REGISTRY}", "txHash": tx_hash, "chainExplorer": basescan_tx(tx_hash), "registeredAt": now_iso()}]
    save_json("agent.json", payload)
    print(f"Agent registered: #{agent_id}\n{basescan_tx(tx_hash)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-only", action="store_true", help="refresh local metadata without a transaction")
    parser.add_argument("--print-uri", action="store_true", help="print the data: URI that would be registered")
    args = parser.parse_args()
    main(args.write_only, args.print_uri)
