# %%

import pandas as pd
import numpy as np
import re
import os
from pathlib import Path
from spellchecker import SpellChecker

# start spell checker
spell = SpellChecker()

# %%

# Read the SAS dataset into a pandas DataFrame
#df = pd.read_sas('C:/Projects/OLIS Cleaning/Data/olis_lipids.sas7bdat', format='sas7bdat', encoding='latin1')
#value_value = df.groupby(['VALUE', 'OBSERVATIONCODE', 'ORDERSID', 'TESTREQUESTPOSITIONINORDER', 'OBSERVATIONPOSINTESTREQUEST']).size().reset_index(name='cn')

# Rename column for clarity
#value_value = value_value.rename(columns={'VALUE': 'value_encoded'})

#dftest=df.head(5)

# %%
def clean_lipid(value_encoded:str):
    def anydigit(s):
        return any(char.isdigit() for char in s)

    def anyalpha(s):
        return any(char.isalpha() for char in s)

    def anypunct(s):
        return any(char in ".,;:!?-" for char in s)

    value_derived_d = None
    subvalue_derived_d = None
     
    try:
        value_encoded =  value_encoded.upper();
        if anydigit(value_encoded)>0 and \
            not str.find(self, 'NOT PERFORMED')>0 \
                and str.find(self, 'DISREGARD') >0 \
                    and str.find(self, 'CORRECTED ON') >0 \
        and str.find(self, 'NOT VALID') >0 \
            and str.find(self, 'NOT AVAILABLE') >0 \
                and	str.find(self, 'UNABLE') >0 \
                    and	str.find(self, 'UNSUITABLE') >0 \
        and	str.find(self, 'INVALID') >0 \
            and	str.find(self, 'NOT BE CALCULATED') >0 \
                and	str.find(self, 'NOT ACCURATE') >0 \
        and	str.find(self, 'UNRELIABLE') >0 \
            and	str.find(self, 'NOT REP\TABLE') >0 \
                and	str.find(self, 'IS DECREASED') >0 \
                    and	str.find(self, 'NOT BEEN SIGNED') >0 \
        and	str.find(self, 'NOT BEEN PERF\MED') >0 \
            and	str.find(self, 'INC\RECTLY') >0 \
                and	str.find(self, 'CANCELLED') >0 \
                    and	str.find(self, 'DELETE') >0 \
        and	str.find(self, 'MODIFIED RESULT') >0 \
            and	str.find(self, 'GUIDELINE') >0 \
                and	str.find(self, 'N/A') >0 \
                    and	str.find(self, 'ERROR') >0 \
        and	str.find(self, 'REJECTION') >0 \
            and	str.find(self, 'MISLABELLED') >0 \
                and	str.find(self, 'DUPLICATE') >0 \
                    and	str.find(self, 'DEPRESSED') >0 \
        and	str.find(self, 'INC\RECT') >0 \
            and	str.find(self, 'FRS*') >0 \
                and	str.find(self, 'AMENDED') >0 \
                    and	str.find(self, 'UNLABELLED') >0 \
        and	str.find(self, 'GROSSLY LIPEMIC') >0 \
            and	str.find(self, 'NO SAMPLE') >0 \
                and	str.find(self, 'NOT CALCULATED') >0 \
                    and	str.find(self, "CAN'T BE CALCULATED") >0 \
        and	str.find(self, 'NOT \DERED') >0 \
            and	str.find(self, 'INACCURATE') >0 \
               and  str.find(self, 'NOT PROCESSED') >0:
               
                   
	# If value has just numbers and decimals;
        elif re.match(r'^[0-9.]+$', upvalue):
                valuetemp1 = upvalue.replace('..', '.')
                value_derived = float(valuetemp1)
    
    # If value contains \.BR\;
        elif re.search(r'\.BR\\', upvalue):
            valuetemp1 = upvalue.replace(".BR\\", "").strip()
            if re.match(r'^[0-9. ]+$', valuetemp1):
                value_derived = float(valuetemp1.replace(' ', ''))

    #If it has < or > and no letter;
        if '<>' in upvalue and all(c in '0123456789. <>' for c in upvalue):
            if '<' in upvalue:
                sub_value1 = '<'
                elif '>' in upvalue:
                    sub_value1 = '>'
        else:
            sub_value1 = ''
        valuetemp1 = upvalue.replace('<>', '')
        value_derived = float(valuetemp1.strip())
    
    #Has !/H/R/L at the end;
    if all(c in '0123456789. !HRL' for c in upvalue):
        valuetemp1 = upvalue.translate(str.maketrans('', '', '!HRL'))
        if not ' ' in valuetemp1.strip():
            value_derived = float(valuetemp1.strip())
    
    # LESS THAN;
    if upvalue.startswith('LESS THAN'):
        subvalue1 = '<'
        valuetemp1 = upvalue.replace('LESS THAN', '').replace('.BR\\', '').strip()
        value_derived = float(valuetemp1.strip())

    #GREATER THAN;
    if upvalue.startswith('LESS THAN'):
        subvalue1 = '<'
        valuetemp1 = upvalue.replace('LESS THAN', '').replace('.BR\\', '').strip()
        value_derived = float(valuetemp1.strip())

