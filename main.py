"""
Nume proiect: File Rename Tool
Autori: Obeloiu Stefania & Mihaila Andreea
Grupă: 3.2

Descriere:
    Acest script automatizează procesul de redenumire a fișierelor de tip imagine 
    (.jpg, .jpeg, .png) dintr-un folder specificat de utilizator. Redenumirea se face 
    pe baza unui șablon configurabil (preluat din 'config.json'). Programul extrage
    data originala din metadata EXIF a pozelor. De asemenea, exista si o functie
    care permite anularea operațiunii (Undo).

Surse și Referințe:
    1. Documentatie librarie Pathlib: https://docs.python.org/3/library/pathlib.html
        - Utilizată pentru gestionarea modernă a căilor de fișiere
    2. Documentație librărie EXIF: https://pypi.org/project/exif/
        - Utilizată pentru extragerea tag-ului 'datetime_original'.
    3. Materiale de curs: https://github.com/DataLabUPT/pyCourse/
    4. Modelul AI Google Gemini:
        - Utilizat exclusiv ca asistent de consultanta tehnica si debugging
        - Notă: Arhitectura aplicației, logica fluxului de redenumire/undo și deciziile 
        finale de implementare a fragmentelor de cod aparțin în totalitate autorilor.

Module standard: pathlib, json, os, datetime
Dependențe externe: exif (v1.6.1)
"""


from pathlib import Path
import json, os
from datetime import datetime
from undo import undo
from exif import Image

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

        try:
            with open(img, 'rb') as p:
                img_exif = Image(p)
                if img_exif.has_exif:
                    data = img_exif.datetime_original
                    data = data.split(' ')[0]
                    data = data.replace(':', '-')
                else:
                    data = str(datetime.today().strftime("%Y-%m-%d"))

        except (KeyError, AttributeError) as e:
            print(e)
            data = str(datetime.today().strftime("%Y-%m-%d"))

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
    print("Redenumire realizata cu succes!\nSe deschide folderul...")

    cale_absoluta = str(folder.resolve())
    os.startfile(cale_absoluta)

    rasp = input("Doriti sa reveniti la numele originale?\nRaspundeti cu 'da' sau 'nu':")
    if rasp == 'da':
        undo(folder)
        
    with open("history.json", "w", encoding='utf-8') as f:
        json.dump({}, f, indent = 4)

else:
    print("Adresa invalida!")
