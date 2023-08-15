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
    os.chdir(r"D:\DA Internship Project")
    df = pd.read_csv("HouseHold Data.csv", encoding = "ISO-8859-1")

# --- Dates --------------------------------------------------------------------------------------------------------
col1, col2 = st.columns((2))
df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")

# Getting min and max date
startDate = pd.to_datetime(df["Date"]).min()
endDate = pd.to_datetime(df["Date"]).max()
  
with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()
st.write("---")
#st.write(df.describe())

# --- Filter data ------------------------------------------------------------------------------------------------------------
st.sidebar.header("Choose your filter:")
LOADS = st.sidebar.multiselect("Pick a LOAD", df["LOADS"].unique())
if not LOADS:
    df2 = df.copy()
else:
    df2 = df[df["LOADS"].isin(LOADS)]
# ----------------------------------------------------------------------------

# --- Average Current ---

def current_average():
    current_values = df["Current"]
    if current_values.empty:
        return None
    total = current_values.sum()
    avg = total / len(current_values)
    return round(avg, 3)

# --- Average Power ---
def power_average():
    power_values = df["Power"]
    if power_values.empty:
        return None
    total = power_values.sum()
    avg = total / len(power_values)
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
    energy_values = df["Energy (in Kwh)"]
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
    card_data = {"title": "Average Current", "content": avg}
    card(card_data["title"], card_data["content"])
with col2:
    avg = power_average()
    card_data = {"title": "Average Power", "content": avg}
    card(card_data["title"], card_data["content"])
with col3:
    avg = voltage_average()
    card_data = {"title": "Average Voltage", "content": avg}
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
    card_data = {"title": "Average Energy", "content": avg}
    card(card_data["title"], card_data["content"])

st.write("---")
# ---------------------------------------------------------------

# --- bar chart ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Current Vs. Voltage")
        cd = pd.DataFrame(df["Current"], df["Voltage"])
        st.bar_chart(cd)
        with col2:
            st.subheader("Loads Vs. Voltage")
            chart_data = pd.DataFrame(df["LOADS"], df["Voltage"])
            st.bar_chart(chart_data)

