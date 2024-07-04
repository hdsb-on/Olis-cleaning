#%%
import pandas as pd
import numpy as np
import re

#%%
extracode = '4269-7'
df = pd.read_sas("S:\\HDSB\\Projects\\Olis_cleaning\\indata\\olis_glucose_top5000.sas7bdat", encoding="latin1")

#%%
data=df

#%%
# Filter out non-numeric values in 'value' column
df['upvalue'] = df['VALUE'].str.upper()
df['value_encoded'] = df['VALUE']

# Creating obs_sup_0 equivalent
obs_sup_0 = df[df['VALUE'].str.contains(r'[^\d\s.]')]

# Creating obs_sup equivalent
excluded_strings = [
    'TEST NOT PERFORMED', 'DISREGARD', 'CORRECTED ON', 'NOT VALID', 
    'ORIGINAL GLUCOSE', 'FLUID', 'DIABETES', 'NO SPECIMEN RECEIVED',
    'NO SAMPLE RECEIVED', 'NOT RECEIVED', 'UNABLE TO COLLECT',
    'NOT SUFFICIENT QUANTITY', 'INSUFFICIENT SAMPLE', 
    'INSUFFICIENT QUANTITY', 'SPECIMEN UNSATISFACTORY', 'MISLABELLED',
    'UNLABELLED SAMPLE', 'HAEMOLYZED', 'HEMOLYZED', 'HEMOLYSED',
    'QUERY SPECIMEN INTEGRITY', 'CONTAMINATION', 'CONTAMINATED',
    'STABILITY LIMIT EXCEEDED', 'AIR BUBBLES IN SAMPLE', 'WRONG TUBE',
    'FAILED TO MEET THE REQUIREMENTS', 'DISCARDED', 'NOT PROCESSED',
    'UNABLE TO PROCESS', 'REJECTION', 'SPECIMEN REJECTED', 
    'HAS BEEN REJECTED', 'REJECTED SPECIMEN', 'UNSUITABLE', 'CANCELLED',
    'CANCEL', 'UNABLE TO PERFORM', 'CANNOT BE PERFORMED', 'NOT PERFORMED',
    'HAS NOT BEEN PERFORMED', 'NOT BEEN SIGNED', 'ERROR', 'NOT REPORTED',
    'WRONG TEST CODE', 'RESULT UNAVAILABLE', 'NOT AVAILABLE', 
    'NOT BE AVAILABLE', 'DELETE', 'INVALID', 'QUESTIONABLE RESULTS', 
    'BELOW THE MINIMUM ACCEPTABLE LEVEL', 'DUPLICATE REQUEST', 
    'DUPLICATE ORDER', 'REQUEST A REDRAW'
]

obs_sup = obs_sup_0[
    (obs_sup_0['OBSERVATIONCODE'] != extracode) & 
    obs_sup_0['upvalue'].apply(lambda x: any(digit.isdigit() for digit in x)) & 
    ~obs_sup_0['upvalue'].apply(lambda x: any(substring in x for substring in excluded_strings))
]
obs_sup=obs_sup.drop(columns=['VALUE'])


# %%
obs_sup2 = df[
    (df['OBSERVATIONCODE'] == extracode) &  # Filtering by ObservationCode
    (df['upvalue'].str.isdigit()) &  # Checking if 'upvalue' contains any digit
    ~df['upvalue'].str.contains(r'TEST NOT PERFORMED|DISREGARD|CORRECTED ON|NOT VALID|ORIGINAL GLUCOSE|FLUID|DIABETES')  # Excluding specific keywords
]
obs_sup2 = obs_sup2.reset_index(drop=True)

