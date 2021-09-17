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
                 index_col='Age Group',
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
df1 = df1[df1['Sex'] == 'All Sexes']


# DROPPING FILTERED COLUMNS
df1.drop(columns=['State', 'Group', 'Sex'], inplace=True)


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

print('COVID AND AGE GROUP DF')
print(df2)
"""
PLOTTING
"""
df2.plot.barh(color='#DB3819')

# PLOT SETTINGS
plt.title("Covid-19 Deaths By Age Group")
plt.xlabel('Deceased')
plt.ylabel('Age Group')

# SAVE FIGURE
plt.savefig(f'{PLOTS_DATA_PATH}/Covid-19_Deaths_By_Age_Group_{str(datetime.now().date())}.png', dpi=1200)
# To Show the Plot
plt.show()


"""
FINAL DATAFRAME: print(df2)

COVID AND AGE GROUP DF
Age Group
All Ages             643858.0
Under 1 year             98.0
0-17 years              412.0
1-4 years                50.0
5-14 years              138.0
15-24 years            1232.0
18-29 years            3043.0
25-34 years            5395.0
30-39 years            8634.0
35-44 years           13567.0
40-49 years           22232.0
45-54 years           35656.0
50-64 years          106674.0
55-64 years           84859.0
65-74 years          144020.0
75-84 years          173655.0
85 years and over    185188.0
Name: COVID-19 Deaths, dtype: float64
"""