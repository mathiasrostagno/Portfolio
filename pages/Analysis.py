import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import datetime as dt
import io

plt.style.use('ggplot')
plt.rcParams["figure.figsize"] = (12,7)

def format_time(datetime_str):
    d = dt.datetime.strptime(datetime_str, '%Y-%m-%d')
    return d.date()

@st.cache
def get_data():
    url = "data/owid-covid-data.csv"
    df = pd.read_csv(url, usecols=['location', 'continent', 'date', 'new_cases_smoothed', 'new_cases_smoothed_per_million', 'new_deaths_smoothed', 'new_deaths_smoothed_per_million', 'reproduction_rate'])
    return df

Options = st.sidebar.radio('Choose what part you want to see (if you are non-technical you can jump directly to the Visualization section)',
                             ('Importing and Cleaning Data', 'Manipulations', 'Visualizations')
                          )

st.write("**You can click on 'Display RAW data' on the left column if you want to see it**")
data = get_data()
RAW = st.sidebar.checkbox('Display RAW Data')

if RAW:
    st.write(data)

###IMPORTING AND CLEANING
if Options == 'Importing and Cleaning Data' :
    st.write("**Informations :**")
    buffer = io.StringIO()
    data.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

    st.write("**Describe :**")
    st.write(data.describe())

    st.write("**And shape :**")
    st.write(data.shape)

    #st.write("**So 67 columns is a lot ! We don't need all of these**")
    #st.write("**Let's keep columns who are useful for our future analysis and convert the date column into datetime format**")

    data_filtered = data.dropna(subset=['continent']).reset_index(drop=True)
    data_filtered["date"] = data_filtered["date"].apply(format_time)

    st.write('**Continents appears in the location column too, we should remove the corresponding rows, cause it could distort our future Analysis**', data_filtered)

    buffer = io.StringIO()
    data_filtered.info(buf=buffer)
    p = buffer.getvalue()
    st.text(p)
    st.write(data_filtered)

    data_filtered['percentage'] = data_filtered['new_deaths_smoothed'] / data_filtered['new_cases_smoothed']
    st.write("**It would be useful to create a new column to calculate the percentage of New Deaths / New Cases**", data_filtered)

    data_filtered.fillna(0, inplace=True)
    st.write("**Some cells are NaN, cause values are divided by 0, let's convert all this cells to a value of 0**", data_filtered)


###MANIPULATING
if Options == 'Manipulations':
    ###Because of scope i re-write variables
    data_filtered = data.dropna(subset=['continent']).reset_index(drop=True)
    data_filtered["date"] = data_filtered["date"].apply(format_time)
    data_filtered['percentage'] = data_filtered['new_deaths_smoothed'] / data_filtered['new_cases_smoothed']
    data_filtered.fillna(0, inplace=True)


    st.write("**Let's begin our Analysis showing daily Cases and Deaths for example between 2022-03-15 and 2022-03-17**")
    data_filtered_by_date = data_filtered[(data_filtered['date'] <= format_time('2022-03-17')) & (data_filtered['date'] >= format_time('2022-03-15'))].reset_index(drop=True)
    st.write(data_filtered_by_date)

    grouped_by_date = data_filtered_by_date.groupby("date")
    for date, group in grouped_by_date:
        st.write("==========")
        st.write(date)
        st.write("==========")
        st.write(group[["location", "continent", "new_cases_smoothed", "new_deaths_smoothed"]])



    data_filtered_daily = data_filtered.groupby(['location', 'date']).sum().groupby(level=0).cumsum()[['new_cases_smoothed','new_deaths_smoothed']].swaplevel(0)
    data_filtered_daily = data_filtered_daily.rename(columns={'new_cases_smoothed':'Total_Cases', 'new_deaths_smoothed':'Total_Deaths'})
    data_filtered_daily['Death ratio'] = data_filtered_daily['Total_Deaths'] / data_filtered_daily['Total_Cases']
    data_filtered_daily.fillna(0, inplace=True)

    st.write("**Let's display the total number of daily cases and deaths, and the percentage between them :**", data_filtered_daily)

    data_filtered_day = data_filtered_daily.loc[format_time('2022-01-25')]
    st.write("**We can display the Data for a specific day (2022-01-25) :**", data_filtered_day)

    data_filtered_day_France = data_filtered_daily.loc[format_time('2022-01-25'), 'France']
    st.write("**For a specific day (2022-01-25) and country (France):**", data_filtered_day_France)


    most_recent_date = data['date'].max()
    st.write("**Now let's get the most recent date in the Data :**", most_recent_date)

    data_most_recent = data_filtered_daily.loc[format_time(most_recent_date),:]
    st.write("**Display informations for the most recent date :**", data_most_recent)


    data_most_confirmed_recent_sorted = data_most_recent.sort_values(by="Total_Cases", ascending=False)
    st.write("**Top 10 countries with the most confirmed cases :**", most_recent_date, data_most_confirmed_recent_sorted.head(10))


