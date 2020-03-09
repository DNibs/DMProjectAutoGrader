"""
This file autogrades the CY305 Datamining Project based on NCAAAM Tournament
"""

import pandas as pd
import glob
import os
import re

submission_fld = 'c:/Users/david.niblick/OneDrive - West Point/CY305/grades/DM_Project/submission_pt1/'
leakage = ['playIn', 'firstRound', 'secondRound', 'sweetSixteen', 'eliteEight', 'finalFour', 'nationalChampGame',
           'champion', 'tourneySuccessFactor']
out_fn = 'grade_results.txt'

os.chdir(submission_fld)
out_file = open(out_fn, 'w')

for file in glob.glob('NCAAMTraining*.xlsx'):
    print(file)
    out_file.write('{},'.format(file))
    cdt_name = re.findall('clean_(\w+).xlsx', file)
    print(cdt_name[0])
    out_file.write('{}\n'.format(cdt_name[0]))
    df = pd.read_excel(file)
    attributes = list(df)
    num_leakage = set(attributes).intersection(leakage)

    # Determine label and leakage
    if num_leakage.__len__() < 1:
        print('No vald label!')
        out_file.write('Label, 0')
    else:
        print('Label: 10')
        out_file.write('Label, 10\n')
    if num_leakage.__len__() > 1:
        print('Leakage, 0')
        out_file.write('Leakage, 0\n')
    else:
        print('No leakage')
        out_file.write('Leakage, 10\n')

    # Test for missing values
    if df.isnull().values.any():
        print('Missing values!')
        out_file.write('Empty, 0\n')
    else:
        print('All values are filled')
        out_file.write('Empty, 10\n')


out_file.close()
print('test2')


