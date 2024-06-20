# -*- coding: utf-8 -*-
"""
Created on Mon Thu 20 07:57:03 2024

@author: KeremAi
"""
# %%
import pandas as pd
import os
from pathlib import Path
import re

# %%
def clean_lipid(indata: pd.DataFrame) -> pd.DataFrame:

    # Group by the specified columns and count occurrences
    value_value = indata.groupby(
        ['VALUE', 'OBSERVATIONCODE', 'ORDERSID', 'TESTREQUESTPOSITIONINORDER', 'OBSERVATIONPOSINTESTREQUEST']
    ).size().reset_index(name='CN')
    
    # Rename columns to match the expected output format
    #value_value.rename(columns={'VALUE': 'VALUE_ENCODED'}, inplace=True)
    # Create a new column 'upvalue' with the uppercase version of 'value'
    value_value['UPVALUE'] = value_value['VALUE'].str.upper()
    
    obs_sup = value_value.rename(columns={'VALUE_ENCODED': 'VALUE'})
# Define the list of substrings to check for exclusion
    exclude_list = [
    'NOT PERFORMED', 'DISREGARD', 'CORRECTED ON', 'NOT VALID', 
    'NOT AVAILABLE', 'UNABLE', 'UNSUITABLE', 'INVALID', 
    'NOT BE CALCULATED', 'NOT ACCURATE', 'UNRELIABLE', 
    'NOT REPORTABLE', 'IS DECREASED', 'NOT BEEN SIGNED', 
    'NOT BEEN PERFORMED', 'INCORRECTLY', 'CANCELLED', 'DELETE', 
    'MODIFIED RESULT', 'GUIDELINE', 'N/A', 'ERROR', 'REJECTION', 
    'MISLABELLED', 'DUPLICATE', 'DEPRESSED', 'INCORRECT', 'FRS*', 
    'AMENDED', 'UNLABELLED', 'GROSSLY LIPEMIC', 'NO SAMPLE', 
    'NOT CALCULATED', "CAN'T BE CALCULATED", 'NOT ORDERED', 
    'INACCURATE', 'NOT PROCESSED'
]

    # Function to check if any exclude substring is in upvalue
    def check_exclusion(upvalue):
        for exclude in exclude_list:
            if exclude in upvalue:
                return True
        return False
    
    
    # Filter the DataFrame based on the conditions
    obs_sup = value_value[
            value_value['UPVALUE'].str.contains(r'\d') & 
            ~value_value['UPVALUE'].apply(check_exclusion)
            ]    
 
        
