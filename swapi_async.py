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


async def get_persons(base_url: str, session: ClientSession, id_list: list) -> list:
    # if not last_id:
    #     last_id = persons_quantity
    coro_list = [session.get(f"{base_url}/{person_id}") for person_id in id_list]
    response_list = await asyncio.gather(*coro_list)
    persons_list = []
    for item in response_list:
        if item.status == 200:
            person_dict = {field: (await item.json())[field] for field in fields}
            persons_list.append(person_dict | {"id": int(str(item.url).split("//")[2])})
    return persons_list


async def add_persons(base_url: str, persons_quantity: int, persons_list: list, session: ClientSession) -> list:
        id_list = [persons_list[-1]["id"] + 1, persons_list[-1]["id"] + 2]
        if len(id_list) > CHUNK_SIZE:
            pass
        while len(persons_list) < persons_quantity:
            new_person = await get_persons(base_url, session, id_list)
            persons_list = [*persons_list, *new_person]
        return persons_list


async def get_attributes(base_url: str, persons_list: list, session: ClientSession=None) -> list:
    for key, value in attributes_to_get.items():
        for item in persons_list:
            # item[key] = ",".join([await get_field_value(link, value, session) for link in item[key]])
            coro_list = [get_field_value(link, value, session) for link in item[key]]
            item[key] = ",".join(await asyncio.gather(*coro_list))
    return persons_list


async def main():
    async with ClientSession() as session:
        persons_quantity = await get_field_value(base_url, "count", session)
        persons_list = []
        for id_list in chunked(range(1, persons_quantity +1), CHUNK_SIZE):
            persons_list_chunk = await get_persons(base_url, session, id_list)
            persons_list_chunk = await get_attributes(base_url, persons_list_chunk, session)
            persons_list = [*persons_list, *persons_list_chunk]
        # if len(persons_list) < persons_quantity:
        #     id_list = [persons_list[-1]["id"] + 1, persons_list[-1]["id"] + 2]
        #     if len(id_list) > CHUNK_SIZE:
        #     persons_list = await add_persons(base_url, persons_quantity, persons_list, session)
        pprint(persons_list)
# async def main():
#     async with ClientSession() as session:
#         return await get_field_value(base_url, "count", session)


if __name__ == '__main__':
    start_time = datetime.now()
    asyncio.run(main())
    print(datetime.now() - start_time)
    # print(type(CHUNK_SIZE))