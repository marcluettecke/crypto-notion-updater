"""
CoinGecko API Test Utility

This module tests the CoinGecko API endpoints to verify connectivity
and display current cryptocurrency prices.

Author: Marc Luettecke
License: MIT
"""

import requests
from datetime import datetime


def test_coingecko_api():
    """
    Test CoinGecko API endpoints and display current cryptocurrency prices.
    
    This function performs the following tests:
    1. Fetches current prices for Bitcoin and Ethereum
    2. Displays detailed price information including 24h changes
    3. Tests the API health endpoint
    """
    print("Testing CoinGecko API...")
    print("-" * 50)
    
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin,ethereum',
        'vs_currencies': 'eur',
        'include_24hr_change': 'true',
        'include_market_cap': 'true',
        'include_24hr_vol': 'true',
        'include_last_updated_at': 'true'
    }
    
    try:
        response = requests.get(url, params=params)
        print(f"API Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\nAPI Response:")
            print(f"Raw data: {data}")
            
            print("\n" + "="*50)
            print("BITCOIN (BTC)")
            print("="*50)
            print(f"Price: €{data['bitcoin']['eur']:,.2f}")
            print(f"24h Change: {data['bitcoin']['eur_24h_change']:.2f}%")
            print(f"Market Cap: €{data['bitcoin']['eur_market_cap']:,.0f}")
            print(f"24h Volume: €{data['bitcoin']['eur_24h_vol']:,.0f}")
            
            btc_timestamp = datetime.fromtimestamp(data['bitcoin']['last_updated_at'])
            print(f"Last Updated: {btc_timestamp}")
            
            print("\n" + "="*50)
            print("ETHEREUM (ETH)")
            print("="*50)
            print(f"Price: €{data['ethereum']['eur']:,.2f}")
            print(f"24h Change: {data['ethereum']['eur_24h_change']:.2f}%")
            print(f"Market Cap: €{data['ethereum']['eur_market_cap']:,.0f}")
            print(f"24h Volume: €{data['ethereum']['eur_24h_vol']:,.0f}")
            
            eth_timestamp = datetime.fromtimestamp(data['ethereum']['last_updated_at'])
            print(f"Last Updated: {eth_timestamp}")
            
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error testing API: {e}")
    
    print("\n" + "-"*50)
    print("Testing API health...")
    ping_url = "https://api.coingecko.com/api/v3/ping"
    try:
        ping_response = requests.get(ping_url)
        print(f"Ping Status: {ping_response.status_code}")
        print(f"Ping Response: {ping_response.json()}")
    except Exception as e:
        print(f"Ping failed: {e}")


if __name__ == "__main__":
    test_coingecko_api()