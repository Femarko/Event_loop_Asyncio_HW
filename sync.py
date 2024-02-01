import requests
from pprint import pprint
from input_data import resource_url, fields, attributes_to_get


def get_resource(resource_url, *attributes_to_get) -> dict:
    response = requests.get(f'{resource_url}').json()
    person = {field: response[field] for field in fields}
    str_dicts = {
        "films": ",".join([requests.get(f'{item}').json()["title"] for item in person["films"]]),
        "species": ",".join([requests.get(f'{item}').json()["name"] for item in person["species"]]),
        "starships": ",".join([requests.get(f'{item}').json()["name"] for item in person["starships"]]),
        "vehicles": ",".join([requests.get(f'{item}').json()["name"] for item in person["vehicles"]])
    }
    # attributes_to_get = {atribute: person[atribute] for atribute in attributes_to_get}
    # return {"person": person, "attributes_to_get": attributes_to_get}
    # str_attributes = {attribute: [requests.get(f'{item}').json()["title"] for item in attribute] for attribute in attributes_to_get}
    # str_attributes = {attribute: requests.get(person[attribute]) for attribute in attributes_to_get}
    # return [person, str_attributes]
    return [person, str_dicts]

def get_attributes(resource_url, *attributes) -> dict:
    person = get_resource(resource_url, *attributes)
    # attr_dict =
    # return attr_dict


def construct_person(resource_url, *attributes):
    attr_dict = get_attributes(resource_url, *fields_to_dive_in)
    str_attributes = {field: get_resource(attr_dict[field])["name"] for field in fields_to_dive_in}


if __name__ == "__main__":
    pprint(get_resource(resource_url, *attributes_to_get))
    # pprint(",".join([requests.get(f'{film}').json()["title"] for film in person["films"]]))
