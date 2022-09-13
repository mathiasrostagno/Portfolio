import streamlit as st
import pandas as pd
import datetime as dt
import folium
import numpy as np
import pydeck as pdk

end_date = dt.date(2022,9,11)
start_date = dt.date(2020,1,1)


def inputs(data):
    st.sidebar.header('Maps')
    choice = st.sidebar.radio(
        "What to display ?", ('Total cases', 'Total deaths', 'Total fully vaccinated'))

    date = st.sidebar.slider('Date', min_value=start_date, max_value=end_date)
    #casmillion = st.sidebar.button('Cases per million')
    #reproduction = st.sidebar.button('Reproduction rate')
    #vaccination = st.sidebar.button('Vaccination')
    return choice, date

@st.cache
def get_data():
    data = pd.read_csv(r'C:\Users\mathi\PycharmProjects\pythonProject2\owid-covid-data.csv')
    data['date'] = pd.to_datetime(data['date']).dt.date
    loc = pd.read_csv(r'C:\Users\mathi\PycharmProjects\pythonProject2\world_country_and_usa_states_latitude_and_longitude_values.csv',
                      usecols=('country_code','latitude','longitude','country'))
    return data, loc


def main():

    data, loc = get_data()
    choice, date = inputs(data)

    merged_data = data.merge(loc, how='inner', left_on='location', right_on='country')
    dateselec = (merged_data['date'] == date)
    selection = merged_data.loc[dateselec].fillna(0).drop(columns=['tests_units'])


    if choice == 'Total deaths':


        layer = pdk.Layer(
                    'ScatterplotLayer',
                    data=selection[['longitude', 'latitude', 'total_deaths']],
                    get_position=['longitude', 'latitude'],
                    get_color='[200, 30, 0, 160]',
                    get_radius='total_deaths',
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
            data=selection[['longitude', 'latitude', 'total_cases']],
            get_position=['longitude', 'latitude'],
            get_color='[200, 30, 0, 160]',
            get_radius='total_cases',
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
            data=selection[['longitude', 'latitude', 'people_fully_vaccinated_per_hundred']],
            get_position=['longitude', 'latitude'],
            get_color='[200, 30, 0, 160]',
            get_radius='people_fully_vaccinated_per_hundred'*500,
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

if __name__ == '__main__' :
    main()