import asyncio, aiohttp, requests
from aiohttp import ClientSession
from more_itertools import chunked
from input_data import base_url, attributes_to_get, fields, CHUNK_SIZE


async def get_field_value(base_url: str, field: str, session: ClientSession) -> int:
    response = await session.get(f"{base_url}")
    json = await response.json()
    return json.get(field)


async def get_persons(base_url: str, session: ClientSession, id_list: list) -> list:
    coro_list = [session.get(f"{base_url}/{person_id}") for person_id in id_list]
    response_list = await asyncio.gather(*coro_list)
    persons_list = []
    for item in response_list:
        if item.status == 200:
            person_dict = {field: (await item.json())[field] for field in fields}
            persons_list.append(person_dict | {"id": int(str(item.url).split("//")[2])})
    return persons_list


async def create_persons_list(last_id: int,
                              base_url: str,
                              session: ClientSession,
                              first_id: int=1,
                              persons_list :list=None) -> list:
    for id_list in chunked(range(first_id, last_id), CHUNK_SIZE):
        persons_list_chunk = await get_persons(base_url, session, id_list)
        persons_list_chunk = await get_attributes(base_url, persons_list_chunk, session)
        persons_list = [*persons_list, *persons_list_chunk]
    return persons_list


async def get_attributes(base_url: str, persons_list: list, session: ClientSession) -> list:
    for key, value in attributes_to_get.items():
        for item in persons_list:
            # item[key] = ",".join([await get_field_value(link, value, session) for link in item[key]])
            coro_list = [get_field_value(link, value, session) for link in item[key]]
            item[key] = ",".join(await asyncio.gather(*coro_list))
    return persons_list