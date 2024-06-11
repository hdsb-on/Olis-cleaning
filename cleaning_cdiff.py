#demo change for github

#import statements
#%%
import pandas as pd
import numpy as np
import re

#%%
# sas_cdiff_data_partA = pd.read_sas("D:\\Users\\HDSB\\Projects\\Olis_cleaning\\indata\\cdiff_clean_parta.sas7bdat", encoding="latin1")

# #%%
# sas_cleaned_cdiff = pd.read_sas("D:\\Users\\HDSB\\Projects\\Olis_cleaning\\sas_cleaned_data\\cdiff_clean.sas7bdat", encoding="latin1")



# %%
def clean_value_p(row):
    observationcode = row['OBSERVATIONCODE']
    value = row['VALUE'].upper()
    value = str(value).strip().upper()
    subvalue_derived, value_derived, backpriority = np.nan, np.nan, np.nan

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
        backpriority = 4



    conditions_n = [
        value.startswith("NEGATIVE"),
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
        backpriority = 3


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
        backpriority = 2  

    conditions_i = [
        "THIS IS A QUALITATIVE TEST" in value,
        "IF STOOL SAMPLE TEST IS POSITIVE FOR CLOSTRIDIUM DIFFICILE TOXIN" in value,
        "VRE SCREENING NOT PERFORMED PATIENT HAS PREVIOUSLY TESTED VRE POSITIVE" in value
    ]

    if any(conditions_i) or pd.isna(subvalue_derived) or observationcode == '41852-5':
        #return ('I', -66660000)
        subvalue_derived = 'I'
        value_derived = -66660000
        backpriority = 1
    
    return pd.Series([subvalue_derived, value_derived, backpriority], index=['SUBVALUE_DERIVED_P', 'VALUE_DERIVED_P', 'BACKPRIORITY'])

        
    
#%%

# def specific_loinc(row):
#     observationcode = row['OBSERVATIONCODE']
#     value = row['VALUE'].upper()
#     subvalue_derived = row['SUBVALUE_DERIVED']
#     value_derived = row['VALUE_DERIVED']

#     if observationcode == "34713-8":
#         if "patient was previously reported as".upper() in value:
#             subvalue_derived = "R"
#             value_derived = -77777777
#         elif "THIS IS A CORRECTED REPORT" in value and "C. DIFFICILE CYTOTOXIN (PCR) POSITIVE BY RT PCR" in value:
#             subvalue_derived = "P"
#             value_derived = 11111111

#     elif observationcode == "34468-9":
#         if any(keyword in value.lower() for keyword in ["eia screen test negative",
#                                                          "clostridioides difficile negative",
#                                                          "specimen is negative for clostridium difficile",
#                                                          "clostridioides difficile not detected"]) :
#             subvalue_derived = "N"
#             value_derived = -11111111
#         elif "CRITICAL VALUE" in value or "TOXIGENIC CLOSTRIDIODES DIFFICILE DETECTED" in value:
#             subvalue_derived = "P"
#             value_derived = 11111111

#     elif observationcode == "54067-4":
#         if "NP CLOSTRIDIUM DIFFICILE TOXIN" in value or "C DIFFICILE RESULT NEGATIVE" in value:
#             subvalue_derived = "N"
#             value_derived = -11111111
#         elif "critical result alert" in value.lower() or "RESULTS BROADCAST TO" in value or "CALLED RESULTS TO" in value or "RESULT PHONED TO" in value:
#             subvalue_derived = "P"
#             value_derived = 11111111

#     elif observationcode == "34712-0":
#         if "previously negative".upper() in value or "previously positive".upper() in value:
#             subvalue_derived = "R"
#             value_derived = -77777777

#     elif observationcode == "61367-9":
#         if "toxigenic clostridioides difficile dna detected".upper() in value:
#             subvalue_derived = "P"
#             value_derived = 11111111

#     elif observationcode == "6365-1":
#         if "no clostridioides formerly clostridium difficile toxin b gene tcdb dna detected".upper() in value:
#             subvalue_derived = "N"
#             value_derived = -11111111

#     elif observationcode == "XON12821-5":
#         if "note confirmed".upper() in value:
#             subvalue_derived = "P"
#             value_derived = 11111111
#         elif "note previous".upper() in value:
#             subvalue_derived = "I"
#             value_derived = -66660000

#     elif observationcode == "XON10441-4":
#         if "REASON FOR REJECTION" in value:
#             subvalue_derived = "R"
#             value_derived = -77777777

#     elif observationcode == "XON10842-3":
#         if 'supportive' in value and 'not' not in value:
#             subvalue_derived = "P"
#             value_derived = 11111111
#         elif 'supportive' in value and 'not' in value:
#             subvalue_derived = "N"
#             value_derived = -11111111
    
#     elif observationcode == "XON12338-0":
#         if 'equivocal result' in value:
#             if 'toxin gene not detected' in value:
#                 subvalue_derived = "N"
#                 value_derived = -11111111
#             elif 'toxin gene detected' in value:
#                 subvalue_derived = "P"
#                 value_derived = 11111111
        
#     elif 'source stool cd status final' in value:
#         if ('organism clostridioides formerly clostridium difficile toxin b gene tcdb dna detected' in value) or ('clostridium difficile toxin b gene tcdb dna detected' in value):
#             subvalue_derived = "P"
#             value_derived = 11111111
#         elif 'no clostridioides formerly clostridium difficile toxin b gene tcdb dna detected' in value:
#             subvalue_derived = "N"
#             value_derived = -11111111        

#     elif re.search(r"/COMMENT:/", value, flags=re.IGNORECASE) and 'the presence of c. difficile toxin dna is not diagnostic' in value.lower():
#         subvalue_derived = ""
#         value_derived = None
        
#         # Check for specific conditions based on uppercase patterns in value_encoded
#         if 'TOXIGENIC CLOSTRIDIUM DIFFICILE STRAIN DETECTED' in value.upper():
#             subvalue_derived = "P"
#             value_derived = 11111111
#         elif 'NO TOXIGENIC CLOSTRIDIUM DIFFICILE DETECTED' in value.upper():
#             subvalue_derived = "N"
#             value_derived = -11111111

#     elif observationcode == "34713-8":
#         if 'this is a corrected report' in value:
#             if 'corrected report:.br\to be tested still' in value:
#                 subvalue_derived = "CI"
#                 value_derived = -66660000
#             elif 'corrected report:.br\c. difficile cytotoxin (pcr) positive' in value:
#                 subvalue_derived = "CP"
#                 value_derived = 11111111
#             elif 'corrected report:.br\\.br\c.difficile cytotoxin (pcr): negative' in value:
#                 subvalue_derived = "CN"
#                 value_derived = -11111111
#         elif 'updated report c difficile cytotoxin pcr positive' in value or 'updated report repeat c difficile cytotoxin pcr c difficile cytotoxin pcr positive' in value:
#             subvalue_derived = "CP"
#             value_derived = 11111111
#         elif 'updated report c difficile cytotoxin pcr negative' in value or 'updated report repeat c difficile cytotoxin pcr negative' in value:
#             subvalue_derived = "CN"
#             value_derived = -11111111
#         elif 'updated report repeat c difficile pcr results invalid' in value or 'updated report specimen in progress' in value:
#             subvalue_derived = "CI"
#             value_derived = -66660000

#     elif 'CORRECTED REPORT' in value.upper():
#         if 'previously negative' in value and 'previously positive' in value:
#             subvalue_derived = "CI"
#             value_derived = -66660000
#         elif any(keyword in value for keyword in [
#             "this is a corrected report clostridium difficile toxin b detected",
#             "proved to be c difficile toxin gene positive",
#             "proven to be c difficile toxin gene positive",
#             "found to be c difficile toxin gene positive",
#             "c difficile toxin gene detected",
#             "c diff negative result is c difficile positive",
#             "c difficile negative result is c difficile toxin gene positive",
#             "corrected report clostridioides clostridium difficile toxin b detected",
#             "positive"
#         ]):
#             subvalue_derived = "CP"
#             value_derived = 11111111
#         elif any(keyword in value for keyword in [
#             "this is a corrected report clostridium difficile not detected",
#             "upon further investigation c difficile toxin gene negative",
#             "previously reported positive has now been changed to negative",
#             "previous report c difficile toxine gene detected negative",
#             "previous c diff positive report is repeated to be c diff negative",
#             "c difficile toxin gene not detected",
#             "this is a corrected report clostridium difficile toxin b not detected"
#         ]):
#             subvalue_derived = "CN"
#             value_derived = -11111111
#         elif any(keyword in value for keyword in [
#             "no specimen received",
#             "no result for this specimen",
#             "this test has not been performed"
#         ]):
#             subvalue_derived = "CR"
#             value_derived = -77777777
#         elif any(keyword in value for keyword in [
#             "specimen will be sent for further testing",
#             "this is a modified report previously reported has now been changed",
#             "pcr result to follow"
#         ]):
#             subvalue_derived = "I"
#             value_derived = -66660000
    
#     elif value_derived is None:
#         subvalue_derived = "I"
#         value_derived = -66660000


#     return pd.Series([subvalue_derived, value_derived], index=['SUBVALUE_DERIVED', 'VALUE_DERIVED'])    

# # we don't have invalid_value_flag column
# def update_values(df):
#     # Create new columns 'subvalue_derived' and 'value_derived'
#     df['SUBVALUE_DERIVED'] = None
#     df['VALUE_DERIVED'] = None
    
#     # we don't have invalid_value_flag column??
#     mask = df['invalid_record_flag'] == 'Y'
#     df.loc[mask, 'subvalue_derived'] = 'I'
#     df.loc[mask, 'value_derived'] = -66660000
    
#     return df

# #%%
# def derived_d_values(subvalue_derived):
#     if subvalue_derived in ("CP", "P"):
#         return 11111111, "P"
#     elif subvalue_derived in ("CN", "N"):
#         return -11111111, "N"
#     elif subvalue_derived in ("CI", "I"):
#         return -66660000, "I"
#     elif subvalue_derived in ("CR", "R"):
#         return -77777777, "R"
#     else:
#         return None, None  # Handle other cases if needed

# def assign_priority(subvalue_derived_d):
#     if subvalue_derived_d == "P":
#         return 4
#     elif subvalue_derived_d == "N":
#         return 3
#     elif subvalue_derived_d == "R":
#         return 2
#     elif subvalue_derived_d == "I":
#         return 1
#     else:
#         return None  # Handle other cases if needed

def select_recommended_values(df):
    # Initialize new columns
    df['subvalue_ordersid_d'] = None
    df['value_ordersid_d'] = None
    
    # Loop through the DataFrame by groups (OrderSid)
    for _, group in df.groupby(['hcn_encrypted', 'OrderSid']):
        last_row = group.iloc[-1]  # Get the last row within each group (OrderSid)
        # Assign values to subvalue_ordersid_d and value_ordersid_d for the last row in each group
        df.loc[df.index == last_row.name, 'subvalue_ordersid_d'] = last_row['subvalue_derived_d']
        df.loc[df.index == last_row.name, 'value_ordersid_d'] = last_row['value_derived_d']
    
    return df

#%%
if __name__ == '__main__':

    cdiff_data = pd.read_sas("D:\\Users\\HDSB\\Projects\\Olis_cleaning\\Data\\olis_cdiff.sas7bdat", encoding="latin1")
    cdiff_data['VALUE_ENCODED'] = cdiff_data['VALUE']

    #backpriority
    #conclusive 0 or 1
    #orderwithordersid
    #order
    #subvalue_recommended
    #value recommmended

    cdiff_data[['SUBVALUE_DERIVED_P', 'VALUE_DERIVED_P', 'BACKPRIOIRITY']] = cdiff_data.apply(clean_value_p, axis=1)
    
    # Specific conditions for SNOMED codes
    # snomed_conditions = df['VALUE_ENCODED'].str.contains('<p1:microorganism xmlns:p1="http://www.ssha.ca">')
    # snomed_conditions_P = df['VALUE_ENCODED'].str.contains('<p1:microorganism xmlns:p1="http://www.ssha.ca"> & 12671002|5933001|96001009')
    # snomed_conditions_N = df['VALUE_ENCODED'].str.contains('<p1:microorganism xmlns:p1="http://www.ssha.ca"> & 854906661000087000|854906661000087105')

    # df.loc[snomed_conditions_P, ['SUBVALUE_DERIVED', 'VALUE_DERIVED']] = ['P', 11111111]
    # df.loc[snomed_conditions_N, ['SUBVALUE_DERIVED', 'VALUE_DERIVED']] = ['N', -11111111]
    # df.loc[snomed_conditions, ['SUBVALUE_DERIVED', 'VALUE_DERIVED']] = ['I', -66660000]  
    
    #codes for specific loinc
    # df[['SUBVALUE_DERIVED', 'VALUE_DERIVED']] = df.apply(specific_loinc, axis=1)

    # Other specific conditions for observation codes
    # df.loc[(df['OBSERVATIONCODE'] == '34713-8') & (df['VALUE'].str.contains('patient was previously reported as')), ['SUBVALUE_DERIVED', 'VALUE_DERIVED']] = ['R', -77777777]
    # df.loc[(df['OBSERVATIONCODE'] == '34713-8') & (df['VALUE_ENOCDED'].str.contains('patient was previously reported as')), ['SUBVALUE_DERIVED', 'VALUE_DERIVED']] = ['R', -77777777]
    # df.loc[(df['OBSERVATIONCODE'] == '34468-9') & (df['VALUE'].str.contains('eia screen test negative')), 'SUBVALUE_DERIVED'] = 'N'
    
    cdiff2 = pd.DataFrame(cdiff_data)
    
    cdiff2.sort_values(by=['HCN_ENCRYPTED', 'ORDERSID', 'OBSERVATIONDATETIME', 'TEST_REQUEST_POSITION_IN_ORDER', 'OBSERVATION_POS_IN_TEST_REQUEST'], inplace=True)

    cdiff2['CONCLUSIVE'] = cdiff2['SUBVALUE_DERIVED_P'].isin(["P", "N"]).astype(int)
    cdiff2['ORDER_WITHIN_ORDESID'] = cdiff2['TEST_REQUEST_POSITION_IN_ORDER'] * 10000 + cdiff2['OBSERVATION_POS_IN_TEST_REQUEST']
    cdiff2['OREDR'] = cdiff2['CONCLUSIVE'] * cdiff2['ORDER_WITHIN_ORDERSID']

    cdiff3 = pd.DataFrame(cdiff2)

    cdiff3.sort_values(by=['HCN_ENCRYPTED', 'ORDERSID', 'ORDER', 'BACKPRIORITY'], inplace=True)

    cdiff4 = select_recommended_values(cdiff3.copy())
    cdiff4.drop(['CONCLUSIVE', 'BACKPRIORITY', 'ORDER', 'SUBVALUE_DERIVED_P'], axis=1, inplace=True)

    cdiff4['OBSDATE'] = pd.to_datetime(cdiff4['OBDERVATIONDATETIME']).dt.date
    cdiff4['OBSDATE'] = cdiff4['OBSDATE'].dt.strftime('%d%b%Y')

    # Sort DataFrame by hcn_encrypted, ObsDate, backpriority
    cdiff4.sort_values(by=['HCN_ENCRYPTED', 'OBSDATE', 'BACKPRIORITY'], inplace=True)

    # Select recommended values based on last ObsDate within each group
    cdiff4['SUBVALUE_RECOMMENDED'] = None
    cdiff4['VALUE_RECOMMENDED'] = None

    for _, group in cdiff4.groupby(['HCN_ENCRYPTED', 'OBSDATE']):
        last_row = group.iloc[-1]  # Get the last row within each group (last ObsDate)
        cdiff4.loc[cdiff4.index == last_row.name, 'SUBVALUE_RECOMMENDED'] = last_row['SUBVALUE_DERIVED_P']
        cdiff4.loc[cdiff4.index == last_row.name, 'VALUE_RECOMMENDED'] = last_row['VALUE_DERIVED_P']

    # Step 5: Drop unnecessary columns
    cdiff4.drop(['BACKPRIORITY', 'SUBVALUE_DERIVED_P', 'VALUE_DERIVED_P', 'OBSDATE'], axis=1, inplace=True)

    # Step 6: Sort DataFrame for final output
    cdiff4.sort_values(by=['HCN_ENCRYPTED', 'ORDERSID', 'TEST_REQUEST_POSITION_IN_ORDER', 'OBSERVATION_POS_IN_TEST_REQUEST'], inplace=True)

    outdata = 'output_data.xlsx'  # Specify output file path
    # # Apply hierarchy within OrdersID
    # df['BACKPRIORITY'] = df['SUBVALUE_DERIVED'].map({'P': 4, 'N': 3, 'R': 2, 'I': 1})
    # df['CONCLUSIVE'] = df['SUBVALUE_DERIVED'].isin(['P', 'N']).astype(int)
    # df['ORDERWITHINORDERSID'] = df['TESTREQUESTPOSITIONINORDER'] * 10000 + df['OBSERVATIONPOSINTESTREQUEST']
    # df['ORDER'] = df['CONCLUSIVE'] * df['ORDERWITHINORDERSID']
    
    # # Sort and select recommended values within OrderSid
    # df = df.sort_values(by=['ORDERSID', 'ORDER', 'BACKPRIORITY'])
    

#sas_cleaned - VALUE_RECOMMENDED_D, VALUE_DERIVED_D, VALUE_DERIVED, SUBVALUE_RECOMMENDED_D, SUBVALUE_DERIVED_D, INVALID_RECORD_FLAG
#normal cleaned - SUBVALUE_DERIVED, ORDER, CONCLUSIVE, BACKPRIORITY