#	/*<P1:STRUCTUREDNUMERIC XMLNS:P1="HTTP://WWW.SSHA.CA"><P1:COMPARATOR>&GT;=</P1:COMPARATOR><P1:NUMBER1>0.64</P1:NUMBER1></P1:STRUCTUREDNUMERIC>*/
#		*** XML;

    if "HTTP://WWW.SSHA.CA" in upvalue:
        if '&GT;' in upvalue:
            subvalue1 = ">"
        elif '&LT;' in upvalue:
            subvalue1 = "<"
        else:
            subvalue1 = ""
        valuetemp1 = upvalue.replace('<P1:STRUCTUREDNUMERIC XMLNS:P1="HTTP://WWW.SSHA.CA">', '').replace('</P1:STRUCTUREDNUMERIC>', '').strip()
        valuetemp2 = valuetemp1.replace('<P1:COMPARATOR>', '').replace('</P1:COMPARATOR>', '').strip()
        valuetemp3 = valuetemp2.replace('<P1:NUMBER1>', '').replace('</P1:NUMBER1>', '').strip()
        valuetemp4 = valuetemp3.replace('<P1:NUMBER2>', '').replace('</P1:NUMBER2>', '').strip()
        valuetemp5 = valuetemp4.replace('<P1:COMPARATOR/>', '').replace('<P1:SEPARATOR/>', '').strip()
        valuetemp6 = valuetemp5.translate(str.maketrans('', '', '=&LTGT;:'))
        value_derived = float(valuetemp6.strip())

    #/*LIPIDS SPECIFIC*/
    elif value_derived is None and re.match(r'^[0-9.-NEG ]+$', upvalue):
        valuetemp1 = upvalue.replace(' NEG', '')
        value_derived = float(valuetemp1.strip())
    
    #/*cholesterol*/ 
    elif (value_derived is None and
          observationcode in ('14646-4', '14647-2', '22748-8', '25371-6', '32309-7', '39469-2', '70204-3')):
        re = r'(CHOL|FHOL|FCHOL|CHOLESTEROL|CHOLESTEOL|HOLESTEROL RESULT|CHOLESTEROL LEVEL|CHOLESEROL RESULTS|FASTING|FASTING\)|SERUM\)|LDL|HDL|HDL RESULT)[IS.:= ]+([<>]?)(\d{1,2}\.\d{1,2})'
        match = re.match(re)
            if match:
                value_derived = float(match.group(3))
                subvalue1 = match.group(2)
                else:
                    re2 = r'LDL[- ]*(CHOLESTEROL|CHOL)? ?(IS|:|=)? (LESS THAN|<) ?1'
           if re.match(re2, upvalue):
                        value_derived = 1
                        subvalue1 = '<'
           elif upvalue == 'VALUE IS GREATER THAN 4.5':
               value_derived = 4.5
               subvalue1 = '>'
               
    #	/*triglycerides*/
    elif (value_derived is None and
        observationcode in ('14927-8', '47210-0')):
        re3 = r'(TRIGLYCERIDES|TRIGLYCERIDES RESULT|TRIGLYCERIDS|TRIGLYCERIDE|TRIG|TRIGLY|TRIGLYCERIDE RESULT|TRIG RESULT)[IS.:= ]+([<>]?)(\d{1,3}\.\d{1,2})'
        match = re.match(re3, upvalue)
        if match:
            value_derived = float(match.group(3))
            subvalue1 = match.group(2)
        else:
            re4 = r'^(\d{1,2}\.\d{2}) (,|\()'
            if re.match(re4, upvalue):
                value_derived = float(re.search(re4, upvalue).group(1))
            elif 'SERUM TRIGLYCERIDES > 50.00' in upvalue or 'SERUM TRIGLYCERIDE RESULT RESULT GREATER\.BR\THAN 50.00' in upvalue:
                value_derived = 50.00
                subvalue1 = '>'
   #/*apolipoprotein*/
    elif (value_derived is None and
        observationcode in ('1869-7', '1884-6')):
        re5 = r'(APOB|RESULT)[IS.:= ]+([<>]?)(\d{1}\.\d{3})'
        match = re.match(re5, upvalue)
        if match:
            value_derived = float(match.group(3))
            subvalue1 = match.group(2)

