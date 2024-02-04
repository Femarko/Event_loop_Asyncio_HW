import asyncio, aiohttp, requests
from aiohttp import ClientSession
from more_itertools import chunked
from input_data import base_url
from pprint import pprint
import platform
if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


CHUNK_SIZE = 10


async def quantity(base_url: str, session: ClientSession) -> int:
    response = await session.get(f"{base_url}")
    json = await response.json()
    return json.get("count")


async def get_persons(base_url: str, session: ClientSession) -> dict:
    persons_quantity = await quantity(base_url, session)
    coro_list = [session.get(f"{base_url}/{person_id}") for person_id in range(1, persons_quantity + 1)]
    response_list = await asyncio.gather(*coro_list)
    persons_list = [await item.json() for item in response_list if item.status == 200]
    return len(response_list)



async def main():
    async with ClientSession() as session:
        return await get_persons(base_url, session)

if __name__ == '__main__':
    pprint(asyncio.run(main()))