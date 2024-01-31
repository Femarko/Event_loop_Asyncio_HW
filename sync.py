import requests
from pprint import pprint
from fields import fields, filds_to_dive_in
def get_person(person_id, *fields):
    response = requests.get(f'https://swapi.dev/api/people/{person_id}/').json()
    result = {field: response[field] for field in fields}
    links = {field: result[field] for field in filds_to_dive_in}
    return result, links


# def get_pers_atr(id, *atr):
#     person = get_person(id)
#     links = {field: person[field] for field in filds_to_dive_in}
#     return links


def main():
    return get_person(1, *fields)

if __name__ == "__main__":
    pprint(main())