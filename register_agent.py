"""Register VeilTrader in the ERC-8004 Identity Registry on Base."""
from __future__ import annotations
import argparse
from common import IDENTITY_REGISTRY, account_from_key, basescan_tx, data_uri, env, load_json, now_iso, save_json, send_tx, w3

ABI = [
  {"name": "register", "type": "function", "stateMutability": "nonpayable", "inputs": [{"name": "agentURI", "type": "string"}], "outputs": [{"type": "uint256"}]},
  {"anonymous": False, "type": "event", "name": "Registered", "inputs": [{"indexed": True, "name": "agentId", "type": "uint256"}, {"indexed": False, "name": "agentURI", "type": "string"}, {"indexed": True, "name": "owner", "type": "address"}]}
]

def main(write_only: bool = False) -> None:
    payload = load_json("agent.json", {})
    payload["wallets"] = {"base": env("TRADER_ADDRESS") or "0x0000000000000000000000000000000000000000"}
    services = payload.get("services", [])
    for item, key in (("web", "PUBLIC_APP_URL"), ("A2A", "A2A_URL"), ("MCP", "MCP_URL"), ("dashboard", "STREAMLIT_URL")):
        for svc in services:
            if svc.get("name") == item and env(key): svc["endpoint"] = env(key)
    if write_only:
        save_json("agent.json", payload); print("Updated agent.json without chain write."); return
    client = w3(); acct = account_from_key(client)
    uri = data_uri(payload)
    registry = client.eth.contract(address=IDENTITY_REGISTRY, abi=ABI)
    tx_hash = send_tx(client, registry.functions.register(uri).build_transaction({"from": acct.address}))
    receipt = client.eth.wait_for_transaction_receipt(tx_hash, timeout=600)
    event = registry.events.Registered().process_receipt(receipt)[0]["args"]
    payload["registrations"] = [{
        "agentId": int(event["agentId"]),
        "agentRegistry": f"eip155:8453:{IDENTITY_REGISTRY}",
        "txHash": tx_hash,
        "chainExplorer": basescan_tx(tx_hash),
        "registeredAt": now_iso(),
    }]
    save_json("agent.json", payload)
    print(f"Agent registered: #{event['agentId']}")
    print(basescan_tx(tx_hash))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-only", action="store_true", help="refresh endpoints locally without a transaction")
    main(parser.parse_args().write_only)
