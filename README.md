# Crypto Notion Price Updater

[![Update Crypto Prices](https://github.com/marcluettecke/crypto-notion-updater/actions/workflows/update-crypto-prices.yml/badge.svg)](https://github.com/marcluettecke/crypto-notion-updater/actions/workflows/update-crypto-prices.yml)

Automatically update Bitcoin and Ethereum prices in your Notion database using GitHub Actions - completely free!

## Features

- Fetches real-time BTC and ETH prices in EUR from CoinGecko API (no authentication required)
- Updates your Notion database automatically
- Runs daily via GitHub Actions (free hosting)
- Can be triggered manually through GitHub Actions
- Shows price, 24h change %, and last update time

## Setup Instructions

### 1. Notion Setup

Your Notion database should have these columns:
- **Cryptocurrency** (Title) - "Bitcoin" or "Ethereum"
- **Current Price** (Number) - Will be updated automatically
- **24h Change %** (Number) - Will be updated automatically
- **Last Updated** (Date) - Will be updated automatically

### 2. Get Notion API Credentials

1. Go to https://www.notion.so/my-integrations
2. Create a new integration
3. Copy the Integration Token
4. Share your database with the integration:
   - Open your database in Notion
   - Click "..." menu → "Add connections"
   - Select your integration

### 3. GitHub Setup

1. Fork or create a new repository with this code
2. Go to Settings → Secrets and variables → Actions
3. Add these secrets:
   - `NOTION_TOKEN`: Your Notion integration token
   - `NOTION_DATABASE_ID`: Your database ID (from the database URL)

### 4. Enable GitHub Actions

The workflow will run:
- Automatically every day at 9:00 AM UTC
- Manually when you trigger it from Actions tab

## Manual Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export NOTION_TOKEN="your_token_here"
export NOTION_DATABASE_ID="your_database_id_here"

# Run the updater
python crypto_price_updater.py
```

## Test API

Run `python test_api.py` to test the CoinGecko API and see current prices.

## Files

- `crypto_price_updater.py` - Main script that fetches prices and updates Notion
- `test_api.py` - Test script to verify API is working
- `.github/workflows/update-crypto-prices.yml` - GitHub Actions workflow
- `requirements.txt` - Python dependencies