# Copy the DataFrame to 'clean'
    clean = obs_sup.copy()
    
    # Define variables (although in Pandas we don't need to predefine lengths)
    clean['VALUE_DERIVED'] = pd.NA  # Initialize with missing values
    clean['SUBVALUE1'] = ''
    clean['VALUETEMP1'] = ''
    clean['VALUETEMP2'] = ''
    clean['VALUETEMP3'] = ''
    clean['VALUETEMP4'] = ''
    clean['VALUETEMP5'] = ''
    clean['VALUETEMP6'] = ''
    
    # Function to check if a string contains only numbers and decimals
    def is_valid_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False    
    
    # Process each row to fill the new columns based on the conditions
    for index, row in clean.iterrows():
        upvalue = str(row['VALUE']).strip()  # Assuming 'VALUE' is the column name
        
        # Condition 1: If value has just numbers and decimals
        if is_valid_number(upvalue.replace('..', '.')):
            valuetemp1 = upvalue.replace('..', '.')
            clean.at[index, 'VALUETEMP1'] = valuetemp1
            clean.at[index, 'VALUE_DERIVED'] = float(valuetemp1)
        
        # Condition 2: If value contains ".BR\"
        elif "\.BR\\" in upvalue:
            valuetemp1 = upvalue.replace("\.BR\\", '').strip()
            if is_valid_number(valuetemp1):
                clean.at[index, 'VALUETEMP1'] = valuetemp1
                clean.at[index, 'VALUE_DERIVED'] = float(valuetemp1)
        
        # Condition 3: If it has < or > and no letter
        elif '<' in upvalue or '>' in upvalue:
            if '<' in upvalue:
                clean.at[index, 'SUBVALUE1'] = '<'
                valuetemp1 = upvalue.replace('<', '').strip()
            elif '>' in upvalue:
                clean.at[index, 'SUBVALUE1'] = '>'
                valuetemp1 = upvalue.replace('>', '').strip()
            
            if is_valid_number(valuetemp1):
                clean.at[index, 'VALUETEMP1'] = valuetemp1
                clean.at[index, 'VALUE_DERIVED'] = float(valuetemp1)    
    
         # Condition 4: If it has !/H/R/L at the end
            elif re.match(r'^.*[!HRL]$', upvalue):
                valuetemp1 = re.sub(r'[!HRL]', '', upvalue).strip()
                if is_valid_number(valuetemp1):
                    clean.at[index, 'VALUETEMP1'] = valuetemp1
                    clean.at[index, 'VALUE_DERIVED'] = float(valuetemp1)
            
            # Condition 5: If it starts with "LESS THAN"
            elif upvalue.startswith('LESS THAN'):
                clean.at[index, 'SUBVALUE1'] = '<'
                valuetemp1 = re.sub(r'LESS THAN[\s\.BR]*', '', upvalue).strip()
                if is_valid_number(valuetemp1):
                    clean.at[index, 'VALUETEMP1'] = valuetemp1
                    clean.at[index, 'VALUE_DERIVED'] = float(valuetemp1)
            
            # Condition 6: If it starts with "GREATER THAN"
            elif upvalue.startswith('GREATER THAN'):
                clean.at[index, 'SUBVALUE1'] = '>'
                valuetemp1 = re.sub(r'GREATER THAN[\sMMOL/L\(\)]*', '', upvalue).strip()
                if is_valid_number(valuetemp1):
                    clean.at[index, 'VALUETEMP1'] = valuetemp1
                    clean.at[index, 'VALUE_DERIVED'] = float(valuetemp1)
            
            # Condition 7: If it contains "HTTP://WWW.SSHA.CA"
            elif "HTTP://WWW.SSHA.CA" in upvalue:
                if '&GT;' in upvalue:
                    clean.at[index, 'SUBVALUE1'] = '>'
                elif '&LT;' in upvalue:
                    clean.at[index, 'SUBVALUE1'] = '<'
                
                structured_start = '<P1:STRUCTUREDNUMERIC XMLNS:P1="HTTP://WWW.SSHA.CA">'
                structured_end = '</P1:STRUCTUREDNUMERIC>'
                comparator_start = '<P1:COMPARATOR>'
                comparator_end = '</P1:COMPARATOR>'
                number1_start = '<P1:NUMBER1>'
                number1_end = '</P1:NUMBER1>'
                
                valuetemp1 = upvalue.split(structured_start)[-1].split(structured_end)[0].strip()
                valuetemp2 = valuetemp1.split(comparator_start)[-1].split(comparator_end)[0].strip()
                valuetemp3 = valuetemp2.split(number1_start)[-1].split(number1_end)[0].strip()
                
                if is_valid_number(valuetemp3):
                    clean.at[index, 'VALUETEMP1'] = valuetemp3
                    clean.at[index, 'VALUE_DERIVED'] = float(valuetemp3)   
    
      # Filter rows where Value_Derived is missing
    unassigned = clean[clean['VALUE_DERIVED'].isna()]
    
    # Group by observationcode, upvalue, Value_Derived and count occurrences
    unassigned_counts = unassigned.groupby(['OBSERVATIONCODE', 'VALUE', 'VALUE_DERIVED']).size().reset_index(name='C')
    
    # Sort by count (descending) and upvalue
    unassigned_counts = unassigned_counts.sort_values(by=['C', 'VALUE'], ascending=[False, True])

    # Step 1: Performing left join and creating initial DataFrame
    a001_lipids = pd.merge(indata, clean, 
                           on=['ORDERSID', 'TESTREQUESTPOSITIONINORDER', 'OBSERVATIONPOSINTESTREQUEST'], 
                           how='left')
        
    # Use one of the columns directly
    a001_lipids['VALUE'] = a001_lipids['VALUE_x']
    a001_lipids['OBSERVATIONCODE'] = a001_lipids['OBSERVATIONCODE_x']

    # Drop the old columns
    a001_lipids.drop(columns=['VALUE_x', 'VALUE_y'], inplace=True)
    a001_lipids.drop(columns=['OBSERVATIONCODE_x', 'OBSERVATIONCODE_y'], inplace=True)
    
        # Step 2: Applying conditional logic to derive Value_derived_d and SubValue_derived_d
    a001_lipids['VALUE'] = pd.to_numeric(a001_lipids['VALUE'], errors='coerce')
    a001_lipids['VALUE_DERIVED_D'] = a001_lipids.apply(lambda row: row['VALUE_DERIVED'] if pd.notna(row['VALUE_DERIVED']) else float(row['VALUE']), axis=1)
    a001_lipids['SubValue_derived_d'] = a001_lipids['SUBVALUE1']
    
    #aaa=a001_lipids.head(3)
    
    # Step 3: Applying conditional logic to derive Value_recommended_d and SubValue_recommended_d
    a001_lipids['Value_recommended_d'] = a001_lipids['VALUE_DERIVED_D']
    a001_lipids['SubValue_recommended_d'] = a001_lipids['SUBVALUE1']
    
      
    #aa=a001_lipids.head(1)
    # return aaa #obs_sup
    return a001_lipids
# %%
if __name__ == '__main__':

    # setup
    projectPath = Path(os.getcwd())
    dataFile = projectPath / ".." / "Data/olis_lipids.sas7bdat"
    #dataFile = projectPath /".."/ "Data/test.sas7bdat"
 

# read in the dataset
    dat0 = pd.read_sas(dataFile, encoding='latin1')
    datanull=dat0.head(1)
# Apply the function
    outdata = clean_lipid(dat0)
    
    
