import asyncio, aiohttp
from aiohttp import ClientSession
from input_data import base_url, attributes_to_get, fields, CHUNK_SIZE
from models import Session, People


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


async def get_attributes(persons_list: list, session: ClientSession) -> list:
    for key, value in attributes_to_get.items():
        for item in persons_list:
            # item[key] = ",".join([await get_field_value(link, value, session) for link in item[key]])
            coro_list = [get_field_value(link, value, session) for link in item[key]]
            item[key] = ",".join(await asyncio.gather(*coro_list))
    return persons_list


async def paste_to_db(*args):
    async with Session() as session:
        people = [People(id=person["id"],
                         name=person["name"],
                         birth_year=person["birth_year"],
                         eye_color=person['eye_color'],
                         films=person["films"],
                         gender=person["gender"],
                         hair_color=person["hair_color"],
                         height=person["height"],
                         homeworld=person["homeworld"],
                         mass=person["mass"],
                         skin_color=person["skin_color"],
                         species=person["species"],
                         starships=person["starships"],
                         vehicles=person["vehicles"]) for person in args]
        session.add_all(people)
        await session.commit()


async def create_persons_list(base_url: str, session: ClientSession, id_list) -> list:
    persons_list = await get_persons(base_url, session, id_list)
    persons_list = await get_attributes(persons_list, session)
    return persons_list
