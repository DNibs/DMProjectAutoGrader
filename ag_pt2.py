"""
Autograder for Submission 2 of the CY305 DM Project
This reads the prediction excel files and determines the True Pos and False Pos rates
For regression models, it calculates the RMSE
It saves the results in an excel file
"""

import pandas as pd
import glob
import os
import re
import datetime

submission_fld = 'c:/Users/david.niblick/OneDrive - West Point/CY305/grades/DM_Project/submission_pt2/'
labels_class = ['firstRound', 'secondRound', 'sweetSixteen', 'eliteEight', 'finalFour', 'nationalChampGame',
           'champion']
labels_regression = ['tourneySuccessFactor']
out_fn = 'results_pt2.txt'
os.chdir(submission_fld)
out_file = open(out_fn, 'w')


def get_team_model_names(fn):
    team_model_string = re.findall(r'(?<=_)\w+', fn)
    team = team_model_string[0]
    model_string = re.findall(r'\w+_', team_model_string[1])
    model = model_string[0][:-1]
    return '{} {}'.format(team, model)


def get_tp_fp_rmse(fn):
    try:
        df = pd.read_excel(fn)
    except:
        out_file.write('file error')
        return

    num_labels = 0
    for column in df.head():
        if column in labels_class:
            # do classification test
            num_labels += 1
            print('class')
        elif column in labels_regression:
            # do regression test
            num_labels += 1
            print('regression')

    if num_labels < 1:
        out_file.write('Incorrect label')
    if num_labels > 1:
        out_file.write('leakage')

    return


def get_class_perf(attribute_name, dataframe):
    num_instances = len(dataframe)


# file name format: 'teamName_modelType_Label.xlsx'
for file in glob.glob('**/*.xlsx'):
    team_model = get_team_model_names(file)
    out_file.write(team_model + '\t')
    get_tp_fp_rmse(file)
    out_file.write('\n')
out_file.close()


