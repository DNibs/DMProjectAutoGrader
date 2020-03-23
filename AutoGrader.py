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
    check for school name or year in  the first half (show that it didn't change role, -2.5 to missingVals)
    calc total
export pandas to csv
print job complete, total graded
"""

import pandas as pd
import glob
import os
import re
import datetime

# Global Vars
submission_fld = 'c:/Users/david.niblick/OneDrive - West Point/CY305/grades/DM_Project/submission_pt1/'
leakage = ['firstRound', 'secondRound', 'sweetSixteen', 'eliteEight', 'finalFour', 'nationalChampGame',
           'champion', 'tourneySuccessFactor']
excess_attributes = ['yearTeamID', 'year', 'school']
excess = ['yearTeamID', 'year', 'school']
out_fn = 'grade_results.txt'
os.chdir(submission_fld)
columns = ['cdtName', 'submitFormat', 'label', 'leakage', 'missingVals', 'excessAttr']
out_df = pd.DataFrame(columns=columns)
i = 0


def check_submission_format(cadet_name):
    num_files = 0
    for fn in glob.glob('*'+cadet_name+'.txt'):
        num_files += 1
    for fn in glob.glob('*'+cadet_name+'.doc?'):
        num_files += 1
    if num_files >= 1:
        return True
    else:
        return False


def get_attributes_and_possible_labels(d_f):
    attr = list(d_f)
    rem_labels = set(attr).intersection(leakage)
    return attr, rem_labels


def check_label(attr, rem_labels):
    """ Checks RapidMiner moved potential label to right of attribute list"""
    attr_len = attr.__len__()
    for item in rem_labels:
        idx_position = attr.index(item)
        if (idx_position / attr_len) > 0.5:
            # valid label present
            return True
    return False


def check_excess_attributes(attr):
    global excess_attributes
    count = 0
    remaining_excess = set(attr).intersection(excess_attributes)
    for item in remaining_excess:
        idx = attr.index(item)
        if (idx / attr.__len__()) < 0.5:
            count += 1
    return count


def check_leakage(rem_labels):
    # Determine leakage
    return rem_labels.__len__() - 1


def check_missing_values():
    return df.isnull().values.sum()


num_files = len(glob.glob('NCAAMTraining*.xlsx'))
print(num_files)
for file in glob.glob('*.xlsx'):
    cdt_name = re.findall('lean_(\w+).xlsx', file)
    print('\r {} of {} files ({:.0%}), CDT {}'.format(i, num_files, i/num_files, cdt_name[0]), end='')

    out_df.at[i, 'cdtName'] = cdt_name[0]
    df = pd.read_excel(file)

    if check_submission_format(cdt_name[0]):
        out_df.at[i, 'submitFormat'] = 4
    else:
        out_df.at[i, 'submitFormat'] = 0

    attributes, remaining_labels = get_attributes_and_possible_labels(df)

    num_leakage = check_leakage(remaining_labels)
    if num_leakage > 3:
        out_df.at[i, 'leakage'] = 0
    elif 3 >= num_leakage > 0:
        out_df.at[i, 'leakage'] = 2
    else:
        out_df.at[i, 'leakage'] = 4

    if check_label(attributes, remaining_labels):
        out_df.at[i, 'label'] = 4
    else:
        out_df.at[i, 'label'] = 0

    num_missing_val = check_missing_values()
    if num_missing_val >= 500:
        out_df.at[i, 'missingVals'] = 0
    elif (num_missing_val < 500) and (num_missing_val > 0):
        out_df.at[i, 'missingVals'] = 2
    else:
        out_df.at[i, 'missingVals'] = 4

    num_excess_att= check_excess_attributes(attributes)
    if num_excess_att > 1:
        out_df.at[i, 'excessAttr'] = 0
    elif num_excess_att == 1:
        out_df.at[i, 'excessAttr'] = 2
    else:
        out_df.at[i, 'excessAttr'] = 4

    i += 1

columns.remove('cdtName')
for item in columns:
    out_df[item] = pd.to_numeric(out_df[item])
out_df['total'] = out_df.sum(axis=1)
out_df['percent'] = out_df['total'] / 20.0
out_df['date'] = datetime.date.today()
out_df.to_csv('grades.csv', index=False)
print('')
print(out_df)
