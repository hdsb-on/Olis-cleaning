# %%

# from curses.ascii import ispunct
import pandas as pd
import numpy as np
import re
import os
from pathlib import Path
from spellchecker import SpellChecker


# start spell checker
spell = SpellChecker()

# fix the numeric value that corresponds to no reading founds
FIX_LOWNUMBER =-88888888.0
FIX_BIGNUMBER = 88888888.0

# %%
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
# %%
def findReading(sentence):
    """checks and returns the numerical value and the bound direction

    Args:
        sentence (_type_): String containing digits with <, ., > at the most.

    Returns:
        _type_: list of [value (numeric), boundl, units], bound is nill it will return blank
            string for bound, units if found will be sent or else Nill string 
    """
    value = FIX_LOWNUMBER
    units="mmol/L"
    subvalue_derived_d = ''
    if re.search("[<>]*(([^a-z]|\s)+)?(\d+[.\d]*)\s*", sentence, re.I):
        match = re.search("[<>]*\s*(\d+[.\d]*)\s*((MG|Mmol)?/(m)?L)?",sentence,re.I)
        
        if match[0][0] == '<':
            subvalue_derived_d = '<'
        elif match[0][0] == '>':
            subvalue_derived_d = '>'
        else:
            subvalue_derived_d = 'U'

        value = re.search("(\d+[.\d]*)\s*([mgol/u]+)?",sentence,re.I)
        units = re.sub(".*\s*(\d+[.\d]*)\s*","", value[0], re.I)
        value = re.search("(\d+[.\d]*)",value[0], re.I)
        if value:
            value = float(value[0])
        else :
            value = FIX_LOWNUMBER
            units = ""
    
    return [value, subvalue_derived_d, units]



