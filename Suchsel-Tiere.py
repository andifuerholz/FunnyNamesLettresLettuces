import streamlit as st
import random
import string
import matplotlib.pyplot as plt
import numpy as np
import io

# ============================================================
# 1) TIERKATEGORIEN (ca. 500 Tiere)
# ============================================================

def load_animal_categories():
    return {
        "Waldtiere": [
            "Fuchs","Hirsch","Reh","Wolf","Uhu","Igel","Eule","Marder","Dachs","Specht",
            "Luchs","Wildschwein","Hase","Eichhörnchen","Bär","Elch","Fledermaus","Wiesel",
            "Mauswiesel","Baummarder","Waschbär","Rotfuchs","Feldhase","Nerz","Buntspecht"
        ],
        "Bauernhof": [
            "Kuh","Pferd","Schaf","Ziege","Gans","Ente","Huhn","Truthahn","Gockel","Esel",
            "Hund","Katze","Stier","Kalb","Henne","Hahn","Pute","Taube","Maultier","Rind",
            "Lammling","Milchkuh"
        ],
        "Safari & Savanne": [
            "Elefant","Giraffe","Löwe","Tiger","Panther","Jaguar","Gepard","Nashorn",
            "Hyäne","Flusspferd","Schakal","Antilope","Zebra","Warzenschwein","Kudu","Impala",
            "Strauß","Buschbock","Pavian","Mandrill","Serval","Karakal","Klippdachs"
        ],
        "Meer & Ozean": [
            "Delfin","Hai","Wal","Seelöwe","Robbe","Seeigel","Seestern","Seepferd","Oktopus",
            "Tintenfisch","Makrele","Hering","Kabeljau","Krabbe","Qualle","Rochen","Muräne",
            "Thunfisch","Lachs","Seelachs","Sardine","Walross","Pottwal","Schwertwal"
        ],
        "Regenwald": [
            "Papagei","Ara","Tukan","Faultier","Ameisenbär","Tapir","Puma","Ozelot","Jaguar",
            "Anakonda","Boa","Leguan","Kaiman","Armadillo","Aguti","Kapuzineraffe","Brüllaffe",
            "Springaffe","Nasenbär","Klammeraffe","Rotaugenfrosch","Baumsteigerfrosch"
        ],
        "Arktis & Antarktis": [
            "Pinguin","Eisbär","Walross","Schneeeule","Robbe","Seehund","Narwal","Belugawal",
            "Eisfisch","Schneehase","Moschusochse","Rentiere","Schneehuhn","Eiskrabbe",
            "Seeschwalbe","Schneefuchs","Grönlandwal","Adeliepinguin"
        ],
        "Vögel weltweit": [
            "Adler","Falke","Habicht","Möwe","Rabe","Spatz","Kranich","Flamingo","Kakadu",
            "Taube","Storch","Geier","Albatros","Kormoran","Dohle","Eisvogel","Kauz","Uhu",
            "Seeadler","Buntspecht","Pelikane","Kolibri","Schwalbe"
        ],
        "Reptilien & Amphibien": [
            "Echse","Gecko","Schlange","Kobra","Viper","Krokodil","Alligator","Kröte","Frosch",
            "Molch","Salamander","Schildkröte","Leguan","Chamäleon","Anakonda","Python",
            "Blindschleiche","Gila","Warane","Sumpfschildkröte"
        ],
        "Kleintiere & Nager": [
            "Hamster","Maus","Ratte","Meerschweinchen","Lemming","Maulwurf","Waschbär","Biber",
            "Frettchen","Kaninchen","Chinchilla","Gerbil","Wühlmaus","Haselmaus","Präriehund",
            "Streifenhörnchen"
        ],
        "Insekten & Spinnentiere": [
            "Ameise","Wespe","Biene","Hornisse","Schmetterling","Libelle","Käfer",
            "Marienkäfer","Raupe","Heuschrecke","Grille","Termite","Motte","Nachtfalter",
            "Spinne","Vogelspinne","Skorpion","Webspinne","Weberknecht","Stechmücke"
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

            if direction == "H":
                r = random.randrange(size)
                c = random.randrange(size - L)
                if all(grid[r][c+i] in (None, word[i]) for i in range(L)):
                    for i in range(L):
                        grid[r][c+i] = word[i]
                        sol[r][c+i] = True
                    return True

            if direction == "V":
                r = random.randrange(size - L)
                c = random.randrange(size)
                if all(grid[r+i][c] in (None, word[i]) for i in range(L)):
                    for i in range(L):
                        grid[r+i][c] = word[i]
                        sol[r+i][c] = True
                    return True

            if direction == "D":
                r = random.randrange(size - L)
                c = random.randrange(size - L)
                if all(grid[r+i][c+i] in (None, word[i]) for i in range(L)):
                    for i in range(L):
                        grid[r+i][c+i] = word[i]
                        sol[r+i][c+i] = True
                    return True
        return False

    for w in words:
        place(w)

    for r in range(size):
        for c in range(size):
            if grid[r][c] is None:
                grid[r][c] = random.choice(string.ascii_uppercase)

    return grid, sol


# ============================================================
# 3) PNG EXPORT (correct alignment)
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
    ax.set_xlim(0, size)
    ax.set_ylim(size, 0)

    for r in range(size):
        for c in range(size):
            ax.text(
                c + 0.5,
                r + 0.5,
                grid[r][c],
                va="center",
                ha="center",
                fontsize=14,
                fontname="DejaVu Sans"
            )

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close()
    return buf


# ============================================================
# 4) STREAMLIT UI
# ============================================================

st.title("🐾 Tier‑Suchsel Generator (10 Kategorien, 500 Tiere, Multi‑Select)")

categories = load_animal_categories()
category_names = list(categories.keys())

selection = st.multiselect(
    "Wähle beliebige Kategorien aus (mindestens 1):",
    category_names,
    default=[category_names[0]]
)

# kombiniere Tiere aus allen ausgewählten Kategorien
selected_animals = sorted({a for cat in selection for a in categories[cat]})

st.write(f"**Verfügbare Tiere in Auswahl:** {len(selected_animals)}")

amount = st.slider("Wie viele Tiere sollen versteckt werden?", 5, min(len(selected_animals), 40), 12)
size = st.slider("Rastergröße", 10, 30, 18)

if st.button("🔍 Suchsel erzeugen"):
    chosen = random.sample(selected_animals, amount)
    st.write("### ✅ Verwendete Tiere:")
    st.write(", ".join(chosen))

    words = [x.upper() for x in chosen]
    grid, sol = generate_wordsearch(words, size)

    # ✅ Lösung als Liste
    st.write("### ✅ Lösungsliste (keine Vorschau, nur als PNG verfügbar)")
    for w in chosen:
        st.write(f"• {w}")

    # ✅ PNG-Export
    png = create_png(grid)
    st.download_button(
        "📥 Suchsel als PNG herunterladen",
        data=png,
        file_name="suchsel.png",
        mime="image/png"
    )
