from fastmcp import FastMCP
from dotenv import load_dotenv
from bharatstock import BharatStock

load_dotenv()

client = BharatStock()
mcp = FastMCP("Demo")

@mcp.tool
def get_stock_details(stock_code: str):
    """Call this function to get stock price details in INR
    args : NSE stock code for a company 
    returns company name and stock price details in INR"""
    
    # await hata diya yahan se
    response = client.stocks.get(stock_code)

    return {
        "industry_name": response.industry,
        "company_name": response.company_name,
        "amount": response.latest_price
    }

if __name__ == "__main__":
    mcp.run()