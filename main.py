from pstats import Stats
import requests
from urllib3 import response

def get_pokemon(name):
    url=f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    response= requests.get(url)

    if response.status_code != 200:
        print("Pokemon bulunamdaı")
        return None

    data = response.json()

    stats = {
        "name": data["name"],
        "hp": data["stats"][0]["base_stat"],
        "attack": data["stats"][1]["base_stat"],
        "defense": data["stats"][2]["base_stat"],
        "speed": data["stats"][5]["base_stat"]
     }   

    return stats

pikachu = get_pokemon("pikachu")
print(pikachu)

