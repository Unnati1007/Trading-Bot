from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def show_dashboard(client):
    try:
        with console.status("[bold green]Fetching live portfolio data..."):
            account_info = client.futures_account()
            positions = client.futures_position_information()
            
        # 1. Show Balances
        wallet_balance = float(account_info['totalWalletBalance'])
        unrealized_pnl = float(account_info['totalUnrealizedProfit'])
        
        balance_table = Table(title="Wallet Summary", show_header=True, header_style="bold magenta")
        balance_table.add_column("Metric", style="cyan")
        balance_table.add_column("Value (USDT)", justify="right")
        
        balance_table.add_row("Total Wallet Balance", f"{wallet_balance:.2f}")
        
        pnl_style = "bold green" if unrealized_pnl >= 0 else "bold red"
        balance_table.add_row("Unrealized PNL", f"[{pnl_style}]{unrealized_pnl:.2f}[/{pnl_style}]")
        
        console.print(balance_table)
        console.print("")
        
        # 2. Show Active Positions
        pos_table = Table(title="Active Positions", show_header=True, header_style="bold blue")
        pos_table.add_column("Symbol")
        pos_table.add_column("Side")
        pos_table.add_column("Size", justify="right")
        pos_table.add_column("Entry Price", justify="right")
        pos_table.add_column("Mark Price", justify="right")
        pos_table.add_column("PNL", justify="right")
        
        has_positions = False
        for pos in positions:
            size = float(pos['positionAmt'])
            if size != 0:
                has_positions = True
                side = "LONG" if size > 0 else "SHORT"
                side_style = "green" if side == "LONG" else "red"
                
                pnl = float(pos['unRealizedProfit'])
                pnl_color = "green" if pnl >= 0 else "red"
                
                pos_table.add_row(
                    pos['symbol'],
                    f"[{side_style}]{side}[/{side_style}]",
                    f"{abs(size)}",
                    f"{float(pos['entryPrice']):.4f}",
                    f"{float(pos['markPrice']):.4f}",
                    f"[{pnl_color}]{pnl:.2f}[/{pnl_color}]"
                )
                
        if has_positions:
            console.print(pos_table)
        else:
            console.print(Panel("No active positions currently open.", border_style="yellow"))
            
    except Exception as e:
        console.print(f"[bold red]❌ Failed to fetch dashboard data: {str(e)}[/bold red]")
