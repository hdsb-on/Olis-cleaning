#%%
import pandas as pd
import numpy as np
import re
import os
from pathlib import Path

#%%
def derive_values(row):
    value = row['value_encoded']
    upvalue = row['upvalue']
    value_derived = None
    subvalue1 = None
    
    if re.search(r"HBA1C (-)+ (\d)(.)(\d)", upvalue):
        value_derived = float(re.search(r"(\d+.\d+)", upvalue).group(1))

    elif upvalue == "7.9%      HI             REF RANGE <6.0%":
        value_derived = float(upvalue[:3])

    elif upvalue == "5.5 %  REF. RANGE < 6.0 %":
        value_derived = float(upvalue[:3])

    elif upvalue == "5.4 %\E\.BR\E\\E\.BR\E\REFERENCE RANGE <6.0%":
        value_derived = float(upvalue[:3])

    elif re.search(r"^HBA2C: ", upvalue):
        value_derived = float(upvalue[7:10])

    elif re.match(r'^[0-9.]+$', upvalue) and '..' not in upvalue:
        value_derived = float(upvalue.strip())

    elif re.match(r'^[0-9.]+$', upvalue) and '..' in upvalue:
        value_derived = float(upvalue.replace('..', '.').strip())

    elif '\\.BR\\' in upvalue:
        valuetemp1 = upvalue.replace('\\.BR\\', ' ').strip()
        if re.fullmatch(r'[0-9. ]+', valuetemp1):
                value_derived = float(valuetemp1)

    elif re.match(r'^[0-9.<> ]+$', upvalue):
        if '<' in upvalue:
            subvalue1 = '<'
        elif '>' in upvalue:
            subvalue1 = '>'
        value_derived = float(re.sub(r'[<>]', '', upvalue).strip())

    elif re.match(r'^[0-9. !HRL]+$', upvalue):
        value_derived = float(re.sub(r'[!HRL]', '', upvalue).strip())

    elif 'LESS THAN' in upvalue:
        subvalue1 = '<'
        value_derived = float(re.sub(r'[^\d.]', '', upvalue).strip())

    elif 'GREATER THAN' in upvalue:
        subvalue1 = '>'
        value_derived = float(re.sub(r'[^\d.]', '', upvalue).strip())

    elif "HTTP://WWW.SSHA.CA" in upvalue:
        if '&GT;' in upvalue or '&GT;=' in upvalue:
            subvalue1 = '>'
        elif '&LT;' in upvalue or '&LT;=' in upvalue:
            subvalue1 = '<'
        value_derived = float(re.sub(r'[^\d.]', '', re.sub(r'<P1:STRUCTUREDNUMERIC XMLNS:P1="HTTP://WWW.SSHA.CA">|</P1:STRUCTUREDNUMERIC>|<P1:COMPARATOR>|</P1:COMPARATOR>|<P1:NUMBER1>|</P1:NUMBER1>|<P1:NUMBER2>|</P1:NUMBER2>|<P1:COMPARATOR/>|<P1:SEPARATOR/>', ' ', upvalue)).strip())

    elif 'NORMAL:' in upvalue:
        match = re.search(r'(\d+\.\d+)', upvalue)
        if match:
            value_derived = float(match.group(1))
        if upvalue[match.start()-1] == '>':
            subvalue1 = '>'
        elif upvalue[match.start()-1] == '<':
            subvalue1 = '<'

    elif 'UNIT' in upvalue:
        match = re.search(r'(\d{1,3}\.\d{1,3})\s*FRACTION', upvalue)
        if match:
            value_derived = float(match.group(1))

    elif 'RESULT:' in upvalue and 'INTERPRETATION:' in upvalue:
        match = re.search(r'(<|>)\s*(\d{1,3}\.\d{1,3})', upvalue)
        if match:
            value_derived = float(match.group(2))
            subvalue1 = match.group(1)

    elif re.match(r'^(\d{1,3}\.\d) *(L|HI|R|\(|MMOL)', upvalue):
        match = re.match(r'^(\d{1,3}\.\d)', upvalue)
        if match:
            value_derived = float(match.group(1))

    elif re.search(r'^A1C (\d)(.)(\d){1,3}', upvalue):
        value_derived = float(upvalue[4:9])

    elif re.search(r'HBA1C(\s)+\d', upvalue):
        value_derived = float(re.sub(r'[%/"]', '', upvalue.split("C")[-1]).strip())

    elif re.search(r'HGBA1C(\s)+\d', upvalue):
        value_derived = float(re.sub(r'[%/"]', '', upvalue.split("C")[-1]).strip())

    elif re.search(r'HEMOGLOBIN A1C(\s)+\d', upvalue):
        value_derived = float(re.sub(r'[%/"]', '', upvalue.split("C")[-1]).strip())

    elif re.search(r'HBA1C > (\d|\w)*', upvalue):
        subvalue1 = '>'
        value_derived = float(upvalue.split(">")[1].split("\\")[0].strip())

    elif re.search(r'HBA1C(\s)*<(\d|\w)*', upvalue):
        subvalue1 = '<'
        value_derived = float(upvalue.split("<")[1].split("\\")[0].strip())

    elif re.search(r'HBA1C  - (\d|\w)*', upvalue):
        value_derived = float(upvalue.split("-")[1].split("%")[0].strip())

    elif re.search(r'^(<|>) (\d|\s)', upvalue):
        subvalue1 = upvalue[0]
        value_derived = float(upvalue.split(subvalue1)[1].split("%")[0].strip())

    elif re.search(r'^HBA1C =', upvalue):
        subvalue1 = upvalue[8]
        value_derived = float(upvalue.split(subvalue1)[1].split("\\")[0].strip())

    elif re.search(r'HBA1C >', upvalue):
        subvalue1 = '>'
        value_derived = float(upvalue.split(">")[1][:5].strip())

    elif re.search(r'\.+RESULT', upvalue):
        subvalue1 = '>'
        value_derived = float(upvalue.split(">")[1][:5].strip())

    elif re.search(r'RESULT =', upvalue):
        value_derived = float(upvalue.split("=")[1][:5].strip())

    elif re.search(r'^(>|<)\s*(\d)+(\.)*', upvalue):
        subvalue1 = upvalue[0]
        value_derived = float(upvalue.split(subvalue1)[1][:5].strip())

    elif re.search(r'^RESULT (<|>)', upvalue):
        value = upvalue.replace(" ", "")
        subvalue1 = value[6]
        value_derived = float(value.split(subvalue1)[1][:5].strip())

    elif re.search(r'^HEMOGLOBIN A1C =', upvalue):
        value_derived = float(upvalue.split("=")[1].strip())
    
    return pd.Series([value_derived, subvalue1])
