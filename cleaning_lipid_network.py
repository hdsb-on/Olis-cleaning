# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 09:41:03 2024

@author: KeremAi
"""

# %%
import pandas as pd
import re
import os
from pathlib import Path

# %%
def derive_value(upvalue, observationcode):

    value_derived = None
    subvalue1 = None
    
    try:
        # If value has just numbers and decimals
        if re.fullmatch(r'[0-9.]+', upvalue):
            valuetemp1 = upvalue.replace('..', '.')
            value_derived = float(valuetemp1)
        
        # If value contains \.BR\
        elif "\\.BR\\" in upvalue:
            valuetemp1 = upvalue.replace("\\.BR\\", ' ').strip()
            if re.fullmatch(r'[0-9. ]+', valuetemp1):
                value_derived = float(valuetemp1.strip())
        
        # If it has < or > and no letter
        elif any(op in upvalue for op in '<>') and re.fullmatch(r'[0-9. <>]+', upvalue):
            if '<' in upvalue:
                subvalue1 = '<'
            elif '>' in upvalue:
                subvalue1 = '>'
            valuetemp1 = re.sub(r'[<>]', '', upvalue).strip()
            if re.fullmatch(r'[0-9.]+', valuetemp1):
                value_derived = float(valuetemp1)
        
        # Has !/H/R/L at the end
        elif re.fullmatch(r'[0-9. !HRL]+', upvalue):
            valuetemp1 = re.sub(r'[!HRL]', '', upvalue).strip()
            if ' ' not in valuetemp1 and re.fullmatch(r'[0-9.]+', valuetemp1):
                value_derived = float(valuetemp1)
        
        # LESS THAN
        elif upvalue.startswith('LESS THAN'):
            subvalue1 = '<'
            valuetemp1 = re.sub(r'LESS THAN|\.BR\\', '', upvalue).strip()
            if re.fullmatch(r'[0-9.]+', valuetemp1):
                value_derived = float(valuetemp1)
        
        # GREATER THAN
        elif upvalue.startswith('GREATER THAN'):
            subvalue1 = '>'
            valuetemp1 = re.sub(r'GREATER THAN MMOL/L\(\)|\.BR\\', '', upvalue).strip()
            if re.fullmatch(r'[0-9.]+', valuetemp1):
                value_derived = float(valuetemp1)
        
        # XML
        elif "HTTP://WWW.SSHA.CA" in upvalue:
            if '&GT;' in upvalue:
                subvalue1 = ">"
            elif '&LT;' in upvalue:
                subvalue1 = "<"
            
            valuetemp1 = re.sub(r'<P1:STRUCTUREDNUMERIC XMLNS:P1="HTTP://WWW.SSHA.CA">|</P1:STRUCTUREDNUMERIC>', ' ', upvalue).strip()
            valuetemp2 = re.sub(r'<P1:COMPARATOR>|</P1:COMPARATOR>', ' ', valuetemp1).strip()
            valuetemp3 = re.sub(r'<P1:NUMBER1>|</P1:NUMBER1>', ' ', valuetemp2).strip()
            valuetemp4 = re.sub(r'<P1:NUMBER2>|</P1:NUMBER2>', ' ', valuetemp3).strip()
            valuetemp5 = re.sub(r'<P1:COMPARATOR/>|<P1:SEPARATOR/>', ' ', valuetemp4).strip()
            valuetemp6 = re.sub(r'[=&LTGT;:]', '', valuetemp5).strip()
            if re.fullmatch(r'[0-9.]+', valuetemp6):
                value_derived = float(valuetemp6)
        
        # LIPIDS SPECIFIC
        if value_derived is None and re.fullmatch(r'[0-9.-NEG ]+', upvalue):
            valuetemp1 = re.sub(r' NEG', '', upvalue).strip()
            if re.fullmatch(r'[0-9.-]+', valuetemp1):
                value_derived = float(valuetemp1)

        # Cholesterol
        elif value_derived is None and observationcode in ['14646-4', '14647-2', '22748-8', '25371-6', '32309-7', '39469-2', '70204-3']:
            match = re.search(r'(CHOL|FHOL|FCHOL|CHOLESTEROL|CHOLESTEOL|HOLESTEROL RESULT|CHOLESTEROL LEVEL|CHOLESEROL RESULTS|FASTING|FASTING\)|SERUM\)|LDL|HDL|HDL RESULT)[IS.:= ]+([<>]?)(\d{1,2}\.\d{1,2})', upvalue)
            if match:
                value_derived = float(match.group(3))
                subvalue1 = match.group(2)
            
            match = re.search(r'LDL[- ]*(CHOLESTEROL|CHOL)? ?(IS|:|=)? (LESS THAN|<) ?1', upvalue)
            if match:
                value_derived = 1
                subvalue1 = '<'
            
            if upvalue == 'VALUE IS GREATER THAN 4.5':
                value_derived = 4.5
                subvalue1 = '>'
        
        # Triglycerides
        elif value_derived is None and observationcode in ['14927-8', '47210-0']:
            match = re.search(r'(TRIGLYCERIDES|TRIGLYCERIDES RESULT|TRIGLYCERIDS|TRIGLYCERIDE|TRIG|TRIGLY|TRIGLYCERIDE RESULT|TRIG RESULT)[IS.:= ]+([<>]?)(\d{1,3}\.\d{1,2})', upvalue)
            if match:
                value_derived = float(match.group(3))
                subvalue1 = match.group(2)
            
            match = re.search(r'^(\d{1,2}\.\d{2}) (,|\()', upvalue)
            if match:
                value_derived = float(match.group(1))
            
            if 'SERUM TRIGLYCERIDES > 50.00' in upvalue or 'SERUM TRIGLYCERIDE RESULT RESULT GREATER\.BR\THAN 50.00' in upvalue:
                value_derived = 50.00
                subvalue1 = '>'
        
        # Apolipoprotein
        elif value_derived is None and observationcode in ['1869-7', '1884-6']:
            match = re.search(r'(APOB|RESULT)[IS.:= ]+([<>]?)(\d{1}\.\d{3})', upvalue)
            if match:
                value_derived = float(match.group(3))
                subvalue1 = match.group(2)
        
        # <1.70 MMOL/L NORMAL
        # >5.64 MMOL/L VERY HIGH
        if value_derived is None and observationcode in ['47210-0', "39469-2", "14647-2", "14646-4"]:
            match = re.search(r'^([<>]?)(\d{1,3}\.\d{1,2})\s*MMOL\/L', upvalue)
            if match:
                value_derived = float(match.group(2))
                subvalue1 = match.group(1)
        
        if value_derived is None and observationcode in ['1884-6']:
            match = re.search(r'([=]?)(\d{1,3}\.\d{1,3}) G\/L', upvalue)
            if match:
                value_derived = float(match.group(2))
    
    except ValueError as e:
        print(f"ValueError: Could not convert value to float for upvalue: {upvalue}. Error: {e}")
    
    return value_derived, subvalue1    



# %%
if __name__ == '__main__':

    # setup
    projectPath = Path(os.getcwd())
    #dataFile = projectPath / ".." / "Data/olis_lipids.sas7bdat"
    dataFile = projectPath / "Data/olis_lipid2.sas7bdat"

  
    # read in the dataset
    dat0 = pd.read_sas(dataFile, encoding='latin1')
    value_value = dat0.groupby(['VALUE', 'OBSERVATIONCODE', 'ORDERSID', 'TESTREQUESTPOSITIONINORDER', 'OBSERVATIONPOSINTESTREQUEST']).size().reset_index(name='cn')
    # Rename the column 'value' to 'value_encoded'
    value_value = value_value.rename(columns={'VALUE': 'VALUE_ENCODED'})

    
    # %%

    # Rename the column 'value_encoded' to 'value'
    value_value = value_value.rename(columns={'VALUE_ENCODED': 'VALUE'})
    
    # Create a new column 'upvalue' with the uppercase version of 'value'
    value_value['UPVALUE'] = value_value['VALUE'].str.upper()   
    
    # %%
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

# %%
# Apply the function to the DataFrame
    import pandas as pd
    import re
    
    clean = pd.DataFrame(obs_sup)
    clean[['Value_derived', 'SubValue1']] = clean.apply(lambda row: derive_value(row['UPVALUE'], row['OBSERVATIONCODE']), axis=1, result_type='expand')

# %%

# Filter rows where Value_Derived is NaN
    unassigned = clean[clean['Value_derived'].isna()]
    
    # Group by 'observationcode', 'upvalue', and 'Value_Derived', and count occurrences
    unassigned_grouped = unassigned.groupby(['OBSERVATIONCODE', 'UPVALUE', 'Value_derived']).size().reset_index(name='c')
    
    # Sort by count (c) in descending order, and then by 'upvalue'
    unassigned_sorted = unassigned_grouped.sort_values(by=['c', 'UPVALUE'], ascending=[False, True])
    # %%
    # Merge df and clean DataFrames
    clean_lipid_df = pd.merge(
        dat0, clean,
        on=['ORDERSID', 'TESTREQUESTPOSITIONINORDER', 'OBSERVATIONPOSINTESTREQUEST'],
        how='left')


