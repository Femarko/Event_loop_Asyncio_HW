import asyncio, aiohttp, requests
from datetime import datetime
from urllib import parse
from aiohttp import ClientSession
from more_itertools import chunked
from input_data import base_url, attributes_to_get, fields
from pprint import pprint
import platform
if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


CHUNK_SIZE = 10


async def get_field_value(base_url: str, field: str, session: ClientSession) -> int:
    response = await session.get(f"{base_url}")
    json = await response.json()
    return json.get(field)


async def get_persons(base_url: str, persons_quantity, session: ClientSession, first_id: int=1, last_id: int=None) -> list:
    if not last_id:
        last_id = persons_quantity
    coro_list = [session.get(f"{base_url}/{person_id}") for person_id in range(first_id, last_id + 1)]
    response_list = await asyncio.gather(*coro_list)
    persons_list = []
    for item in response_list:
        if item.status == 200:
            person_dict = {field: (await item.json())[field] for field in fields}
            persons_list.append(person_dict | {"id": int(str(item.url).split("//")[2])})
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


async def get_attributes(base_url: str, persons_list: list, session: ClientSession=None) -> dict:
    atrr_dict = {}
    for key, value in attributes_to_get.keys():
        links_dict = {item["id"]: {key: item[key]} for item in persons_list}
        atrr_dict = atrr_dict | links_dict
    return atrr_dict


async def main():
    async with ClientSession() as session:
        persons_quantiy = await get_field_value(base_url, "count", session)
        persons_list = await get_persons(base_url, persons_quantiy, session)
        if len(persons_list) < persons_quantiy:
            persons_list = await add_persons(base_url, persons_quantiy, persons_list, session)
        pprint(persons_list)

# async def main():
#     async with ClientSession() as session:
#         return await get_field_value(base_url, "count", session)


if __name__ == '__main__':
    start_time = datetime.now()
    asyncio.run(main())
    print(datetime.now() - start_time)