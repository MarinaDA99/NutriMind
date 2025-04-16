import streamlit as st
import pandas as pd
import csv
import os
from datetime import datetime, timedelta

# --- Configuración de la página ---
st.set_page_config(page_title="Dieta vegetal 30x", layout="centered")
st.title("🌱 La regla de oro: ¡30 plantas distintas por semana!")

# --- Diccionario de categorías y alimentos ---
# ... (mismo bloque de "categorias" que tienes tú, omitido aquí por espacio)

# --- Grupos válidos como vegetales ---
grupos_vegetales = [
    "🥦 Verduras y hortalizas",
    "🍎 Frutas",
    "🫘 Legumbres",
    "🌰 Frutos secos y semillas",
    "🌾 Cereales y pseudocereales"
]

# --- Set de alimentos vegetales válidos ---
vegetales_validos = set()
for grupo in grupos_vegetales:
    if grupo in categorias:
        vegetales_validos.update([a.lower() for a in categorias[grupo]])

# --- Lista de todos los alimentos (para multiselect) ---
todos_alimentos = sorted({item for sublist in categorias.values() for item in sublist})

# --- Formulario diario ---
with st.form("registro"):
    st.subheader("📋 Registro diario")
    seleccionados = st.multiselect("¿Qué comiste hoy?", options=todos_alimentos)
    sueno = st.number_input("¿Horas de sueño?", min_value=0.0, max_value=24.0, step=0.5)
    ejercicio = st.text_input("¿Ejercicio realizado?")
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

# --- Cargar datos ---
archivo_csv = "data/habitos.csv"
if os.path.exists(archivo_csv):
    df = pd.read_csv(archivo_csv, encoding="utf-8-sig")
    if not df.empty:
        df.columns = ["fecha", "comida", "sueno", "ejercicio", "animo"]
        df["fecha"] = pd.to_datetime(df["fecha"]).dt.date

        # --- Mostrar vegetales únicos por día ---
        st.markdown("---")
        st.subheader("📅 Vegetales únicos por día")
        for fecha, grupo in df.groupby("fecha"):
            diarios = set()
            for entrada in grupo["comida"].dropna():
                diarios.update([
                    item.strip().lower() for item in entrada.split(",")
                    if item.strip().lower() in vegetales_validos
                ])
            st.markdown(f"📆 **{fecha}**: {len(diarios)} vegetales: {', '.join(sorted(diarios))}")

        # --- Análisis semanal ---
        st.markdown("---")
        st.subheader("🌿 Diversidad vegetal semanal")
        inicio_semana = datetime.now().date() - timedelta(days=datetime.now().weekday())
        df_semana = df[df["fecha"] >= inicio_semana]

        vegetales_semana = set()
        for entrada in df_semana["comida"].dropna():
            vegetales_semana.update([
                item.strip().lower() for item in entrada.split(",")
                if item.strip().lower() in vegetales_validos
            ])

        progreso = len(vegetales_semana)
        total = 30
        st.markdown(f"Esta semana has comido **{progreso} / 30** vegetales diferentes.")
        st.markdown("🟩" * progreso + "⬜" * (total - progreso))

        # --- Sugerencias ---
        st.markdown("---")
        st.subheader("💡 Sugerencias para hoy")
        sugerencias = sorted(list(vegetales_validos - vegetales_semana))[:5]
        if sugerencias:
            st.markdown("🎯 Prueba algo nuevo:")
            st.markdown(", ".join(sugerencias))
        else:
            st.success("🎉 ¡Ya has probado 30 vegetales distintos esta semana!")
else:
    st.info("Aún no has registrado comidas.")
