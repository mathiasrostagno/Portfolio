import streamlit as st
import pandas as pd
import datetime as dt
from datetime import date, timedelta
import folium
import numpy as np
import pydeck as pdk

end_date = date.today() - timedelta(days=1)
start_date = dt.date(2020,1,1)


def inputs():
    st.sidebar.header('Maps')
    RAW = st.sidebar.checkbox('Display RAW Data')
    choice = st.sidebar.radio(
        "What to display ?", ('Total cases', 'Total deaths', 'Total fully vaccinated'))

    date = st.sidebar.slider('Date', min_value=start_date, max_value=end_date)
    #casmillion = st.sidebar.button('Cases per million')
    #reproduction = st.sidebar.button('Reproduction rate')
    #vaccination = st.sidebar.button('Vaccination')
    return choice, date, RAW

@st.cache
def get_data():
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    data = pd.read_csv(url)
    data['date'] = pd.to_datetime(data['date']).dt.date
    loc = pd.read_csv('data/world_country_and_usa_states_latitude_and_longitude_values.csv',
                      usecols=('country_code','latitude','longitude','country'))
    return data, loc




data, loc = get_data()
choice, date, RAW = inputs()

merged_data = data.merge(loc, how='inner', left_on='location', right_on='country')
dateselec = (merged_data['date'] == date)
selection = merged_data.loc[dateselec].fillna(0).drop(columns=['tests_units'])
selection['total_deaths_radius'] = selection['total_deaths']*2
selection['total_cases_radius'] = selection['total_cases']/15
selection['people_fully_vaccinated_per_hundred_radius'] = selection['people_fully_vaccinated_per_hundred'] *6000

if RAW:
    st.write(merged_data)

if choice == 'Total deaths':


    layer = pdk.Layer(
                'ScatterplotLayer',
                data=selection[['longitude', 'latitude', 'total_deaths_radius']],
                get_position=['longitude', 'latitude'],
                get_color='[200, 30, 0, 160]',
                get_radius='total_deaths_radius',
                get_line_color=[0, 0, 255],
                )
    view_state = pdk.ViewState(latitude=45,
                               longitude=10,
                               zoom=3,
                               pitch=35)
    st.pydeck_chart(pdk.Deck(
        initial_view_state=view_state,
        layers=[layer],
    ))


if choice == 'Total cases':

    layer = pdk.Layer(
        'ScatterplotLayer',
        data=selection[['longitude', 'latitude', 'total_cases_radius']],
        get_position=['longitude', 'latitude'],
        get_color='[200, 30, 0, 160]',
        get_radius='total_cases_radius',
        get_line_color=[0, 0, 255],
    )
    view_state = pdk.ViewState(latitude=45,
                               longitude=10,
                               zoom=3,
                               pitch=35)
    st.pydeck_chart(pdk.Deck(
        initial_view_state=view_state,
        layers=[layer],
    ))

if choice == 'Total fully vaccinated':
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=selection[['longitude', 'latitude', 'people_fully_vaccinated_per_hundred_radius']],
        get_position=['longitude', 'latitude'],
        get_color='[200, 30, 0, 160]',
        get_radius='people_fully_vaccinated_per_hundred_radius',
        get_line_color=[0, 0, 255],
    )
    view_state = pdk.ViewState(latitude=45,
                               longitude=10,
                               zoom=3,
                               pitch=35)
    st.pydeck_chart(pdk.Deck(
        initial_view_state=view_state,
        layers=[layer],
    ))


st.write(selection)