def check_and_call_missing(row):
    value = row['value_encoded']
    upvalue = row['upvalue']
    observationcode = row['OBSERVATIONCODE']
    
    compressed_value = ''.join(value.split()).upper()
    
    if any(keyword in compressed_value for keyword in ["NOTIMEINDICATED", "NOTTIMEINDICATED", "OWNGLUCOMETER", "NOTIMEGIVEN"]):
        row['value_encoded'] = None
        row['upvalue'] = None
    elif observationcode in ["14759-5", "14771-0"] and any(keyword in compressed_value for keyword in ["30M", "1.0H", "1H", "ONEHOUR", "NOTIMEINDICATED", "3.0H", "0.5H", "MIN", "3H"]):
        row['value_encoded'] = None
        row['upvalue'] = None
    elif observationcode == "14761-1" and "3HR" in compressed_value:
        row['value_encoded'] = None
        row['upvalue'] = None
    elif observationcode == "14767-8" and any(keyword in compressed_value for keyword in ["30M", "1.0H", "1H", "ONEHOUR", "NOTIMEINDICATED", "3.0H", "0.5H", "MIN", "FASTING", "2H"]):
        row['value_encoded'] = None
        row['upvalue'] = None
    elif observationcode == "14995-5" and any(keyword in compressed_value for keyword in ["1/2", "1H", "FASTING"]):
        row['value_encoded'] = None
        row['upvalue'] = None
    
    return row

obs_sup_ = obs_sup.apply(check_and_call_missing, axis=1)


