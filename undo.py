import json
from pathlib import Path

def undo(adresa):
    folder = Path(adresa)

    try:
        with open("history.json", 'r', encoding='utf-8') as f:
            istoric = json.load(f)

        if not istoric:
            print("Istoricul este gol!")
            return
        else:
            print("Istoric initializat!\n Se incepe restaurarea...")

        for k,v in istoric.items():
                cale_noua = folder / k
                cale_veche = folder / v
                cale_noua.rename(cale_veche)
            
    except FileNotFoundError:
        print("Eroare: Fisierul history.json nu a fost gasit in folderul curent!")
    
    else:
        print("Restaurare realizata cu scuces!")
