"""
__author__ = 'Joseph Fernandez'
Data Source: https://data.cdc.gov/NCHS/Provisional-COVID-19-Deaths-by-Sex-and-Age/9bhg-hcku/data
"""
import pandas as pd
from matplotlib import pyplot as plt
import os
from datetime import datetime


PLOTS_DATA_PATH = '../plots'
if not os.path.exists(PLOTS_DATA_PATH):
    os.mkdir(PLOTS_DATA_PATH)

df = pd.read_csv(filepath_or_buffer=r"../data/Provisional_COVID-19_Deaths_by_Sex_and_Age.csv",
                 low_memory=False,
                 index_col='Sex',
                 parse_dates=True,
                 dayfirst=True)

# Drop Columns
df1 = df.drop(columns=['Footnote', 'Pneumonia, Influenza, or COVID-19 Deaths', 'Pneumonia and COVID-19 Deaths',
                       'Data As Of', 'Start Date', 'Year', 'Month', 'Total Deaths', 'End Date'],
              axis=1)

"""
NOT TO INCLUDE DUPLICATE DATA
"""
# FILTER DATA - BY UNITED STATES
df1 = df1[df1['State'] == 'United States']

# FILTER DATA - GROUP BY MONTH
df1 = df1[df1['Group'] == 'By Total']

# FILTER DATA - BY ALL SEXES
df1 = df1[df1['Age Group'] == 'All Ages']


# DROPPING FILTERED COLUMNS
df1.drop(columns=['State', 'Group', 'Age Group'], inplace=True)


# NORMALIZING DATA/CLEANING DATA

# GETTING COLUMNS
all_columns = df1.columns
print(f'\n***All Columns: {all_columns}***\n')

"""
REMOVING COMMAS 
"""


# NOT USING THIS FUNCTION
def replace_commas(x):
    # lambda x: x.str.replace(',', '').astype(float) -> Replaces this function
    return x.str.replace(',', '').astype(float)


print(df1)

"""
APPLY CONVERSION TO NUMERIC - TO ALL COLUMNS
"""
# df1['COVID-19 Deaths'] = pd.to_numeric(df1['COVID-19 Deaths'], errors='coerce') # DON"T USE 'coerce' - fills with NA
df1[all_columns] = df1[all_columns].apply(pd.to_numeric, errors='ignore')

# FILLING NOT A NUMBER & NOT AVAILABLE WITH ZERO
df1 = df1.fillna(0)


print(df1)

df2 = df1['COVID-19 Deaths']

print('COVID AND GENDER DATA FRAME')
print(df2)
"""
PLOTTING
"""
df2.plot.bar(color='green')

# PLOT SETTINGS
plt.title("Covid-19 Deaths By Gender")
plt.xlabel('Gender')
plt.ylabel('Deceased')

# SAVE FIGURE
plt.savefig(f'{PLOTS_DATA_PATH}/Covid-19_Deaths_By_Gender_{str(datetime.now().date())}.png', dpi=1200)
# To Show the Plot
plt.show()


"""
FINAL DATAFRAME: print(df2)

COVID AND GENDER DATA FRAME
Sex
All Sexes    643858.0
Male         353805.0
Female       290053.0
"""