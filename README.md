# Cryptocurrency Data Science Assessment

A Python-based solution for the cryptocurrency data science assessment, addressing both Task 1 (wallet analysis) and Task 2 (market forensics).

## Challenge Overview

This project provides solutions for two main tasks:

### Task 1: Wallet Transaction Analysis
- Fetches recent transactions (max 15) for cryptocurrency wallet address (Binance wallet)
- Creates transaction network graph visualizations (nodes = addresses, edges = transactions)

### Task 2: Market Forensics Analysis  
- Detects unusual market activity in cryptocurrency token (SynFutures chosen)
- Identifies suspicious activity like pump-and-dump schemes via analysis of price and volume anomalies

## Installation

### Prerequisites
- Python 3.8+
- Etherscan API key (free tier available)
- pip package manager

### Quick Setup
```bash
# Clone the repository
git clone https://github.com/linette-g/crypto-challenge.git
cd crypto-challenge

# Install dependencies
pip install -r requirements.txt
```

### Required API Keys

You need an **Etherscan API key** to run this project.
1. Get a free API key from [Etherscan](https://etherscan.io/myapikey).
2. Add the key to a `.env` file in your project directory:

```env
ETHERSCAN_API_KEY=YourActualAPIKeyHere
```

## Example Usage
```bash
# Go into the correct directory
cd src
python transactions.py  # task 1
python analyser.py  # task 2
```

## Results

### Task 1 
Transaction Graph

![transaction graph](./transaction-graph.png)

### Task 2
Anomalies Graph

![anomalies graph](./synfutures-analysis.png)

Printed output

![printed output](./print-output.png)
