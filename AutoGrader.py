"""
This file autogrades the CY305 Datamining Project based on NCAAAM Tournament
"""

import pandas as pd

excel_fn = 'NCAAMTraining.xlsx'
out_fn = 'out.xlsx'
df = pd.read_excel(excel_fn)

# Determine label and leakage
attributes = list(df)
leakage = ['playIn', 'firstRound', 'secondRound', 'sweetSixteen', 'eliteEight',
           'finalFour', 'nationalChampGame', 'champion', 'tourneySuccessFactor']
num_leakage = set(attributes).intersection(leakage)
if num_leakage.__len__() < 1:
    print('No vald label!')
else:
    print('At least one label selected')
if num_leakage.__len__() > 1:
    print('Leakage occured!')
else:
    print('No leakage')

# Test for missing values
if df.isnull().values.any():
    print('Missing values!')
else:
    print('All values are filled')


