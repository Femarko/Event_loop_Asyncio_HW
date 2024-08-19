import asyncio, aiohttp
from aiohttp import ClientSession
from input_data import base_url, attributes_to_get, fields, CHUNK_SIZE
from models import Session, People


async def get_field_value(base_url: str, field: str, session: ClientSession) -> int | str | list[str]:
    """
    Retrieves the value of a specific field from the JSON response obtained by sending a GET request to the provided
    base URL using the given session.

    Args:
        base_url (str): The base URL to send the GET request to.
        field (str): The field to extract the value from in the JSON response.
        session (ClientSession): The aiohttp client session to make the HTTP requests.

    Returns:
        str | list[str]: The value of the specified field from the JSON response.
    """
    response = await session.get(f"{base_url}")
    json = await response.json()
    return json.get(field)


async def get_persons(base_url: str, session: ClientSession, id_list: list) -> list[dict[str, str | int]]:
    """
    Asynchronously retrieves information about persons from the given base URL using input_data.fields
    and a list of IDs.

    Parameters:
        base_url (str): The base URL to fetch the person information from.
        session (ClientSession): The aiohttp client session to make the HTTP requests.
        id_list (list): A list of IDs for the persons to fetch.

    Returns:
        list of dictionaries: A list of dictionaries containing information about the persons, where keys
        correspond to input_data.fields and additionally information about a person's ID is present.
    """
    coro_list = [session.get(f"{base_url}/{person_id}") for person_id in id_list]
    response_list = await asyncio.gather(*coro_list)
    persons_list = []
    for item in response_list:
        if item.status == 200:
            person_dict = {field: (await item.json())[field] for field in fields}
            persons_list.append(person_dict | {"id": int(str(item.url).split("//")[2])})
    return persons_list


async def get_attributes(persons_list: list, session: ClientSession) -> list[dict[str, str | int]]:
    """
    Retrieves attributes for each person in the provided list using the given session.

    Args:
        persons_list (list[dict[str, str | int]]): The list of dictionaries, returned by get_persons() function.

        session (ClientSession): The aiohttp client session to make the HTTP requests.

    Returns:
        list of dictionaries: The list of dictionaries, returned by get_persons() function, where values of attributes
        listed in input_data.attributes_to_get are present.
    """
    for key, value in attributes_to_get.items():
        for item in persons_list:
            coro_list = [get_field_value(base_url=link, field=value, session=session) for link in item[key]]
            item[key]: str = ",".join(await asyncio.gather(*coro_list))
    return persons_list


async def paste_to_db(*args):
    """
    Asynchronously pastes the provided data to the database using the given session.

    Args:
        *args: Iterable, containing a variable number of dictionaries representing person information.

    Returns:
        None
    """
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
    """
    Asynchronously creates a list of dictionaries, representing persons, by means of successive calling of
    get_persons() and get_attributes() functions.

    Args:
        base_url (str): The base URL used to fetch the persons.
        session (ClientSession): The aiohttp client session to make the HTTP requests.
        id_list: The list of IDs to fetch persons.

    Returns:
        list of dictionaries: A list of dictionaries containing information about the persons, where keys
        correspond to input_data.fields and additionally information about a person's ID as well as values of attributes
        listed in input_data.attributes_to_get are present.
    """
    persons_list = await get_persons(base_url, session, id_list)
    persons_list = await get_attributes(persons_list, session)
    return persons_list
