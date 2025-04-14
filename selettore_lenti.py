import streamlit as st
from PIL import Image, ImageOps
import base64
import io

# Sfondo gradiente più marcato: bianco -> blu profondo + larghezza massima container
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #ffffff, #ffffff);
        background-attachment: fixed;
    }
    .block-container {
        max-width: 90% !important;
        padding: 2rem 3rem;
    }
    </style>
""", unsafe_allow_html=True)

# Menu link in alto a sinistra
st.markdown("""
    <style>
    .top-menu {
        position: absolute;
        top: 60px;
        left: 0px;
        z-index: 1;
    }
    .top-menu a {
        display: block;
        background-color: #004890;
        color: white;
        padding: 8px 16px;
        margin-bottom: 8px;
        text-decoration: none;
        border-radius: 6px;
        font-size: 14px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: background 0.3s;
    }
    .top-menu a:hover {
        background-color: #0060b0;
    }
    </style>
    <div class="top-menu">
        <a href="https://selettore-cs.streamlit.app/">Calcolatore CS</a>
        <a href="https://selettore-scl-adv.streamlit.app/">Calcolatore SCL-ADV</a>
        <a href="https://www.tslac.it/">Work in progress</a>
        <a href="https://www.tslac.it/">Work in progress</a>
    </div>
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
val1 = st.number_input("Inserisci SAG 5.00mm 0°", value=1800, step=10)
val2 = st.number_input("Inserisci SAG 5.00mm 180°", value=1800, step=10)
val3 = st.number_input("Central Clearance", value=350, step=10)

# Calcolo
risultato = (val1 + val2) / 2 + 2000 + val3
risultato2 = (val1 + val2) / 2 + 1200 + val3
st.markdown(f"### SAG Lente: {int(risultato)} µm")

# Determina quali immagini evidenziare
indici = []

# Prima fila (0–6)
if 3600 <= risultato <= 3850:
    indici.append(0)
if 3851 <= risultato <= 4050:
    indici.append(1)
if 4051 <= risultato <= 4250:
    indici.append(2)
if 4251 <= risultato <= 4450:
    indici.append(3)
if 4451 <= risultato <= 4650:
    indici.append(4)
if 4651 <= risultato <= 4850:
    indici.append(5)
if 4851 <= risultato <= 5050:
    indici.append(6)

# Seconda fila (7–13)
if 3200 <= risultato2 <= 3450:
    indici.append(7)
if 3451 <= risultato2 <= 3650:
    indici.append(8)
if 3651 <= risultato2 <= 3850:
    indici.append(9)
if 3900 <= risultato <= 4150:
    indici.append(10)
if 4151 <= risultato <= 4350:
    indici.append(11)
if 4351 <= risultato <= 4550:
    indici.append(12)
if 4551 <= risultato <= 4750:
    indici.append(13)

# Percorsi immagini
paths = [
    "scl1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png"
]
sag_labels = ["SAG 3800µm", "SAG 4000µm", "SAG 4200µm", "SAG 4400µm", "SAG 4600µm", "SAG 4800µm", "SAG 5000µm"]

paths_2 = ["8.png", "9.png", "10.png", "11.png", "12.png", "13.png", "14.png"]
sag_labels_2 = ["SAG 3400µm", "SAG 3600µm", "SAG 3800µm", "SAG 4100µm", "Toric SAG 4300µm", "Toric SAG 4500µm", "Toric SAG 4700µm"]

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
    is_selected = i in indici
    img_html = f"<img src='data:image/png;base64,{pil_to_base64(img)}' style='width: 190px; border-radius: 10px;' class='{'selected' if is_selected else ''}'>"
    arrow_html = "<div class='arrow'>⬇️</div>" if is_selected else ""
    label = f"{sag_labels[i]}{' (Lente ideale)' if is_selected else ''}"
    lens_html = f"<div class='lens'>{arrow_html}{img_html}<div>{label}</div></div>"
    cassette_html += lens_html
cassette_html += "</div>"

# Seconda riga
cassette_html += "<div class='cassette-row'>"
for i in range(7):
    index = i + 7
    img = Image.open(paths_2[i])
    is_selected = index in indici
    img_html = f"<img src='data:image/png;base64,{pil_to_base64(img)}' style='width: 190px; border-radius: 10px;' class='{'selected' if is_selected else ''}'>"
    arrow_html = "<div class='arrow'>⬇️</div>" if is_selected else ""
    label = f"{sag_labels_2[i]}{' (Lente ideale)' if is_selected else ''}"
    lens_html = f"<div class='lens'>{arrow_html}{img_html}<div>{label}</div></div>"
    cassette_html += lens_html
cassette_html += "</div>"

cassette_html += "</div>"

# Mostriamo tutto
st.markdown(cassette_html, unsafe_allow_html=True)

# Carica due immagini diverse
with open("scladv1.png", "rb") as img_file_a:
    encoded_a = base64.b64encode(img_file_a.read()).decode()

with open("scladv2.png", "rb") as img_file_b:
    encoded_b = base64.b64encode(img_file_b.read()).decode()

# Mostra affiancate le due immagini
st.markdown(f"""
    <div style='margin-top: 30px; display: flex; justify-content: center; gap: 40px;'>
        <img src='data:image/png;base64,{encoded_a}' style='width: 500px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);'>
        <img src='data:image/png;base64,{encoded_b}' style='width: 500px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);'>
    </div>
""", unsafe_allow_html=True)

# Carica immagine finale
#with open("totalsagc.png", "rb") as img_file_c:
#    encoded_c = base64.b64encode(img_file_c.read()).decode()

# Mostra immagine finale centrata
#st.markdown(f"""
#    <div style='margin-top: 40px; text-align: center;'>
 #       <img src='data:image/png;base64,{encoded_c}' style='width: 700px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);'>
  #  </div>
#""", unsafe_allow_html=True)
