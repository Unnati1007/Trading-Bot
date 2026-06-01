import argparse
from datetime import datetime
from bot.client import get_client
from bot.orders import place_order
from bot.validators import validate_order
from bot.logging_config import setup_logger

def main():
    setup_logger()

    parser = argparse.ArgumentParser(description="CLI-based trading bot for Binance Futures Testnet")
    parser.add_argument("--symbol", help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", help="BUY or SELL")
    parser.add_argument("--type", help="MARKET or LIMIT")
    parser.add_argument("--quantity", type=float, help="Order quantity")
    parser.add_argument("--price", type=float, help="Price for LIMIT orders")

    args = parser.parse_args()

    # Better CLI UX: interactive input for missing arguments
    if not args.symbol:
        args.symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
    if not args.side:
        args.side = input("Enter side (BUY/SELL): ").strip().upper()
    if not args.type:
        args.type = input("Enter order type (MARKET/LIMIT): ").strip().upper()
    if not args.quantity:
        args.quantity = float(input("Enter quantity: ").strip())
    if args.type == "LIMIT" and not args.price:
        args.price = float(input("Enter price for LIMIT order: ").strip())

    try:
        validate_order(
            args.symbol,
            args.side,
            args.type,
            args.quantity,
            args.price
        )

        client = get_client()

        print("\n📊 Order Summary:")
        print(vars(args))

        order = place_order(
            client,
            args.symbol,
            args.side,
            args.type,
            args.quantity,
            args.price
        )

        print("\n✅ Order Success!")
        print(f"Order ID: {order.get('orderId')}")
        print(f"Status: {order.get('status')}")
        print(f"Executed Qty: {order.get('executedQty')}")
        
        avg_price = order.get('avgPrice')
        if avg_price:
            print(f"Avg Price: {avg_price}")
            
        update_time = order.get('updateTime')
        if update_time:
            formatted_time = datetime.fromtimestamp(update_time / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Time: {formatted_time}")

    except Exception as e:
        print("\n❌ Order Failed:", str(e))

if __name__ == "__main__":
    main()
