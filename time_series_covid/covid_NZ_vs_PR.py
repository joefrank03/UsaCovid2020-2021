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
"""New Zealand"""
df_nz = df[df['Country/Region'] == 'New Zealand']
df_nz = df_nz.rename(columns={'deaths': 'NewZealand'})
df_nz = df_nz.drop('Country/Region', axis=1)
df_nz = df_nz.set_index('date')

"""Panama"""
df_p = df[df['Country/Region'] == 'Panama']
df_p = df_p.rename(columns={'deaths': 'Panama'})
df_p = df_p.drop('Country/Region', axis=1)
df_p = df_p.set_index('date')


df_nz = df_nz[df_nz['NewZealand'] != 0]
df_p = df_p[df_p['Panama'] != 0]

df_plot = pd.concat([df_nz, df_p])  # Can Add More Countries


print(df_nz)


print(df_p)


df_plot.plot(kind='line', style="*")
plt.title('New Zealand vs Panama Covid-19 Deaths')
plt.xlabel('Date')
plt.ylabel('Deceased')
plt.show()
