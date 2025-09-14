import requests
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import networkx as nx

load_dotenv()
    
def get_transactions(address: str, limit: int = 15) -> List[Dict]:
    api_key = os.getenv('ETHERSCAN_API_KEY')

    if not api_key or "YourActualAPIKeyHere" in api_key:
        raise ValueError(
            "API key not configured. "
            "Please create a .env file with ETHERSCAN_API_KEY=YourActualKeyHere."
        )
    
    base_url = 'https://api.etherscan.io/api'

    params = {
        'module': 'account',
        'action': 'txlist',
        'address': address,
        'startblock': 0,
        'endblock': 99999999,
        'sort': 'desc',
        'apikey': api_key
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] == '1' and data['message'] == 'OK':
            transactions = data['result'][:limit]
            print(f"Fetched {len(transactions)} transactions")
            return transactions
        else:
            print(f"API Error: {data.get('message', 'Unknown error')}")
            return []
            
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
    
def get_transaction_graph(transactions: List[Dict]) -> nx.DiGraph:
    G = nx.DiGraph()
    
    for tx in transactions:
        sender_addr = tx.get('from', '')
        receiver_addr = tx.get('to', '')
        
        if sender_addr and receiver_addr:
            # ethereum uses Wei
            value_eth = float(tx.get('value', 0)) / 1e18
            G.add_edge(sender_addr, receiver_addr, weight=value_eth)
    
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=200, font_size=8)
    edge_labels = {(u, v): f"{G[u][v]['weight']:.2f}ETH" for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    plt.title("Transaction Network")
    plt.show()


wallet_address = "0x28C6c06298d514Db089934071355E5743bf21d60"   # Binance wallet
transactions = get_transactions(wallet_address, limit=15)
get_transaction_graph(transactions)
