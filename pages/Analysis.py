import streamlit as st
import pandas as pd
import datetime as dt
from datetime import date, timedelta
import plotly.express as px

end_date = date.today() - timedelta(days=1)
start_date = dt.date(2020,1,1)

@st.cache
def get_data():
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    data = pd.read_csv(url)
    data['date'] = pd.to_datetime(data['date']).dt.date

    return data

def inputs(data):
    st.sidebar.header('Analysis')

    groupby_column = st.sidebar.selectbox(
        'Question',
        ('Is Mortality higher for people older than 65 ?', 'Is Mortality higher for people older than 70 ?', 'Do Gross Domestic Product (GDP) per Capita has an influence ?')
            )
    pays = st.sidebar.multiselect(
        "Select countries", list(pd.unique(data['location'])
                                 ))
    generate = st.sidebar.button('Generate Chart !')
    st.sidebar.write('OR')
    top10 = st.sidebar.button('Display top 10')

    return groupby_column, pays, generate, top10


data = get_data()
groupby_column, pays, generate, top10 = inputs(data)
pays.sort()

output_columns = ['location', 'total_deaths_per_million', 'aged_65_older', 'aged_70_older', 'gdp_per_capita']
dateselect = data[data['date'] == end_date]

paysselect = dateselect[pd.DataFrame(dateselect.location.tolist()).isin(pays).any(1).values][output_columns]


#data_grouped = data_today.groupby(by=[pays], as_index=False)[output_columns].mean()
#data_grouped_sorted = data_grouped.sort_values('total_deaths_per_million', ascending=False)

if generate:
    if groupby_column == 'Is Mortality higher for people older than 65 ?':
        fig = px.bar(
             paysselect,
             x=pays,
             y='total_deaths_per_million',
             color='aged_65_older',
             color_continuous_scale=['green', 'yellow', 'red'],
             template='plotly_white',
             title=f'<b> Is Mortality higher for people older than 65 ? </b>',
             labels={'x': 'country', 'total_deaths_per_million': 'Death / Million', 'aged_65_older': 'Population > 65 (%)'}
                  )

        st.plotly_chart(fig)

    elif groupby_column == 'Is Mortality higher for people older than 70 ?':
        fig = px.bar(
            paysselect,
            x=pays,
            y='total_deaths_per_million',
            color='aged_70_older',
            color_continuous_scale=['green', 'yellow', 'red'],
            template='plotly_white',
            title=f'<b> Is Mortality higher for people older than 70 ? </b>',
            labels={'x': 'country', 'total_deaths_per_million': 'Death / Million',
                    'aged_70_older': 'Population > 70 (%)'}
        )

        st.plotly_chart(fig)

    elif groupby_column == 'Do Gross Domestic Product (GDP) per Capita has an influence ?':
        fig = px.bar(
            paysselect,
            x=pays,
            y='total_deaths_per_million',
            color='gdp_per_capita',
            color_continuous_scale=['red', 'yellow', 'green'],
            template='plotly_white',
            title=f'<b> Do Gross Domestic Product (GDP) per Capita has an influence ? </b>',
            labels={'x': 'country', 'total_deaths_per_million': 'Death / Million',
                    'aged_70_older': 'Population > 70 (%)'}
        )

        st.plotly_chart(fig)

    else:
        st.write('oops')

if top10:
    data_grouped_sorted = dateselect.sort_values('total_deaths_per_million', ascending=False).head(10)

    if groupby_column == 'Is Mortality higher for people older than 65 ?':
        fig = px.bar(
             data_grouped_sorted,
             x='location',
             y='total_deaths_per_million',
             color='aged_65_older',
             color_continuous_scale=['green', 'yellow', 'red'],
             template='plotly_white',
             title=f'<b> Is Mortality higher for people older than 65 ? </b>',
             labels={'location': 'country', 'total_deaths_per_million': 'Death / Million', 'aged_65_older': 'Population > 65 (%)'}
                  )

        st.plotly_chart(fig)

    elif groupby_column == 'Is Mortality higher for people older than 70 ?':
        fig = px.bar(
            data_grouped_sorted,
            x='location',
            y='total_deaths_per_million',
            color='aged_70_older',
            color_continuous_scale=['green', 'yellow', 'red'],
            template='plotly_white',
            title=f'<b> Is Mortality higher for people older than 70 ? </b>',
            labels={'location': 'country', 'total_deaths_per_million': 'Death / Million',
                'aged_70_older': 'Population > 70 (%)'}
                )
        st.plotly_chart(fig)

    elif groupby_column == 'Do Gross Domestic Product (GDP) per Capita has an influence ?':
        fig = px.bar(
            data_grouped_sorted,
            x='location',
            y='total_deaths_per_million',
            color='gdp_per_capita',
            color_continuous_scale=['red', 'yellow', 'green'],
            template='plotly_white',
            title=f'<b> Do Gross Domestic Product (GDP) per Capita has an influence ? </b>',
            labels={'location': 'country', 'total_deaths_per_million': 'Death / Million',
                    'aged_70_older': 'Population > 70 (%)'}
        )

        st.plotly_chart(fig)