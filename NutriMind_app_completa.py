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
st.header("Weekly Plant-Based Diversity Analysis")

# Only perform analysis if the CSV file exists and has data
if os.path.exists(file_path):
    # Load the data
    df = pd.read_csv(file_path, parse_dates=["fecha"])
    if df.empty:
        st.write("No data available yet. Add some records above!")
    else:
        # Ensure 'fecha' column is in date format (not just datetime64)
        df['fecha'] = pd.to_datetime(df['fecha']).dt.date
        
        # Define the start date for the last 7 days window
        one_week_ago = datetime.now().date() - timedelta(days=7)
        
        # Filter data for the last 7 days (including today)
        last_week_data = df[df['fecha'] >= one_week_ago]
        
        if last_week_data.empty:
            st.write("No data in the last week to analyze.")
        else:
            # Calculate diversity: number of unique plant-based categories in the last week
            diversity_categories = set()
            if "categories" in last_week_data.columns:
                # If categories are stored in a single column as comma-separated string
                for entry in last_week_data["categories"].dropna():
                    if isinstance(entry, str):
                        # Split the string by comma to get individual categories
                        for cat in entry.split(","):
                            cat = cat.strip()
                            if cat:
                                diversity_categories.add(cat)
            else:
                # If categories were stored in separate columns (e.g., one column per category)
                possible_categories = ["Fruits", "Vegetables", "Legumes", "Whole Grains", "Nuts/Seeds", "Others"]
                for cat_col in possible_categories:
                    if cat_col in last_week_data.columns:
                        # Count this category if any record in the last week has a positive value or True
                        if last_week_data[cat_col].astype(bool).any():
                            diversity_categories.add(cat_col)
            
            diversity_count = len(diversity_categories)
            st.write(f"In the last 7 days, you have consumed from **{diversity_count}** different plant-based food categories.")
else:
    st.write("No data recorded yet. Use the form above to add daily records.")
#show data
if os.path.exists("data/habitos.csv"):
    st.subheader("📋 Registros guardados")
    df = pd.read_csv("data/habitos.csv")
    st.dataframe(df)
