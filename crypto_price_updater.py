"""
Crypto Price Updater for Notion

This module fetches current cryptocurrency prices from the CoinGecko API
and updates a Notion database with the latest values.

Author: Marc Luettecke
License: MIT
"""

import requests
import os
from datetime import datetime
from notion_client import Client


def get_crypto_prices():
    """
    Fetch current Bitcoin and Ethereum prices from CoinGecko API.
    
    Returns:
        dict: A dictionary containing price data for Bitcoin and Ethereum,
              including current price, 24h change percentage, and market cap.
              Returns None if the API request fails.
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin,ethereum',
        'vs_currencies': 'eur',
        'include_24hr_change': 'true',
        'include_market_cap': 'true'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return {
            'bitcoin': {
                'price': data['bitcoin']['eur'],
                'change_24h': data['bitcoin']['eur_24h_change'],
                'market_cap': data['bitcoin']['eur_market_cap']
            },
            'ethereum': {
                'price': data['ethereum']['eur'],
                'change_24h': data['ethereum']['eur_24h_change'],
                'market_cap': data['ethereum']['eur_market_cap']
            }
        }
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return None


def update_notion_database(prices):
    """
    Update Notion database with the latest cryptocurrency prices.
    
    This function queries the Notion database for all BTC and ETH entries
    and updates their 'Price today' and 'Last updated' fields.
    
    Args:
        prices (dict): Dictionary containing current prices for Bitcoin and Ethereum
    """
    notion = Client(auth=os.environ.get("NOTION_TOKEN"))
    database_id = os.environ.get("NOTION_DATABASE_ID")
    
    if not notion or not database_id:
        print("Missing NOTION_TOKEN or NOTION_DATABASE_ID environment variables")
        return
    
    if prices['bitcoin']['price'] < 1000 or prices['bitcoin']['price'] > 1000000:
        print(f"Warning: Bitcoin price {prices['bitcoin']['price']} seems unrealistic, skipping update")
        return
    
    if prices['ethereum']['price'] < 10 or prices['ethereum']['price'] > 100000:
        print(f"Warning: Ethereum price {prices['ethereum']['price']} seems unrealistic, skipping update")
        return
    
    try:
        all_pages = []
        
        filter_query = {
            "or": [
                {"property": "Ticker", "select": {"equals": "BTC"}},
                {"property": "Ticker", "select": {"equals": "ETH"}}
            ]
        }
        
        response = notion.databases.query(
            database_id=database_id,
            filter=filter_query
        )
        
        all_pages.extend(response['results'])
        
        while response.get('has_more'):
            response = notion.databases.query(
                database_id=database_id,
                filter=filter_query,
                start_cursor=response['next_cursor']
            )
            all_pages.extend(response['results'])
        
        btc_count = 0
        eth_count = 0
        
        btc_price = prices['bitcoin']['price']
        eth_price = prices['ethereum']['price']
        current_timestamp = datetime.now().isoformat()
        
        for page in all_pages:
            properties = page['properties']
            
            if 'Ticker' in properties and properties['Ticker'].get('select'):
                ticker = properties['Ticker']['select'].get('name', '')
                
                if ticker == 'BTC':
                    update_data = {
                        'Price today': {
                            'number': btc_price
                        },
                        'Last updated': {
                            'date': {
                                'start': current_timestamp
                            }
                        }
                    }
                    notion.pages.update(page_id=page['id'], properties=update_data)
                    btc_count += 1
                    
                elif ticker == 'ETH':
                    update_data = {
                        'Price today': {
                            'number': eth_price
                        },
                        'Last updated': {
                            'date': {
                                'start': current_timestamp
                            }
                        }
                    }
                    notion.pages.update(page_id=page['id'], properties=update_data)
                    eth_count += 1
        
        if btc_count > 0:
            print(f"Updated {btc_count} Bitcoin entries with price: €{btc_price:,.2f}")
        if eth_count > 0:
            print(f"Updated {eth_count} Ethereum entries with price: €{eth_price:,.2f}")
                    
    except Exception as e:
        print(f"Error updating Notion database: {e}")


def main():
    """
    Main execution function.
    
    Fetches cryptocurrency prices and updates the Notion database.
    """
    print(f"Starting crypto price update at {datetime.now()}")
    
    prices = get_crypto_prices()
    
    if prices:
        print(f"Bitcoin: €{prices['bitcoin']['price']:,.2f} ({prices['bitcoin']['change_24h']:.2f}%)")
        print(f"Ethereum: €{prices['ethereum']['price']:,.2f} ({prices['ethereum']['change_24h']:.2f}%)")
        
        update_notion_database(prices)
        print("Update completed successfully!")
    else:
        print("Failed to fetch crypto prices")


if __name__ == "__main__":
    main()