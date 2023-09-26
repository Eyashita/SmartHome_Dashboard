# Import Modules
import streamlit as st
import plotly.express as px
import pandas as pd
import warnings
import plotly.graph_objects as go
import pymongo
import time
import uuid


warnings.filterwarnings("ignore")
st.set_page_config(page_title="Dynamic Dashboard", page_icon = ":electric_plug:", layout = "wide")

# --- import css file ---
def local_css(file_name):
 with open(file_name) as f:
  st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("./Style.css")

# --------------------------------------------------------------------------------------------------------------------------
st.title(":electric_plug: IoT Enabled Smart Home Dashboard")
st.markdown('<style> div.block-container{padding-top: 1rem;}</style>', unsafe_allow_html = True)
st.write("---")
# --- Importing Data --------------------------------------------------------------------------------------------------------

# # Importing from MongoDB cloud
client = pymongo.MongoClient("mongodb+srv://eyashita_1o:chunmun1010@cluster0.ljpgyjo.mongodb.net/")
db = client["Dashboard"]
collection = db["Household_data"]
 
# --- Import DATA FILE ----------------------------------------------------------------------------------------------------------------------
fl = st.file_uploader(":file_folder: Upload a file", type=(["csv","txt","xlsx", "xls"]))

@st.cache_data(ttl=1)
def load_data():
    # Fetch data from MongoDB and convert to DataFrame
    cursor = collection.find({})
    df = pd.DataFrame(list(cursor))
    return df

df = load_data()
st.session_state['df'] = df
df = df.fillna(0)

# # Create a Streamlit interval to refresh data every 5 seconds
# refresh_interval = st.experimental_get_query_params().get("refresh_interval", [1])[0]
# st.experimental_set_query_params(refresh_interval=refresh_interval)  # Persist query parameter

# # Create a Streamlit interval to refresh data every 5 seconds
# refresh_interval = 1 * 1000

# @st.cache_data(ttl=refresh_interval)

def update_data():
    # Fetch updated data from MongoDB and convert to DataFrame
    cursor = collection.find({})
    updated_df = pd.DataFrame(list(cursor))
    return updated_df

placeholder = st.empty()

while True:
    with placeholder.container():
        # placeholder.text(f"Data Loaded at: {time.strftime('%H:%M:%S')}")
        df = update_data()
        st.write(len(df))
        df = df.fillna(0)
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
        prefix = "Voltage-"
        # Use list comprehension to select columns with the specified prefix
        selected_columns = [col for col in df.columns if col.startswith(prefix)]
        # Sum the selected columns along the rows to create the 'Current' column
        df['Voltage'] = df[selected_columns].sum(axis=1)

        prefix = "Current-"
        # Use list comprehension to select columns with the specified prefix
        selected_columns = [col for col in df.columns if col.startswith(prefix)]
        # Sum the selected columns along the rows to create the 'Current' column
        df['Current'] = df[selected_columns].sum(axis=1)

        prefix = "Power-"
        # Use list comprehension to select columns with the specified prefix
        selected_columns = [col for col in df.columns if col.startswith(prefix)]
        # Sum the selected columns along the rows to create the 'Current' column
        df['Power'] = df[selected_columns].mean(axis=1)

        prefix = "Frequency-"
        # Use list comprehension to select columns with the specified prefix
        selected_columns = [col for col in df.columns if col.startswith(prefix)]
        # Sum the selected columns along the rows to create the 'Current' column
        df['Frequency'] = df[selected_columns].mean(axis=1)

        prefix = "Powerfactor-"
        # Use list comprehension to select columns with the specified prefix
        selected_columns = [col for col in df.columns if col.startswith(prefix)]
        # Sum the selected columns along the rows to create the 'Current' column
        df['Powerfactor'] = df[selected_columns].mean(axis=1)

        prefix = "Energy-"
        # Use list comprehension to select columns with the specified prefix
        selected_columns = [col for col in df.columns if col.startswith(prefix)]
        # Sum the selected columns along the rows to create the 'Current' column
        df['Energy'] = df[selected_columns].sum(axis=1)

        # Drop columns with null values
        df.dropna(axis=1, inplace=True)

        # --- Average Current ---
        def current_sum():
            current_values = df["Current"]
            if current_values.empty:
                return None
            total = current_values.mean()
            return round(total, 3)

        # --- Average Power ---
        def power_sum():
            power_values = df["Power"]
            if power_values.empty:
                return None
            total = power_values.mean()
            return round(total, 3)

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
            pf_values = df["Powerfactor"]
            if pf_values.empty:
                return None
            total = pf_values.sum()
            avg = total / len(pf_values)
            return round(avg, 3)

        # --- Average Energy ---
        def energy_sum():
            energy_values = df["Energy"]
            if energy_values.empty:
                return None
            total = energy_values.sum()
            return round(total, 3)

        st.markdown("<h1 style='text-align: center;'>Summary</h1>", unsafe_allow_html=True)

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
            total = current_sum()
            card_data = {"title": "Average Current (in A)", "content": total}
            card(card_data["title"], card_data["content"])
        with col2:
            total = power_sum()
            card_data = {"title": "Average Power (in W)", "content": total}
            card(card_data["title"], card_data["content"])
        with col3:
            avg = voltage_average()
            card_data = {"title": "Average Voltage (in V)", "content": avg}
            card(card_data["title"], card_data["content"])

        col4, col5, col6 = st.columns(3)
        with col4:
            avg = freq_average()
            card_data = {"title": "Average Frequency", "content": avg}
            card(card_data["title"], card_data["content"])
        with col5:
            avg = pf_average()
            card_data = {"title": "Average Power Factor", "content": avg}
            card(card_data["title"], card_data["content"])
        with col6:
            total = energy_sum()
            card_data = {"title": "Total Energy (in Kwh)", "content": total}
            card(card_data["title"], card_data["content"])
        st.write("---")

        selected = st.selectbox("Select Attribute:", ["Current", "Voltage", "Power", "Frequency", "Powerfactor"])

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
        name="Current",
        mode="markers+lines", x=df["Date"], y=df["Current"],
        marker_symbol="star"
        ))
        fig.add_trace(go.Scatter(
        name="Voltage",
        mode="markers+lines", x=df["Date"], y=df["Voltage"],
        xperiod="M1",
        xperiodalignment="start"
        ))
        fig.add_trace(go.Scatter(
        name="Power",
        mode="markers+lines", x=df["Date"], y=df["Power"],
        xperiod="M1",
        xperiodalignment="middle"
        ))
        fig.add_trace(go.Bar(
        name="Energy",
        x=df["Date"], y=df["Energy"],
        xperiod="M1",
        xperiodalignment="middle"
        ))
        fig.update_xaxes(showgrid=True, ticklabelmode="period")
        st.plotly_chart(fig, use_container_width=True)
        st.write("---")


        st.title('Custom Tick Labels')
        columns = ["Current", "Voltage", "Power", "Frequency", "Powerfactor"]
        fig = px.line(df, x="Date", y= columns, hover_data={"Date": "|%B %d, %Y"})
        fig.update_xaxes(
        dtick="M1", tickformat="%b\n%Y", ticklabelmode="period")
        st.plotly_chart(fig, use_container_width=True)

        # Display the filtered DataFrame
        st.title("Data")
        st.write("Number of rows :",len(df.index))
        selected_columns = ["Timestamp", "Date", "Current", "Voltage", "Power", "Frequency", "Powerfactor", "Energy"]
        df_selected = df[selected_columns]
        st.write(df_selected, use_container_width=True)
        st.write("Summary")
        st.write(df_selected.describe())

        time.sleep(1)
 