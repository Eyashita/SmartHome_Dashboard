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
import matplotlib.animation as animation


warnings.filterwarnings("ignore")
st.set_page_config(page_title="LOAD", page_icon = ":electric_plug:", layout = "wide")

# --------------------------------------------------------------------------------------------------------------------------
st.title(":electric_plug: IoT Enabled Smart Home Dashboard")
st.markdown('<style> div.block-container{padding-top: 1rem;}</style>', unsafe_allow_html = True)
st.write("---")

# --- Importing Data --------------------------------------------------------------------------------------------------------

# # Importing from MongoDB cloud
# mongo_uri = ""

# --- import css file ---
def local_css(file_name):
 with open(file_name) as f:
  st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("./Style.css")

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

# --- CARD ---------------------------------------------------
def card(card_title, card_content):
    card_html = f'''
    <div class = "card" >
        <h3>{card_title}</h3>
        <p>{card_content}</p>
    </div>'''
    st.markdown(card_html, unsafe_allow_html=True)

# --- CREATING TABLES FOR LOADS ----------------------------------------------------------------

LOAD_tables = {}  # Create an empty dictionary to store the tables

for i in range(1, 9):  # Adjust the range to match your load count (1 to 8 in this case)
    LOAD_columns = [f'Timestamp', f'Voltage-{i}', f'Current-{i}', f'Power-{i}', f'Energy-{i}', f'Powerfactor-{i}', f'Frequency-{i}']
    LOAD_tables[i] = df[LOAD_columns].copy()  # Store the table in the dictionary

# --- TIME SERIES PLOT --------------------------------------------------------------------------
def create_animated_plot(load_table, load_number):
    # Create a Matplotlib figure
    fig, ax = plt.subplots()

    # Define an initialization function (customize it based on your needs)
    def init():
        ax.clear()
        ax.set_xlabel('Current')
        ax.set_ylabel('Timestamp')
        line, = ax.plot([], [], lw=2)
        return line,

    def animate(k):
        # t is a parameter
        t = 0.1 * k

        # x, y values to be plotted
        X = load_table[f"Current-{load_number}"]
        Y = load_table['Timestamp']

        # Update the data on the line object
        line.set_data(X, Y)

        return line,

    # hiding the axis details
    ax.axis('off')

    # call the animator
    anim = animation.FuncAnimation(fig, animate, init_func=init, blit=True)

    # Display the Matplotlib plot in Streamlit
    st.markdown(f"<h3 style='text-align:center;'>Load {i}</h3>", unsafe_allow_html=True)
    st.pyplot(fig)


# --- Filter data ------------------------------------------------------------------------------------------------------------
st.sidebar.header("Choose your filter:")
selected_loads = st.sidebar.multiselect("Pick LOAD(s)", range(1, 9))  # Allow selecting multiple loads

filtered_tables = [LOAD_tables[i] for i in selected_loads]  # Get the tables for the selected loads

# Display the filtered tables using Streamlit
for i, table in zip(selected_loads, filtered_tables):
    avg_current = table[f'Current-{i}'].mean()
    avg_voltage = table[f'Voltage-{i}'].mean()
    avg_power = table[f'Power-{i}'].mean()
    avg_pf = table[f'Powerfactor-{i}'].mean()
    avg_energy = table[f'Energy-{i}'].mean()
    avg_freq = table[f'Frequency-{i}'].mean()
    avg_current = round(avg_current, 3)
    avg_voltage = round(avg_voltage, 3)
    avg_power = round(avg_power, 3)
    avg_pf = round(avg_pf, 3)
    avg_freq = round(avg_freq, 3)
    avg_energy = round(avg_energy, 3)

    st.markdown(f"<h3 style='text-align:center;'>Load {i}</h3>", unsafe_allow_html=True)
    st.write(LOAD_tables[i])

    load_table = LOAD_tables[i]
    create_animated_plot(load_table, i)


    col1, col2, col3 = st.columns(3)
    # Add content to the columns
    with col1:
        card_data = {"title": "Average Current (in A)", "content": avg_current}
        card(card_data["title"], card_data["content"])
    with col2:
        card_data = {"title": "Average Power (in W)", "content": avg_power}
        card(card_data["title"], card_data["content"])
    with col3:
        card_data = {"title": "Average Voltage (in V)", "content": avg_voltage}
        card(card_data["title"], card_data["content"])

    # Create another row of columns
    col4, col5, col6 = st.columns(3)

    # Add content to the new columns
    with col4:
        card_data = {"title": "Average Frequency", "content": avg_freq}
        card(card_data["title"], card_data["content"])
    with col5:
        card_data = {"title": "Average Power Factor", "content": avg_pf}
        card(card_data["title"], card_data["content"])
    with col6:
        card_data = {"title": "Average Energy (in Kwh)", "content": avg_energy}
        card(card_data["title"], card_data["content"])

    st.write("---")

    load_table = LOAD_tables[i]
    create_animated_plot(load_table, i)

