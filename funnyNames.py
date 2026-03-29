import streamlit as st
import random
import string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import tempfile
import os

# -------------------------------------------------------------
# Random name generator
# -------------------------------------------------------------
def generate_random_name():
    start = ["Mi", "Mu", "La", "Lu", "Ki", "Ka", "Ko", "Fi", "Fo", "Bu", "Be", "Bo", "Tu", "Ti", "Te", "Ni", "No", "Nu"]
    middle = ["mi", "mu", "li", "la", "ra", "ri", "ro", "ru", "fi", "fo", "fa", "fe"]
    end = ["na", "ra", "lo", "la", "ta", "to", "ti", "po", "pe", "ni", "nu", "mi", "ku", "ko"]

    # structure: Start + Middle + End (2–3 Silben)
    syllables = random.randint(2, 3)
    if syllables == 2:
        name = random.choice(start) + random.choice(end)
    else:
        name = random.choice(start) + random.choice(middle) + random.choice(end)

    # Funny addon
    addon = [" Flitz", " Wusel", " Purzel", " Krawall", " Tröti", " Mumpel", " Schnurps", " Kuller", " Muggel", ""]
    name += random.choice(addon)

    return name.replace(" ", "").upper()


# -------------------------------------------------------------
# Word search generator
# -------------------------------------------------------------
def generate_wordsearch(words, size=15):
    grid = [[None for _ in range(size)] for _ in range(size)]
    solution_mask = [[False]*size for _ in range(size)]

    def place(name):
        for _ in range(2000):
            direction = random.choice(["H", "V", "D"])
            if direction == "H":
                r = random.randrange(size)
                c = random.randrange(size - len(name))
                if all(grid[r][c+i] in (None, name[i]) for i in range(len(name))):
                    for i in range(len(name)):
                        grid[r][c+i] = name[i]
                        solution_mask[r][c+i] = True
                    return True

            if direction == "V":
                r = random.randrange(size - len(name))
                c = random.randrange(size)
                if all(grid[r+i][c] in (None, name[i]) for i in range(len(name))):
                    for i in range(len(name)):
                        grid[r+i][c] = name[i]
                        solution_mask[r+i][c] = True
                    return True

            if direction == "D":
                r = random.randrange(size - len(name))
                c = random.randrange(size - len(name))
                if all(grid[r+i][c+i] in (None, name[i]) for i in range(len(name))):
                    for i in range(len(name)):
                        grid[r+i][c+i] = name[i]
                        solution_mask[r+i][c+i] = True
                    return True
        return False

    # place words
    for w in words:
        place(w)

    # fill empty cells
    for r in range(size):
        for c in range(size):
            if grid[r][c] is None:
                grid[r][c] = random.choice(string.ascii_uppercase)

    return grid, solution_mask


# -------------------------------------------------------------
# PDF export
# -------------------------------------------------------------
def create_pdf(grid, solution_mask, cell=30):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    filename = tmp.name

    c = canvas.Canvas(filename, pagesize=letter)
    margin = 40
    size = len(grid)

    # Page 1
    for r in range(size):
        for col in range(size):
            x = margin + col * cell
            y = 700 - r * cell
            c.rect(x, y, cell, cell)
            c.drawCentredString(x + cell/2, y + cell/2 - 5, grid[r][col])
    c.showPage()

    # Page 2 (solution)
    for r in range(size):
        for col in range(size):
            x = margin + col * cell
            y = 700 - r * cell
            c.rect(x, y, cell, cell)
            if solution_mask[r][col]:
                c.setFillColor(colors.red)
            else:
                c.setFillColor(colors.black)
            c.drawCentredString(x + cell/2, y + cell/2 - 5, grid[r][col])
            c.setFillColor(colors.black)

    c.save()
    return filename


# -------------------------------------------------------------
# STREAMLIT UI
# -------------------------------------------------------------
st.title("🎲 Zufälliger Suchsel-Generator mit Fantasienamen")

amount = st.slider("Wieviele zufällige Namen?", 5, 20, 10)
size = st.slider("Grid-Grösse", 10, 25, 15)

if st.button("🎉 Neues Suchsel erzeugen"):
    # generate random names
    words = [generate_random_name() for _ in range(amount)]
    st.write("**Zufällige Namen:**")
    st.write(words)

    # create puzzle
    grid, solution_mask = generate_wordsearch(words, size)

    st.subheader("🔍 Suchsel")
    for row in grid:
        st.text(" ".join(row))

    # PDF generation
    pdf_file = create_pdf(grid, solution_mask)

    with open(pdf_file, "rb") as f:
        st.download_button(
            "📄 PDF herunterladen",
            f,
            file_name="suchsel.pdf",
            mime="application/pdf"
        )

    os.remove(pdf_file)
