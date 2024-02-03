base_url = "https://swapi.dev/api/people/"
person_url = "https://swapi.dev/api/people/1"


fields = [
    "birth_year",
    "eye_color",
    "films",
    "gender",
    "hair_color",
    "height",
    "homeworld",
    "mass",
    "name",
    "skin_color",
    "species",
    "starships",
    "vehicles"
]

attributes_to_get = {
    "films": "title",
    "species": "name",
    "starships": "name",
    "vehicles": "name"
}
