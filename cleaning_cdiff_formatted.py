#%%
# from curses.ascii import ispunct
import pandas as pd
import numpy as np
import re
import os
from pathlib import Path

#NOTE: I have not considered value_encoded in the clean_value_p function, only value
#%%
def clean_value_p(row):

    #Derive free text
    observationcode = row['observationcode']
    value = row['value'].lower()
    value = str(value).strip().lower()
    subvalue_derived, value_derived, backpriority = np.nan, np.nan, np.nan

    # print(value)

    #positive conditions
    conditions_p = [
        "positive" in value,
        "toxin pos" in value,
        "toxin testing positive" in value,
        "c difficile testing pos" in value,
        "cytotoxin pcr positive" in value,
        (value.find("detected") > -1 and 
        (value.find("not") > value.find("detected") or value.find("no") > value.find("detected"))),
        (value.find("detected") > -1 and value.find("not ") == -1 and value.find("no ")==-1),
        # re.search(r'(?<!\b(NO|NOT)).*DETECTED', value),
        ("clostridium difficile toxin detected by pcr" in value and "no clostridium difficile toxin detected by pcr" not in value),
        "critical results" in value,
        "final interpretation toxigenic c difficile detected" in value,
        "c difficile toxin gene p" in value
    ]

    if any(conditions_p):
        #return ('P', 11111111)
        subvalue_derived = 'P'
        value_derived = 11111111
        backpriority = 4



    conditions_n = [
        value.startswith("negative"),
        "negative" == value.split()[-1],
        "not detected" in value,
        "non-detected" in value,
        "c difficile toxin testing neg" in value,
        "c difficile testing neg" in value,
        "test no toxigenic c difficile detected" in value,
        "c difficile toxin gene nd" in value,
        "c difficile toxin gene negative" in value,
        "c difficile toxin negative" in value,
        "no c difficile toxin gene detected" in value,
        "cytotoxin pcr negative" in value,
        "toxigenic c difficile negative" in value,
        "no clostridium difficile toxin" in value,
        "no clostridium difficile cytotoxin" in value,
        ("antigenpos" in value and "toxinneg" in value),
        ("antigenneg" in value and "toxinneg" in value),
        "the correct result is:\\.br\\negative" in value,
        "toxin not\\.br\\detected" in value,
        "toxin not\\e\\.br\\e\\detected" in value,
        "final interpretation no toxigenic c difficile detected" in value,
        "no hiv p24 antigen" in value
    ]
    
    if any(conditions_n):
        #return ('N', -11111111)
        subvalue_derived = 'N'
        value_derived = -11111111
        backpriority = 3


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
        "np" == value
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
        backpriority = 2  

    conditions_i = [
        "this is a qualitative test" in value,
        "if stool sample test is positive for clostridium difficile toxin" in value,
        "vre screening not performed patient has previously tested vre positive" in value, 
        "parvovirus b19 igg antibodies detected" in value,
        "unable to quantify" in value,
        "source: bld aerobic 2\.br\microscopic: gram-negative bacilli" in value,
        "source: bld aerobic\.br\microscopic: gram-negative bacilli" in value
    ]

    if any(conditions_i):
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000
        backpriority = 1

    #Snomed codes 

    #Reset for LOINC 41852-5 only - use Snomed. Others=I
    if observationcode == "41852-5":
        subvalue_derived = ""
        value_derived = np.nan

    if '<p1:microorganism xmlns:p1="http://www.ssha.ca">' in value:
        if "12671002" in value or "5933001" in value or "96001009" in value:
            subvalue_derived = "P"
            value_derived = 11111111
        elif "854906661000087000" in value or "854906661000087105" in value:
            subvalue_derived = "N"
            value_derived = -11111111
        else:
            subvalue_derived = "I"
            value_derived = -66660000

    #codes for specific loinc

    #Specific codes for 34713-8 - Overwrite;
	#previously reported and therefore specimen not processed;
    if observationcode == "34713-8":
        if "patient was previously reported as" in value:
            subvalue_derived = "R"
            value_derived = -77777777
        
        if "this is a corrected report" in value and "c. difficile cytotoxin (pcr) positive by rt pcr" in value:
            subvalue_derived = "P"
            value_derived = 11111111

    #Specific codes for 34468-9
    if observationcode == "34468-9":
        if "eia screen test negative" in value \
           or "clostridioides difficile negative" in value \
           or "TOXIGENIC CLOSTRIDIODES DIFFICILE NOT DETECTED" in value.upper() \
           or "specimen is negative for clostridium difficile" in value:
            subvalue_derived = "N"
            value_derived = -11111111
        
        if "CRITICAL VALUE" in value.upper() \
           or "TOXIGENIC CLOSTRIDIODES DIFFICILE DETECTED" in value.upper():
            subvalue_derived = "P"
            value_derived = 11111111

    #Specific codes for 54067-4
    if observationcode == "54067-4":
        if "NP CLOSTRIDIUM DIFFICILE TOXIN" in value.upper() \
           or "c difficile result negative" in value.lower():
            subvalue_derived = "N"
            value_derived = -11111111
        
        if "critical result alert" in value.lower():
            subvalue_derived = "P"
            value_derived = 11111111
        
        # From previous Bogdan's cleaning
        if "RESULTS BROADCAST TO" in value.upper() \
           or "CALLED RESULTS TO" in value.upper() \
           or "RESULT PHONED TO" in value.upper():
            subvalue_derived = "P"
            value_derived = 11111111

    #Specific codes for 34712-0
    if observationcode == "34712-0" and ("previously negative" in value or "previously positive" in value):
        subvalue_derived = "R"
        value_derived = -77777777       

    #Specific codes for 61367-9
    if observationcode == "61367-9" and "toxigenic clostridioides difficile dna detected" in value:
        subvalue_derived = "P"
        value_derived = 11111111

    #Specific codes for 6365-1
    if observationcode == "6365-1" and "no clostridioides formerly clostridium difficile toxin b gene tcdb dna detected" in value:
        subvalue_derived = "N"
        value_derived = -11111111
    
    #Specific codes for XON12821-5
    if observationcode == "XON12821-5":
        if "note confirmed" in value:
            subvalue_derived = "P"
            value_derived = 11111111
        elif "note previous" in value:
            subvalue_derived = "I"
            value_derived = -66660000

    #Specific codes for XON10441-4 and overwrite
    if observationcode == "XON10441-4" and "REASON FOR REJECTION" in value.upper():
        subvalue_derived = "R"
        value_derived = -77777777
    
    #Specific codes for XON10842-3
    if observationcode == "XON10842-3":
        if "supportive" in value and "not" not in value:
            subvalue_derived = "P"
            value_derived = 11111111
        elif "supportive" in value and "not" in value:
            subvalue_derived = "N"
            value_derived = -11111111

    #Specific codes for XON12338-0
    if observationcode == "XON12338-0" and "equivocal result" in value:
        if "toxin gene not detected" in value:
            subvalue_derived = "N"
            value_derived = -11111111
        elif "toxin gene detected" in value:
            subvalue_derived = "P"
            value_derived = 11111111
    
    if observationcode == "XON12338-0" and "source stool cd status final" in value:
        if "organism clostridioides formerly clostridium difficile toxin b gene tcdb dna detected" in value \
           or "clostridium difficile toxin b gene tcdb dna detected" in value:
            subvalue_derived = "P"
            value_derived = 11111111
        elif "no clostridioides formerly clostridium difficile toxin b gene tcdb dna detected" in value:
            subvalue_derived = "N"
            value_derived = -11111111

    #Reset and records
    if ("/COMMENT:/" in value.upper()) and ("the presence of c. difficile toxin dna is not diagnostic" in value.lower()):
        subvalue_derived = ""
        value_derived = np.nan
        
        if "TOXIGENIC CLOSTRIDIUM DIFFICILE STRAIN DETECTED" in value.upper():
            subvalue_derived = "P"
            value_derived = 11111111
        elif "NO TOXIGENIC CLOSTRIDIUM DIFFICILE DETECTED" in value.upper():
            subvalue_derived = "N"
            value_derived = -11111111

    #Corrected reports
    if observationcode == "34713-8":
        if "THIS IS A CORRECTED REPORT" in value.upper():
            if "corrected report:\.br\to be tested still" in value:
                subvalue_derived = "CI"
                value_derived = -66660000
            elif "corrected report:\.br\c. difficile cytotoxin (pcr) positive" in value:
                subvalue_derived = "CP"
                value_derived = 11111111
            elif "corrected report:\.br\\.br\c.difficile cytotoxin (pcr): negative" in value:
                subvalue_derived = "CN"
                value_derived = -11111111
        
        elif "updated report" in value.lower():
            if "c difficile cytotoxin pcr positive" in value.lower():
                subvalue_derived = "CP"
                value_derived = 11111111
            elif "c difficile cytotoxin pcr negative" in value.lower():
                subvalue_derived = "CN"
                value_derived = -11111111
            elif "c difficile pcr results invalid" in value.lower() or "specimen in progress" in value.lower():
                subvalue_derived = "CI"
                value_derived = -66660000

    if "corrected report" in value:
        if "previously negative" in value and "previously positive" in value:
            subvalue_derived = "CI"
            value_derived = -66660000
        
        elif any(keyword in value for keyword in ["this is a corrected report clostridium difficile toxin b detected",
                                                  "proved to be c difficile toxin gene positive",
                                                  "proven to be c difficile toxin gene positive",
                                                  "found to be c difficile toxin gene positive",
                                                  "c difficile toxin gene detected",
                                                  "c diff negative result is c difficile positive",
                                                  "c difficile negative result is c difficile toxin gene positive",
                                                  "corrected report clostridioides clostridium difficile toxin b detected"]) \
            or "/positive/" in value:
            subvalue_derived = "CP"
            value_derived = 11111111
        
        elif any(keyword in value for keyword in ["this is a corrected report clostridium difficile not detected",
                                                  "upon further investigation c difficile toxin gene negative",
                                                  "previously reported positive has now been changed to negative",
                                                  "previous report c difficile toxine gene detected negative",
                                                  "previous c diff positive report is repeated to be c diff negative",
                                                  "c difficile toxin gene not detected",
                                                  "this is a corrected report clostridium difficile toxin b not detected"]):
            subvalue_derived = "CN"
            value_derived = -11111111
        
        elif any(keyword in value for keyword in ["no specimen received",
                                                  "no result for this specimen",
                                                  "this test has not been performed"]):
            subvalue_derived = "CR"
            value_derived = -77777777
        
        elif any(keyword in value for keyword in ["specimen will be sent for further testing",
                                                           "this is a modified report previously reported has now been changed",
                                                           "pcr result to follow"]):
            subvalue_derived = "I"
            value_derived = -66660000

    # All others as I
    if pd.isna(value_derived):
        subvalue_derived = "I"
        value_derived = -66660000
    
    
    return pd.Series([subvalue_derived, value_derived, backpriority], index=['subvalue_derived_p', 'value_derived_p', 'backpriority'])
