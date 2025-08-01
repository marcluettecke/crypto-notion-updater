import requests
import os
from datetime import datetime
from notion_client import Client

def get_crypto_prices():
    """Fetch current BTC and ETH prices from CoinGecko API"""
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
    """Update Notion database with latest crypto prices"""
    notion = Client(auth=os.environ.get("NOTION_TOKEN"))
    database_id = os.environ.get("NOTION_DATABASE_ID")
    
    if not notion or not database_id:
        print("Missing NOTION_TOKEN or NOTION_DATABASE_ID environment variables")
        return
    
    try:
        # Query the database to get all entries
        response = notion.databases.query(database_id=database_id)
        
        for page in response['results']:
            properties = page['properties']
            
            # Check if this is a Bitcoin or Ethereum entry
            # Adjust these property names based on your Notion database structure
            if 'Cryptocurrency' in properties:
                crypto_name = properties['Cryptocurrency'].get('title', [{}])[0].get('text', {}).get('content', '').lower()
                
                if crypto_name == 'bitcoin' and prices['bitcoin']:
                    update_data = {
                        'Current Price': {
                            'number': prices['bitcoin']['price']
                        },
                        '24h Change %': {
                            'number': round(prices['bitcoin']['change_24h'], 2)
                        },
                        'Last Updated': {
                            'date': {
                                'start': datetime.now().isoformat()
                            }
                        }
                    }
                    
                    notion.pages.update(page_id=page['id'], properties=update_data)
                    print(f"Updated Bitcoin price: €{prices['bitcoin']['price']:,.2f}")
                    
                elif crypto_name == 'ethereum' and prices['ethereum']:
                    update_data = {
                        'Current Price': {
                            'number': prices['ethereum']['price']
                        },
                        '24h Change %': {
                            'number': round(prices['ethereum']['change_24h'], 2)
                        },
                        'Last Updated': {
                            'date': {
                                'start': datetime.now().isoformat()
                            }
                        }
                    }
                    
                    notion.pages.update(page_id=page['id'], properties=update_data)
                    print(f"Updated Ethereum price: €{prices['ethereum']['price']:,.2f}")
                    
    except Exception as e:
        print(f"Error updating Notion database: {e}")

def main():
    print(f"Starting crypto price update at {datetime.now()}")
    
    # Fetch latest prices
    prices = get_crypto_prices()
    
    if prices:
        print(f"Bitcoin: €{prices['bitcoin']['price']:,.2f} ({prices['bitcoin']['change_24h']:.2f}%)")
        print(f"Ethereum: €{prices['ethereum']['price']:,.2f} ({prices['ethereum']['change_24h']:.2f}%)")
        
        # Update Notion database
        update_notion_database(prices)
        print("Update completed successfully!")
    else:
        print("Failed to fetch crypto prices")

if __name__ == "__main__":
    main()