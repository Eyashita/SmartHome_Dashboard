# Import Modules
import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import plotly.graph_objects as go
import requests
from streamlit_lottie import st_lottie
import numpy as np

warnings.filterwarnings("ignore")
st.set_page_config(page_title="Dynamic Dashboard", page_icon = ":electric_plug:", layout = "wide")


st.sidebar.success("Select a page above.")

# --- import css file ---
def local_css(file_name):
 with open(file_name) as f:
  st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("./Style.css")

# --- Function to import Lottiefiles ---
def load_lottiurl(url):
 r = requests.get(url)
 if r.status_code != 200:
  return None
 return r.json()

# --------------------------------------------------------------------------------------------------------------------------
st.title(":electric_plug: IoT Enabled Smart Home Dashboard")
st.markdown('<style> div.block-container{padding-top: 1rem;}</style>', unsafe_allow_html = True)
st.write("---")

# --- Importing Data --------------------------------------------------------------------------------------------------------

# # Importing from MongoDB cloud
# mongo_uri = ""

# --- Import DATA FILE ----------------------------------------------------------------------------------------------------------------------
fl = st.file_uploader(":file_folder: Upload a file", type=(["csv","txt","xlsx", "xls"]))

if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    os.chdir(r"D:/Projects/Dashboard")
    df = pd.read_csv("data.csv", encoding = "ISO-8859-1")

# --- Dates --------------------------------------------------------------------------------------------------------
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df["Date"] = df['Timestamp'].dt.date

# Getting min and max date
startDate = pd.to_datetime(df["Date"]).min()
endDate = pd.to_datetime(df["Date"]).max()

col1, col2 = st.columns((2))  
with col1:
    date1 = st.date_input("Start Date", startDate)
with col2:
    date2 = st.date_input("End Date", endDate)

date1 = pd.Timestamp(date1)
date2 = pd.Timestamp(date2)

df = df[(df["Date"] >= date1.date()) & (df["Date"] <= date2.date())].copy()
# Drop columns with null values
df.dropna(axis=1, inplace=True)
st.write("---")

# ----------------------------------------------------------------------------

# --- Creating AVG. columns ---
df['Current'] = df[['Current-1', 'Current-2', 'Current-3', 'Current-4', 'Current-5', 'Current-6', 'Current-7', 'Current-8']].mean(axis=1)
df['Voltage'] = df[['Voltage-1', 'Voltage-2', 'Voltage-3', 'Voltage-4', 'Voltage-5', 'Voltage-6', 'Voltage-7', 'Voltage-8']].mean(axis=1)
df['Power'] = df[['Power-1', 'Power-2', 'Power-3', 'Power-4', 'Power-5', 'Power-6', 'Power-7', 'Power-8']].mean(axis=1)
df['Frequency'] = df[['Frequency-1', 'Frequency-2', 'Frequency-3', 'Frequency-4', 'Frequency-5', 'Frequency-6', 'Frequency-7', 'Frequency-8']].mean(axis=1)
df['Power Factor'] = df[['Powerfactor-1', 'Powerfactor-2', 'Powerfactor-3', 'Powerfactor-4', 'Powerfactor-5', 'Powerfactor-6', 'Powerfactor-7', 'Powerfactor-8']].mean(axis=1)
df['Energy'] = df[['Energy-1', 'Energy-2', 'Energy-3', 'Energy-4', 'Energy-5', 'Energy-6', 'Energy-7', 'Energy-8']].mean(axis=1)
# Drop columns with null values
df.dropna(axis=1, inplace=True)
# Display the filtered DataFrame
st.write(df)

# --- Average Current ---
def current_average():
    current_values = df["Current"]
    if current_values.empty:
        return None
    avg = current_values.mean()
    return round(avg, 3)

# --- Average Power ---
def power_average():
    power_values = df["Power"]
    if power_values.empty:
        return None
    avg = power_values.mean()
    return round(avg, 3)

# --- Average Voltage ---
def voltage_average():
    voltage_values = df["Voltage"]
    if voltage_values.empty:
        return None
    total = voltage_values.sum()
    avg = total / len(voltage_values)
    return round(avg, 3)

# --- Average Frequency ---
def freq_average():
    freq_values = df["Frequency"]
    if freq_values.empty:
        return None
    total = freq_values.sum()
    avg = total / len(freq_values)
    return round(avg, 3)

# --- Average PowerFactor ---
def pf_average():
    pf_values = df["Power Factor"]
    if pf_values.empty:
        return None
    total = pf_values.sum()
    avg = total / len(pf_values)
    return round(avg, 3)

