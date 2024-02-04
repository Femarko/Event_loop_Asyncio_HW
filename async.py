import asyncio, aiohttp, requests
from aiohttp import ClientSession
from more_itertools import chunked
from input_data import base_url
from pprint import pprint


CHUNK_SIZE = 10


async def lector(person_id, session):
    response = await session.get(f'https://swapi.py4e.com/api/people/{person_id}/')
    json = await response.json()
    return json


async def quantity(base_url: str) -> int:
    session = ClientSession()
    response = await session.get(f"{base_url}")
    json = await response.json()
    await session.close()
    result = json.get("count")
    pprint(result)


# async def get_person(base_url: str, first_id: int, session: ClientSession) -> ClientSession.get():
#     response = await session.get(f"{base_url}/{first_id}")
#     return [persons_quantity, response]


# def persons_count(base_url: str) -> int:
#     response = await requests.get(f'{base_url}').json().get("count")
#     return response


# async def main(base_url: str, first_id: int, session: ClientSession) -> dict:
#     status_code = get_person().status_code
#     if status_code == 200:
#         while status_code == 200: # TODO: условие - пока общее количество со статусом 200 не сравняется с persons_count
#             last_id = first_id + 11
#             coros = [get_person(people_id, session) for people_id in range(first_id, last_id)]
#
#             person = {field: response.json()[field] for field in fields}
#             for key, value in attributes_to_get.items():
#                 str_attrs = {key: ",".join([requests.get(f'{item}').json()[value] for item in person[key]])}
#                 for key, value in str_attrs.items():
#                     person[key] = value
#                 person["id"] = person_id
#             result_list.append(person)
#             person_id += 1
#             response = requests.get(f'{resource_url}/{person_id}')
#             status_code = response.status_code


def get_while(resource_url: str, first_id=82, **attributes_to_get: dict) -> list:
    person_id = first_id
    response = requests.get(f'{resource_url}/{person_id}')
    status_code = response.status_code
    result_list = []
    while status_code == 200:
        person = {field: response.json()[field] for field in fields}
        for key, value in attributes_to_get.items():
            str_attrs = {key: ",".join([requests.get(f'{item}').json()[value] for item in person[key]])}
            for key, value in str_attrs.items():
                person[key] = value
            person["id"] = person_id
        result_list.append(person)
        person_id += 1
        response = requests.get(f'{resource_url}/{person_id}')
        status_code = response.status_code
    return result_list


async def main():
    async with ClientSession() as session:
        res = await lector(1, session)
        print(res)

if __name__ == '__main__':
    asyncio.run(quantity(base_url))
    print('шозахрень?')