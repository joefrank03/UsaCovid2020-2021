"""
__author__ = 'Joseph Fernandez'
Data Source: https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data
"""
import pandas as pd
from matplotlib import pyplot as plt


CONFIRMED_URL = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/' \
                r'csse_covid_19_time_series/time_series_covid19_deaths_global.csv'

wwd = pd.read_csv(CONFIRMED_URL)  # From URL
print(wwd.head())
wwd = wwd.drop(['Lat', 'Long'], axis=1)


wwd = wwd.melt(id_vars=['Province/State', 'Country/Region'],
               value_name='deaths',
               var_name='date').astype({'date': 'datetime64[ns]', 'deaths': 'float'},
                                       errors='ignore')  # Data Types of "date" and "confirmed"
print(wwd)

for c in wwd['Country/Region']:
    print(c)
df = wwd

# Dropping
df = df.drop('Province/State', axis=1)


def get_country_data(country, data_frame=df):
    df_c = data_frame[data_frame['Country/Region'] == country]
    df_c = df_c.rename(columns={'deaths': country})
    df_c = df_c.drop('Country/Region', axis=1)
    df_c = df_c.set_index('date')
    return df_c


# Getting Country Specific Data
"""US"""
df_us = df[df['Country/Region'] == 'US']
df_us = df_us.rename(columns={'deaths': 'US'})
df_us = df_us.drop('Country/Region', axis=1)
df_us = df_us.set_index('date')

"""Brazil"""
df_brazil = df[df['Country/Region'] == 'Brazil']
df_brazil = df_brazil.rename(columns={'deaths': 'Brazil'})
df_brazil = df_brazil.drop('Country/Region', axis=1)
df_brazil = df_brazil.set_index('date')

"""Mexico"""
df_mexico = df[df['Country/Region'] == 'Mexico']
df_mexico = df_mexico.rename(columns={'deaths': 'Mexico'})
df_mexico = df_mexico.drop('Country/Region', axis=1)
df_mexico = df_mexico.set_index('date')

df_us = df_us[df_us['US'] != 0]
df_brazil = df_brazil[df_brazil['Brazil'] != 0]
df_mexico = df_mexico[df_mexico['Mexico'] != 0]

df_plot = pd.concat([df_us, df_mexico, df_brazil])  # Can Add More Countries


print(df_us)


print(df_brazil)

print(df_mexico)


df_plot.plot(kind='line', style="+")

plt.title('US vs Brazil vs Mexico - Covid-19 Deaths')
plt.xlabel('Date')
plt.ylabel('Deceased')
plt.show()
