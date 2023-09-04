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
from matplotlib.animation import FuncAnimation
import random


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

# --- Filter data ------------------------------------------------------------------------------------------------------------
st.sidebar.header("Choose your filter:")
selected_load = st.sidebar.selectbox("Pick a LOAD", range(1, 9))  # Allow selecting only one load

# Display the filtered table using Streamlit for the selected load
avg_current = LOAD_tables[selected_load][f'Current-{selected_load}'].mean()
avg_voltage = LOAD_tables[selected_load][f'Voltage-{selected_load}'].mean()
avg_power = LOAD_tables[selected_load][f'Power-{selected_load}'].mean()
avg_pf = LOAD_tables[selected_load][f'Powerfactor-{selected_load}'].mean()
avg_energy = LOAD_tables[selected_load][f'Energy-{selected_load}'].mean()
avg_freq = LOAD_tables[selected_load][f'Frequency-{selected_load}'].mean()
avg_current = round(avg_current, 3)
avg_voltage = round(avg_voltage, 3)
avg_power = round(avg_power, 3)
avg_pf = round(avg_pf, 3)
avg_freq = round(avg_freq, 3)
avg_energy = round(avg_energy, 3)

st.markdown(f"<h3 style='text-align:center;'>Load {selected_load}</h3>", unsafe_allow_html=True)
st.write(len(df.index))
# st.write(LOAD_tables[selected_load])

# Visualizing cards
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


selected = st.selectbox("Select Attribute:", [f"Current-{selected_load}", f"Voltage-{selected_load}", f"Power-{selected_load}", f"Frequency-{selected_load}", f"Power Factor-{selected_load}"])
# Line graph
st.title(f'Time vs. {selected}')
fig = px.line(df, x='Timestamp', y=selected)
st.plotly_chart(fig, use_container_width=True)
st.write("---")

# Histogram
st.title(f"Histogram of {selected} on Time Axes")
fig = px.histogram(df, x="Timestamp", y=selected, histfunc="avg")
fig.update_xaxes(showgrid=True, ticklabelmode="period", dtick="M1", tickformat="%b\n%Y")
fig.update_layout(bargap=0.1)
scatter_trace = go.Scatter(mode="markers", x=df["Timestamp"], y=df[selected], name=f"Mean {selected}")
fig.add_trace(scatter_trace)
st.plotly_chart(fig, use_container_width=True)
st.write("---")

# Time Series with Aligned Periods
st.title('Time Series with Aligned Periods')
fig = go.Figure()
fig.add_trace(go.Scatter(
    name=f"Current",
    mode="markers+lines", x=df["Date"], y=df[f"Current-{selected_load}"],
    marker_symbol="star"
))
fig.add_trace(go.Scatter(
    name="Voltage",
    mode="markers+lines", x=df["Date"], y=df[f"Voltage-{selected_load}"],
    xperiod="M1",
    xperiodalignment="start"
))
fig.add_trace(go.Scatter(
    name="Power",
    mode="markers+lines", x=df["Date"], y=df[f"Power-{selected_load}"],
    xperiod="M1",
    xperiodalignment="middle"
))
fig.add_trace(go.Bar(
    name="Energy",
    x=df["Date"], y=df[f"Energy-{selected_load}"],
    xperiod="M1",
    xperiodalignment="middle"
))
fig.update_xaxes(showgrid=True, ticklabelmode="period")
st.plotly_chart(fig, use_container_width=True)
st.write("---")

# Custome tick labels
columns_to_melt = [f"Current-{selected_load}", f"Voltage-{selected_load}", f"Power-{selected_load}", f"Frequency-{selected_load}", f"Powerfactor-{selected_load}"]
df_long = pd.melt(df, id_vars=["Timestamp", "Date"], value_vars=columns_to_melt, var_name="Variable", value_name="Value")
st.title('Custom Tick Labels')
fig = px.line(df_long, x="Date", y="Value", color="Variable", hover_data={"Date": "|%B %d, %Y"})
fig.update_xaxes(
    dtick="M1", tickformat="%b\n%Y", ticklabelmode="period")
st.plotly_chart(fig, use_container_width=True)

# Display the filtered DataFrame
st.title("Data")
st.write("Number of rows :",len(df.index))
selected_columns = ["Timestamp", "Date", f"Current-{selected_load}", f"Voltage-{selected_load}", f"Power-{selected_load}", f"Frequency-{selected_load}", f"Powerfactor-{selected_load}", f"Energy-{selected_load}" ]
df_selected = df[selected_columns]
st.write(df_selected, use_container_width=True)
st.write("Summary")
st.write(df_selected.describe())