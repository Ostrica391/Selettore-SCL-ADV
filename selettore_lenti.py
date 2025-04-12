import streamlit as st
from PIL import Image, ImageOps
import base64
import io

# Sfondo gradiente più marcato: bianco -> blu profondo + larghezza massima container
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #ffffff, #fffff9);
        background-attachment: fixed;
    }
    .block-container {
        max-width: 90% !important;
        padding: 2rem 3rem;
    }
    </style>
""", unsafe_allow_html=True)

# Logo centrato
st.markdown("""
    <div style='text-align: center;'>
        <img src='data:image/png;base64,""" + base64.b64encode(open("TSLAC.png", "rb").read()).decode() + """' style='width: 400px; margin-bottom: 10px;'>
    </div>
""", unsafe_allow_html=True)

# Titolo
st.title("Selettore SCL ADV - TS LAC")

# Input
val1 = st.number_input("Inserisci SAG 5.00mm 0°", value=1700, step=10)
val2 = st.number_input("Inserisci SAG 5.00mm 180°", value=1700, step=10)
val3 = st.number_input("Central Clearance", value=250, step=5)

# Calcolo
risultato = (val1 + val2) / 2 + 1080 + val3
st.markdown(f"### SAG Lente: {int(risultato)} µm")

# Determina quale immagine evidenziare
indice = None
if 3600 <= risultato <= 3850:
    indice = 0
elif 3851 <= risultato <= 4050:
    indice = 1
elif 4051 <= risultato <= 4250:
    indice = 2
elif 4251 <= risultato <= 4450:
    indice = 3
elif 4451 <= risultato <= 4650:
    indice = 4
elif 4651 <= risultato <= 4850:
    indice = 5
elif 4851 <= risultato <= 5050:
    indice = 6

# Percorsi immagini
paths = [
    "1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png"
]

# Etichette personalizzate sotto ogni lente
sag_labels = ["SAG 3800µm", "SAG 4000µm", "SAG 4200µm", "SAG 4400µm", "SAG 4600µm", "SAG 4800µm", "SAG 5000µm"]

paths_2 = [ "8.png", "9.png", "10.png", "11.png", "12.png", "13.png", "14.png" ]
sag_labels_2 = ["SAG 3400µm", "SAG 3600µm", "SAG 3800µm", "SAG 4100µm", "SAG 4300µm", "SAG 4500µm", "SAG 4700µm"]

# Funzione per convertire immagine in base64
def pil_to_base64(img):
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return encoded

# CSS + HTML layout
st.markdown("""
    <style>
.cassette {
    background-color: #f8f9fa;
    border-radius: 20px;
    padding: 30px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 25px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    margin: 30px auto;
    border: 2px solid #ccc;
    width: 100%;
    max-width: 100%;
    overflow-x: auto;
}
.cassette-row {
    display: flex;
    justify-content: center;
    gap: 25px;
}

    .lens {
        text-align: center;
        margin: 0 5px;
    }
    .selected {
        border: 5px solid red;
        padding: 5px;
        border-radius: 12px;
    }
    .arrow {
        font-size: 30px;
        margin-bottom: 5px;
        color: red;
    }
    </style>
""", unsafe_allow_html=True)

# Titolo cassetta
st.markdown("## Lenti di prova SCL-Advance")

cassette_html = "<div class='cassette'>"

# Prima riga
cassette_html += "<div class='cassette-row'>"
for i in range(7):
    img = Image.open(paths[i])
    img_html = f"<img src='data:image/png;base64,{pil_to_base64(img)}' style='width: 190px; border-radius: 10px;' class='{'selected' if i == indice else ''}'>"
    arrow_html = "<div class='arrow'>⬇️</div>" if i == indice else ""
    label = f"{sag_labels[i]}{' (Lente ideale)' if i == indice else ''}"
    lens_html = f"<div class='lens'>{arrow_html}{img_html}<div>{label}</div></div>"
    cassette_html += lens_html
cassette_html += "</div>"

# Seconda riga
cassette_html += "<div class='cassette-row'>"
for i in range(7):
    img = Image.open(paths_2[i])
    img_html = f"<img src='data:image/png;base64,{pil_to_base64(img)}' style='width: 190px; border-radius: 10px;'>"
    label = f"{sag_labels_2[i]}"
    lens_html = f"<div class='lens'>{img_html}<div>{label}</div></div>"
    cassette_html += lens_html
cassette_html += "</div>"

cassette_html += "</div>"

# Mostriamo tutto
st.markdown(cassette_html, unsafe_allow_html=True)

# Carica due immagini diverse
with open("totalsag.png", "rb") as img_file_a:
    encoded_a = base64.b64encode(img_file_a.read()).decode()

with open("totalsagb.png", "rb") as img_file_b:
    encoded_b = base64.b64encode(img_file_b.read()).decode()

# Mostra affiancate le due immagini
st.markdown(f"""
    <div style='margin-top: 30px; display: flex; justify-content: center; gap: 40px;'>
        <img src='data:image/png;base64,{encoded_a}' style='width: 610px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);'>
        <img src='data:image/png;base64,{encoded_b}' style='width: 610px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);'>
    </div>
""", unsafe_allow_html=True)

# Carica immagine finale
with open("totalsagc.png", "rb") as img_file_c:
    encoded_c = base64.b64encode(img_file_c.read()).decode()

# Mostra immagine finale centrata
st.markdown(f"""
    <div style='margin-top: 40px; text-align: center;'>
        <img src='data:image/png;base64,{encoded_c}' style='width: 700px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);'>
    </div>
""", unsafe_allow_html=True)

