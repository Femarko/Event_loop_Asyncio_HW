from more_itertools import chunked
import asyncio, aiohttp
from input_data import persons_list


async def get_people(base_url: str, person_id: int, session: aiohttp) -> object:
    response = await session.get(f"{base_url}/{person_id}")