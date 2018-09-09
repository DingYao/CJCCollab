# coding: utf-8

# Import Libraries
import sys
import os
import pandas as pd
import numpy as np
import re

def harmonize_case_data(original_filepath, mode, case_type_dic_filepath):
    
    case_type_dic = pd.read_csv(case_type_dic_filepath)
    if re.search(r'xlsx', original_filepath):
        output_file_path = original_filepath[:-5] + '_harmonized.csv'
    else:
        output_file_path = original_filepath[:-4] + '_harmonized.csv'
    
    if mode.lower() == 'lspbs':
        # Load data
        case_lspbs = pd.read_excel(original_filepath)

        # Rename LSPBS Columns
        case_lspbs.rename(columns={'CASE TYPE':'CASE_TYPE_LSPBS',
                                   'RELATIONSHIP OF ADVERSE PARTY':'RELATIONSHIP_OF_ADVERSE_PARTY',
                                   'CASE SYNOPSIS':'CASE_SYNOPSIS',
                                   'ADVICE SOUGHT':'ADVICE_SOUGHT'}, inplace=True)

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
        case_lspbs_harmonize = case_lspbs.merge(case_type_dic_filter.rename(columns={'LSPBS':'CASE_TYPE_LSPBS', 
                                                                                     'CJC':'CASE_TYPE_CJC', 
                                                                                     'Case Type':'CASE_TYPE_GROUP_CJC'}),
                                                on='CASE_TYPE_LSPBS', how='left')


        # Remove the newlines in the case descriptions for easier data exploration and processing
        def replace_newline(x):

            if type(x) == str:
                return x.replace('\n', ' ')
            return x

        case_lspbs_harmonize['CASE_SYNOPSIS'] = case_lspbs_harmonize['CASE_SYNOPSIS'].apply(replace_newline)
        case_lspbs_harmonize['ADVICE_SOUGHT'] = case_lspbs_harmonize['ADVICE_SOUGHT'].apply(replace_newline)
        
        # Output file to data/original folder
        case_lspbs_harmonize.to_csv(output_file_path, header=True, index=False)
        
        return None
    
    elif mode.lower() == 'cjc':
        # Load data
        case_cjc = pd.read_excel(original_filepath)

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
        case_cjc_harmonize = case_cjc.merge(case_type_dic_filter.rename(columns={'LSPBS':'CASE_TYPE_LSPBS', 
                                                                                 'CJC':'CASE_TYPE_CJC', 
                                                                                 'Case Type':'CASE_TYPE_GROUP_CJC'}),
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
        case_cjc_harmonize.to_csv(output_file_path, header=True, index=False)
        return None
    
    else:
        return None
    
if __name__ == '__main__':
    original_filepath = sys.argv[1]
    mode = sys.argv[2]
    case_type_dic_filepath = sys.argv[3]
    
    harmonize_case_data(original_filepath, mode, case_type_dic_filepath)
        
