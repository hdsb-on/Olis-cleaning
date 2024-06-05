# %%
import pandas as pd
import numpy as np
import re

# %%
cdiff_data = pd.read_sas("D:\\Users\\HDSB\\Projects\\Olis_cleaning\\Data\\olis_cdiff.sas7bdat", encoding="latin1")
cdiff_data['VALUE_ENCODED'] = cdiff_data['VALUE']

df = cdiff_data.copy(deep = True)


# %% [markdown]
# Connected to Python 3.11.9

# %%
import pandas as pd
import numpy as np
import re

# %%
cdiff_data = pd.read_sas("D:\\Users\\HDSB\\Projects\\Olis_cleaning\\Data\\olis_cdiff.sas7bdat", encoding="latin1")
cdiff_data['VALUE_ENCODED'] = cdiff_data['VALUE']

df = cdiff_data.copy(deep = True)

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    #positive conditions
    conditions_p = [
        "POSITIVE" in value,
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        ("DETECTED" in value and "NOT DETECTED" not in value),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111

    conditions_n = [
        "NEGATIVE" in value,
        "NOT DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    value = value.lower()

    conditions_i = [
        "this is a qualitative test" in value,
        "if stool sample test is positive for clostridium difficile toxin" in value,
        "vre screening not performed patient has previously tested vre positive" in value
    ]

    if any(conditions_i):
        return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "unacceptable" in value,
        "unsatisfactory" in value,
        "unsuitable" in value,
        "inappropriate" in value,
        "insufficient" in value,
        "non sufficient" in value,
        "rejected" in value,
        "not processed" in value,
        "not be processed" in value,
        "not performed" in value,
        "not tested" in value,
        "unable to process" in value,
        "test not performed" in value,
        "testing not performed" in value,
        "this test has not been performed" in value,
        "test not done" in value,
        "no specimen" in value,
        "no stool specimen" in value,
        "specimen not received" in value,
        "no sample received" in value,
        "urine specimen" in value,
        "specimen leaking" in value,
        "incorrect container" in value,
        "small amount" in value,
        "not enough sample" in value,
        "only diarrheal stools will be tested" in value,
        "repeat testing is not routinely performed within 7 days" in value,
        "specimens are only accepted at 7 day" in value,
        "c difficile testing on children" in value,
        "formed stool" in value,
        "please recollect" in value,
        "testing not indicated" in value,
        "c difficile toxin gene not done" in value,
        "c difficile toxin test has been cancelled" in value,
        "cancelled by lab specimen was not received" in value,
        "cancelled c difficile testing will only be done once" in value,
        "reason for rejection" in value,
        "stool consistency does not meet criteria" in value,
        "not sufficient quantity" in value,
        "this assay is not approved to test" in value,
        "specimen discarded" in value,
        "should not be tested" in value,
        "np" in value
    ]

    if subvalue_derived == np.nan and any(conditions_r):
        return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
df[['SUBVALUE_DERIVED', 'VALUE_DERIVED']] = df['VALUE'].apply(clean_value_p).apply(pd.Series)

# %%
df['SUBVALUE_DERIVED'].value_counts(dropna=False)

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    #positive conditions
    conditions_p = [
        "POSITIVE" in value,
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        ("DETECTED" in value and "NOT DETECTED" not in value),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111

    conditions_n = [
        "NEGATIVE" in value,
        "NOT DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    value = value.lower()

    conditions_i = [
        "this is a qualitative test" in value,
        "if stool sample test is positive for clostridium difficile toxin" in value,
        "vre screening not performed patient has previously tested vre positive" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "unacceptable" in value,
        "unsatisfactory" in value,
        "unsuitable" in value,
        "inappropriate" in value,
        "insufficient" in value,
        "non sufficient" in value,
        "rejected" in value,
        "not processed" in value,
        "not be processed" in value,
        "not performed" in value,
        "not tested" in value,
        "unable to process" in value,
        "test not performed" in value,
        "testing not performed" in value,
        "this test has not been performed" in value,
        "test not done" in value,
        "no specimen" in value,
        "no stool specimen" in value,
        "specimen not received" in value,
        "no sample received" in value,
        "urine specimen" in value,
        "specimen leaking" in value,
        "incorrect container" in value,
        "small amount" in value,
        "not enough sample" in value,
        "only diarrheal stools will be tested" in value,
        "repeat testing is not routinely performed within 7 days" in value,
        "specimens are only accepted at 7 day" in value,
        "c difficile testing on children" in value,
        "formed stool" in value,
        "please recollect" in value,
        "testing not indicated" in value,
        "c difficile toxin gene not done" in value,
        "c difficile toxin test has been cancelled" in value,
        "cancelled by lab specimen was not received" in value,
        "cancelled c difficile testing will only be done once" in value,
        "reason for rejection" in value,
        "stool consistency does not meet criteria" in value,
        "not sufficient quantity" in value,
        "this assay is not approved to test" in value,
        "specimen discarded" in value,
        "should not be tested" in value,
        "np" in value
    ]

    if subvalue_derived == np.nan and any(conditions_r):
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
df['SUBVALUE_DERIVED'].value_counts(dropna=False)

# %%
sas_cdiff_data_partA = pd.read_sas("D:\\Users\\HDSB\\Projects\\Olis_cleaning\\indata\\cdiff_clean_parta.sas7bdat", encoding="latin1")

# %%
sas_cdiff_data_partA['subvalue_derived'].value_counts(dropna=False)

# %%
sas_cdiff_data_partA

# %%
sas_cdiff_data_partA.columns = sas_cdiff_data_partA.columns.str.upper()

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    #positive conditions
    conditions_p = [
        "POSITIVE" in value,
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        ("DETECTED" in value and "NOT DETECTED" not in value),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111

    conditions_n = [
        "NEGATIVE" in value,
        "NOT DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    value = value.lower()

    conditions_i = [
        "this is a qualitative test" in value,
        "if stool sample test is positive for clostridium difficile toxin" in value,
        "vre screening not performed patient has previously tested vre positive" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "unacceptable" in value,
        "unsatisfactory" in value,
        "unsuitable" in value,
        "inappropriate" in value,
        "insufficient" in value,
        "non sufficient" in value,
        "rejected" in value,
        "not processed" in value,
        "not be processed" in value,
        "not performed" in value,
        "not tested" in value,
        "unable to process" in value,
        "test not performed" in value,
        "testing not performed" in value,
        "this test has not been performed" in value,
        "test not done" in value,
        "no specimen" in value,
        "no stool specimen" in value,
        "specimen not received" in value,
        "no sample received" in value,
        "urine specimen" in value,
        "specimen leaking" in value,
        "incorrect container" in value,
        "small amount" in value,
        "not enough sample" in value,
        "only diarrheal stools will be tested" in value,
        "repeat testing is not routinely performed within 7 days" in value,
        "specimens are only accepted at 7 day" in value,
        "c difficile testing on children" in value,
        "formed stool" in value,
        "please recollect" in value,
        "testing not indicated" in value,
        "c difficile toxin gene not done" in value,
        "c difficile toxin test has been cancelled" in value,
        "cancelled by lab specimen was not received" in value,
        "cancelled c difficile testing will only be done once" in value,
        "reason for rejection" in value,
        "stool consistency does not meet criteria" in value,
        "not sufficient quantity" in value,
        "this assay is not approved to test" in value,
        "specimen discarded" in value,
        "should not be tested" in value,
        "np" in value
    ]

    if subvalue_derived == np.nan and any(conditions_r):
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
sas_cdiff_data_partA[['SUBVALUE_DERIVED_P', 'VALUE_DERIVED_P']] = sas_cdiff_data_partA['VALUE'].apply(clean_value_p).apply(pd.Series)

# %%
sas_cdiff_data_partA.columns

# %%
sas_cdiff_data_partA['SUBVALUE_DERIVED_P'].value_counts(dropna=False)

# %%
sas_cdiff_data_partA['SUBVALUE_DERIVED'].value_counts(dropna=False)

# %%
pd.set_option('display.max_colwidth', None)

# %%
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# %%
sas_cdiff_data_partA.fillna('Na', inplace=True)

# %%
sas_diff_notna = sas_cdiff_data_partA[sas_cdiff_data_partA['SUBVALUE_DERIVED'] != sas_cdiff_data_partA['SUBVALUE_DERIVED_P']]

# %%
sas_diff_notna['SUBVALUE_DERIVED'].value_counts()

# %%
sas_diff_notna['SUBVALUE_DERIVED_P'].value_counts()

# %%
sas_diff_notna3 = sas_diff_notna[['VALUE','SUBVALUE_DERIVED','SUBVALUE_DERIVED_P']]

# %%
sas_diff_notna3_d = sas_diff_notna3.drop_duplicates()

# %%
sas_diff_notna3_d.shape[0]

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value,
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        ("DETECTED" in value and "NOT DETECTED" not in value),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111

    conditions_n = [
        "NEGATIVE" in value,
        "NOT DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" in value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
sas_diff_notna3_d['SUBVALUE_DERIVED'].value_counts()

# %%
sas_diff_notna3_d['SUBVALUE_DERIVED_P'].value_counts()

# %%
def clean_value_re(value):
    value = str(value).strip().upper() 
    subvalue_derived, value_derived = np.nan, np.nan

    pattern_p = re.compile(r"(POSITIVE|POS|CRITICAL\s+RESULTS|DETECTED|TOXIN\s+GENE\s+P)")

    # Check if any positive condition matches using re.search
    if re.search(pattern_p, value):
        subvalue_derived = 'P'
        value_derived = 11111111

    pattern_n = re.compile(r"(NEGATIVE|NOT\s+DETECTED|NO\s+\w+\s+DETECTED|NEG|\s+ND\s+|NO\s+\w+\s+TOXIN|NO\s+\w+\s+CYTOTOXIN|TOXINNEG|)")

    if re.search(pattern_n, value):
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" in value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    return (subvalue_derived, value_derived)

# %%
sas_cdiff_data_partA[['SUBVALUE_DERIVED_P_RE', 'VALUE_DERIVED_P_RE']] = sas_cdiff_data_partA['VALUE'].apply(clean_value_re).apply(pd.Series)

# %%
sas_cleaned_cdiff = pd.read_sas("D:\\Users\\HDSB\\Projects\\Olis_cleaning\\sas_cleaned_data\\cdiff_clean.sas7bdat", encoding="latin1")

# %%
sas_cleaned_cdiff.columns

# %%
sas_cleaned_cdiff[sas_cleaned_cdiff['subvalue_derived_d']==np.nan][:100]

# %%
sas_cleaned_cdiff['subvalue_derived_d'].value_counts(dropna=False)

# %%
send = sas_diff_notna3_d[sas_diff_notna3_d['SUBVALUE_DERIVED']=='Na'][:100]

# %%
send.to_excel("Subvalue_derived_values.xlsx", index=False)

#%%
import pandas as pd
import numpy as np
import re

# %%
clean_value_p("Coagulase Negative Staphylococcus isolated. (two types) \.br\Contamination cannot be ruled out.")

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value,
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        ("DETECTED" in value and "NOT DETECTED" not in value),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" in value,
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" in value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value,
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        ("DETECTED" in value and "NOT DETECTED" not in value),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" in value[0],
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" in value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value[0],
        "POSITIVE" in value[-1],
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        ("DETECTED" in value and "NOT DETECTED" not in value),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" in value[0],
        "NEGATIVE" in value[-1]
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" in value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

#%%
import pandas as pd
import numpy as np
import re

#%%
sas_cdiff_data_partA = pd.read_sas("D:\\Users\\HDSB\\Projects\\Olis_cleaning\\indata\\cdiff_clean_parta.sas7bdat", encoding="latin1")

# %%
sas_diff_notna3_d[sas_diff_notna3_d['SUBVALUE_DERIVED']=='Na'].shape[0]

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value[0],
        "POSITIVE" in value[-1],
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        ("DETECTED" in value and "NOT DETECTED" not in value),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" in value[0],
        "NEGATIVE" in value[-1]
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" == value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value[0],
        "POSITIVE" in value[-1],
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        ("DETECTED" in value and "NOT DETECTED" not in value),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" in value[0],
        "NEGATIVE" in value[-1],
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" == value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value[0],
        "POSITIVE" in value[-1],
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        ("DETECTED" in value and "NOT DETECTED" not in value),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" in value[0],
        "NEGATIVE" in value[-1],
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" in value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value[0],
        "POSITIVE" in value[-1],
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        ("DETECTED" in value and "NOT DETECTED" not in value),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" in value[0],
        "NEGATIVE" in value[-1],
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" == value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value[0],
        "POSITIVE" in value[-1],
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        (value.find("DETECTED") > -1 and value.find("NOT") > value.find("DETECTED")),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" in value[0],
        "NEGATIVE" in value[-1],
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" == value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
sas_diff_notna3_d[sas_diff_notna3_d['SUBVALUE_DERIVED']=='Na']

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value[0],
        "POSITIVE" in value[-1],
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        (value.find("DETECTED") > -1 and 
        (value.find("NOT") > value.find("DETECTED") or value.find("NO") > value.find("DETECTED"))),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" in value[0],
        "NEGATIVE" in value[-1],
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" == value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
sas_diff_notna3_d[sas_diff_notna3_d['SUBVALUE_DERIVED']=='Na'].shape[0]

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value[0],
        "POSITIVE" in value[-1],
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        (value.find("DETECTED") > -1 and 
        (value.find("NOT") > value.find("DETECTED") and value.find("NO") > value.find("DETECTED"))),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" in value[0],
        "NEGATIVE" in value[-1],
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" == value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
sas_diff_notna3_d[sas_diff_notna3_d['SUBVALUE_DERIVED']=='Na'].to_excel("Sas_NA_Py_NotNA.xlsx")

# %%
sas_diff_notna3_d[sas_diff_notna3_d['SUBVALUE_DERIVED_P']=='Na'].shape[0]

# %%
sas_diff_notna3_d[sas_diff_notna3_d['SUBVALUE_DERIVED_P']=='Na'][:100]

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value.split()[0],
        "POSITIVE" in value.split()[-1],
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        (value.find("DETECTED") > -1 and 
        (value.find("NOT") > value.find("DETECTED") and value.find("NO") > value.find("DETECTED"))),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" in value[0],
        "NEGATIVE" in value[-1],
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" == value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value,
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        (value.find("DETECTED") > -1 and 
        (value.find("NOT") > value.find("DETECTED") and value.find("NO") > value.find("DETECTED"))),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" in value.split()[0],
        "NEGATIVE" in value.split()[-1],
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" == value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
sas_diff_notna3_d[sas_diff_notna3_d['SUBVALUE_DERIVED']=='Na']

# %%
sas_diff_notna3_d[(sas_diff_notna3_d['SUBVALUE_DERIVED']=='Na') & (sas_diff_notna3_d['SUBVALUE_DERIVED_P']=='P')]

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value,
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        (value.find("DETECTED") > -1 and 
        (value.find("NOT") > value.find("DETECTED") and value.find("NO") > value.find("DETECTED"))),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" == value.split()[0],
        "NEGATIVE" == value.split()[-1],
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" == value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
sas_diff_notna3_d[sas_diff_notna3_d['SUBVALUE_DERIVED_P']=='Na'][:100]

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value,
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        # (value.find("DETECTED") > -1 and 
        # (value.find("NOT") > value.find("DETECTED") and value.find("NO") > value.find("DETECTED"))),
        re.search(r'(?<!\b(NO|NOT)).*DETECTED', value),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" == value.split()[0],
        "NEGATIVE" == value.split()[-1],
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" == value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
clean_value_p("COVID-19 virus DETECTED by real-time PCR.\.br\Testing Site: London Health Sciences Centre, Microbiology/Virology Laboratory, 8-10 Victoria Hospital, 800 Commissioners Road East, London, Ontario N0A 5W9")

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value,
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        (value.find("DETECTED") > -1 and 
        (value.find("NOT") > value.find("DETECTED") and value.find("NO") > value.find("DETECTED"))),
        (value.find("DETECTED") > -1 and value.find("NOT") == -1 and value.find("NO")==-1),
        # re.search(r'(?<!\b(NO|NOT)).*DETECTED', value),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" == value.split()[0],
        "NEGATIVE" == value.split()[-1],
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" == value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
sas_diff_notna3_d[sas_diff_notna3_d['SUBVALUE_DERIVED']=='Na'].shape[0]

# %%
sas_diff_notna3_d[sas_diff_notna3_d['SUBVALUE_DERIVED']=='Na']

# %%
sas_diff_notna3_d[sas_diff_notna3_d['SUBVALUE_DERIVED_P']=='Na'].shape[0]

# %%
sas_diff_notna3_d[sas_diff_notna3_d['SUBVALUE_DERIVED_P']=='Na']

# %%
clean_value_p("Epstein Barr Virus detected. \.br\1.08E4 IU/mL \.br\(Tested using : altona Diagnostics RealStar EBV PCR Kit 1.0. \.br\Molecular amplification assays to be interpreted only in conjunction with clinical findings")

# %%
value = "Epstein Barr Virus detected. \.br\1.08E4 IU/mL \.br\(Tested using : altona Diagnostics RealStar EBV PCR Kit 1.0. \.br\Molecular amplification assays to be interpreted only in conjunction with clinical findings"

# %%
clean_value_p(value)

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value,
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        (value.find("DETECTED") > -1 and 
        (value.find("NOT") > value.find("DETECTED") and value.find("NO") > value.find("DETECTED"))),
        (value.find("DETECTED") > -1 and value.find("NOT") == -1 and value.find("NO")==-1),
        # re.search(r'(?<!\b(NO|NOT)).*DETECTED', value),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" == value.split()[0],
        "NEGATIVE" == value.split()[-1],
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" == value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value,
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        (value.find("DETECTED") > -1 and 
        (value.find("NOT") > value.find("DETECTED") and value.find("NO") > value.find("DETECTED"))),
        (value.find("DETECTED") > -1 and value.find("NOT") == -1 and value.find("NO")==-1),
        # re.search(r'(?<!\b(NO|NOT)).*DETECTED', value),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" == value.split()[0],
        "NEGATIVE" == value.split()[-1],
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" == value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
(value.find("DETECTED") > -1 and value.find("NOT") == -1 and value.find("NO")==-1)

# %%
value = str(value).strip().upper()

# %%
value

# %%
value.find("DETECTED") > -1

# %%
value.find("NOT") == -1

# %%
value.find("NO")==-1

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value,
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        (value.find("DETECTED") > -1 and 
        (value.find("NOT") > value.find("DETECTED") and value.find("NO") > value.find("DETECTED"))),
        (value.find("DETECTED") > -1 and value.find("NOT ") == -1 and value.find("NO ")==-1),
        # re.search(r'(?<!\b(NO|NOT)).*DETECTED', value),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" == value.split()[0],
        "NEGATIVE" == value.split()[-1],
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000

    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" == value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777        
    
    return (subvalue_derived, value_derived)

# %%
sas_diff_notna3_d[sas_diff_notna3_d['SUBVALUE_DERIVED']=='Na']

# %%
sas_cleaned_cdiff = pd.read_sas("D:\\Users\\HDSB\\Projects\\Olis_cleaning\\sas_cleaned_data\\cdiff_clean.sas7bdat", encoding="latin1")

# %%
sas_cleaned_cdiff.columns = sas_cleaned_cdiff.columns.str.upper()

# %%
sas_cleaned_cdiff.columns

# %%
sas_cleaned_cdiff[['SUBVALUE_DERIVED_P', 'VALUE_DERIVED_P']] = sas_cleaned_cdiff['VALUE'].apply(clean_value_p).apply(pd.Series)

# %%
sas_cleaned_cdiff['SUBVALUE_DERIVED_P'].value_counts(dropna=False)

# %%
sas_cleaned_cdiff['SUBVALUE_DERIVED_D'].value_counts(dropna=False)

# %%
sas_cleaned_cdiff.fillna('Na', inplace=True)

# %%
sas_cdiff_diff = sas_cleaned_cdiff[sas_cleaned_cdiff['SUBVALUE_DERIVED_D'] != sas_cleaned_cdiff['SUBVALUE_DERIVED_P']]

# %%
sas_cdiff_diff['SUBVALUE_DERIVED_D'].value_counts()

# %%
sas_cdiff_diff['SUBVALUE_DERIVED_P'].value_counts()

# %%
sas_cdiff_diff_d = sas_cdiff_diff[['VALUE','SUBVALUE_DERIVED_D','SUBVALUE_DERIVED_P']]

# %%
sas_cdiff_diff_d3 = sas_cdiff_diff_d.drop_duplicates()

# %%
sas_cdiff_diff_d3.shape[0]

# %%
sas_cdiff_diff_d3['SUBVALUE_DERIVED_D'].value_counts()

# %%
sas_cdiff_diff_d3['SUBVALUE_DERIVED_P'].value_counts()

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value,
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        (value.find("DETECTED") > -1 and 
        (value.find("NOT") > value.find("DETECTED") and value.find("NO") > value.find("DETECTED"))),
        (value.find("DETECTED") > -1 and value.find("NOT ") == -1 and value.find("NO ")==-1),
        # re.search(r'(?<!\b(NO|NOT)).*DETECTED', value),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" == value.split()[0],
        "NEGATIVE" == value.split()[-1],
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111


    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" == value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777  

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i) or subvalue_derived == np.nan:
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000      
    
    return (subvalue_derived, value_derived)

# %%
def clean_value_p(value):
    value = str(value).strip().upper()
    subvalue_derived, value_derived = np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "POSITIVE" in value,
        "TOXIN POS" in value,
        "TOXIN TESTING POSITIVE" in value,
        "C DIFFICILE TESTING POS" in value,
        "CYTOTOXIN PCR POSITIVE" in value,
        (value.find("DETECTED") > -1 and 
        (value.find("NOT") > value.find("DETECTED") and value.find("NO") > value.find("DETECTED"))),
        (value.find("DETECTED") > -1 and value.find("NOT ") == -1 and value.find("NO ")==-1),
        # re.search(r'(?<!\b(NO|NOT)).*DETECTED', value),
        ("CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" in value and "NO CLOSTRIDIUM DIFFICILE TOXIN DETECTED BY PCR" not in value),
        "CRITICAL RESULTS" in value,
        "FINAL INTERPRETATION TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE P" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111



    conditions_n = [
        "NEGATIVE" == value.split()[0],
        "NEGATIVE" == value.split()[-1],
        "NOT DETECTED" in value,
        "NON-DETECTED" in value,
        "C DIFFICILE TOXIN TESTING NEG" in value,
        "C DIFFICILE TESTING NEG" in value,
        "TEST NO TOXIGENIC C DIFFICILE DETECTED" in value,
        "C DIFFICILE TOXIN GENE ND" in value,
        "C DIFFICILE TOXIN GENE NEGATIVE" in value,
        "C DIFFICILE TOXIN NEGATIVE" in value,
        "NO C DIFFICILE TOXIN GENE DETECTED" in value,
        "CYTOTOXIN PCR NEGATIVE" in value,
        "TOXIGENIC C DIFFICILE NEGATIVE" in value,
        "NO CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "NO CLOSTRIDIUM DIFFICILE CYTOTOXIN" in value,
        ("ANTIGENPOS" in value and "TOXINNEG" in value),
        ("ANTIGENNEG" in value and "TOXINNEG" in value),
        "THE CORRECT RESULT IS:\\.BR\\NEGATIVE" in value,
        "TOXIN NOT\\.BR\\DETECTED" in value,
        "TOXIN NOT\\E\\.BR\\E\\DETECTED" in value,
        "FINAL INTERPRETATION NO TOXIGENIC C DIFFICILE DETECTED" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111


    conditions_r = [
        "UNACCEPTABLE" in value,
        "UNSATISFACTORY" in value,
        "UNSUITABLE" in value,
        "INAPPROPRIATE" in value,
        "INSUFFICIENT" in value,
        "NON SUFFICIENT" in value,
        "REJECTED" in value,
        "NOT PROCESSED" in value,
        "NOT BE PROCESSED" in value,
        "NOT PERFORMED" in value,
        "NOT TESTED" in value,
        "UNABLE TO PROCESS" in value,
        "TEST NOT PERFORMED" in value,
        "TESTING NOT PERFORMED" in value,
        "THIS TEST HAS NOT BEEN PERFORMED" in value,
        "TEST NOT DONE" in value,
        "NO SPECIMEN" in value,
        "NO STOOL SPECIMEN" in value,
        "SPECIMEN NOT RECEIVED" in value,
        "NO SAMPLE RECEIVED" in value,
        "URINE SPECIMEN" in value,
        "SPECIMEN LEAKING" in value,
        "INCORRECT CONTAINER" in value,
        "SMALL AMOUNT" in value,
        "NOT ENOUGH SAMPLE" in value,
        "ONLY DIARRHEAL STOOLS WILL BE TESTED" in value,
        "REPEAT TESTING IS NOT ROUTINELY PERFORMED WITHIN 7 DAYS" in value,
        "SPECIMENS ARE ONLY ACCEPTED AT 7 DAY" in value,
        "C DIFFICILE TESTING ON CHILDREN" in value,
        "FORMED STOOL" in value,
        "PLEASE RECOLLECT" in value,
        "TESTING NOT INDICATED" in value,
        "C DIFFICILE TOXIN GENE NOT DONE" in value,
        "C DIFFICILE TOXIN TEST HAS BEEN CANCELLED" in value,
        "CANCELLED BY LAB SPECIMEN WAS NOT RECEIVED" in value,
        "CANCELLED C DIFFICILE TESTING WILL ONLY BE DONE ONCE" in value,
        "REASON FOR REJECTION" in value,
        "STOOL CONSISTENCY DOES NOT MEET CRITERIA" in value,
        "NOT SUFFICIENT QUANTITY" in value,
        "THIS ASSAY IS NOT APPROVED TO TEST" in value,
        "SPECIMEN DISCARDED" in value,
        "SHOULD NOT BE TESTED" in value,
        "NP" == value
    ]

    if any(conditions_r):
        #return ('N', -11111111)
        subvalue_derived = 'R'
        value_derived = -77777777

    # if subvalue_derived == np.nan and any(conditions_r):
    #     #return ('R', -77777777)
    #     subvalue_derived = 'R'
    #     value_derived = -77777777

    if "this test has not been performed" in value or "test not performed" in value:
        #return ('R', -77777777)
        subvalue_derived = 'R'
        value_derived = -77777777  

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i) or subvalue_derived == nan:
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000      
    
    return (subvalue_derived, value_derived)


