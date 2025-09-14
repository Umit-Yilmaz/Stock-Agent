import yfinance as yf
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("stock_prices")

@mcp.tool()
async def get_stock_price(ticker: str) -> str:
    """Get the current stock price"""
    if not ticker:
        return "No ticker provided"
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        if hist.empty:
            return f"No data found for {ticker}"
        current_price = hist["Close"].iloc[-1]
        return f"{ticker.upper()} current price: ${current_price:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("MCP Stock Price server started...", flush=True)
    mcp.run(transport="stdio")
