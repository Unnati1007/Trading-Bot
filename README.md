# 🚀 Binance Futures Testnet CLI Trading Bot

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Binance](https://img.shields.io/badge/Binance-API-yellow?style=for-the-badge&logo=binance)
![Status](https://img.shields.io/badge/Status-Success-brightgreen?style=for-the-badge)

A robust, CLI-based Python trading bot that connects to the **Binance Futures Testnet**. It features fully interactive command-line prompts, robust validation, and detailed logging.

---

## 🏗️ Project Architecture

```text
trading_bot/
├── bot/
│   ├── __init__.py          # Module initialization
│   ├── client.py            # Binance API connection logic
│   ├── orders.py            # Market and Limit order logic
│   ├── validators.py        # Input sanitization and checks
│   └── logging_config.py    # Log formatting and setup
├── cli.py                   # Main CLI entry point
├── requirements.txt         # Dependencies
├── .env                     # API Credentials
└── README.md                # Documentation
```

---

## ⚙️ Installation & Setup

1. **Navigate to the folder**.
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

You can run the bot in two modes: **Interactive Mode** (highly recommended) or **Direct Command Mode**.

### ✨ 1. Interactive Mode (Bonus Feature)
If you run the script without any arguments, it will interactively prompt you for all the details. 

```bash
python cli.py
```

**✅ Live Output Example:**
![Order Success](screenshot.png)

*(Note: To see the image above on GitHub or in your editor preview, just save the screenshot you took as `screenshot.png` inside this folder!)*

<details>
<summary><strong>View Terminal Text Output</strong></summary>

```console
PS C:\Users\HP\Desktop\CLI-based trading bot> python cli.py
Enter symbol (e.g., BTCUSDT): BTCUSDT
Enter side (BUY/SELL): BUY
Enter order type (MARKET/LIMIT): MARKET
Enter quantity: 0.01

📊 Order Summary:
{'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.01, 'price': None}

✅ Order Success!
Order ID: 13716089666
Status: NEW
Executed Qty: 0.0000
```
</details>

### ⚡ 2. Direct Command Mode

**Market Order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

**Limit Order:**
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000
```

---

## 🛡️ Features & Validation
- **Smart Validation**: Prevents invalid order types, negative quantities, and missing limit prices.
- **Detailed Logging**: All actions and API responses are safely saved to `trading_bot.log`.
- **Error Handling**: Gracefully catches Binance API errors (like invalid keys or insufficient balance) and displays them cleanly.

---

> **Note**: This bot is explicitly configured for the Binance Futures Testnet (`https://testnet.binancefuture.com`). Do not use Mainnet keys in this environment.
