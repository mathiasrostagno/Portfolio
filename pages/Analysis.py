import streamlit as st
import pandas as pd
import datetime as dt
import plotly.express as px

end_date = dt.date(2022,9,11)
start_date = dt.date(2020,1,1)

@st.cache
def get_data():
    data = pd.read_csv('owid-covid-data.csv')
    data['date'] = pd.to_datetime(data['date']).dt.date

    return data

def inputs(data):
    st.sidebar.header('Analysis')
    groupby_column = st.selectbox(
        'What do you want to analyse ?',
        ('location', 'continent')
    )

    return groupby_column

def main():
    data = get_data()
    groupby_column = inputs(data)
    st.dataframe(data)

    output_columns = ['total_deaths_per_million', 'people_fully_vaccinated_per_hundred']
    data_grouped = data.groupby(by=[groupby_column], as_index=False)[output_columns].mean()
    data_grouped_sorted = data_grouped.sort_values('total_deaths_per_million', ascending=False)


    fig = px.bar(
        data_grouped_sorted.head(10),
        x=groupby_column,
        y='total_deaths_per_million',
        color='people_fully_vaccinated_per_hundred',
        color_continuous_scale=['red', 'yellow', 'green'],
        template='plotly_white',
        title=f'<b>Total death per million and population density by {groupby_column} </b>'
    )
    st.plotly_chart(fig)

if __name__ == '__main__' :
    main()