###VISUALIZATION
if Options == 'Visualizations':
    ###Because of scope i re-write variables
    data_filtered = data.dropna(subset=['continent']).reset_index(drop=True)
    data_filtered["date"] = data_filtered["date"].apply(format_time)
    data_filtered['percentage'] = data_filtered['new_deaths_smoothed'] / data_filtered['new_cases_smoothed']
    data_filtered.fillna(0, inplace=True)
    data_filtered_daily = data_filtered.groupby(['location', 'date']).sum().groupby(level=0).cumsum()[
        ['new_cases_smoothed', 'new_deaths_smoothed']].swaplevel(0)
    data_filtered_daily = data_filtered_daily.rename(
        columns={'new_cases_smoothed': 'Total_Cases', 'new_deaths_smoothed': 'Total_Deaths'})
    data_filtered_daily['Death ratio'] = data_filtered_daily['Total_Deaths'] / data_filtered_daily['Total_Cases']
    data_filtered_daily.fillna(0, inplace=True)
    most_recent_date = data['date'].max()
    data_most_recent = data_filtered_daily.loc[format_time(most_recent_date), :]
    data_most_confirmed_recent_sorted = data_most_recent.sort_values(by="Total_Cases", ascending=False)
    data_most_deaths_recent_sorted = data_most_recent.sort_values(by="Total_Deaths", ascending=False)


    st.write('**You can choose countries below and see what is the ratio between confirmed cases and deaths**')
    pays = st.multiselect(
            "Select countries", list(pd.unique(data_filtered_daily.index.get_level_values('location')))
                         )
    paysselect = data_filtered_daily[pd.DataFrame(data_filtered_daily.index.get_level_values('location').tolist()).isin(pays).any(1).values]


    for country, df_country in paysselect.groupby(level=1):
        dates = list(df_country.index.get_level_values('date'))
        confirmed = list(df_country.Total_Cases)
        deaths = list(df_country.Total_Deaths)
        fig, ax = plt.subplots()
        plt.bar(dates, confirmed, color='lightblue',
            label="Total number of confirmed cases")
        plt.bar(dates, deaths, color='red',
            label="Total number of deaths")
        plt.xlabel("Dates")
        plt.ylabel("Number of people")
        plt.title(country)
        plt.legend()
        st.pyplot(fig)


    def plot_pie(data, column, title):
        labels = list(data.index)
        sizes = list(data[column])
        explode = [0 for n in range(10)]

        with plt.style.context(
                {"axes.prop_cycle": plt.cycler("color",
                                               plt.cm.tab20c.colors)}):
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes,
                    explode=explode,
                    labels=labels,
                    autopct='%1.2f%%',
                    shadow=False,
                    startangle=0)
            ax1.axis('equal')
            plt.legend()
            plt.title(title)

        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        st.pyplot(fig)

    st.write("**Here's the top 10 countries with the most confirmed cases**")

    top10_countries_cases = data_most_confirmed_recent_sorted.head(10)
    plot_pie(top10_countries_cases,
             "Total_Cases",
             "Top 10 Country of most confirmed cases")

    top10_countries_deaths = data_most_deaths_recent_sorted.head(10)
    plot_pie(top10_countries_deaths,
             "Total_Deaths",
             "Top 10 Country of most Deaths")
