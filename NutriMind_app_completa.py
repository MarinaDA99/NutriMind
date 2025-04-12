
import pandas as pd
import streamlit as st
import csv
from datetime import datetime, timedelta
import os


st.set_page_config(page_title="NutriMind", layout="centered")
st.title("🌱 NutriMind: Tu coach de hábitos saludables")

# ------------------------------
# 🧠 PLANTAS CONOCIDAS
# ------------------------------
plantas_conocidas = [
    # Verduras y hortalizas
    "acelga", "apio", "berenjena", "brócoli", "calabacín", "calabaza", "cardo", "cebolla", "cebolleta", "col blanca",
    "col de bruselas", "col lombarda", "col rizada", "coliflor", "endibia", "escarola", "espárrago", "espinaca",
    "hinojo", "judía verde", "lechuga romana", "lechuga iceberg", "nabo", "pepino", "pimiento rojo", "pimiento verde",
    "puerro", "rábano", "remolacha", "tomate", "zanahoria", "alcachofa", "chirivía", "boniato", "patata", "ñame",
    "taro", "malanga", "yuca", "okra", "pak choi", "berza", "acedera", "mostaza verde", "diente de león", "berro",
    "canónigos", "mizuna", "tatsoi", "escarola rizada",

    # Frutas
    "manzana", "pera", "plátano", "naranja", "mandarina", "kiwi", "uva", "granada", "fresa", "frambuesa", "mora",
    "arándano", "cereza", "melocotón", "albaricoque", "ciruela", "mango", "papaya", "piña", "melón", "sandía", "higo",
    "caqui", "lichi", "maracuyá", "guayaba", "chirimoya", "carambola", "níspero", "pomelo", "lima", "limón", "coco",
    "aguacate", "tomate cherry", "grosella", "zarzamora", "mandarino", "plátano macho", "dátil",

    # Frutos secos y semillas
    "almendra", "avellana", "nuez", "nuez de brasil", "nuez de macadamia", "pistacho", "anacardo", "cacahuete",
    "pipa de girasol", "pipa de calabaza", "semilla de sésamo", "semilla de chía", "semilla de lino",
    "semilla de amapola", "semilla de cáñamo", "semilla de alcaravea", "semilla de hinojo", "semilla de mostaza",
    "semilla de albahaca", "semilla de comino", "semilla de coriandro", "semilla de anís", "semilla de cardamomo",
    "semilla de nigella", "semilla de fenogreco", "semilla de ajonjolí negro", "semilla de calabaza tostada",
    "semilla de girasol tostada", "semilla de lino dorado", "semilla de chía blanca",

    # Legumbres
    "lenteja", "garbanzo", "judía blanca", "judía roja", "judía negra", "habas", "guisantes", "soja", "azuki", "mungo",
    "lupino", "alubia pinta", "alubia canela", "alubia carilla", "alubia de lima", "alubia de riñón", "alubia moteada",
    "alubia escarlata", "alubia borlotti", "alubia navy",

    # Cereales y pseudocereales
    "trigo integral", "avena", "cebada", "centeno", "arroz integral", "maíz", "quinoa", "amaranto", "mijo", "teff",
    "alforfón", "espelta", "kamut", "sorgo", "farro", "freekeh", "trigo bulgur", "trigo candeal", "trigo sarraceno",
    "arroz salvaje",

    # Setas y hongos
    "champiñón", "shiitake", "maitake", "gírgola", "enoki", "portobello", "rebozuelo", "trompeta de la muerte",
    "seta de cardo", "seta de chopo", "seta de pie azul", "seta de pino", "seta de haya", "seta de álamo",
    "seta de abedul", "seta de roble", "seta de caoba", "seta de castaño", "seta de aliso", "seta de fresno",

    # Hierbas y especias
    "albahaca", "perejil", "cilantro", "menta", "hierbabuena", "romero", "tomillo", "orégano", "salvia", "estragón",
    "eneldo", "cebollino", "laurel", "mejorana", "ajedrea", "hinojo", "lemongrass", "curry", "hoja de lima kaffir",
    "hoja de laurel indio"
]

def extraer_plantas(comida, lista_plantas):
    comida = comida.lower()
    return [planta for planta in lista_plantas if planta in comida]

# ------------------------------
# 📝 Registro diario
# ------------------------------
with st.form("registro"):
    st.subheader("📋 Registro diario")
    comida_seleccionada = st.multiselect(
        "Selecciona los alimentos vegetales que comiste hoy:",
        options=sorted(set(plantas_conocidas)),
        help="Puedes seleccionar varios (usa Ctrl/Cmd)"
    )
    comida = ", ".join(comida_seleccionada)
    sueno = st.number_input("¿Cuántas horas dormiste?", min_value=0.0, max_value=24.0, step=0.5)
    ejercicio = st.text_input("¿Ejercicio realizado (ej: 30 min caminata)?")
    animo = st.slider("¿Cómo te sientes hoy?", 1, 5, 3)
    submitted = st.form_submit_button("Guardar")

    if submitted:
        fecha = datetime.now().strftime('%Y-%m-%d')
        plantas = extraer_plantas(comida, plantas_conocidas)
        fila = [fecha, comida, sueno, ejercicio, animo, ";".join(plantas)]

        os.makedirs("data", exist_ok=True)
        with open("data/habitos.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(fila)
        st.success("✅ Registro guardado correctamente.")

# ------------------------------
# 📊 Diversidad semanal
# ------------------------------
st.markdown("---")
st.subheader("🌿 Diversidad vegetal esta semana")

def contar_plantas_semana():
    try:
        df = pd.read_csv("data/habitos.csv", header=None,
                         names=["fecha", "comida", "sueno", "ejercicio", "animo", "plantas"])
        df["fecha"] = pd.to_datetime(df["fecha"])
        inicio_semana = datetime.now() - timedelta(days=datetime.now().weekday())
        df_semana = df[df["fecha"] >= inicio_semana]
        plantas_semana = set()
        for entry in df_semana["plantas"].dropna():
            plantas_semana.update(entry.split(";"))
        return len(plantas_semana), plantas_semana
    except:
        return 0, set()

n_plantas, lista_plantas = contar_plantas_semana()

if n_plantas < 30:
    st.warning(f"Esta semana has consumido {n_plantas} plantas distintas. Intenta llegar a 30 para cuidar tu microbiota 🌱.")
else:
    st.success(f"🎉 ¡Excelente! Has alcanzado {n_plantas} plantas distintas esta semana.")
    with st.expander("Ver lista de plantas consumidas"):
        st.write(", ".join(sorted(lista_plantas)))
