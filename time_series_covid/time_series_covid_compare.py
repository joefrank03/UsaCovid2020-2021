"""
__author__ = 'Joseph Fernandez'
Data Source: https://data.cdc.gov/NCHS/Provisional-COVID-19-Deaths-by-Sex-and-Age/9bhg-hcku/data
"""
import pandas as pd
from matplotlib import pyplot as plt
import os
from datetime import datetime


PLOTS_DATA_PATH = 'time_series_covid/plots'
if not os.path.exists(PLOTS_DATA_PATH):
    os.mkdir(PLOTS_DATA_PATH)

df = pd.read_csv(filepath_or_buffer=r"time_series_covid/data/Provisional_COVID-19_Deaths_by_Sex_and_Age.csv",
                 low_memory=False,
                 index_col='End Date',
                 parse_dates=True,
                 dayfirst=True)

# Drop Columns
df1 = df.drop(columns=['Footnote', 'Pneumonia, Influenza, or COVID-19 Deaths', 'Pneumonia and COVID-19 Deaths',
                       'Data As Of', 'Start Date', 'Year', 'Month', 'Total Deaths',  'Sex'],
              axis=1)

"""
NOT TO INCLUDE DUPLICATE DATA
"""
# FILTER DATA - BY UNITED STATES
df1 = df1[df1['State'] == 'United States']
# FILTER DATA - GROUP BY MONTH
df1 = df1[df1['Group'] == 'By Month']
# FILTER DATA - BY AGE GROUP
df1 = df1[df1['Age Group'] == 'All Ages']


# DROPPING FILTERED COLUMNS
df1.drop(columns=['State', 'Group', 'Age Group'], inplace=True)

# IF Index Column(index_col) is not set on read_csv
# df1['End Date'] = pd.to_datetime(df1['End Date'])
# df1.set_index('End Date')


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

# REMOVING COMMAS
# df1[all_columns] = df1[all_columns].apply(lambda x: x.str.replace(',', '').astype(float))


"""
APPLY CONVERSION TO NUMERIC - TO ALL COLUMNS
"""
# df1['COVID-19 Deaths'] = pd.to_numeric(df1['COVID-19 Deaths'], errors='coerce') # DON"T USE 'coerce' - fills with NA
df1[all_columns] = df1[all_columns].apply(pd.to_numeric, errors='ignore')

# FILLING NOT A NUMBER & NOT AVAILABLE WITH ZERO
df1 = df1.fillna(0)


print(df1)

# INDEX COLUMN IS ALREADY SET AND IT IS 'End Date' AND IT IS DATE TIME TYPE
"""
GROUPING AND SUMMING THE VALUES BY MONTH AND YEAR
"""
df2 = df1.groupby([lambda x: x.year, lambda x: x.month]).sum()

print(df2)

"""
PLOTTING
"""
df2.plot()

# PLOT SETTINGS
plt.title("Comparison Covid-19 Vs Pneumonia Vs Influenza")
plt.xlabel('Year Month (2020 - 2021)')
plt.ylabel('Deceased')

# SAVE FIGURE
plt.savefig(f'{PLOTS_DATA_PATH}/covid_comparison_{str(datetime.now().date())}.png', dpi=1200)
# To Show the Plot
plt.show()


"""
FINAL DATAFRAME: print(df2)

                   COVID-19 Deaths  Pneumonia Deaths  Influenza Deaths
End Date End Date                                                     
2020     1                    12.0           35818.0            4248.0
         2                    38.0           31474.0            4744.0
         3                 14316.0           44956.0            4874.0
         4                130952.0           92852.0            2476.0
         5                 76596.0           58006.0             252.0
         6                 36008.0           38564.0              80.0
         7                 62222.0           54236.0             100.0
         8                 59762.0           54700.0              86.0
         9                 38276.0           42248.0              56.0
         10                49808.0           48630.0             138.0
         11               106410.0           76550.0             206.0
         12               196098.0          125720.0             312.0
2021     1                209972.0          139908.0             286.0
         2                 96174.0           76042.0             180.0
         3                 45610.0           48308.0             134.0
         4                 36890.0           41666.0              92.0
         5                 29134.0           37392.0              64.0
         6                 15332.0           29304.0              72.0
         7                 18138.0           30244.0              60.0
         8                  7314.0            7398.0               4.0
"""