#		*<1.70 MMOL/L        NORMAL
#	*>5.64 MMOL/L        VERY HIGH;


    elif (value_derived is None and
        observationcode in ('1884-6')):
        re5 = r'([=]?)(\d{1,3}\.\d{1,3}) G\/L'
        match = re.match(re5, upvalue)
        if match:
            value_derived = float(match.group(2))
            subvalue1 = match.group(1)
    except :
         print (" failed at: ", value_encoded)



        return value_derived_d, subvalue_derived_d


# %%
if __name__ == '__main__':

    # setup
    projectPath = Path(os.getcwd())
    #dataFile = projectPath / ".." / "Data/olis_lipids.sas7bdat"
    dataFile = projectPath / "Data/olis_lipids.sas7bdat"
#    df = pd.read_sas('C:/Projects/OLIS Cleaning/Data/olis_lipids.sas7bdat', format='sas7bdat', encoding='latin1')
#   value_value = df.groupby(['VALUE', 'OBSERVATIONCODE', 'ORDERSID', 'TESTREQUESTPOSITIONINORDER', 'OBSERVATIONPOSINTESTREQUEST']).size().reset_index(name='cn')

    # Rename column for clarity
#    value_value = value_value.rename(columns={'VALUE': 'value_encoded'})
   
    # read in the dataset
    dat0 = pd.read_sas(dataFile, encoding='latin1')
    value_value = dat0.groupby(['VALUE', 'OBSERVATIONCODE', 'ORDERSID', 'TESTREQUESTPOSITIONINORDER', 'OBSERVATIONPOSINTESTREQUEST']).size().reset_index(name='cn')
    dat1 = value_value.rename(columns={'VALUE': 'value_encoded'})
    
#    dat1=value_value.copy()


    #%%
    dat1.columns= dat1.columns.str.lower()
    # test couple of things first
    t1 = pd.DataFrame()
    t1['value_derived'],t1['subvalue_derived_d'] = zip(*dat1.value.apply(clean_sup_data))

    t1 = pd.concat([t1,dat1[['value']]], axis=1)
    # send in the data from cleaningcolumns=['value_encoded','subvalue_derived_d']
    #%%
    t2 = t1[t1.value.str.len()>7]
    t2.value_derived = pd.to_numeric(t2.value_derived,errors='coerce')
    t2 [t2.value_derived == -88888888.0]
    
    # %%
    t3 = t2[t2.value_derived.isna()].value.value_counts().reset_index().rename(columns={'index':'issue'}).sort_values('value', ascending=False)
