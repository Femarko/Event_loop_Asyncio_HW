import requests
from pprint import pprint
from input_data import resource_url, fields, fields_to_dive_in


def get_resource(parameter) -> dict:
    response = requests.get(f'{resource_url}/{parameter}/').json()
    result = {field: response[field] for field in fields}
    return result


def get_attributes(id, *atributes):
    person = get_resource(id)
    links = {atribute: person[atribute] for atribute in atributes}
    return links


def main():
    # return pprint(get_person(1, *fields))
    return pprint(get_attributes(1, *fields_to_dive_in))
    # return fields_to()

if __name__ == "__main__":
    main()