# %%
def clean_sup_data(value_encoded:str):

    orignal_value_encoded = value_encoded
    value_encoded  = re.sub(r"\\.br\\"," ", value_encoded,re.I)

    value_derived_d = None
    subvalue_derived_d = None
    try :
        # Cleaning operations
        # value_encoded =  value_encoded.upper();
        # IF VALUE IS xxx mmol/L, SET TO THE NUMBER
        if 8 <= len(value_encoded) <= 15 and any(char.isdigit() for char in value_encoded) and 'mmol/l' in value_encoded.lower():
            value_derived_d = re.sub(r'[^0-9.]', '', value_encoded)

        # IF VALUE IS JUST A NUMBER, SET TO THE NUMBER
        elif 1 <= len(value_encoded) <= 5 and value_encoded.isdigit():
            value_derived_d = value_encoded

        # IF VALUE IS ALL NUMERAL WITH A DECIMAL OR COMMA, SET TO THE NUMBER
        elif 1 <= len(value_encoded) <= 7 and value_encoded.replace('.', '').replace(',', '').isdigit() and value_encoded[1] != '/':
            value_derived_d = value_encoded.replace(',', '')

        # IF VALUE IS OF THE FORM <XXXX OR SOMETHING HIGHLY SIMILAR, THEN REPORT AS XXXX
        elif len(value_encoded) < 9 and value_encoded[0] in ('<', '>') and value_encoded[1:].isdigit():
            value_derived_d = value_encoded.strip('<> ')
        elif len(value_encoded) < 9 and value_encoded[0] in ('<', '>') and not anyalpha(value_encoded):
            value_derived_d = value_encoded.strip('<> ')
            subvalue_derived_d = value_encoded[0]

        # IF VALUE IS OF THE FORM "LESS THAN XXXX", REPORT AS XXXX
        elif re.search("(?<=LESS THAN)\s+\d+\.*\d*",value_encoded, re.I):
            m = re.search("(?<=LESS THAN\s)\s*\d+\.*\d*",value_encoded, re.I)
            subvalue_derived_d = '<'
            value_derived_d = float(m[0])

        # IF VALUE IS OF THE FORM "GREATER THAN XXXX", REPORT AS XXXX
        elif re.search("(?<=GREATER THAN)\s+\d+\.*\d*",value_encoded, re.I):
            m = re.search("(?<=GREATER THAN\s)\s*\d+\.*\d*",value_encoded, re.I)
            subvalue_derived_d = '>'
            value_derived_d = m[0]
            print ( "GT : ", value_derived_d)

        # IF VALUE IS OF THE FORM "XXXX TO YYYY", REPORT AS THE AVERAGE OF THE TWO NUMBERS
        elif re.match('\s*\d+\.*\d*\s*to\s*\d+\.*\d*\s*', value_encoded,re.I):
            values = [float(x.strip) for x in value_encoded.split('TO') if x.strip().isdigit()]
            if len(values) == 2:
                value_derived_d = float(str(sum(values) / len(values)))

        elif len(value_encoded) >= 6 and value_encoded.endswith('\.br\\'):
            print( ' > 6 endswith .br')
            value_derived_d = float(value_encoded.split(' ')[0])

        # if value is html's fill form format
        elif re.match("<p1:StructuredNumeric", value_encoded, re.I):
            # print( '.. found html...')
            m = re.search("(?<=number1>)(\d+\.*\d*)", value_encoded, re.IGNORECASE)
            m2 = re.search("(?<=number2>)(\d+\.*\d*)", value_encoded, re.I)
            value_derived_d = m[0]
            if re.search("<p1:Seperator>-", value_encoded, re.I): # then read the second number
                value_derived_d = str((float(m[0])+ float(m2[0]))/2)
            else :
                m = re.search("(?<=<p1:comparator>[^A-z])([lgt]+)", value_encoded, re.IGNORECASE)
                if m is not None:
                    if m[0] == 'lt':
                        subvalue_derived_d = '<'
                    elif m[0] == 'gt':
                        subvalue_derived_d = '>'

        else:
            # start with spell checker for big one:
            value_spell = correction(value_encoded)
            # print(value_encoded)
            if re.search("^(Urine|creatinine|microalbumin|(albumin\s)?random urine)", value_spell, re.I) or \
                re.search("^.*\s*Result(s)?:.*",value_spell, re.I ) or \
                'CLINICAL ALBUMINURIA: ' in value_spell or \
                'Accession' in value_spell :
                value_derived_d, subvalue_derived_d,units = findReading(value_encoded)

            elif  re.search("(DETECTION|\sRANGE)", value_spell, re.I):
                value_derived_d = FIX_LOWNUMBER
                if re.search('below', value_spell, re.I):
                    subvalue_derived_d = '<'
                    value_derived_d, _,units = findReading(value_encoded)
                elif re.search('above', value_spell, re.I):
                    subvalue_derived_d = '>'
                    value_derived_d, _,units = findReading(value_encoded)

                else:
                    subvalue_derived_d = ' '
            # elif re.search("NO (SAMPLE|SPECIMEN)",value_spell,re.I) or \
            #        re.search("(BLOOD|AMENDED|PREVIOUS)",value_spell,re.I):
            #     value_derived_d = np.nan
            #     subvalue_derived_d = 'U'

            elif re.search( "TO LOW (LIMIT)? URINE (ALBUMIN|creatinine)", value_spell, re.I):
                value_derived_d,subvalue_derived_d,units =  findReading(value_encoded)
                subvalue_derived_d = '<'
    
            else:
                value_derived_d = FIX_LOWNUMBER
                subvalue_derived_d = 'U'
    
    except :
        print (" failed at:", value_encoded)
        raise
    
    if re.search("(TAMPERING|FALSELY ELEVATED|INTERFERENCE|INCORRECT|DISREGARD)",value_encoded,re.I):
        value_derived_d = np.nan
        subvalue_derived_d = ' '

    
    return value_derived_d, subvalue_derived_d


import pandas as pd

