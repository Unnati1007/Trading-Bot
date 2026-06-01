import asciichartpy
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def render_price_chart(client, symbol: str):
    try:
        # Fetch last 50 intervals of 15m candles
        klines = client.futures_klines(symbol=symbol, interval='15m', limit=50)
        
        # kline format: [Open time, Open, High, Low, Close, Volume, ...]
        closes = [float(kline[4]) for kline in klines]
        
        if not closes:
            return
            
        chart = asciichartpy.plot(closes, {'height': 10, 'format': '{:8.2f}'})
        
        panel = Panel(
            Text(chart, style="cyan"),
            title=f"[bold yellow]{symbol} - Last 12.5 Hours (15m Candles)[/bold yellow]",
            border_style="blue"
        )
        console.print(panel)
        
    except Exception as e:
        # Silently fail or log debug if chart fails, so it doesn't interrupt trading
        console.print(f"[dim red]Could not render chart: {e}[/dim red]")
