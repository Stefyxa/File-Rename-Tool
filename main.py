from pathlib import Path
import json, os
from datetime import datetime
from undo import undo

adresa = input("Intrduceti adresa folder-ului:")
folder = Path(adresa)
# rezolva partea de adresa a fisierului

try:
    with open("config.json", 'r', encoding='utf-8') as f:
        config = json.load(f)
        sablon = config["sablon"]

except FileNotFoundError:
    print("Eroare: Fisierul config.json nu a fost gasit in folderul curent!")
    exit()
# deschide fisierul config.json il citeste si preia valoarea cu cheia "sablon" daca exista in folder

if folder.exists() and folder.is_dir():
    print("Adresa valida!")

    poze = sorted([item for item in folder.iterdir() if item.is_file() and item.suffix.lower() in ['.jpg','.jpeg', '.png']])
    # creaza o lista cu fiecare element din folder doar daca este fisier de tip imagine

    istoric = {}
    
    for index, img in enumerate(poze, start=1):
        data = str(datetime.today().strftime("%d-%m-%Y"))

        extensie = img.suffix
        nume_nou = sablon
        nume_nou = nume_nou.replace("{index}", f"{index:03}")
        nume_nou = nume_nou.replace("{data}",data) 
        nume_nou = nume_nou + extensie
        adresaNoua = Path(folder / nume_nou)
        #creaza noua adresa din sablon

        istoric[nume_nou] = img.name

        img.rename(adresaNoua)

    with open("history.json", "w", encoding='utf-8') as f:
        json.dump(istoric, f, indent=4)
    print("Redenumire realizata cu succes!\n Se deschide folderul...")

    cale_absoluta = str(folder.resolve())
    os.startfile(cale_absoluta)

    rasp = input("Doriti sa se salveze schimbarile?\n Raspundeti cu 'da' sau 'nu':")
    if rasp == 'nu':
        undo(folder)
        
    with open("history.json", "w", encoding='utf-8') as f:
        json.dump({}, f, indent = 4)

else:
    print("Adresa invalida!")
