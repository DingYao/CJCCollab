# coding: utf-8

# Import Libraries
import os
import pandas as pd


# Define path to data
path2data = os.path.join('..', 'original')

# Load data
case_cjc = pd.read_excel(os.path.join(path2data,'cjc_cases_bankruptcy.xlsx'))
case_type_dic = pd.read_csv(os.path.join(path2data, 'case_type_harmonization.csv'))


# Rename CJC Columns
case_cjc.rename(columns={'Registered On':'REGISTERED_ON',
                  'Case Type':'CASE_TYPE_GROUP_CJC',
                  'Civil':'CIVIL_GROUP_CASE_TYPE_CJC',
                  'Criminal':'CRIMINAL_GROUP_CASE_TYPE_CJC',
                  'Family':'FAMILY_GROUP_CASE_TYPE_CJC',
                  'Detailed information of background facts':'BACKGROUND_INFORMATION',
                  'Legal issues':'LEGAL_ISSUES',
                  'Advice':'ADVICE'}, inplace=True)

def collapse_cjc_subtypes(row):
    if row['CASE_TYPE_GROUP_CJC'] == 'Family' :
        return row['FAMILY_GROUP_CASE_TYPE_CJC']
    if row['CASE_TYPE_GROUP_CJC'] == 'Criminal' :
       return row['CRIMINAL_GROUP_CASE_TYPE_CJC']
    if row['CASE_TYPE_GROUP_CJC'] == 'Civil' :
       return row['CIVIL_GROUP_CASE_TYPE_CJC']
   
case_cjc['CASE_TYPE_CJC'] = case_cjc.apply (lambda row: collapse_cjc_subtypes(row),axis=1)


# Obtain CJC to LSPBS case mapping
case_type_dic_filter = case_type_dic.groupby(['Case Type','CJC'], as_index=False).count()
case_type_dic_filter = case_type_dic_filter.loc[case_type_dic_filter['LSPBS'] <= 1, ['Case Type','CJC']]
case_type_dic_filter = case_type_dic_filter.merge(case_type_dic, on=['Case Type','CJC'])


# Harmonize case types
case_cjc_harmonize = case_cjc.merge(case_type_dic_filter.rename(columns={'LSPBS':'CASE_TYPE_LSPBS', 'CJC':'CASE_TYPE_CJC', 'Case Type':'CASE_TYPE_GROUP_CJC'}),
                                        on=['CASE_TYPE_GROUP_CJC','CASE_TYPE_CJC'], how='left')


# Remove the newlines in the case descriptions for easier data exploration and processing
def replace_newline(x):

    if type(x) == str:
        return x.replace('\n', ' ')
    return x

case_cjc_harmonize['BACKGROUND_INFORMATION'] = case_cjc_harmonize['BACKGROUND_INFORMATION'].apply(replace_newline)
case_cjc_harmonize['LEGAL_ISSUES'] = case_cjc_harmonize['LEGAL_ISSUES'].apply(replace_newline)
case_cjc_harmonize['ADVICE'] = case_cjc_harmonize['ADVICE'].apply(replace_newline)

# Output file to data/original folder
case_cjc_harmonize.to_csv(os.path.join(path2data, 'cjc_cases_20178_sample_20180808_harmonized.csv'), header=True, index=False)

