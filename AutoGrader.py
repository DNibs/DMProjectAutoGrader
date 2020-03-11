"""
This file autogrades the CY305 Datamining Project based on NCAAAM Tournament

write grades to DF
cdtName - submitFormat (0-5) - label (0-5) - leakage (0-5) - missingVals (0-5) - total (0-20)
init variables (directories, label/leakage list,
for EACH_FILE_.XLSX:
    get indexed attributes list
    check for txt or doc file
    check label - item from label/leakage in attributes to back 3rd
    check leakage - more than one item from label/leakage in attributes anywhere
    check missing vals - less than 100, -2.5, otherwise -5
    check for school name or year in  the first third (show that it didn't change role, -2.5 to missingVals)
    calc total
export pandas to csv
print job complete, total graded
"""

import pandas as pd
import glob
import os
import re

submission_fld = 'c:/Users/david.niblick/OneDrive - West Point/CY305/grades/DM_Project/submission_pt1/'
leakage = ['playIn', 'firstRound', 'secondRound', 'sweetSixteen', 'eliteEight', 'finalFour', 'nationalChampGame',
           'champion', 'tourneySuccessFactor']
excess = ['yearTeamID', 'year', 'school']
out_fn = 'grade_results.txt'

os.chdir(submission_fld)
out_file = open(out_fn, 'w')
# create empty dataframe, columns above, might need to get # xlsx files first to determine max index
out_df = pd.DataFrame(columns=['cdtName', 'submitFormat', 'label', 'leakage', 'missingVals', 'total'])

for file in glob.glob('NCAAMTraining*.xlsx'):
    print(file)
    out_file.write('{},'.format(file))
    cdt_name = re.findall('clean_(\w+).xlsx', file)
    print(cdt_name[0])
    out_file.write('{}\n'.format(cdt_name[0]))
    df = pd.read_excel(file)
    attributes = list(df)
    remaining_labels = set(attributes).intersection(leakage)

    # Determine leakage
    if remaining_labels.__len__() > 1:
        print('Leakage, 0')
        out_file.write('Leakage, 0\n')
    else:
        print('No leakage')
        out_file.write('Leakage, 10\n')

    # Determine labels (rapidminer moves labels to far right, so attribute index should be greater than 16)
    # (Rapidminer moves attributes with replaced values to left)
    # replaced values - untouched attributes - label - special attributes
    num_actual_labels = 0
    for attr in remaining_labels:
        if attributes.index(attr) > 16:
            num_actual_labels += 1
    if num_actual_labels == 1:
        print('Label, 10')
        out_file.write('Label, 10\n')
    else:
        print('Label, 0')
        out_file.write('Label, 0\n')

    # Test for missing values
    if df.isnull().values.any():
        print('Missing values!')
        out_file.write('Empty, 0\n')
    else:
        print('All values are filled')
        out_file.write('Empty, 10\n')

    # Test for pace (attribute with fewest values - should be removed as part of data cleaning)
    # if 'pace' in attributes:


# 2010 last year for pace, 3491 all, 541 tourney
# tourney invite = 1508



out_file.close()
print('test2')