# %%
def process_row(row):
    upvalue = row['upvalue']
    observationcode = row['OBSERVATIONCODE']
    Value_derived = None
    SubValue1 = ''

    # Define regular expressions for matching patterns
    if re.match(r'^[\d. ]+$', upvalue) and '..' not in upvalue:
        Value_derived = float(upvalue.strip())
    elif re.match(r'^[\d. ]+$', upvalue) and '..' in upvalue:
        valuetemp1 = upvalue.replace('..', '.')
        Value_derived = float(valuetemp1.strip())
    elif '\.BR\\' in upvalue:
        valuetemp1 = upvalue.replace('\.BR\\', '').strip()
        if re.match(r'^[\d. ]+$', valuetemp1):
            Value_derived = float(valuetemp1)
    elif any(c in upvalue for c in '<>') and re.match(r'^[\d. <>]+$', upvalue):
        SubValue1 = '<' if '<' in upvalue else '>'
        valuetemp1 = upvalue.replace('<', '').replace('>', '').strip()
        Value_derived = float(valuetemp1)
    elif 'LESS THAN' in upvalue and upvalue.index('LESS THAN') == 0:
        SubValue1 = '<'
        valuetemp1 = upvalue.replace('LESS THAN', '').strip()
        Value_derived = float(valuetemp1)
    elif 'GREATER THAN' in upvalue and upvalue.index('GREATER THAN') == 0:
        SubValue1 = '>'
        valuetemp1 = upvalue.replace('GREATER THAN', '').strip()
        Value_derived = float(valuetemp1)
    elif 'HTTP://WWW.SSHA.CA' in upvalue:
        if '&GT;' in upvalue:
            SubValue1 = '>'
        elif '&LT;' in upvalue:
            SubValue1 = '<'
        valuetemp1 = re.sub(r'<P1:STRUCTUREDNUMERIC XMLNS:P1="HTTP://WWW.SSHA.CA">', '', upvalue)
        valuetemp1 = re.sub(r'</P1:STRUCTUREDNUMERIC>', '', valuetemp1)
        valuetemp2 = re.sub(r'<P1:COMPARATOR>', '', valuetemp1)
        valuetemp2 = re.sub(r'</P1:COMPARATOR>', '', valuetemp2)
        valuetemp3 = re.sub(r'<P1:NUMBER1>', '', valuetemp2)
        valuetemp3 = re.sub(r'</P1:NUMBER1>', '', valuetemp3)
        valuetemp4 = re.sub(r'<P1:NUMBER2>', '', valuetemp3)
        valuetemp4 = re.sub(r'</P1:NUMBER2>', '', valuetemp4)
        valuetemp5 = re.sub(r'<P1:COMPARATOR/>', '', valuetemp4)
        valuetemp5 = re.sub(r'<P1:SEPARATOR/>', '', valuetemp5)
        valuetemp6 = re.sub(r'&LTGT;:', '', valuetemp5)
        # Inside your process_row function
        if valuetemp6 and any(char.isdigit() for char in valuetemp6):
           valuetemp6 = re.sub(r'[^\d\.]', '', valuetemp6)
           try:
                Value_derived = float(valuetemp6)
           except ValueError:
                Value_derived = None
        else:
            Value_derived = None







    elif re.match(r'^\d{1,3}\.\d *(R|\(|MMOL)', upvalue):
        re_pattern = re.compile(r'^(\d{1,3}\.\d) *(R|\(|MMOL)')
        match = re_pattern.match(upvalue)
        if match:
            Value_derived = float(match.group(1))
    elif re.match(r'^\d{1,3}\.\d{1,2} *\d(\.\d)? (HR\.|HOUR) COLLECTION', upvalue):
        re_pattern = re.compile(r'^(\d{1,3}\.\d{1,2}) *\d(\.\d)? (HR\.|HOUR) COLLECTION')
        match = re_pattern.match(upvalue)
        if match:
            Value_derived = float(match.group(1))
    elif 'RANDOM' in upvalue:
        pos = upvalue.index('RANDOM')
        valuetemp1 = upvalue[pos:]
        re_pattern = re.compile(r'(IS|=|RESULT) ?(\d{1,3}\.\d)')
        match = re_pattern.search(valuetemp1)
        if match:
            Value_derived = float(match.group(2))
    elif 'GLU' in upvalue:
        re_pattern = re.compile(r'(GLU|GLUF|GLUR|R GLU|SER|GLUCOSE RESULT|GLUCOSE) ?[=:] ?(\d{1,3}\.\d)')
        match = re_pattern.search(upvalue)
        if match:
            Value_derived = float(match.group(2))
    elif 'NO TIME' in upvalue or 'TIME STUDY' in upvalue:
        re_pattern = re.compile(r'(\d{1,3}\.\d)')
        match = re_pattern.search(upvalue)
        if match:
            Value_derived = float(match.group(1))
    elif 'FASTING' in upvalue:
        pos = upvalue.index('FASTING')
        valuetemp1 = upvalue[pos:]
        re_pattern = re.compile(r'(SERUM|=|RESULT|OF)+ *(\d{1,3}\.\d)')
        match = re_pattern.search(valuetemp1)
        if match:
            Value_derived = float(match.group(2))
    elif observationcode in ['14757-9', '14995-5', '14759-5', '14761-1', '25668-5']:
        re_pattern = re.compile(r'GLUCOSE TOLERANCE \(RESULT IS|- 1.0H\) *(\d{1,3}\.\d)')
        match = re_pattern.search(upvalue)
        if match:
            Value_derived = float(match.group(1))
        re_pattern = re.compile(r'(H|NEW RESULT) +(\d{1,3}\.\d)')
        match = re_pattern.search(upvalue)
        if match:
            Value_derived = float(match.group(2))
    elif observationcode in ['20441-2', '14771-0', '53094-9', '25680-0', '1552-9', '14996-3', '47622-6', '40148-9', '34059-6', '40193-5']:
        re_pattern = re.compile(r'(HR|GLUCOSE|H|NEW RESULT) +(\d{1,3}\.\d)')
        match = re_pattern.search(upvalue)
        if match:
            Value_derived = float(match.group(2))
    elif observationcode in ['15074-8', '39481-7', '51596-5', '39480-9', '14749-6']:
        re_pattern = re.compile(r'(FASTING|RESULT OF|GLUCOSE|RESULT|GLUCOSE REPORTED AS|GLU RESULT IS) +(\d{1,3}\.\d)')
        match = re_pattern.search(upvalue)
        if match:
            Value_derived = float(match.group(2))
        re_pattern = re.compile(r'LESS THAN (\d{1,3}\.\d)')
        match = re_pattern.search(upvalue)
        if match:
            SubValue1 = '<'
            Value_derived = float(match.group(1))
    elif '>' in upvalue:
        re_pattern = re.compile(r'^> ?(\d{1,3}\.\d)')
        match = re_pattern.search(upvalue)
        if match:
            SubValue1 = '>'
            Value_derived = float(match.group(1))
        re_pattern = re.compile(r'(GLUCOSE|RESULT OF) ?> ?(\d{1,3}\.\d|\d{1,3})')
        match = re_pattern.search(upvalue)
        if match:
            SubValue1 = '>'
            Value_derived = float(match.group(2))
    elif '<' in upvalue:
        re_pattern = re.compile(r'^< ?(\d{1,3}\.\d)')
        match = re_pattern.search(upvalue)
        if match:
            SubValue1 = '<'
            Value_derived = float(match.group(1))
    elif 'ABSURD' in upvalue:
        re_pattern = re.compile(r'ABSURD ?(RESULT|VALUE) ?OF ?(\d{1,3}.\d)')
        match = re_pattern.search(upvalue)
        if match:
            Value_derived = float(match.group(2))
    elif upvalue == "GLUCOSE 1.0 HR              4.7 MMOL/L":
        Value_derived = float(upvalue.split('HR')[1].strip())
    elif upvalue == "5.5\.BR\5.5":
        Value_derived = 5.5
    elif "INTERPRET RESULTS WITH CAUTION.\\.BR\\NO TIME RECORDED ON 2.0 HOUR SPECIMEN." in upvalue:
        Value_derived = None
    elif "TIME STUDY\\.BR\\TIME (MINUTES)        GLUCOSE (MMOL/L)\\.BR\\FASTING   0            5.8\\.BR\\30                     12.7\\.BR\\60                     11.0\\.BR\\120                      9.3\\.BR\\180                      3.7\\.BR\\240                      3.7\\.BR\\" in upvalue:
        Value_derived = None
    elif "2 SAMPLES WERE RECEIVED WITH THE REQUISITION FOR\\.BR\\2 HOUR 75 GM OGTT\\.BR\\TUBES WERE LABELLED: PANZO ELLIDUS, AXVIERA\\.BR\\1979/03/24\\.BR\\MARCH 6, 2014\\.BR\\THERE WAS NO INDICATION ON THE TUBES WHICH TUBE\\.BR\\WAS FASTING OR 2 HOUR AND NO TIMES ON THE TUBES\\.BR\\IN ORDER TO IDENTIFY WE LABELLED THE TUBES A AND B\\.BR\\TUBE A PLASMA GLUCOSE RESULT WAS 5.4 MMOL/L\\.BR\\TUBE B PLASMA GLUCOSE RESULT WAS 4.7 MMOL/L\\.BR\\WE ARE UNABLE TO IDENTIFY WHICH TUBE RECEIVED WAS\\.BR\\THE FASTING OR PRE-DOSE SAMPLE AND WHICH TUBE\\.BR\\WAS THE 2 HOUR OR POST-DOSE SAMPLE\\.BR\\MR  2014/MAR/07" in upvalue:
        Value_derived = None


    return pd.Series({'Value_derived': Value_derived, 'SubValue1': SubValue1})