def cleaning_urine_creatinine(olis_urine_table: pd.DataFrame, code_list: list) -> pd.DataFrame:
    """
    Clean and transform urine creatinine data.

    Parameters:
        olis_urine_table (pd.DataFrame): DataFrame containing urine creatinine data.
        code_list (list): List of observation codes to filter the data.

    Returns:
        pd.DataFrame: Cleaned and transformed urine creatinine data.
    """
    non_ratio_codes = {"1754-1", "14683-7", "14957-5", "XON10382-0", "XON12400-8"}

    def anydigit(s):
        return any(char.isdigit() for char in s)

    def anyalpha(s):
        return any(char.isalpha() for char in s)

    def anypunct(s):
        return any(char in ".,;:!?-" for char in s)



    # Filter rows based on the condition 'observationcode in (&code_list)'
    olis_creatinine = olis_urine_table[olis_urine_table['observationcode'].isin(code_list)]

    # Extracting observationdate from observationdatetime
    olis_creatinine['observationdate'] = pd.to_datetime(olis_creatinine['observationdatetime']).dt.date

    # Extracting year from observationdate
    olis_creatinine['year'] = pd.to_datetime(olis_creatinine['observationdate']).dt.year

    # Assuming 'non_ratio_codes' is a list containing non-ratio codes
    non_ratio_codes = ["1754-1", "14683-7", "14957-5", "XON10382-0", "XON12400-8"]

    # apply the above function;
    olis_creatinine[['value_derived_d','subvalue_derived_d']] = olis_creatinine['value'].apply(clean_sup_data)
    olis_creatinine.value_derived_d= pd.to_numeric(olis_creatinine.value_derived_d, errors='coerce')
    
    # Filter rows based on the condition 'observationcode in (&non_ratio_codes.)'
    non_ratio_olis_creatinine = olis_creatinine[olis_creatinine['observationcode'].isin(non_ratio_codes)]
    non_ratio_olis_creatinine['value_derived_d'] = np.nan
    non_ratio_olis_creatinine['subvalue_derived_d'] = ''

    # Filter rows based on observation code not in non_ratio_codes
    olis_creatinine = olis_creatinine[olis_creatinine['observationcode'].notin(non_ratio_codes)]

    # Removing rows with null values in 'value' column
    non_ratio_olis_creatinine = non_ratio_olis_creatinine.dropna(subset=['value'])

    # Converting 'value' column to numeric
    non_ratio_olis_creatinine['value'] = pd.to_numeric(non_ratio_olis_creatinine['value'], errors='coerce')
    
    outdata = pd.concat([non_ratio_olis_creatinine, olis_creatinine],axis=1)

    # Dropping unnecessary columns
    outdata.drop(columns=['observationdatetime'], inplace=True)

    return outdata

# %%
if __name__ == '__main__':

    # setup
    projectPath = Path(os.getcwd())
    dataFile = projectPath / ".." / "Data/olis_urine.sas7bdat"
    # read in the dataset
    dat1 = pd.read_sas(dataFile, encoding='latin1')

    #%%
    dat1.columns= dat1.columns.str.lower()
    # test couple of things first
    t1 = pd.DataFrame()
    t1['value_derived'],t1['subvalue_derived_d'] = zip(*dat1.value.apply(clean_sup_data))

    t1 = pd.concat([t1,dat1[['value']]], axis=1)
    # send in the data from cleaningcolumns=['value_encoded','subvalue_derived_d']

    # %% Runn the function
    
    #%%
    t2 = t1[t1.value.str.len()>7]
    t2.value_derived = pd.to_numeric(t2.value_derived,errors='coerce')
    t2 [t2.value_derived == -88888888.0]
    
    # %%
    t3 = t2[t2.value_derived.isna()].value.value_counts().reset_index().rename(columns={'index':'issue'}).sort_values('value', ascending=False)

# %%
clean_sup_data(val1)
# %%
