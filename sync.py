import requests
from pprint import pprint
from input_data import person_url, fields, attributes_to_get, base_url

def persons_count(resource_url: str) -> int:
    response = requests.get(f'{resource_url}').json().get("count")
    return response

def all_statuses(base_url: str) -> list:
    return [{person_id: requests.get(f"{base_url}/{person_id}").status_code} for person_id in range(1, 85)]


def get_while(resource_url: str, first_id=82, **attributes_to_get: dict) -> list:
    person_id = first_id
    response = requests.get(f'{resource_url}/{person_id}')
    status_code = response.status_code
    result_list = []
    while status_code == 200: # TODO: условие - пока общее количество со статусом 200 не сравняется с persons_count
        person = {field: response.json()[field] for field in fields}
        for key, value in attributes_to_get.items():
            str_attrs = {key: ",".join([requests.get(f'{item}').json()[value] for item in person[key]])} # todo: этот словарь - лишний?
            for key, value in str_attrs.items():
                person[key] = value
            person["id"] = person_id
        result_list.append(person)
        person_id += 1
        response = requests.get(f'{resource_url}/{person_id}')
        status_code = response.status_code
    return result_list


def get_resource(resource_url, **attributes_to_get) -> dict:
    response = requests.get(f'{resource_url}')
    if response.status_code == 200:
        person = {field: response.json()[field] for field in fields}
        str_attrs = {
            key: ",".join([requests.get(f'{item}').json()[value] for item in person[key]]) \
            for key, value in attributes_to_get.items()
        }
        for key, value in str_attrs.items():
            person[key] = value
        return person
    else:
        return {"status code": response.status_code}


if __name__ == "__main__":
    # pprint(get_resource(person_url, **attributes_to_get))
    # for item in get_persons_list(person_url):
    #     print(item["name"])
    # pprint(get_persons_list(base_url))
    # print(requests.get(f'{person_url}').status_code)
    # pprint(get_while(base_url, **attributes_to_get))
    # pprint(persons_count(base_url))
    pprint(all_statuses(base_url))
