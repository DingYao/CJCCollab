# coding: utf-8

# Import Libraries
import os
import pandas as pd
import numpy as np
import re


# Define path to data
path2data = os.path.join('..', 'original')

# Load data
case_lspbs = pd.read_excel(os.path.join(path2data, 'lspbs_cases2016_sample.xlsx'))
case_type_dic = pd.read_csv(os.path.join(path2data, 'case_type_harmonization.csv'))


# Rename LSPBS Columns
case_lspbs.rename({'CASE TYPE':'CASE_TYPE_LSPBS',
                  'RELATIONSHIP OF ADVERSE PARTY':'RELATIONSHIP_OF_ADVERSE_PARTY',
                  'CASE SYNOPSIS':'CASE_SYNOPSIS',
                  'ADVICE SOUGHT':'ADVICE_SOUGHT'}, axis='columns', inplace=True)

# Correct LSPBS Case Type
def clean_lspbs_casetype(x):

    if type(x) == str:
        return re.sub(r'2$', '', x)
    return x

case_lspbs['CASE_TYPE_LSPBS'] = case_lspbs['CASE_TYPE_LSPBS'].apply(clean_lspbs_casetype)


# Obtain only many-to-one maps from LSPBS to CJC Case Types
case_type_dic_filter = case_type_dic[['LSPBS', 'CJC']].groupby('LSPBS', as_index=False).count()
case_type_dic_filter = case_type_dic_filter.loc[case_type_dic_filter['CJC'] <= 1, ['LSPBS']]
case_type_dic_filter = case_type_dic_filter.merge(case_type_dic, on='LSPBS')


# Harmonize case types
case_lspbs_harmonize = case_lspbs.merge(case_type_dic_filter.rename({'LSPBS':'CASE_TYPE_LSPBS', 'CJC':'CASE_TYPE_CJC', 'Case Type':'CASE_TYPE_GROUP_CJC'}, axis='columns'),
                                        on='CASE_TYPE_LSPBS', how='left')


# Remove the newlines in the case descriptions for easier data exploration and processing
def replace_newline(x):

    if type(x) == str:
        return x.replace('\n', ' ')
    return x

case_lspbs_harmonize['CASE_SYNOPSIS'] = case_lspbs_harmonize['CASE_SYNOPSIS'].apply(replace_newline)
case_lspbs_harmonize['ADVICE_SOUGHT'] = case_lspbs_harmonize['ADVICE_SOUGHT'].apply(replace_newline)

# Output file to data/original folder
case_lspbs_harmonize.to_csv(os.path.join(path2data, 'lspbs_sample_2016_harmonized.csv'), header=True, index=False)

