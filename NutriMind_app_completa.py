import streamlit as st
import pandas as pd
import csv
import os
from datetime import datetime, timedelta

# --- Configuración de página ---
st.set_page_config(page_title="NutriBioMind", layout="centered")
st.title("🌱 La regla de oro para una microbiota saludable: 30 plantas por semana")

# --- Alimentos por categorías ---
categorias = {
    "🥦 Verduras y hortalizas": ["acelga", "apio", "berenjena", "brócoli", "calabacín", "calabaza", "cardo", "cebolla", "cebolleta", "col blanca", "col de Bruselas", "col lombarda", "col rizada (kale)", "coliflor", "endibia", "escarola", "espárrago", "espinaca", "hinojo", "judía verde", "lechuga romana", "lechuga iceberg", "nabo", "pepino", "pimiento rojo", "pimiento verde", "puerro", "rábano", "remolacha", "tomate", "zanahoria", "alcachofa", "chirivía", "boniato (batata)", "patata", "ñame", "taro", "malanga", "yuca", "okra", "pak choi", "berza", "acedera", "mostaza verde", "diente de león (hojas)", "berro", "canónigos", "mizuna", "tatsoi", "escarola rizada"],
    "🍎 Frutas": ["manzana", "pera", "plátano", "naranja", "mandarina", "kiwi", "uva", "granada", "fresa", "frambuesa", "mora", "arándano", "cereza", "melocotón", "albaricoque", "ciruela", "mango", "papaya", "piña", "melón", "sandía", "higo", "caqui", "lichi", "maracuyá", "guayaba", "chirimoya", "carambola", "níspero", "pomelo", "lima", "limón", "coco", "aguacate", "tomate cherry", "grosella", "zarzamora", "mandarino", "plátano macho", "dátil"],
    "🫘 Legumbres": ["lenteja", "garbanzo", "judía blanca", "judía roja", "judía negra", "habas", "guisantes", "soja", "azuki", "mungo", "lupino", "alubia pinta", "alubia canela", "alubia carilla", "alubia de Lima", "alubia de riñón", "alubia moteada", "alubia escarlata", "alubia borlotti", "alubia navy"],
    "🌰 Frutos secos y semillas": ["almendra", "avellana", "nuez", "nuez de Brasil", "nuez de macadamia", "pistacho", "anacardo", "cacahuete", "pipa de girasol", "pipa de calabaza", "semilla de sésamo", "semilla de chía", "semilla de lino", "semilla de amapola", "semilla de cáñamo", "semilla de alcaravea", "semilla de hinojo", "semilla de mostaza", "semilla de albahaca", "semilla de comino", "semilla de coriandro", "semilla de anís", "semilla de cardamomo", "semilla de nigella", "semilla de fenogreco", "semilla de ajonjolí negro"],
    "🌾 Cereales y pseudocereales": ["trigo integral", "avena", "cebada", "centeno", "arroz integral", "maíz", "quinoa", "amaranto", "mijo", "teff", "alforfón (trigo sarraceno)", "espelta", "kamut", "sorgo", "farro", "freekeh", "bulgur", "candeal", "arroz salvaje"]
}

# --- Set de vegetales válidos ---
grupos_vegetales = ["🥦 Verduras y hortalizas", "🍎 Frutas", "🫘 Legumbres", "🌰 Frutos secos y semillas", "🌾 Cereales y pseudocereales"]
vegetales_validos = set()
for grupo in grupos_vegetales:
    vegetales_validos.update([a.lower() for a in categorias[grupo]])

# --- Lista completa de alimentos ---
todos_alimentos = sorted({item for sublist in categorias.values() for item in sublist})

# --- Formulario de registro ---
with st.form("registro"):
    st.subheader("📋 Registro diario")

    seleccionados = st.multiselect("Selecciona los alimentos que comiste hoy:", options=todos_alimentos)
    sueno = st.number_input("¿Cuántas horas dormiste?", min_value=0.0, max_value=24.0, step=0.5)
    ejercicio = st.text_input("¿Ejercicio realizado (ej: 30 min caminata)?")
    animo = st.slider("¿Cómo te sientes hoy?", 1, 5, 3)
    submitted = st.form_submit_button("Guardar")

    if submitted:
        fecha = datetime.now().strftime('%Y-%m-%d')
        os.makedirs("data", exist_ok=True)
        archivo_csv = "data/habitos.csv"
        registro = [fecha, ", ".join(seleccionados), sueno, ejercicio, animo]
        nuevo = not os.path.exists(archivo_csv)

        with open(archivo_csv, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            if nuevo:
                writer.writerow(["fecha", "comida", "sueno", "ejercicio", "animo"])
            writer.writerow(registro)

        st.success("✅ Registro guardado correctamente.")

# --- Análisis semanal de vegetales únicos ---
st.markdown("---")
st.subheader("🌿 Diversidad vegetal semanal")

archivo_csv = "data/habitos.csv"
if os.path.exists(archivo_csv):
    df = pd.read_csv(archivo_csv, encoding="utf-8-sig")
    if not df.empty:
        df.columns = ["fecha", "comida", "sueno", "ejercicio", "animo"]
        df["fecha"] = pd.to_datetime(df["fecha"])
        inicio_semana = datetime.now() - timedelta(days=datetime.now().weekday())
        df_semana = df[df["fecha"] >= inicio_semana]

        alimentos_unicos = set()
        for entrada in df_semana["comida"].dropna():
            alimentos = [a.strip().lower() for a in entrada.split(",")]
            alimentos_unicos.update(alimentos)

        vegetales_consumidos = [v for v in alimentos_unicos if v in vegetales_validos]
        progreso = len(set(vegetales_consumidos))
        total = 30
        bloques_llenos = "🟩" * progreso
        bloques_vacios = "⬜" * (total - progreso)

        st.markdown(f"**{progreso}/30 vegetales únicos esta semana**")
        st.markdown(f"{bloques_llenos}{bloques_vacios}")

        if progreso < total:
            faltan = total - progreso
            st.info(f"💡 Puedes sumar {faltan} vegetales distintos esta semana.")
    else:
        st.info("Aún no hay registros esta semana.")
else:
    st.info("Aún no has guardado ningún registro.")


