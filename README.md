# 🚀 Binance Futures Testnet CLI Trading Bot

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Binance](https://img.shields.io/badge/Binance-API-yellow?style=for-the-badge&logo=binance)
![Status](https://img.shields.io/badge/Status-Success-brightgreen?style=for-the-badge)

A premium, highly polished CLI-based Python trading bot that connects to the **Binance Futures Testnet**. It features a stunning terminal UI, live ASCII price charts, automatic bracket orders, and a real-time portfolio dashboard.

---

## 🏗️ Project Architecture

```text
trading_bot/
├── bot/
│   ├── __init__.py          # Module initialization
│   ├── client.py            # Binance API connection logic
│   ├── orders.py            # Market, Limit, TP, and SL order logic
│   ├── validators.py        # Input sanitization and checks
│   ├── charts.py            # Terminal ASCII chart rendering
│   ├── dashboard.py         # Live portfolio & PNL dashboard
│   └── logging_config.py    # Log formatting and setup
├── cli.py                   # Main CLI entry point with Rich UI
├── requirements.txt         # Dependencies
├── .env                     # API Credentials
└── README.md                # Documentation
```

---

## ✨ Features (The "Wow" Factor)

- 🎨 **Gorgeous Terminal UI**: Built with `rich`, featuring colorful tables, loading spinners, and styled prompts.
- 📈 **Live Terminal Price Charts**: Automatically fetches and draws a live 12.5-hour ASCII candlestick chart before you execute trades!
- 🛡️ **Auto Bracket Orders**: Easily attach Take-Profit and Stop-Loss percentages to your orders (`--tp` & `--sl`).
- 📊 **Live Portfolio Dashboard**: View your wallet balance, active positions, and unrealized PNL directly in the terminal (`--dashboard`).
- 🛡️ **Smart Validation & Logging**: Safe error handling and comprehensive file logging (`trading_bot.log`).

---

## ⚙️ Installation & Setup

1. **Clone the repository** and navigate to the folder.
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API Keys**:
   Ensure your `.env` file is in the root directory with your Binance **Futures Testnet** credentials:
   ```env
   API_KEY=your_testnet_api_key
   API_SECRET=your_testnet_api_secret
   ```

---

## 💻 Usage & Commands

### 1. Interactive Mode (Highly Recommended)
Run the script without arguments. It will draw a live price chart and prompt you for trade details.
```bash
python cli.py
```
*(You can also optionally add Take-Profit and Stop-Loss brackets during the prompts!)*

### 2. Live Portfolio Dashboard
Check your real-time PNL and active positions:
```bash
python cli.py --dashboard
```

### 3. Direct Command Mode (with TP/SL)
Execute orders instantly from your terminal, including advanced bracket orders:

**Market Order with TP/SL:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01 --tp 5 --sl 2
```
*(This places a market buy, sets a Take-Profit at +5%, and a Stop-Loss at -2%)*

**Limit Order:**
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000
```

---

> **Note**: This bot is explicitly configured for the Binance Futures Testnet (`https://testnet.binancefuture.com`). Do not use Mainnet keys in this environment.
