import asyncio, aiohttp, requests
from aiohttp import ClientSession
from more_itertools import chunked
from input_data import base_url
from pprint import pprint
import platform
if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


CHUNK_SIZE = 10


async def persons_quantity(base_url: str, session: ClientSession) -> int:
    response = await session.get(f"{base_url}")
    json = await response.json()
    return json.get("count")


async def get_persons(base_url: str, session: ClientSession, first_id: int=1, last_id: int=None) -> dict:
    if not last_id:
        last_id = await persons_quantity(base_url, session)
    coro_list = [session.get(f"{base_url}/{person_id}") for person_id in range(first_id, last_id + 1)]
    response_list = await asyncio.gather(*coro_list)
    persons_dict = {
        int(str(item.url).split("//")[2]): await item.json() for item in response_list if item.status == 200
    }
    return persons_dict


async def add_persons(
        base_url: str,
        persons_quantity: int,
        persons_dict: dict,
        session: ClientSession,
        first_id: int=1,
        last_id: int=None
) -> dict:
        first_id = max(persons_dict.keys()) + 1
        last_id = first_id + 1
        while len(persons_dict.keys()) < persons_quantity:
            new_person = await get_persons(base_url, session, first_id=first_id, last_id=last_id)
            persons_dict = persons_dict | new_person
        return persons_dict


async def main():
    async with ClientSession() as session:
        persons_quantiy = await persons_quantity(base_url, session)
        persons_dict = await get_persons(base_url, session)
        if len(persons_dict.keys()) < persons_quantiy:
            persons_dict = await add_persons(base_url, persons_quantiy, persons_dict, session)
        return persons_dict

if __name__ == '__main__':
    pprint(asyncio.run(main()))