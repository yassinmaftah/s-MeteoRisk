import streamlit as st
import pandas as pd
from sqlalchemy import text
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gold.create_db import engine

st.set_page_config(page_title="MeteoRisk Dashboard", layout="wide")
st.title("S-MeteoRisk: Meteorological Risk Analysis")

@st.cache_data
def load_data():
    query = """
        SELECT c.name AS city, w.date, w.temp_max, w.precip_max, 
               w.wind_gusts, w.risk_total, w.temp_category, 
               w.precip_category, w.wind_category
        FROM cities c
        JOIN weather_risks w ON c.id = w.city_id
    """
    with engine.connect() as cnx_db:
        return pd.read_sql(text(query), cnx_db)

df = load_data()

st.sidebar.header("Filtres")

cities = df['city'].unique().tolist()
selected_cities = st.sidebar.multiselect("Villes", cities, default=cities)

min_date = df['date'].min()
max_date = df['date'].max()
selected_dates = st.sidebar.date_input("time :", [min_date, max_date])

min_risk = float(df['risk_total'].min())
max_risk = float(df['risk_total'].max())

selected_risk = st.sidebar.slider("Minimum risk level", min_risk, max_risk,min_risk)

if len(selected_dates) == 2:
    start_date, end_date = selected_dates
    all_filters = (
        (df['city'].isin(selected_cities)) & 
        (df['date'] >= start_date) & 
        (df['date'] <= end_date) &
        (df['risk_total'] >= selected_risk)
    )
    filtered_df = df[all_filters]
else:
    filtered_df = df

st.header("Global KPIs")
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Cities count", value=filtered_df['city'].nunique())
col2.metric("Max Temperature", f"{filtered_df['temp_max'].max()} °C")
col3.metric("Max Precipitation", f"{filtered_df['precip_max'].max()} %")
col4.metric("Max Risk", f"{filtered_df['risk_total'].max()}")
st.divider()





st.subheader("Top Temperatures by City")
st.bar_chart(filtered_df.groupby('city')['temp_max'].max())


st.subheader("Top Precipitation by City")
st.bar_chart(filtered_df.groupby('city')['precip_max'].max())


st.subheader("Risk Dispersion by City and Date")
scatter_df = filtered_df.copy()
scatter_df['date_str'] = pd.to_datetime(scatter_df['date']).dt.strftime('%Y-%m-%d')
st.scatter_chart(
    scatter_df,
    x='date_str',
    y='risk_total',
    color='city'
)