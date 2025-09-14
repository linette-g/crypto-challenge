import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.analyser import *
from src.transactions import *

test_tokens = [
    "synfutures",
    "unibase", 
    "humanity",
    "anvil",
    "INVALID_TOKEN",
    "",
    "1232325",
]

def run_token_tests():
    print("Running token tests...")
    print("=" * 50)

    for token in test_tokens:
        try:
            print(f"\nTesting token: {token}")
            df = get_token_data(token, 30)
            
            if df is not None and not df.empty:
                print(f"Data retrieved successfully ({len(df)} records)")
                anomalies = detect_anomalies(df)
                
                print(f"Found {len(anomalies)} anomalies")
            else:
                print(f"No data found for token: {token}")
                
        except Exception as e:
            print(f"Error with {token}.")
    
    print("\n" + "=" * 50)
    print("Token tests complete!")

if __name__ == "__main__":
    run_token_tests()