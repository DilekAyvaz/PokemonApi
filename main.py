import requests
from tkinter import *

#Fonksiyonlar
# Pokémon verisini API'den çekme fonksiyonu
def get_pokemon(name):
    # API URL'ini oluşturuyoruz (girilen ismi küçük harfe çeviriyoruz)
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

#Hasar Hesaplama 
def calculate_damage(attacker ,defender ):
    damage = attacker ["attack"] - (defender["defense"]/2)
    #hasar minimum ve 1 olmalı -li olmaması için ve tam sayıya çevirdik.
    return max(1, int(damage))

# ----------------------------------------
# Savaş fonksiyonu
# ----------------------------------------
def battle():
    text_output.delete("1.0",END) #önceki sonucu temizliyoruz
    p1_name = entry_pokemon1.get().strip()
    p2_name =entry_pokemon2.get().strip()

    p1= get_pokemon(p1_name)
    p2= get_pokemon(p2_name)

    if not p1 or not p2:
        text_output.insert(END, "Hatalı Pokemon adi!\n")
        return

    hp1 = p1["hp"]# p1’in başlangıç HP’si
    hp2 = p2["hp"]# p2’in başlangıç HP’si

    if p1["speed"] > p2["speed"]:
        first, second = p1, p2
        hp_first, hp_second = hp1, hp2
    else:
        first, second = p2, p1
        hp_first, hp_second = hp2, hp1

    text_output.insert(END, f"İlk saldıran: {first['name']}\n\n")

    while hp_first > 0 and hp_second > 0:
        dmg = calculate_damage(first, second)
        hp_second -= dmg
        text_output.insert(END, f"{first['name']} {dmg} hasar verdi! ({second['name']} HP: {max(0, hp_second)})\n")

        if hp_second <= 0:
            text_output.insert(END, f"\n🏆 Kazanan: {first['name']}!\n")
            return

        dmg = calculate_damage(second, first)
        hp_first -= dmg
        text_output.insert(END, f"{second['name']} {dmg} hasar verdi! ({first['name']} HP: {max(0, hp_first)})\n\n")

        if hp_first <= 0:
            text_output.insert(END, f"\n🏆 Kazanan: {second['name']}!\n")
            return

# --------------- GUI -----------------
window = Tk()
window.title("Pokémon Battle Simulator")
window.geometry("500x400")
window.config(padx=20, pady=20)

# Başlık
Label(window, text="Pokémon Battle Simulator", font=("Arial", 16, "bold")).pack(pady=10)

# Pokémon girişleri
entry_pokemon1 = Entry(window, width=20)
entry_pokemon1.pack(pady=5)
entry_pokemon1.insert(0, "pikachu")  # Örnek başlangıç

entry_pokemon2 = Entry(window, width=20)
entry_pokemon2.pack(pady=5)
entry_pokemon2.insert(0, "charizard")  # Örnek başlangıç

# Savaştır butonu
Button(window, text="Savaştır", command=battle).pack(pady=10)

# Sonuç alanı
text_output = Text(window, height=15, width=60)
text_output.pack(pady=10)

window.mainloop()