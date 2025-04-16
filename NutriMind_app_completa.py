import streamlit as st
import pandas as pd
from datetime import datetime, timedelta  # Added missing import for timedelta
import os

# Ensure the data directory exists (for saving the CSV file)
os.makedirs('data', exist_ok=True)
file_path = 'data/habitos.csv'

# Title of the app
st.title("Plant-Based Food Consumption Tracker")

# Form for daily input of food, sleep, mood, and exercise
with st.form("daily_entry_form"):
    st.header("Daily Entry")
    # Date input (default to today); using this instead of a redefined 'fecha' outside
    date_input = st.date_input("Fecha", value=datetime.now().date())
    
    # Multi-select for plant-based food categories consumed today
    categories = st.multiselect(
        "Plant-based food categories consumed today:",
        ["Fruits", "Vegetables", "Legumes", "Whole Grains", "Nuts/Seeds", "Others"]
    )
    
    # Numeric input for hours of sleep
    sleep_hours = st.number_input("Hours of Sleep", min_value=0.0, max_value=24.0, value=8.0, step=0.5)
    
    # Slider or select slider for mood (1 to 5)
    mood = st.select_slider("Mood (1 = lowest, 5 = highest)", options=[1, 2, 3, 4, 5], value=3)
    
    # Selectbox for exercise (Yes/No)
    exercise = st.selectbox("Exercise today?", ["Yes", "No"])
    
    # Submit button for the form
    submitted = st.form_submit_button("Save Daily Record")

# If the form is submitted, save the data to CSV
if submitted:
    # Prepare the new data record as a dictionary
    categories_str = ", ".join(categories)  # join list of categories into a single string
    new_record = {
        "fecha": date_input,
        "categories": categories_str,
        "sleep_hours": sleep_hours,
        "mood": mood,
        "exercise": exercise
    }
    
    # Convert the record to a DataFrame
    df_new = pd.DataFrame([new_record])
    # Append to CSV: write header only if file did not already exist
    file_exists = os.path.isfile(file_path)
    df_new.to_csv(file_path, mode='a', index=False, header=not file_exists)
    
    # Confirmation message
    st.success("Daily record saved successfully!")

# Weekly analysis of plant-based food diversity
st.header("🌿 Diversidad vegetal semanal")

if os.path.exists("data/habitos.csv"):
    df = pd.read_csv("data/habitos.csv", encoding="utf-8-sig")
    df.columns = ["fecha", "comida", "sueno", "ejercicio", "animo"] + list(categorias.keys())
    df["fecha"] = pd.to_datetime(df["fecha"])

    # Get start of the current week (Monday)
    inicio_semana = datetime.now() - timedelta(days=datetime.now().weekday())
    df_semana = df[df["fecha"] >= inicio_semana]

    alimentos_unicos = set()
    for entrada in df_semana["comida"].dropna():
        alimentos = [a.strip().lower() for a in entrada.split(",")]
        alimentos_unicos.update(alimentos)

    # Filtrar por vegetales válidos (para no contar carnes, etc.)
    vegetales_consumidos = [v for v in alimentos_unicos if v in vegetales_validos]
    total = 30
    progreso = len(set(vegetales_consumidos))

    st.markdown(f"**{progreso}/30** vegetales únicos esta semana 🌱")
    st.markdown("🟩" * progreso + "⬜" * (total - progreso))

    if progreso < 30:
        faltantes = total - progreso
        st.info(f"¡Puedes sumar {faltantes} vegetales más esta semana! 💪")
else:
    st.warning("Aún no hay datos para esta semana.")
#show data
if os.path.exists("data/habitos.csv"):
    st.subheader("📋 Registros guardados")
    df = pd.read_csv("data/habitos.csv")
    st.dataframe(df)
