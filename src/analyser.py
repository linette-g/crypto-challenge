import requests
import pandas as pd
import matplotlib.pyplot as plt

def get_token_data(token_id='dogecoin', days=30):
    url = f"https://api.coingecko.com/api/v3/coins/{token_id}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days,
        'interval': 'daily'
    }
    
    response = requests.get(url, params=params, timeout=30)
    data = response.json()
    
    df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    df['volume'] = [v[1] for v in data['total_volumes']]
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('date', inplace=True)
    
    return df[['price', 'volume']]

def detect_anomalies(df):
    df = df.copy()
    df['price_change'] = df['price'].pct_change() * 100
    df['volume_change'] = df['volume'].pct_change() * 100
    
    anomalies = []
    for date, row in df.iterrows():
        if row['price_change'] > 30:
            anomalies.append({'date': date, 'type': 'price', 'change': row['price_change']})
        if row['volume_change'] > 500:
            anomalies.append({'date': date, 'type': 'volume', 'change': row['volume_change']})
    
    return anomalies

def print_anomalies(anomalies):
    print("Anomalies Detected:")
    for anomaly in anomalies:
        print(f"Date: {anomaly['date'].strftime('%Y-%m-%d')} | Type: {anomaly['type']:6} | Change: {anomaly['change']:8.1f}%")
    print("------Complete------")

def plot_anomalies(df, anomalies):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # prices
    ax1.plot(df.index, df['price'], 'b-')
    ax1.set_ylabel('Price (USD)')
    
    # volumes
    ax2.bar(df.index, df['volume'], color='green')
    ax2.set_ylabel('Volume')
    
    price_anomaly_dates = set()
    volume_anomaly_dates = set()

    # anomalies
    for anomaly in anomalies:
        date = anomaly['date']
        
        ax1.axvline(anomaly['date'], color='red', linestyle='--')
        ax2.axvline(anomaly['date'], color='red', linestyle='--')
        
        if anomaly['type'] == 'price':
            price_anomaly_dates.add(date)
            ax1.text(date, df['price'].max(), f"price spike: {anomaly['change']:.0f}%", 
                rotation=15, ha='center')
        else:
            volume_anomaly_dates.add(date)
            ax2.text(date, df['volume'].max(), f"volume spike: {anomaly['change']:.0f}%", 
                rotation=15, ha='center')

    suspicious_dates = price_anomaly_dates & volume_anomaly_dates

    for date in suspicious_dates:
        ax1.text(date, df['price'].min(), "Suspicious Activity", 
                rotation=15, ha='right', color='red')

    plt.show()

df = get_token_data('synfutures', 30)
anomalies = detect_anomalies(df)
print_anomalies(anomalies)
plot_anomalies(df, anomalies)
