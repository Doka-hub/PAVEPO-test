from decimal import Decimal

from tronpy import AsyncTron
from tronpy.providers import AsyncHTTPProvider

from app.config import get_settings


async def get_tron_info(address: str) -> dict:
    provider = AsyncHTTPProvider(
        "https://api.trongrid.io",
        api_key=get_settings().TRON_API_KEY,
    )
    client = AsyncTron(provider=provider)

    info = await client.get_account(address)
    bandwidth = await client.get_bandwidth(address)
    return {
        "address": address,
        "bandwidth": bandwidth,
        "energy": info.get('account_resource', {}).get('energy_window_size'),
        "balance": Decimal(info.get("balance", 0)) / 1_000_000,
    }