#%%

#%%
def unassigned_hba1c_counts(cleaned_data: pd.DataFrame) -> pd.DataFrame:
    # Filter the DataFrame where Value_Derived is NaN (equivalent to . in SAS)
    unassigned_hba1c = cleaned_data[cleaned_data['value_derived'].isna()]

    # Group by 'observationcode', 'upvalue', and 'value_derived', and count the occurrences
    grouped_data = unassigned_hba1c.groupby(['observationcode', 'upvalue']).size().reset_index(name='c')

    # Sort by count in descending order, then by 'upvalue'
    sorted_data = grouped_data.sort_values(by=['c', 'upvalue'], ascending=[False, True])

    return sorted_data
#%%

#%%
def clean_and_scale_values(cleaned_data: pd.DataFrame) -> pd.DataFrame:
    # Create a copy of the DataFrame to avoid modifying the original data
    clean_data = cleaned_data.copy()
    
    # Initialize the 'scaled_value' column with the values from 'value_derived'
    clean_data['scaled_value'] = clean_data['value_derived']

    # Rescale values between 0.020 and 0.219
    clean_data.loc[(clean_data['scaled_value'] >= 0.020) & (clean_data['scaled_value'] <= 0.219), 'scaled_value'] *= 100

    # Specific case where scaled_value equals 130
    clean_data.loc[clean_data['scaled_value'] == 130, 'scaled_value'] = 13

    # Identify outliers
    clean_data['scaled_outlier'] = ~((clean_data['scaled_value'] >= 2) & (clean_data['scaled_value'] <= 21.9) | clean_data['scaled_value'].isna())

    # Handle outliers by setting the values to NaN and clearing 'subValue1' and 'subValue2'
    clean_data.loc[clean_data['scaled_outlier'], ['scaled_value', 'subValue1', 'subValue2']] = [np.nan, '', '']

    return clean_data

