import argparse
import sys
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, FloatPrompt

from bot.client import get_client
from bot.orders import place_order
from bot.validators import validate_order
from bot.logging_config import setup_logger
from bot.charts import render_price_chart
from bot.dashboard import show_dashboard

console = Console()

def main():
    setup_logger()

    parser = argparse.ArgumentParser(description="Professional CLI Trading Bot for Binance Futures Testnet")
    parser.add_argument("--symbol", help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", help="BUY or SELL")
    parser.add_argument("--type", help="MARKET or LIMIT")
    parser.add_argument("--quantity", type=float, help="Order quantity")
    parser.add_argument("--price", type=float, help="Price for LIMIT orders")
    parser.add_argument("--tp", type=float, help="Take Profit percentage (e.g. 5 for 5%)")
    parser.add_argument("--sl", type=float, help="Stop Loss percentage (e.g. 2 for 2%)")
    parser.add_argument("--dashboard", action="store_true", help="View live portfolio dashboard")

    args = parser.parse_args()
    client = get_client()

    if args.dashboard:
        show_dashboard(client)
        sys.exit(0)

    console.print(Panel.fit("[bold cyan]🚀 Binance Futures Testnet CLI Bot[/bold cyan]"))

    # Interactive Prompt Mode using rich
    if not args.symbol:
        args.symbol = Prompt.ask("[bold yellow]Enter Symbol[/bold yellow] (e.g. BTCUSDT)").strip().upper()
    
    # Render Chart before confirming rest
    with console.status("[bold green]Loading Market Data..."):
        render_price_chart(client, args.symbol)

    if not args.side:
        args.side = Prompt.ask("[bold yellow]Enter Side[/bold yellow]", choices=["BUY", "SELL"]).upper()
    if not args.type:
        args.type = Prompt.ask("[bold yellow]Enter Order Type[/bold yellow]", choices=["MARKET", "LIMIT"]).upper()
    if not args.quantity:
        args.quantity = FloatPrompt.ask("[bold yellow]Enter Quantity[/bold yellow]")
    if args.type == "LIMIT" and not args.price:
        args.price = FloatPrompt.ask("[bold yellow]Enter Price for LIMIT order[/bold yellow]")
        
    if not args.tp and Prompt.ask("[dim]Add Take-Profit Bracket?[/dim]", choices=["y", "n"], default="n") == "y":
        args.tp = FloatPrompt.ask("[bold green]Take-Profit %[/bold green] (e.g., 5)")
    if not args.sl and Prompt.ask("[dim]Add Stop-Loss Bracket?[/dim]", choices=["y", "n"], default="n") == "y":
        args.sl = FloatPrompt.ask("[bold red]Stop-Loss %[/bold red] (e.g., 2)")

    try:
        validate_order(args.symbol, args.side, args.type, args.quantity, args.price)

        with console.status(f"[bold green]Placing {args.side} {args.type} order..."):
            order = place_order(
                client,
                args.symbol,
                args.side,
                args.type,
                args.quantity,
                args.price,
                args.tp,
                args.sl
            )

        # Build Success Table
        table = Table(title="Order Success Receipt", show_header=True, header_style="bold green")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="magenta")

        table.add_row("Order ID", str(order.get('orderId')))
        table.add_row("Status", str(order.get('status')))
        table.add_row("Symbol", str(order.get('symbol')))
        table.add_row("Executed Qty", str(order.get('executedQty')))
        
        avg_price = order.get('avgPrice')
        if avg_price and float(avg_price) > 0:
            table.add_row("Avg Execution Price", str(avg_price))
            
        if order.get('tp_price'):
            table.add_row("Take-Profit (Target)", str(order.get('tp_price')))
        if order.get('sl_price'):
            table.add_row("Stop-Loss (Protection)", str(order.get('sl_price')))

        update_time = order.get('updateTime')
        if update_time:
            formatted_time = datetime.fromtimestamp(update_time / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
            table.add_row("Timestamp", formatted_time)

        console.print(table)

    except Exception as e:
        console.print(Panel(f"[bold red]❌ Order Failed:[/bold red]\n{str(e)}", border_style="red"))

if __name__ == "__main__":
    main()
