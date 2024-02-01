from sync import get_resource, get_attributes
from input_data import fields, fields_to_dive_in, resource_url
from pprint import pprint

# def main():
#     # return pprint(get_person(1, *fields))
#     return pprint(get_attributes(1, *fields_to_dive_in))
#     # return fields_to()


def main():
    pprint(get_resource(resource_url, *fields_to_dive_in))


if __name__ == "__main__":
    main()