#%%

#%%
def process_hba1c_data(in_data: pd.DataFrame, trim_top: float, trim_bottom: float) -> pd.DataFrame:

    # Copy input data to avoid modifying the original data
    df = in_data.copy()
    
    # Step 1: Initial data processing
    def to_numeric(value):
        try:
            # Attempt to convert to float
            return float(value)
        except ValueError:
            # If conversion fails, return a default value
            return 99999999

    # Apply function and create 'num_value' column
    df['num_value'] = df['value'].apply(lambda x: to_numeric(x.strip()))

    # Step 2: Process observation data
    df['observationcode_units'] = df['observationcode'].str.strip() + '_' + df['units'].str.strip()
    df['bpercentunit'] = df['units'].str.strip() == "%"
    df['bmolunit'] = df['units'].str.strip().isin(['ZZ', 'mmol/mol'])

    # Set credible clinical range for some known ObservationCode_units
    df['scaled_value'] = df.apply(lambda row: (
        row['num_value'] if row['bpercentunit'] else
        row['num_value'] * 100 if not row['bmolunit'] else
        0.09148 * row['num_value'] + 2.152
    ) if row['observationcode_units'] not in ["4547-6_", "4547-6_FRAC OF 1", "51196-4_%"] else np.nan, axis=1)

    # Identify outliers
    df['outlier_low'] = df['scaled_value'] < trim_bottom
    df['outlier_high'] = df['scaled_value'] > trim_top
    df['outlier'] = df['outlier_low'] | df['outlier_high']

    # Fix mix % and frac problem
    df.loc[df['bpercentunit'] & (df['num_value'].between(0.02, 0.219)), 'scaled_value'] = df['num_value'] * 100
    df.loc[~df['bpercentunit'] & ~df['bmolunit'] & df['num_value'].between(trim_bottom, trim_top), 'scaled_value'] = df['num_value']

    # Final check for scaled outliers
    df['scaled_outlier'] = ~((df['scaled_value'].between(trim_bottom, trim_top)) | df['scaled_value'].isna())

    return df

#%%
def merge_and_update_data(hba1c_temp: pd.DataFrame, clean1: pd.DataFrame, trim_top: float, trim_bottom: float) -> pd.DataFrame:
    # Merge hba1c_temp and clean1
    merged_df = pd.merge(hba1c_temp, clean1, how='left', on=['ordersid', 'testrequestpositioninorder', 'observationposintestrequest'],suffixes=('', '_clean1'))

    # Create the new columns based on the given conditions
    merged_df['value_derived_d'] = np.where(merged_df['num_value'] == 99999999, merged_df['scaled_value_clean1'], merged_df['scaled_value'])
    merged_df['subvalue_derived_d'] = merged_df['subvalue1']
    merged_df['value_recommended_d'] = np.where(merged_df['num_value'] == 99999999, merged_df['scaled_value_clean1'], merged_df['scaled_value'])
    merged_df['subvalue_recommended_d'] = merged_df['subvalue1']

    # Update the recommended values
    merged_df.loc[~merged_df['value_derived_d'].between(trim_bottom, trim_top), ['value_recommended_d', 'subvalue_recommended_d']] = [np.nan, '']

    merged_df = merged_df[['hcn_encrypted', 'ordersid', 'observationcode', 'observationdatetime',
       'observationreleasets', 'value', 'valuetype', 'units', 'refrange',
       'observationposintestrequest', 'testrequestpositioninorder',
       'value_encoded', 'upvalue', 'num_value', 'observationcode_units',
       'bpercentunit', 'bmolunit', 'scaled_value', 'outlier_low',
       'outlier_high', 'outlier', 'scaled_outlier','value_derived_d', 'subvalue_derived_d',
       'value_recommended_d', 'subvalue_recommended_d']]

    return merged_df