# --- Average Energy ---
def energy_average():
    energy_values = df["Energy"]
    if energy_values.empty:
        return None
    total = energy_values.sum()
    avg = total / len(energy_values)
    return round(avg, 3)

# --- Card container -------------------------------------
def card(card_title, card_content):
    card_html = f'''
    <div class = "card" >
        <h3>{card_title}</h3>
        <p>{card_content}</p>
    </div>'''
    st.markdown(card_html, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
# Add content to the columns
with col1:
    avg = current_average()
    card_data = {"title": "Average Current (in A)", "content": avg}
    card(card_data["title"], card_data["content"])
with col2:
    avg = power_average()
    card_data = {"title": "Average Power (in W)", "content": avg}
    card(card_data["title"], card_data["content"])
with col3:
    avg = voltage_average()
    card_data = {"title": "Average Voltage (in V)", "content": avg}
    card(card_data["title"], card_data["content"])

# Create another row of columns
col4, col5, col6 = st.columns(3)

# Add content to the new columns
with col4:
    avg = freq_average()
    card_data = {"title": "Average Frequency", "content": avg}
    card(card_data["title"], card_data["content"])
with col5:
    avg = pf_average()
    card_data = {"title": "Average Power Factor", "content": avg}
    card(card_data["title"], card_data["content"])
with col6:
    avg = energy_average()
    card_data = {"title": "Average Energy (in Kwh)", "content": avg}
    card(card_data["title"], card_data["content"])

st.write("---")
# ---------------------------------------------------------------

# # --- CREATING TABLES FOR LOADS ----------------------------------------------------------------

# LOAD_tables = {}  # Create an empty dictionary to store the tables

# for i in range(1, 9):  # Adjust the range to match your load count (1 to 8 in this case)
#     LOAD_columns = [f'Voltage-{i}', f'Current-{i}', f'Power-{i}', f'Energy-{i}', f'Powerfactor-{i}', f'Frequency-{i}']
#     LOAD_tables[i] = df[LOAD_columns].copy()  # Store the table in the dictionary

# # --- Filter data ------------------------------------------------------------------------------------------------------------
# st.sidebar.header("Choose your filter:")
# selected_loads = st.sidebar.multiselect("Pick LOAD(s)", range(1, 9))  # Allow selecting multiple loads

# filtered_tables = [LOAD_tables[i] for i in selected_loads]  # Get the tables for the selected loads

# # Display the filtered tables using Streamlit
# for i, table in zip(selected_loads, filtered_tables):
#     avg_current = table[f'Current-{i}'].mean()
#     avg_voltage = table[f'Voltage-{i}'].mean()
#     avg_power = table[f'Power-{i}'].mean()
#     avg_pf = table[f'Powerfactor-{i}'].mean()
#     avg_energy = table[f'Energy-{i}'].mean()
#     avg_freq = table[f'Frequency-{i}'].mean()
#     avg_current = round(avg_current, 3)
#     avg_voltage = round(avg_voltage, 3)
#     avg_power = round(avg_power, 3)
#     avg_pf = round(avg_pf, 3)
#     avg_freq = round(avg_freq, 3)
#     avg_energy = round(avg_energy, 3)

#     st.markdown(f"<h3 style='text-align:center;'>Load {i}</h3>", unsafe_allow_html=True)

#     col1, col2, col3 = st.columns(3)
#     # Add content to the columns
#     with col1:
#         card_data = {"title": "Average Current (in A)", "content": avg_current}
#         card(card_data["title"], card_data["content"])
#     with col2:
#         avg = power_average()
#         card_data = {"title": "Average Power (in W)", "content": avg_power}
#         card(card_data["title"], card_data["content"])
#     with col3:
#         avg = voltage_average()
#         card_data = {"title": "Average Voltage (in V)", "content": avg_voltage}
#         card(card_data["title"], card_data["content"])

#     # Create another row of columns
#     col4, col5, col6 = st.columns(3)

#     # Add content to the new columns
#     with col4:
#         avg = freq_average()
#         card_data = {"title": "Average Frequency", "content": avg_freq}
#         card(card_data["title"], card_data["content"])
#     with col5:
#         avg = pf_average()
#         card_data = {"title": "Average Power Factor", "content": avg_pf}
#         card(card_data["title"], card_data["content"])
#     with col6:
#         avg = energy_average()
#         card_data = {"title": "Average Energy (in Kwh)", "content": avg_energy}
#         card(card_data["title"], card_data["content"])

#     st.write("---")

# st.set_page_config( page_title = "Multipage App", page_icon = ":electric_plug:",)
# st.title("Main Page")
