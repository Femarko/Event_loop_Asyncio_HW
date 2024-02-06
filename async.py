import asyncio, aiohttp, requests
from datetime import datetime

from aiohttp import ClientSession
from more_itertools import chunked
from input_data import base_url, attributes_to_get
from pprint import pprint
import platform
if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


CHUNK_SIZE = 10


async def persons_quantity(base_url: str, session: ClientSession) -> int:
    response = await session.get(f"{base_url}")
    json = await response.json()
    return json.get("count")


async def get_persons(base_url: str, persons_quantity, session: ClientSession, first_id: int=1, last_id: int=None) -> list:
    if not last_id:
        last_id = persons_quantity
    coro_list = [session.get(f"{base_url}/{person_id}") for person_id in range(first_id, last_id + 1)]
    response_list = await asyncio.gather(*coro_list)
    # persons_dict = {
    #     int(str(item.url).split("//")[2]): await item.json() for item in response_list if item.status == 200
    # }
    persons_list = [
        await item.json() | {"id": int(str(item.url).split("//")[2])} for item in response_list if item.status == 200
    ]
    return persons_list


async def add_persons(
        base_url: str,
        persons_quantity: int,
        persons_list: list,
        session: ClientSession,
        first_id: int=1,
        last_id: int=None
) -> list:
        first_id = persons_list[-1]["id"] + 1
        last_id = first_id + 1
        while len(persons_list) < persons_quantity:
            new_person = await get_persons(base_url, persons_quantity, session, first_id=first_id, last_id=last_id)
            persons_list = [*persons_list, *new_person]
        return persons_list


async def get_attributes(base_url: str, persons_list: list, session: ClientSession=None):
    atrr_dict = dict.fromkeys(attributes_to_get.keys())
    return {str(type(item)): item for item in persons_list}



async def main():
    async with ClientSession() as session:
        persons_quantiy = await persons_quantity(base_url, session)
        persons_list = await get_persons(base_url, persons_quantiy, session)
        if len(persons_list) < persons_quantiy:
            persons_list = await add_persons(base_url, persons_quantiy, persons_list, session)
    for item in persons_list:
        print(f"{type(item) = }")
# async def main():
#     async with ClientSession() as session:
#         return await get_persons(base_url, session)


if __name__ == '__main__':
    start_time = datetime.now()
    asyncio.run(main())
    print(datetime.now() - start_time)