#%%
def final_data_cleanup(hba1c: pd.DataFrame) -> pd.DataFrame:
    # Further data cleanup based on invalid_record_flag
    # We don't have inavlid_)record_flag column.
    # hba1c.loc[hba1c['invalid_record_flag'] == 'Y', ['value_recommended_d', 'subvalue_recommended_d']] = [np.nan, '']

    # Drop unnecessary columns
    columns_to_drop = ['observationcode_units', 'bpercentunit', 'bmolunit', 'scaled_value', 
                       'num_value', 'outlier_low', 'outlier_high', 'outlier', 'scaled_outlier',
                       'value_derived_d', 'subvalue_derived_d']
    hba1c.drop(columns=columns_to_drop, inplace=True)

    # Round the recommended values
    hba1c['value_recommended_d'] = hba1c['value_recommended_d'].round(1)

    return hba1c
#%%
def exclusion(olis_hba1c: pd.DataFrame) -> pd.DataFrame:
    olis_hba1c['value_encoded'] = olis_hba1c['value']

    olis_hba1c['upvalue'] = olis_hba1c['value_encoded'].str.upper()
    
    # Define the exclusion criteria
    exclusion_criteria = [
        'TEST NOT PERFORMED', 'DISREGARD', 'CORRECTED ON', 'NOT VALID', 'ORIGINAL GLUCOSE',
        'FLUID', 'DIABETES', 'DUPLICATE', 'HGBA1C MAY NOT BE ACCURATE DUE TO TRANSFUSION',
        'INSUFFICIENT QUANTITY', 'DUE TO IMPROPER HANDLING.', 'UNABLE', 'NOT WARRANTED',
        'NOT BEEN PROCESSED', 'RESULT INVALID', 'CANCELLED', 'UNRELIAB', 'CLOT', 'DUPLICARE',
        'EXCEEDED', '30 DAYS', 'NOT BE AVAIALABLE', 'ACCESSION', 'NOT BE AVAILABLE',
        'ABOVE ASSAY RANG', 'NOT PERFORMED', 'UNAVAILABLE', 'NOT AVAILABLE', 'NOT REPORTED',
        'INSUFFICIENT SPECIMEN', 'DELETE', 'BELOW ANALYTICAL RANGE', 'ABOVE ANALYTICAL RANGE',
        'BELOW DETECTION LIMIT', 'NOT PROCESSED', 'CANCEL', 'INVALID RESULT', 'MISLABELLED SAMPLE',
        'NO SPECIMEN RECEIVED', 'ORDERED IN ERROR', 'DUPLCATE', 'DUPLCIATE', 'DUPLICAATE',
        'BELOW THE DETECTION LIMIT', 'BELOW TEST LIMIT', 'NOT REPORTABLE', 'CANNOT BE PROCESSED',
        'INSUFFICIENT SAMPLE', 'NO RESULT AVAILABLE', 'NO SAMPLE RECEIVED', 'NOT SUFFICIENT QUANTITY',
        'IS REJECTED', 'FAILED TO MEET THE REQUIREMENTS', 'NOT SUITABLE', 'SPECIMEN UNSATISFACTORY',
        'UNSUITABLE', 'HAS BEEN REJECTED', 'NOT BEEN PERFORMED', 'WRONG TEST', 'WRONG TUBE',
        'HOMOZYGOUS', 'HBSC DISEASE', 'NOT INDICATED'
    ]
    
    # Filter rows based on exclusion criteria
    exclusion_pattern = '|'.join(exclusion_criteria)
    mask = olis_hba1c['upvalue'].str.contains(r'\d') & ~olis_hba1c['upvalue'].str.contains(exclusion_pattern)

    clean_data = olis_hba1c[mask].copy()

    return clean_data

