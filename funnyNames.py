import streamlit as st
import random
import string
import matplotlib.pyplot as plt
import numpy as np
import re
import requests
import io

# ============================================================
# 1) LOAD ANIMALS (with fallback + categories)
# ============================================================

def load_animals():
    """
    Tries to load animal names from Wikipedia via regex.
    Falls back to ~120 predefined animals in categorized form.
    """
    url = "https://de.wikipedia.org/wiki/Liste_von_Tiernamen"
    try:
        r = requests.get(url, timeout=2)
        if r.status_code == 200:
            text = r.text

            # Extract possible animal nouns directly via RegEx
            found = re.findall(r">([A-ZÄÖÜ][a-zA-ZäöüÄÖÜ]{2,20})<", text)
            animals = [a for a in found if "ß" not in a]

            # Only accept if large enough
            if len(animals) > 30:
                return animals
    except:
        pass

    # ✅ FALLBACK
    return {
        "Waldtiere": [
            "Fuchs","Hirsch","Reh","Wolf","Uhu","Igel","Eule","Marder","Dachs","Specht",
            "Luchs","Wildschwein","Hase","Eichhörnchen"
        ],
        "Bauernhof": [
            "Kuh","Pferd","Schaf","Ziege","Huhn","Gans","Ente","Esel","Truthahn","Gockel",
            "Hund","Katze","Stier"
        ],
        "Safari": [
            "Elefant","Giraffe","Löwe","Tiger","Panther","Jaguar","Gepard",
            "Antilope","Zebra","Nashorn","Hyäne","Flusspferd","Schakal"
        ],
        "Meer": [
            "Delfin","Hai","Wal","Seelöwe","Robbe","Seeigel","Seestern","Seepferd",
            "Oktopus","Tintenfisch","Makrele","Hering","Kabeljau","Krabbe"
        ],
        "Vögel": [
            "Adler","Falke","Habicht","Möwe","Rabe","Spatz","Kranich","Flamingo",
            "Papagei","Kakadu","Taube","Storch","Geier"
        ],
        "Reptilien & Amphibien": [
            "Echse","Gecko","Schlange","Kobra","Viper","Krokodil","Alligator",
            "Kröte","Frosch","Molch","Salamander","Schildkröte"
        ],
        "Kleintiere": [
            "Hamster","Maus","Ratte","Meerschweinchen","Lemming","Maulwurf",
            "Waschbär","Biber","Frettchen","Kaninchen"
        ],
        "Insekten": [
            "Ameise","Wespe","Biene","Hornisse","Schmetterling","Libelle",
            "Käfer","Marienkäfer","Raupe","Heuschrecke"
        ]
    }


# ============================================================
# 2) WORD SEARCH GENERATOR
# ============================================================

def generate_wordsearch(words, size=15):
    grid = [[None] * size for _ in range(size)]
    sol = [[False] * size for _ in range(size)]

    def place(word):
        L = len(word)
        for _ in range(2000):
            direction = random.choice(["H", "V", "D"])

            # Horizontal
            if direction == "H":
                r = random.randrange(size)
                c = random.randrange(size - L)
                if all(grid[r][c+i] in (None, word[i]) for i in range(L)):
                    for i in range(L):
                        grid[r][c+i] = word[i]
                        sol[r][c+i] = True
                    return True

            # Vertical
            if direction == "V":
                r = random.randrange(size - L)
                c = random.randrange(size)
                if all(grid[r+i][c] in (None, word[i]) for i in range(L)):
                    for i in range(L):
                        grid[r+i][c] = word[i]
                        sol[r+i][c] = True
                    return True

