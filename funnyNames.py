import streamlit as st
import random
import string
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import io

# ---------------------------------------------------------
# Load animal names from Wikipedia (no emojis, no ß)
# ---------------------------------------------------------
@st.cache_data
def load_animals_from_web():
    url = "https://de.wikipedia.org/wiki/Liste_von_Tiernamen"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    animals = []
    for li in soup.select("div.mw-parser-output ul li"):
        text = li.get_text().strip()

        # Basic filters
        if 3 < len(text) < 20 \
            and text[0].isupper() \
            and " " not in text \
            and "ß" not in text:     # requests no ß
            animals.append(text)

    return sorted(set(animals))


# ---------------------------------------------------------
# Word search generator
# ---------------------------------------------------------
def generate_wordsearch(words, size=15):
    grid = [[None] * size for _ in range(size)]
    sol = [[False] * size for _ in range(size)]

    def place(word):
        for _ in range(2000):
            direction = random.choice(["H", "V", "D"])
            L = len(word)

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

    # place words
    for w in words:
        place(w)

    # fill empty
    for r in range(size):
        for c in range(size):
            if grid[r][c] is None:
                grid[r][c] = random.choice(string.ascii_uppercase)

    return grid, sol


# ---------------------------------------------------------
# PNG creation
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------
st.title("🐾 Tier‑Suchsel Generator (PNG‑Export + Lösung im Browser)")

animals = load_animals_from_web()
st.success(f"{len(animals)} Tiernamen geladen!")

amount = st.slider("Wie viele Tiere verstecken?", 5, 25, 15)
size = st.slider("Grösse des Suchsel‑Rasters", 10, 25, 15)

if st.button("🔍 Suchsel erzeugen"):
    selected = random.sample(animals, amount)
    st.write("**Ausgewählte Tiere:**")
    st.write(", ".join(selected))

    grid, sol = generate_wordsearch([a.upper() for a in selected], size)

    # ---------- show puzzle ----------
    st.subheader("📘 Suchsel (Rätsel)")
    for row in grid:
        st.text(" ".join(row))

    # ---------- show solution ----------
    st.subheader("✅ Lösung (nur hier, nicht im Download)")

    sol_display = []
    for r in range(size):
        row = []
        for c in range(size):
            if sol[r][c]:
                row.append(f":red[{grid[r][c]}]")
            else:
                row.append(grid[r][c])
        sol_display.append(" ".join(row))

    for line in sol_display:
        st.markdown(line)

    # ---------- PNG download ----------
    png = create_png(grid)

    st.download_button(
        "📥 Suchsel als PNG herunterladen",
        data=png,
        file_name="suchsel.png",
        mime="image/png"
    )
