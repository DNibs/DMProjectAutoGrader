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
import numpy as np
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

    for column in df.head():
        label = re.search('prediction\((.*)\)', column)
    print(label.group(1))

    num_leakage = 0
    num_pred_labels = 0
    for column in df.head():
        if column in labels_class:
            out_file.write('{} \t'.format(column))
            for column2 in df.head():
                if 'prediction('+column+')' == column2:
                    # do classification test
                    write_class_perf(column, df)
                    num_pred_labels += 1
            num_leakage += 1
        elif column in labels_regression:
            out_file.write('{} \t'.format(column))
            for column2 in df.head():
                if 'prediction('+column+')' == column2:
                    # do regression test
                    write_regression_perf(column, df)
                    num_pred_labels += 1
            num_leakage += 1

    if (num_leakage == 0) or (num_pred_labels == 0):
        out_file.write('Incorrect label  \t')
    if num_leakage > 1:
        out_file.write('leakage  \t')

    return


def write_class_perf(attribute_name, dataframe):
    num_instances = len(dataframe.index)
    tp = 0
    fp = 0
    pred_attribute = 'prediction(' + attribute_name + ')'
    for i in range(0, num_instances):
        if (dataframe.at[i, attribute_name] == True) and (dataframe.at[i, pred_attribute] == True):
            tp += 1
        if (dataframe.at[i, attribute_name] == False) and (dataframe.at[i, pred_attribute] == True):
            fp += 1
    out_file.write('tp: {} \t'.format(tp))
    out_file.write('fp: {} \t'.format(fp))


def write_regression_perf(attribute_name, dataframe):
    num_instances = len(dataframe.index)
    pred_attribute = 'prediction(' + attribute_name + ')'
    residual = 0
    for i in range(0, num_instances):
        residual += np.square(dataframe.at[i, attribute_name] - dataframe.at[i, pred_attribute])
    mse = residual / num_instances
    rmse = np.sqrt(mse)
    out_file.write('RMSE: {} \t'.format(rmse))


# file name format: 'teamName_modelType_Label.xlsx'
num_files = len(glob.glob('**/*.xlsx'))
i = 0
for file in glob.glob('**/*.xlsx'):
    print('\r{} / {} files    '.format(i, num_files), end='')
    team_model = get_team_model_names(file)
    out_file.write(team_model + '\t')
    get_tp_fp_rmse(file)
    out_file.write('\n')
    i += 1
out_file.close()