#%%
def cleaning_hba1c(olis_hba1c: pd.DataFrame) -> pd.DataFrame:
    
    clean_data = exclusion(olis_hba1c)
    #obs_sup = clean_data

    #I didn't convert obs_sup2

    # Initialize new columns
    clean_data['value_derived'] = None
    clean_data['subvalue1'] = None
    clean_data['valuetemp1'] = None
    clean_data['valuetemp2'] = None
    clean_data['valuetemp3'] = None
    clean_data['valuetemp4'] = None
    clean_data['valuetemp5'] = None
    clean_data['valuetemp6'] = None
    
    clean_data[['value_derived', 'subvalue1']] = clean_data.apply(derive_values, axis=1)

    unassigned_hba1c = unassigned_hba1c_counts(clean_data)

    clean1 = clean_and_scale_values(clean_data)

    trim_top = 21.9
    trim_bottom = 2

    hba1c_temp = process_hba1c_data(olis_hba1c, trim_top, trim_bottom)

    hba1c = merge_and_update_data(hba1c_temp, clean1, trim_top, trim_bottom)

    # Final cleanup
    outdata = final_data_cleanup(hba1c)

    return outdata

#%%
def anydigit(s):
    return any(char.isdigit() for char in s)

def anyalpha(s):
    return any(char.isalpha() for char in s)

def anypunct(s):
    return any(char in ".,;:!?-/" for char in s)
    # return any(char.ispunct() for char in s)

def correction(sentence):
    # Split the sentence into words
    words = sentence.split()

    # Initialize a list to store the corrected words
    corrected_words = []

    # Iterate through each word
    for word in words:
        # Check if the word is misspelled
        if spell.unknown([word]) and len(word)>1:
            # If misspelled, correct it
            corrected_word = spell.correction(word)

            # Preserve punctuation
            if corrected_word != None and word[-1] in ",.?!;:/><":
                corrected_word += word[-1]  # Add the punctuation mark to the corrected word
            else:
                corrected_word = word
            corrected_words.append(corrected_word)
        else:
            # If correctly spelled, keep the word as it is
            corrected_words.append(word)

    # Join the corrected words back into a sentence
    corrected_sentence = ' '.join(corrected_words)

    return corrected_sentence

if __name__ == '__main__':

    #%%
    # projectPath = Path(os.getcwd())
    # projectPath = Path("\\hscpigdcapmdw05\SAS\USERS\HDSB\Projects\Olis Cleaning")
    # dataFile = projectPath / ".." / "Data/olis_cdiff.sas7bdat"
    dataFile = "D:\\Users\\HDSB\\Projects\\Olis_cleaning\\Data\\olis_hba1c.sas7bdat"

    #%%
    # read in the dataset
    dat1 = pd.read_sas(dataFile, encoding='latin1')
    dat1.columns= dat1.columns.str.lower()

    # %% Run the function
    dat2 = cleaning_hba1c(dat1)
    dat2  = dat2.fillna(value=np.nan)
    #dat2 = python cleaned code
    
    # %% compare the results with that of output from SAS code;
    # resultfile = projectPath / ".." / "sas_cleaned_data/cdiff_clean.sas7bdat"
    resultfile = "D:\\Users\\HDSB\\Projects\\Olis_cleaning\\sas_cleaned_data\\hba1c_clean.sas7bdat"

    res = pd.read_sas(resultfile, encoding='latin1')
    res.columns = res.columns.str.lower()
    #res = sas cleaned code
    
    # %%
    #Code to calculate number of mismatched values between sas and python results
    indexcols = ['ordersid','observationcode','observationdatetime','testrequestpositioninorder','observationposintestrequest']
    sasVsours = (res[ indexcols+ ['value_recommended_d','subvalue_recommended_d']]
            .rename(columns={"value_recommended_d":"res_value", "subvalue_recommended_d":"res_subvalue"})
            .merge( dat2[ indexcols + ['value_recommended_d','subvalue_recommended_d']],
                    how="inner", on=indexcols))
    diff_values = sasVsours[
        ((sasVsours.res_value - sasVsours.value_recommended_d).abs() > 10e-6) |
        (sasVsours.res_value.isna() & sasVsours.value_recommended_d.notna()) |
        (sasVsours.res_value.notna() & sasVsours.value_recommended_d.isna())
    ]
    print("total missmatch in values: ", diff_values.shape[0])
    diff = sasVsours[(sasVsours.res_subvalue !=  sasVsours.subvalue_recommended_d) ]
    print ("total missmatch in subvalues" , diff.shape[0])
# %%


