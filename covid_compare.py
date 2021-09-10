"""
__author__ = ''
Data Source: https://data.cdc.gov/NCHS/Provisional-COVID-19-Deaths-by-Sex-and-Age/9bhg-hcku/data
"""
import pandas as pd
import seaborn as sns
from matplotlib import dates
from matplotlib import pyplot as plt

df = pd.read_csv(r"C:\Users\ferna\Documents\Final Project\Provisional_COVID-19_Deaths_by_Sex_and_Age.csv",
                 low_memory=False,
                 index_col='End Date',
                 parse_dates=True,
                 dayfirst=True)

# Drop Columns
df1 = df.drop(columns=['Group', 'Footnote', 'Pneumonia, Influenza, or COVID-19 Deaths', 'Pneumonia and COVID-19 Deaths',
                       'Data As Of', 'Start Date', 'Year', 'Month', 'Total Deaths', 'State', 'Sex', 'Age Group'],
              axis=1)

# Cast Types
df1['Influenza Deaths'] = df1['Influenza Deaths'].str.replace(',', '').astype(float)

df1['Pneumonia Deaths'] = df1['Pneumonia Deaths'].str.replace(',', '').astype(float)

df1['COVID-19 Deaths'] = df1['COVID-19 Deaths'].str.replace(',', '').astype(float)

# Fill Na
# TODO: Handle FillNa Better
#df1['Influenza Deaths'].fillna(0, inplace=True)

#df1['Pneumonia Deaths'].fillna(0, inplace=True)

#df1['COVID-19 Deaths'].fillna(0, inplace=True)
df1.fillna(value=pd.NaT)

"""SEABORN Plotting"""
sns.set_theme(style="ticks")

print('Plotting')
sns.lineplot(data=df1)
sns.set(style='dark')

dtFmt = dates.DateFormatter('%B_%Y')  # define the formatting
plt.gca().xaxis.set_major_formatter(dtFmt)  # apply the format to the desired axis
plt.ylabel('Cases')
plt.gca().yaxis.set_visible(False)

plt.xlabel('Month_Year')

plt.legend(loc='best')
plt.xticks(rotation=45)

plt.title("2020 - 2021 Comparison Covid-19 Vs Pneumonia Vs Influenza")
plt.tight_layout()

# SAVE FIGURE
plt.savefig('covid_compare.jpg', dpi=600)

plt.show()