clean = obs_sup_.apply(process_row, axis=1)
clean = pd.concat([obs_sup_, clean], axis=1)

# %%
clean

# %%

df = pd.read_sas("S:\\HDSB\\Projects\\Olis_cleaning\\indata\\olis_glucose_top5000.sas7bdat", encoding="latin1")
df=df.rename(columns={'HCN_ENCRYPTED':'HCN_ENCRYPTED',
                      'ORDERSID':'ORDERSID',
                      'OBSERVATIONCODE':'OBSERVATIONCODE',
                      'OBSERVATIONDATETIME':'OBSERVATIONDATETIME',
                      'OBSERVATIONRELEASETS':'OBSERVATIONRELEASETS',
                      'VALUETYPE':'VALUETYPE',
                      'UNITS':'UNITS',
                      'REFRANGE':'REFRANGE',
                      'OBSERVATIONPOSINTESTREQUEST':'OBSERVATIONPOSINTESTREQUEST',
                      'TESTREQUESTPOSITIONINORDER':'TESTREQUESTPOSITIONINORDER'})

clean_date = pd.merge(clean, df[['ORDERSID', 'TESTREQUESTPOSITIONINORDER', 'OBSERVATIONPOSINTESTREQUEST','OBSERVATIONDATETIME']], 
                      how='left', 
                      on=['ORDERSID', 'TESTREQUESTPOSITIONINORDER', 'OBSERVATIONPOSINTESTREQUEST'])


# %%
clean1 = clean.copy()

