import requests
from pprint import pprint
from input_data import resource_url, fields, attributes_to_get


def get_resource(resource_url, **attributes_to_get) -> dict:
    response = requests.get(f'{resource_url}').json()
    person = {field: response[field] for field in fields}
    str_attrs = {
        key: ",".join([requests.get(f'{item}').json()[value] for item in person[key]]) \
        for key, value in attributes_to_get.items()
    }
    for key, value in str_attrs.items():
        person[key] = value
    return person


if __name__ == "__main__":
    pprint(get_resource(resource_url, **attributes_to_get))
