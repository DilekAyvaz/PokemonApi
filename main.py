import requests
from tkinter import *
from PIL import Image, ImageTk  # Resimleri göstermek için Pillow kütüphanesi
from io import BytesIO
import random

#Fonksiyonlar
# Pokémon verisini API'den çekme fonksiyonu
def get_random_pokemon():
    # Rastgele ID seçiyoruz (1-898)
    rand_id = random.randint(1, 898)
    url = f"https://pokeapi.co/api/v2/pokemon/{rand_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return get_random_pokemon()  # Hatalı ID olursa tekrar dene
    data = response.json()
    return {
        "name": data["name"],
        "hp": data["stats"][0]["base_stat"],
        "attack": data["stats"][1]["base_stat"],
        "defense": data["stats"][2]["base_stat"],
        "speed": data["stats"][5]["base_stat"],
        "sprite": data["sprites"]["front_default"]
    }

#Hasar Hesaplama 
def calculate_damage(attacker ,defender ):
    damage = attacker ["attack"] - (defender["defense"]/2)
    #hasar minimum ve 1 olmalı -li olmaması için ve tam sayıya çevirdik.
    return max(1, int(damage))


def load_image(url, size=(120,120)):
    response = requests.get(url)
    img_data = Image.open(BytesIO(response.content))
    img_data = img_data.resize(size)
    return ImageTk.PhotoImage(img_data)

# Savaş fonksiyonu
def battle():
    text_output.delete("1.0",END) #önceki sonucu temizliyoruz
   
    p1= get_random_pokemon()
    p2= get_random_pokemon()

    if not p1 or not p2:
        text_output.insert(END, "Hatalı Pokemon adi!\n")
        return

    # Resimleri yükle ve GUI'de göster
    global img1, img2  # Tkinter için referans kaybolmaması gerekiyor
    img1 = load_image(p1["sprite"])
    img2 = load_image(p2["sprite"])
    label_p1.config(image=img1)
    label_p2.config(image=img2)

    hp1 = p1["hp"]# p1’in başlangıç HP’si
    hp2 = p2["hp"]# p2’in başlangıç HP’si

    if p1["speed"] > p2["speed"]:
        first, second = p1, p2
        hp_first, hp_second = hp1, hp2
    else:
        first, second = p2, p1
        hp_first, hp_second = hp2, hp1

    text_output.insert(END, f"İlk saldıran: {first['name']}\n\n","center")

    while hp_first > 0 and hp_second > 0:
        dmg = calculate_damage(first, second)
        hp_second -= dmg
        text_output.insert(END, f"{first['name']} {dmg} hasar verdi! ({second['name']} HP: {max(0, hp_second)})\n","center")

        if hp_second <= 0:
            text_output.insert(END, f"\n🏆 Kazanan: {first['name']}!\n","center")
            return

        dmg = calculate_damage(second, first)
        hp_first -= dmg
        text_output.insert(END, f"{second['name']} {dmg} hasar verdi! ({first['name']} HP: {max(0, hp_first)})\n\n","center")

        if hp_first <= 0:
            text_output.insert(END, f"\n🏆 Kazanan: {second['name']}!\n","center")
            return

# --------------- GUI -----------------
window = Tk()
window.title("Pokémon Battle Simulator")
window.geometry("700x600")
window.config(padx=20, pady=20)

# Başlık
Label(window, text="Pokémon Battle Simulator", font=("Marker felt", 30, "bold")).pack(pady=15)

# Savaştır butonu
Button(window, text="Savaştır",font=("Marker felt", 21, "bold"), command=battle).pack(pady=10)

# Pokémon resimleri için label
frame_images = Frame(window)
frame_images.pack(pady=20)
label_p1 = Label(frame_images)
label_p1.pack(side=LEFT, padx=40)
label_p2 = Label(frame_images)
label_p2.pack(side=RIGHT, padx=40)

# Sonuç alanı
# Log alanı için ayrı frame
frame_log = Frame(window)
frame_log.pack(expand=True)
text_output = Text(frame_log, height=25, width=80,font=("Marker felt", 21, "bold"))
text_output.pack(expand=True, fill=BOTH)
text_output.tag_configure("center", justify="center")

text_output = Text(window, height=25, width=80,font=("Marker felt", 21, "bold"))
text_output.pack(pady=10)
text_output.tag_configure("center", justify="center")


window.mainloop()