from typing import Any
import os
from dotenv import load_dotenv
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("currency-converter")

load_dotenv()

API_KEY = os.getenv("API_KEY")

#https://v6.exchangerate-api.com/v6/pair/EUR/GBP/AMOUNT - Pair-wise Converion with Amount

async def make_exchange_request(url: str) -> dict[str, Any] | None:
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
        
@mcp.tool()
async def get_exchange_rates(from_currency: str, to_currency: str) -> str:
    url = f"https://v6.exchangerate-api.com/v6/latest/{from_currency}"

    response = await make_exchange_request(url)
    conversion_rate = response["conversion_rates"][to_currency]

    if not response or "conversion_rates" not in response:
        return "No conversion rates found."

    return f"{from_currency} -> {to_currency}: {conversion_rate}"

def main():
    mcp.run(transport = "stdio")

if __name__ == "__main__":
    main()