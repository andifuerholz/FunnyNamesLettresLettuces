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

            found = re.findall(r">([A-ZÄÖÜ][a-zA-ZäöüÄÖÜ]{2,20})<", text)
            animals = [a for a in found if "ß" not in a]

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

            # Diagonal
            if direction == "D":
                r = random.randrange(size - L)
                c = random.randrange(size - L)
                if all(grid[r+i][c+i] in (None, word[i]) for i in range(L)):
                    for i in range(L):
                        grid[r+i][c+i] = word[i]
                        sol[r+i][c+i] = True
                    return True
        return False

    # Place all words
    for w in words:
        place(w)

    # Fill remaining cells
    for r in range(size):
        for c in range(size):
            if grid[r][c] is None:
                grid[r][c] = random.choice(string.ascii_uppercase)

    return grid, sol

# ============================================================
# 3) PNG EXPORT
# ============================================================

def create_png(grid):
    size = len(grid)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(np.zeros((size, size)), cmap="gray_r")

    ax.set_xticks(np.arange(size))
    ax.set_yticks(np.arange(size))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(color="black", linewidth=1)

    for r in range(size):
        for c in range(size):
            ax.text(
                c, r,
                grid[r][c],
                va="center", ha="center",
                fontsize=14, fontname="DejaVu Sans"
            )

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close()
    return buf


# ============================================================
# 4) STREAMLIT UI
# ============================================================

st.title("🐾 Tier‑Suchsel Generator (mit Kategorien, PNG‑Export)")

animals_data = load_animals()

# If fallback -> categories, else -> flat wikipedia list
if isinstance(animals_data, dict):
    categories = list(animals_data.keys())
    category = st.selectbox("Kategorie auswählen:", categories)
    animals = animals_data[category]
else:
    category = "Alle"
    animals = animals_data
    st.info("Wikipedia‑Modus aktiv")

st.write(f"**Verfügbare Tiere:** {len(animals)}")

amount = st.slider("Wie viele Tiere verstecken?", 5, min(len(animals), 30), 10)
size = st.slider("Grösse des Suchsels", 10, 25, 15)

if st.button("🔍 Suchsel erzeugen"):
    selected = random.sample(animals, amount)
    st.write("**Ausgewählte Tiere:**")
    st.write(", ".join(selected))

    words = [a.upper() for a in selected]
    grid, sol = generate_wordsearch(words, size)

    st.subheader("📘 Suchsel")
    for row in grid:
        st.text(" ".join(row))

    st.subheader("✅ Lösung (nur hier sichtbar)")
    for r in range(size):
        line = ""
        for c in range(size):
            char = grid[r][c]
            if sol[r][c]:
                line += f":red[{char}] "
            else:
                line += char + " "
        st.markdown(line)

    png = create_png(grid)
    st.download_button(
        "📥 Suchsel als PNG herunterladen",
        data=png,
        file_name="suchsel.png",
        mime="image/png"
    )
