import streamlit as st
import pandas as pd
import datetime as dt
from datetime import date, timedelta

end_date = date.today() - timedelta(days=1)
start_date = dt.date(2020,1,1)

@st.cache
def get_data():
    url = "data/owid-covid-data.csv"
    data = pd.read_csv(url)
    data['date'] = pd.to_datetime(data['date']).dt.date

    return data

def inputs(data):
    st.sidebar.header('Explore')
    RAW = st.sidebar.checkbox('Display RAW Data')
    pays = st.sidebar.multiselect(
        "Select countries", list(pd.unique(data['location'])
                                 ))
    start = st.sidebar.date_input('Starting Date', start_date)
    end = st.sidebar.date_input('Final Date', end_date)
    casmillion = st.sidebar.button('Cases per million')
    reproduction = st.sidebar.button('Reproduction rate')
    vaccination = st.sidebar.button('Vaccination')

    return pays, RAW, start, end, casmillion, reproduction, vaccination

data = get_data()
pays, RAW, start, end, casmillion, reproduction, vaccination = inputs(data)
pays.sort()

output_columns = ['location', 'total_deaths_per_million', 'aged_65_older', 'aged_70_older', 'gdp_per_capita']
dateselect = data[data['date'] == end_date]
paysselect = dateselect[pd.DataFrame(dateselect.location.tolist()).isin(pays).any(1).values][output_columns]

if RAW:
    st.write(data)

if casmillion:

    st.header(f'Cases per million for  : ')
    st.subheader(f', '.join(pays))
    st.write(f'From {start} to {end}')

    paysselec = data[pd.DataFrame(data.location.tolist()).isin(pays).any(1).values]
    dateselec = (paysselec['date'] >= start) & (paysselec['date'] <= end)
    selection = paysselec.loc[dateselec]

    selectionwide = selection.pivot(index='date', columns='location', values='new_cases_per_million')
    st.line_chart(selectionwide, use_container_width=True)

if reproduction :

    st.header(f'Reproduction rate for  : ')
    st.subheader(f', '.join(pays))
    st.write(f'From {start} to {end}')

    paysselec = data[pd.DataFrame(data.location.tolist()).isin(pays).any(1).values]
    dateselec = (paysselec['date'] >= start) & (paysselec['date'] <= end)
    selection = paysselec.loc[dateselec]

    selectionwide = selection.pivot(index='date', columns='location', values='reproduction_rate')
    st.line_chart(selectionwide, use_container_width=True)

if vaccination:
     st.header(f'Vaccination per hundred  : ')
     st.subheader(f', '.join(pays))
     st.write(f'From {start} to {end}')

     paysselec = data[pd.DataFrame(data.location.tolist()).isin(pays).any(1).values]
     dateselec = (paysselec['date'] >= start) & (paysselec['date'] <= end)
     selection = paysselec.loc[dateselec]

     selectionwide = selection.pivot(index='date', columns='location', values='people_vaccinated_per_hundred')
     st.line_chart(selectionwide, use_container_width=True)