#%%
def assign_backpriority(value):
    if value == "P":
        return 4
    elif value == "N":
        return 3
    elif value == "R":
        return 2
    elif value == "I":
        return 1
    return None

#%%
def cleaning_cdiff(olis_cdiff: pd.DataFrame) -> pd.DataFrame:
    olis_cdiff['value_encoded'] = olis_cdiff['value']

    olis_cdiff[['subvalue_derived_p', 'value_derived_p', 'backpriority']] = olis_cdiff.apply(clean_value_p, axis=1)

    # olis_cdiff.loc[olis_cdiff['value_derived_p'] == pd.NA, 'subvalue_derived_p'] = 'I'
    # olis_cdiff.loc[olis_cdiff['value_derived_p'] == pd.NA, 'value_derived_p'] = -66660000

    #Cleaning 2: 
    # Identify test results that are not valid, invalid_record_flag="Y"
    # Change value to missing

    olis_cdiff2 = pd.DataFrame(olis_cdiff)

    olis_cdiff2['invalid_record_flag'] = pd.NA

    #NOTE: There's no column "invalid_record_flag"
    olis_cdiff2.loc[olis_cdiff2['invalid_record_flag'] == 'Y', 'subvalue_derived_p'] = 'I'
    olis_cdiff2.loc[olis_cdiff2['invalid_record_flag'] == 'Y', 'value_derived_p'] = -66660000

    olis_cdiff2.sort_values(by=['hcn_encrypted', 'ordersid', 'observationdatetime', 'testrequestpositioninorder', 'observationposintestrequest'], inplace=True)

    olis_cdiff3 = pd.DataFrame(olis_cdiff2)

    conditions = [
        (olis_cdiff3['subvalue_derived_p'].isin(['CP', 'P'])),
        (olis_cdiff3['subvalue_derived_p'].isin(['CN', 'N'])),
        (olis_cdiff3['subvalue_derived_p'].isin(['CI', 'I'])),
        (olis_cdiff3['subvalue_derived_p'].isin(['CR', 'R']))
    ]

    choices_value_d = [11111111, -11111111, -66660000, -77777777]
    choices_subvalue_d = ['P', 'N', 'I', 'R']

    olis_cdiff3['value_derived_p'] = np.select(conditions, choices_value_d, default=pd.NA)
    olis_cdiff3['subvalue_derived_p'] = np.select(conditions, choices_subvalue_d, default=pd.NA)

    # Hierarchy P>N>R>I
    conditions_bp = [
        (olis_cdiff3['subvalue_derived_p'] == 'P'),
        (olis_cdiff3['subvalue_derived_p'] == 'N'),
        (olis_cdiff3['subvalue_derived_p'] == 'R'),
        (olis_cdiff3['subvalue_derived_p'] == 'I')
    ]

    choices_bp = [4, 3, 2, 1]

    olis_cdiff3['backpriority'] = np.select(conditions_bp, choices_bp, default=pd.NA)

    # Conclusive column
    olis_cdiff3['conclusive'] = 0
    olis_cdiff3.loc[olis_cdiff2['subvalue_derived_p'].isin(['P', 'N']), 'conclusive'] = 1

    # OrderWithinOrderSid and order columns
    olis_cdiff3['orderwithinordersid'] = olis_cdiff3['testrequestpositioninorder'] * 10000 + olis_cdiff3['observationposintestrequest']
    olis_cdiff3['order'] = olis_cdiff3['conclusive'] * olis_cdiff3['orderwithinordersid']

    olis_cdiff3.sort_values(by=['hcn_encrypted', 'ordersid', 'order', 'backpriority'], inplace=True)

    # Recommended value within OrderSid
    groups = olis_cdiff3.groupby(['hcn_encrypted', 'ordersid', 'order', 'backpriority'])

    for name, group in groups:
        last_index = group.index[-1]  
        olis_cdiff3.loc[last_index, 'subvalue_ordersid_p'] = group['subvalue_derived_p'].iloc[-1] 
        olis_cdiff3.loc[last_index, 'value_ordersid_p'] = group['value_derived_p'].iloc[-1]  


    #NOTE: Different from sas code --> I'm not dropping these columns
    # olis_cdiff4 = olis_cdiff3.drop(columns=['conclusive', 'backpriority', 'order', 'subvalue_derived_p'])
    olis_cdiff4 = pd.DataFrame(olis_cdiff3)

    # Prioritize within hcn_encrypted+ObservationDate
	# Recommended value same observation date
    olis_cdiff4['backpriority'] = olis_cdiff4['subvalue_ordersid_p'].apply(assign_backpriority)

    # Convert observationdatetime to date
    olis_cdiff4['obsdate'] = pd.to_datetime(olis_cdiff4['observationdatetime']).dt.date

    # Ensure the ObsDate is formatted as date
    # olis_cdiff4['ObsDate'] = olis_cdiff4['ObsDate'].apply(lambda x: x.strftime('%Y-%m-%d'))

    olis_cdiff4.sort_values(by=['hcn_encrypted', 'obsdate', 'backpriority'], inplace=True)

    groups = olis_cdiff4.groupby(['hcn_encrypted', 'obsdate', 'backpriority'])

    # Iterate over groups to set subvalue_recommended_d and value_recommended_d
    for name, group in groups:
        last_index = group.index[-1]  # Get index of the last row in each group
        olis_cdiff4.loc[last_index, 'subvalue_recommended_p'] = group['subvalue_ordersid_p'].iloc[-1]  # Assign last subvalue_ordersid_d
        olis_cdiff4.loc[last_index, 'value_recommended_p'] = group['value_ordersid_p'].iloc[-1]  # Assign last value_ordersid_d

    # Handle missing hcn_encrypted
    olis_cdiff4.loc[olis_cdiff4['hcn_encrypted'].isna(), 'subvalue_recommended_p'] = olis_cdiff4['subvalue_ordersid_p']
    olis_cdiff4.loc[olis_cdiff4['hcn_encrypted'].isna(), 'value_recommended_p'] = olis_cdiff4['value_ordersid_p']

    # Drop unnecessary columns
    # olis_cdiff4.drop(columns=['backpriority', 'subvalue_ordersid_p', 'value_ordersid_p', 'obsdate'], inplace=True)

    olis_cdiff4.drop(columns=['backpriority', 'conclusive', 'order', 'subvalue_ordersid_p', 'value_ordersid_p', 'obsdate'], inplace=True)

    outdata = olis_cdiff4.sort_values(by=['hcn_encrypted', 'ordersid', 'testrequestpositioninorder', 'observationposintestrequest'])

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
    dataFile = "D:\\Users\\HDSB\\Projects\\Olis_cleaning\\Data\\olis_cdiff.sas7bdat"

    #%%
    # read in the dataset
    dat1 = pd.read_sas(dataFile, encoding='latin1')
    dat1.columns= dat1.columns.str.lower()

    # %% Run the function
    dat2 = cleaning_cdiff(dat1)
    dat2  = dat2.fillna(value=np.nan)
    #dat2 = python cleaned code
    
    # %% compare the results with that of output from SAS code;
    # resultfile = projectPath / ".." / "sas_cleaned_data/cdiff_clean.sas7bdat"
    resultfile = "D:\\Users\\HDSB\\Projects\\Olis_cleaning\\sas_cleaned_data\\cdiff_clean.sas7bdat"

    res = pd.read_sas(resultfile, encoding='latin1')
    res.columns = res.columns.str.lower()
    #res = sas cleaned code
    
    # %%
    #Code to calculate number of mismatched values between sas and python results
    indexcols = ['ordersid','observationcode','observationdatetime','testrequestpositioninorder','observationposintestrequest']
    sasVsours = (res[ indexcols+ ['value_encoded','value_derived_d','subvalue_derived_d']]
            .rename(columns={"value_derived_d":"res_value", "subvalue_derived_d":"res_subvalue"})
            .merge( dat2[ indexcols + ['value_derived_p','subvalue_derived_p']],
                    how="inner", on=indexcols))
    diff_values = sasVsours[
        ((sasVsours.res_value - sasVsours.value_derived_p).abs() > 10e-6) |
        (sasVsours.res_value.isna() & sasVsours.value_derived_p.notna()) |
        (sasVsours.res_value.notna() & sasVsours.value_derived_p.isna())
    ]
    print("total missmatch in values: ", diff_values.shape[0])
    diff = sasVsours[(sasVsours.res_subvalue !=  sasVsours.subvalue_derived_p) ]
    print ("total missmatch in suvalues" , diff.shape[0])
# %%
