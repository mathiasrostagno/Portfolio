import streamlit as st
import pandas as pd
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt

end_date = dt.date(2022,9,11)
start_date = dt.date(2020,1,1)

def inputs(data):
    st.sidebar.header('Graphs')
    pays = st.sidebar.multiselect(
        "Pays/Region", list(pd.unique(data['location'])
                         ))
    start = st.sidebar.date_input('Date de départ', start_date)
    end = st.sidebar.date_input('Date de fin', end_date)
    casmillion = st.sidebar.button('Cases per million')
    reproduction = st.sidebar.button('Reproduction rate')
    vaccination = st.sidebar.button('Vaccination')
    return pays, start, end, casmillion, reproduction, vaccination

@st.cache
def get_data():
    data = pd.read_csv(r'C:\Users\mathi\PycharmProjects\pythonProject2\owid-covid-data.csv')
    data['date'] = pd.to_datetime(data['date']).dt.date
    return data

def main():
    data = get_data()
    pays, start, end, casmillion, reproduction, vaccination = inputs(data)
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




if __name__ == '__main__' :
    main()