def process_row(row):
    if pd.isnull(row['Value_derived']) and 'ORIGINAL' in row['upvalue']:
        re_pattern = r"(\d{2})-(\w{3})-(\d{2})"
        match = re.search(re_pattern, row['upvalue'])
        if match:
            date_str = match.group(0)
            date = pd.to_datetime(date_str, format='%d-%b-%y', errors='coerce')
            if pd.notnull(date) and pd.to_datetime(row['observationdatetime']).date() == date.date():
                re_pattern_value = r"(\d\.\d)"
                match_value = re.search(re_pattern_value, row['upvalue'])
                if match_value:
                    value = float(match_value.group(1))
                    if row['upvalue'][match_value.start() - 1] == '>':
                        row['SubValue1'] = '>'
                    elif row['upvalue'][match_value.start() - 1] == '<':
                        row['SubValue1'] = '<'
                    row['Value_derived'] = value
    return row

# Apply the function row-wise
clean1 = clean1.apply(process_row, axis=1)

# %%
clean1

# %%
filtered_df = clean1[clean1['Value_derived'].isna()]
grouped_df = filtered_df.groupby(['OBSERVATIONCODE', 'upvalue', 'Value_derived']).size().reset_index(name='c')
unassigned = grouped_df.sort_values(by='c', ascending=False)


# %%
clean2 = obs_sup2.copy()
clean2['Value_derived'] = np.nan
clean2['SubValue1'] = ''

clean2.loc[clean2['upvalue'].str.contains('\.\.', regex=False), 'Value_derived'] = clean2['upvalue'].str.replace('..', '.', regex=False)
clean2.loc[clean2['upvalue'].str.contains('50|75|100'), 'Value_derived'] = clean2['upvalue'].str[:4].str.replace('[A-Z<>/\\ (]', '', regex=True)
clean2.loc[clean2['upvalue'].str.contains('G'), 'Value_derived'] = clean2['upvalue'].str[:clean2['upvalue'].str.index('G')].str.replace('[A-Z<>/\\ (]', '', regex=True)

clean2.loc[clean2['upvalue'].str.contains('5O', regex=False), 'Value_derived'] = 50
clean2.loc[clean2['upvalue'].str.contains('\+', regex=False), 'Value_derived'] = clean2['upvalue'].apply(
    lambda x: float(x[:x.index('+')]) + float(x[x.index('+')+1:x.index('+')+4])
)
clean2['Value_derived'] = pd.to_numeric(clean2['Value_derived'], errors='coerce')



# %%
unassigned = clean2[clean2['Value_derived'].isna()]
unassigned = unassigned.groupby(['OBSERVATIONCODE', 'upvalue', 'Value_derived']).size().reset_index(name='c')
unassigned = unassigned.sort_values(by='c', ascending=False)

# %%
cleaned_glucose = pd.concat([clean1, clean2], ignore_index=True)

# %%
myobs_sup = pd.read_sas("S:\\HDSB\\Projects\\Olis_cleaning\\indata\\olis_glucose_top5000.sas7bdat", encoding="latin1")

def convert_value(value):
    if value.replace('.', '').isdigit():
        return float(value)
    else:
        return 99999999

myobs_sup['num_value'] = myobs_sup['VALUE'].apply(convert_value)


# %%
myobs_sup

#%%
cleaned_glucose

# %%
glucose = pd.merge(myobs_sup, cleaned_glucose[['ORDERSID', 'TESTREQUESTPOSITIONINORDER', 'OBSERVATIONPOSINTESTREQUEST','Value_derived','SubValue1']], how='left',
                   on=['ORDERSID', 'TESTREQUESTPOSITIONINORDER', 'OBSERVATIONPOSINTESTREQUEST'])

def calculate_value(row):
    if row['num_value'] == 99999999:
        return row['Value_derived']
    else:
        return row['num_value']

glucose['Value_derived_d'] = glucose.apply(calculate_value, axis=1)
glucose['SubValue_derived_d'] = glucose['SubValue1']
glucose['Value_recommended_d'] = glucose.apply(calculate_value, axis=1)
glucose['SubValue_recommended_d'] = glucose['SubValue1']

glucose=glucose.drop(columns=['Value_derived','SubValue1'], axis=1)


# %%
trim_bottom = 2  
trim_top = 21.9  
glucose.loc[
    (~glucose['Value_derived_d'].between(trim_bottom, trim_top)) & (glucose['OBSERVATIONCODE'] != '4269-7') |
    (glucose['UNITS'] == 'HOURS'),
    ['Value_recommended_d', 'SubValue_recommended_d']
] = [np.nan, '']

#%%
glucose
