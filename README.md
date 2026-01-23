# Crypto Notion Price Updater

[![Update Crypto Prices](https://github.com/marcluettecke/crypto-notion-updater/actions/workflows/update-crypto-prices.yml/badge.svg)](https://github.com/marcluettecke/crypto-notion-updater/actions/workflows/update-crypto-prices.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Automated cryptocurrency price tracker that updates Bitcoin and Ethereum prices in your Notion database using GitHub Actions.

## 🚀 Features

- **Real-time Price Updates**: Fetches current BTC and ETH prices in EUR from CoinGecko API access
- **Automated Daily Updates**: Runs automatically every day at 7:00 AM CEST/6:00 AM CET
- **Notion Integration**: Directly updates your investment tracking database
- **GitHub Actions**: Free hosting and execution, no server required
- **Price Validation**: Built-in sanity checks to prevent erroneous updates
- **Batch Updates**: Efficiently updates all crypto entries in a single run

## 📋 Prerequisites

- A Notion account with an investment tracking database
- A GitHub account
- Basic knowledge of GitHub repository management

## 🛠️ Installation

### 1. Notion Database Setup

Your Notion database must include the following properties:

| Property Name | Type | Description |
|--------------|------|-------------|
| `Ticker` | Select | Must include "BTC" and "ETH" options |
| `Price today` | Number | Current price (automatically updated) |
| `Last updated` | Date | Timestamp of last update (automatically set) |

### 2. Notion Integration

1. Visit [Notion Integrations](https://www.notion.so/my-integrations)
2. Click "New integration"
3. Give it a name (e.g., "Crypto Price Updater")
4. Select the workspace where your database is located
5. Copy the "Internal Integration Token"
6. Share your database with the integration:
   - Open your database in Notion
   - Click "..." menu → "Add connections"
   - Search for and select your integration

### 3. GitHub Repository Setup

1. Fork this repository or create a new one with the provided code
2. Navigate to Settings → Secrets and variables → Actions
3. Add the following repository secrets:
   - `NOTION_TOKEN`: Your Notion integration token
   - `NOTION_DATABASE_ID`: Your database ID (extract from the database URL)
     ```
     https://notion.so/workspace/[DATABASE_ID]?v=...
     ```

### 4. Enable GitHub Actions

GitHub Actions should be enabled by default. The workflow will:
- Run automatically at 5:00 AM UTC daily (7:00 AM CEST / 6:00 AM CET)
- Execute on every push to the main branch
- Allow manual triggering via the Actions tab

## 💻 Local Development

### Prerequisites

```bash
# Clone the repository
git clone https://github.com/yourusername/crypto-notion-updater.git
cd crypto-notion-updater

# Install dependencies
pip install -r requirements.txt
```

### Testing

```bash
# Test CoinGecko API connection
python test_api.py

# Run the updater locally
export NOTION_TOKEN="your_token_here"
export NOTION_DATABASE_ID="your_database_id_here"
python crypto_price_updater.py
```

## 📁 Project Structure

```
crypto-notion-updater/
├── .github/
│   └── workflows/
│       └── update-crypto-prices.yml  # GitHub Actions workflow
├── crypto_price_updater.py          # Main update script
├── test_api.py                      # API testing utility
├── requirements.txt                 # Python dependencies
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## 🔧 Configuration

### Modifying Update Schedule

Edit `.github/workflows/update-crypto-prices.yml`:

```yaml
schedule:
  - cron: '0 5 * * *'  # Runs at 5:00 AM UTC
```

Use [crontab.guru](https://crontab.guru/) to customize the schedule.

### Adding More Cryptocurrencies

Modify the `get_crypto_prices()` function in `crypto_price_updater.py`:

```python
params = {
    'ids': 'bitcoin,ethereum,solana',  # Add more crypto IDs
    'vs_currencies': 'eur',
    'include_24hr_change': 'true',
    'include_market_cap': 'true'
}
```

## 🚨 Troubleshooting

### Workflow Not Running

1. Check if Actions are enabled in your repository settings
2. Verify that secrets are correctly set
3. Check the Actions tab for error logs

### Notion Updates Not Working

1. Ensure the integration has access to your database
2. Verify property names match exactly (case-sensitive)
3. Check that Ticker values are "BTC" and "ETH" (not "Bitcoin"/"Ethereum")

### API Rate Limits

CoinGecko's free tier allows 50 calls/minute. This should be sufficient for daily updates.

## 📊 API Reference

This project uses the [CoinGecko API v3](https://www.coingecko.com/en/api/documentation) free tier, which requires no authentication.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [CoinGecko](https://www.coingecko.com/) for providing free cryptocurrency data
- [Notion API](https://developers.notion.com/) for database integration capabilities
- GitHub Actions for free workflow execution

---

**Note**: This tool is for personal use. Always verify critical financial data from multiple sources.
