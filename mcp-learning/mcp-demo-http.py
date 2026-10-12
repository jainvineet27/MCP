from fastmcp import FastMCP
import math
import asyncio
from dotenv import load_dotenv
from bharatstock import BharatStock

load_dotenv()

client = BharatStock()

mcp = FastMCP("Get Stock Details..")

print(mcp.version)


@mcp.tool
async def get_stock_details(stock_code: str):

    response = await client.stocks.get(stock_code)

    return {"latest_price": response.industry, "company_name": response.company_name}


if __name__ == "__main__":
    asyncio.run(mcp.run(
        transport="http",
        host="127.0.0.1",
        port=800


    ))
