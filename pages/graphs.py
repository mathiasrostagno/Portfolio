import streamlit as st
import pandas as pd
import datetime as dt
from datetime import date, timedelta
import seaborn as sns
import matplotlib.pyplot as plt

end_date = date.today() - timedelta(days=1)  #penser à remplacer à today en mettant l'url du csv (datetime.today.date() )
start_date = dt.date(2020,1,1)

def inputs(data):
    st.sidebar.header('Graphs')
    RAW = st.sidebar.checkbox('Display RAW Data')
    pays = st.sidebar.multiselect(
        "Pays/Region", list(pd.unique(data['location'])
                         ))
    start = st.sidebar.date_input('Starting Date', start_date)
    end = st.sidebar.date_input('Final Date', end_date)
    casmillion = st.sidebar.button('Cases per million')
    reproduction = st.sidebar.button('Reproduction rate')
    vaccination = st.sidebar.button('Vaccination')
    return pays, start, end, casmillion, reproduction, vaccination, RAW

@st.cache
def get_data():
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    data = pd.read_csv(url)
    data['date'] = pd.to_datetime(data['date']).dt.date
    return data




data = get_data()
pays, start, end, casmillion, reproduction, vaccination, RAW = inputs(data)

if RAW:
    st.write(data)

if casmillion :

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
