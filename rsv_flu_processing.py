# %%
import textwrap
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import nltk
import re
import datetime
import time
import os
from pathlib import Path
import warnings
import argparse
from argparse import RawTextHelpFormatter
warnings.filterwarnings("ignore")

# %% define variables
file_path = Path(".")

# name of patientid variable in input dataset, will be renamed as 'patientid'
# input_patientid_var = 'patientsid'
input_patientid_var = 'patientid'

micro_org_cols =['covid', 'adenovirus', 'bocavirus', 'coronavirus', 'flu', 'flu_a', 'flu_a_h1', 'flu_a_h3', 'flu_b',
         'entero_rhino', 'hmv', 'para', 'rsv', 'rsv_a', 'rsv_b', 'pneumonia', 'others']
output_values = True # indicates  write a file with cleaned_value for our review;
flursvcols = ['flu','flu_a','flu_a_h1','flu_a_h3','flu_b','rsv','rsv_a','rsv_b']

# output additional columns
#1 = with key columns, 2 = with ALL columns
output_flag = 1

writeflag = True

# clean punctuation, xml field, numbers, other text
puncs = [';', ':', ',', '.', '-', '_', '/', '(', ')', '[', ']', '{', '}', '<', '>', '*', '#', '?', '.', '+', 
        'br\\', '\\br', '\\e\\', '\\f\\', '\\t\\', '\\r\\', '\\', "'", '"', '=']
terms_to_space = ['detected', 'by', 'positive', 'parainfluenza', 'accession']
nums_following = ['date', 'telephone', 'tel', 'phone', 'received', 'collected',  
                 'result', 'on', 'at', '@', 'approved', 'final', 'time', 'number']
strings_to_replace = {'non detected':'not detected','nt detected':'not detected' ,'npot detected':'not detected', 
                      'nor detected':'not detected', 'mot detected':'not detected', 
                      'n0t detected':'not detected', 'nit detected':'not detected','agenot detected':'not detected',
                      'covid 19 virus not interpretation detected':'covid 19 virus interpretation not detected',
                      'presumptive interpretation':'interpretation presumptive',
                      'preliminary interpretation':'interpretation preliminary',
                      'covid 19 not detected and covid 19 detected':'covid 19 detected and covid 19 not detected',
                      'virusnot':'virus not', 'prevuous':'previous'}
date_id_patterns = [r'\d{2,4} \d{2} \d{2,4} ', r'\d{4} \d{2} ', r'\d{4}h ', 
                   r' \d{0,2}[a-z]{0,2}\d{5,}[a-z]{0,1}', r' [a-z]{0,2}\d{1,3}[a-z]{1,3}\d{4,}[a-z]{0,1}',
                   r' \d{2}[a-z]{1}\d{3}[a-z]{2}\d{4}', r' [a-z]{4,}\d{7,}']


#assign labels for useful tokens based on some dictionaries and exclusions
easy_virus_dict = {'v_adenovirus':['aden'], 'v_bocavirus':['boca', 'bocca'], 'v_coronavirus':['coro', 'cora'],
                   'v_entero_rhino':['enterol', 'enterov', 'entervir', 'rhino', 'rhini'], 'v_hmv':['metap']}
hard_virus_dict = {'v_rsv':['rsv'], 'v_flu':['nflu', 'flue','flua','flub'], 'v_para':['parai', 'pata', 'parta'],
                   'v_covid':['cov', 'sars', 'orf1', 'orfl', 'or1lab']} #fluvid 
indirect_matches_dict = {'r_pos': ['posi','pos1','covpos'], 
                         'r_neg': ['neg', 'naeg', 'neag'],  
                         'r_ind': ['indeter', 'eterminate', 'inconclu', 'inderter',
                                   'equivocal', 'unresolved'],
                         'r_can': ['cancel', 'incorrect', 'duplicate', 'mislabel','unlabel',
                                   'recollect', 'mistaken', 'wrong', 'redirect'],
                         'r_rej': ['reject', 'inval', 'leak', 'unable', 'insuffic', 
                                   'spill', 'inapprop', 'nsq', 'poor', 'uninterpret'],
                         'presumptive': ['presump', 'prelim', 'possi'], 
                         'retest': ['retest']} #'sent', 'send', 'forwarded'
direct_matches_dict = {'r_pos': ['detected', 'pos', 'deteced', 'postive', 'organism','isolated'],
                       'r_neg': ['no', 'not'],
                       'r_ind': ['ind'],
                       'r_pen': ['pending', 'progress', 'follow', 'ordered', 'reordered','reorder'],
                       'presumptive': ['single', 'possible', 'probable'],
                       'xml': ['p1'], 
                       'reset': ['deleted','anesthesiologist'],
                       'stop': ['specific', 'required', 'error', 'copy', 'see', 'laboratory',
                                'note', 'stability', 'changed', 'recollect', 'moh', 'if', 'before'],
                       'final': ['interpretation', 'interpetation', 'interp', 'pretation', 'interpretive',
                                 'final', 'overall', 'corrected', 'proved', 'correct','current'],
                       'skip': ['reason', 'identify', 'confirmation'],
                       'end': ['mutation','voc','vocs','variant','variants','serology'],
                       'connecting': ['screen', 'presence', 'as', 'real',
                                      'is', 'of', 'in', '1', '2', '3', '4', 'a', 'b', 'c',
                                      '229e', 'nl63', 'hku1', 'oc43', '19', '2019', 'low',
                                      'biosafety', 'hazard', 'has', 'been', 'for', 'changed', 'identified', 
                                      'result', 'other', 'testing', 'using', 'to', 'from', 'tested',
                                      'phl', 'phol', 'phlo', 'new', 'request', 'lab', 'will',
                                      'panel', 'seasonal', 'human', 'report', 'said', 'updated', 'dob',
                                      'requisition', 'form','label'
                                      ]}
test_type_dict = {'t_oth': ['eia', 'rapid', 'immunoassay', 'ict', 'immunochromatographic', 'antigen'], 
                  't_pcr': ['multiplex', 'naat', 'nat', 'pcr', 'rrt', 'rna', 'gen', 
                            'reverse', 'polymerase', 'chain', 'simplexa'],
                  't_gene': ['gene', 'targets', 'tagets', 'target']}


# %%
def read_input(input_path =None):
    """This function is for reading the SAS dataset or if the input_path is empty then you can 
        it should read it from the SQL database.

    Args:
        input_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    df = None
    if input_path is not None:
        df = pd.read_sas( input_path ,encoding="latin1")
    else :
        # write  a function to read it from red-shift database.
        print(" current we don't have anything")
    
    df.columns = df.columns.str.lower()
    df.fillna('', inplace=True)
    print('# of records:',len(df))
    #df_raw = df.copy(deep = True)

    return df

def process_input(df):
    df = df.rename(columns={input_patientid_var:'patientid','fillerordernumber':'fillerordernumberid',
                       'observationvalue':'value','observationsubid':'subid'})
        
    key_cols = ['patientid', 'ordersid', 'fillerordernumberid', 
            'reportinglaborgname', 'performinglaborgname', 'observationdatetime', 
            'testrequestcode', 'observationcode', 'observationreleasets', 
            'observationresultstatus', 'subid', 'value']
    df = df[key_cols]

    df_W = df.loc[df['observationresultstatus'] == 'W', ['ordersid', 'observationcode', 'value']]
    print(df_W.head())
    df_excl = df[['ordersid', 'observationcode', 'value']].reset_index().merge(df_W, how='inner').set_index('index')
    df['exclude_flag'] = 'N'
    df.loc[df.index.isin(df_excl.index),['exclude_flag']] = 'Y'
    print(df['exclude_flag'].value_counts())

    group_cols = ['patientid','ordersid', 'fillerordernumberid', 'reportinglaborgname', 'testrequestcode',
         'observationcode','observationdatetime', 'observationreleasets', 'observationresultstatus']
    df_gp_subid = df.reset_index().groupby(group_cols).agg({'index':tuple, 'subid':tuple}).reset_index()
    df_gp_subid = df_gp_subid.rename(columns={'index':'original_indexes'})

    # only concatenate ones where there are more than two subids, 
    # all the subids are numbers and contains 1
    df_to_concat = df_gp_subid[df_gp_subid['subid'].apply(lambda x: all([subid.isdigit() for subid in x]) and len(x) > 2 and '1' in x)]
    concat_indexes = [i for tup in df_to_concat['original_indexes'] for i in tup]

    # concatenate based on subid
    df_gp_concat = df[df.index.isin(concat_indexes)].reset_index()
    df_gp_concat['subid'] = df_gp_concat['subid'].apply(int)
    df_gp_concat = df_gp_concat.sort_values(by = group_cols+['subid']).groupby(group_cols)
    df_gp_concat = df_gp_concat.agg({'index': tuple,
                    'value': lambda x: ' '.join(map(str, x))}).reset_index()

    # add on records that were not concatenated
    df_gp = df.loc[~df.index.isin(concat_indexes), group_cols+['value']].reset_index()
    df_gp['index'] = df_gp['index'].apply(lambda x: (x,))
    df_gp = pd.concat([df_gp_concat, df_gp], sort=False).rename(columns={'index':'original_indexes'})

    # narrow down columns of df
    df_cols = ['patientid','ordersid','fillerordernumberid','observationdatetime','testrequestcode',
            'observationcode','observationreleasets', 'observationresultstatus','exclude_flag']
    df = df[df_cols]

    print('# of TEST RESULTS:', len(df_gp))

    return  df, df_gp

def readin_TR_LOINC_file(filename):
  
    dataf = pd.read_csv(filename,sep=",",header=0)
    dataf.loinc = np.where(dataf['trcode'].notna(), np.nan, dataf['loinc'])
    # forward fill the missing trcode by copying.
    dataf.trcode.ffill(inplace=True)
    # rename and replace TR_ANY by Null
    dataf = (dataf.dropna(subset=['loinc'])
            .rename(columns={'loinc':'observationcode','trcode':'testrequestcode'})
            .replace('TR_ANY',np.nan)
            )
    # print(dataf.virus_type.value_counts(dropna=False))
    # convert and strip the end spaces 
    dataf.virus_type = dataf.virus_type.str.strip()

    return dataf

def clean(value):
    cleaned = value.lower()

    #clean xml field, only keep text field surrounded with 'p1 text'
    pattern = r'(<p1:microorganism xmlns)(.+)(<p1:text>.+</p1:text>)(.+)(</p1:microorganism>)'
    while re.search(pattern, cleaned):
        cleaned = re.sub(pattern, r'\g<3>', cleaned)

    #surround terms with spaces (some terms found stuck together)
    for t in terms_to_space:
        cleaned = cleaned.replace(t, ' ' + t + ' ')

    #replace punctuation with space
    for punc in puncs:
        cleaned = cleaned.replace(punc, ' ')

    #remove consecutive spaces
    while '  ' in cleaned:
        cleaned = cleaned.replace('  ', ' ')

    cleaned = cleaned.strip()     

    #remove numbers after certain terms
    for term in nums_following:
        pattern = term + r' \d{1,4}'

        while re.search(pattern, cleaned):
            cleaned = re.sub(pattern, term, cleaned)

    #remove more dates and ids
    for pattern in date_id_patterns:
        while re.search(pattern, cleaned):
            cleaned = re.sub(pattern, '', cleaned)

    #remove numbers at the end
    while len(cleaned) > 0 and (cleaned[-1].isdigit() or cleaned[-1] == ' '):
        cleaned = cleaned[:-1]

    #remove "no" at the end
    while cleaned.endswith(' no') or cleaned == 'no':
        cleaned = cleaned[:-3]

    #fix certain strings
    for k, v in strings_to_replace.items():
        cleaned = cleaned.replace(k, v)

    return cleaned

#tokenize values using nltk
def tokenize(value):
    tokenized = nltk.word_tokenize(value)

    return tokenized

def assign_labels(tokenized):
    tokenized_length = len(tokenized)
    useful = [None]*tokenized_length #store same list length of tokens and update each accordingly

    for counter, token in enumerate(tokenized):

        #skip if already assigned
        if useful[counter]:
            continue

        ###easy viruses dictionary (non-exact matching)
        for virus, patterns in easy_virus_dict.items():
            if any([pattern in token for pattern in patterns]):
                useful[counter] = virus
                break

        #extra rhino/entero rule (exact matching)
        if token in ('rhino', 'entero'):
            useful[counter] = 'v_entero_rhino'

        ###hard viruses dictionary (non-exact matching)

        #COVID19 
        #e/envelope/n/nucleocapsid/s/spike gene
        elif token in ('e', 'envelope', 'n', 'nucleocapsid', 's', 'spike') and (tokenized_length > counter+1)\
        and tokenized[counter+1] == 'gene':
            useful[counter:counter+2] = ['v_covid', 't_gene']

        #rdrp gene
        elif token == 'rdrp' and (tokenized_length > counter+1)\
        and tokenized[counter+1] == 'gene' and 'v_coronavirus' not in useful[:counter]:
            useful[counter:counter+2] = ['v_covid', 't_gene']

        #orf1ab
        elif any([pattern in token for pattern in ['orf1','orfl','or1lab']]) and (tokenized_length > counter+1)\
        and tokenized[counter+1] == 'gene' and 'mers' not in tokenized[counter-3:counter]:
            useful[counter:counter+2] = ['v_covid', 't_gene']

        elif any([pattern in token for pattern in hard_virus_dict['v_covid']])\
        and not any([pattern in token for pattern in ('ecov', 'cove', 'covpos')])\
        and not any([word==pattern for word in tokenized[counter-3:counter] 
                     for pattern in ('mers', 'caesarean', 'xpress')])\
        and not tokenized[counter-1] == 'non':
            useful[counter] = 'v_covid'

        #extra rule for seasonal coronavirus, if preceded by novel or followed by 19/disease/cov/sars/2
        elif any([pattern in token for pattern in easy_virus_dict['v_coronavirus']]):
            if 'nove' in tokenized[counter-1] or tokenized[counter-1] == 'nivel':
                useful[counter-1:counter+1] = ['connecting', 'v_covid']

            covid_extra = [] #extra terms
            look_forward = 3 #how many terms to look forward for
            max_forward = min(counter+look_forward, tokenized_length-1) #limit if record is too short
            covid_extra = [(tokenized[covid_pos], covid_pos) for covid_pos in range(counter+1, max_forward+1)\
                       if any([pattern in tokenized[covid_pos] for pattern in ('19', 'disea', 'cov', 'sars')]\
                              +[tokenized[covid_pos] == '2'])]

            #assign range of relevant tokens as virus change and 'non' not in tokenized[counter+1:max_forward+1]
            if len(covid_extra) > 0 and 'non' not in tokenized[counter+1:max_forward+1]:
                last_pos = max([x[1] for x in covid_extra])
                useful[counter:last_pos+1] = ['v_covid']+['connecting']*(last_pos-counter)
            else:
                pass

        #PARA
        elif any([pattern in token for pattern in hard_virus_dict['v_para']]+[token == 'para'])\
        and tokenized[counter-1] != 'haemophilus':
            para_extra = []
            look_forward = 5
            max_forward = min(counter+look_forward, tokenized_length-1)
            para_extra = [(tokenized[para_pos], para_pos) for para_pos in range(counter+1, max_forward+1)\
                              if tokenized[para_pos] in ('1','2','3','4')]

            if len(para_extra) > 0:
                last_pos = max([x[1] for x in para_extra])
                para_nums = [x[0] for x in para_extra]
                useful[counter:last_pos+1] = ['v_para_' + '_'.join(para_nums)]+['connecting']*(last_pos-counter)
            else:
                useful[counter] = 'v_para'

        #FLU
        elif any([pattern in token for pattern in hard_virus_dict['v_flu']]+[token in ('flu', 'inf')])\
        and tokenized[counter-1] != 'haemophilus' and tokenized[counter] != 'fluab':
            flu_extra = []
            look_forward = 4
            max_forward = min(counter+look_forward, tokenized_length-1)

            for flu_pos in range(counter+1, max_forward+1):
                if tokenized[flu_pos] in ('a','b') or 'h1' in tokenized[flu_pos] or 'h3' in tokenized[flu_pos]:
                    flu_extra.append((tokenized[flu_pos], flu_pos))
                elif 'flu' in tokenized[flu_pos]: #to deal with influenza a influenza b
                    break

            if len(flu_extra) > 0:
                last_pos = max([x[1] for x in flu_extra])
                flu_types = [x[0] for x in flu_extra]
                if 'a' in flu_types and 'b' in flu_types:
                    useful[counter:last_pos+1] = ['v_flu_a_b']+['connecting']*(last_pos-counter)
                elif 'b' in flu_types:
                    useful[counter:last_pos+1] = ['v_flu_b']+['connecting']*(last_pos-counter)
                elif any(['h1' in f for f in flu_types]) and any(['h3' in f for f in flu_types]):
                    useful[counter:last_pos+1] = ['v_flu_a_h1_h3']+['connecting']*(last_pos-counter)
                elif any(['h1' in f for f in flu_types]):
                    useful[counter:last_pos+1] = ['v_flu_a_h1']+['connecting']*(last_pos-counter)
                elif any(['h3' in f for f in flu_types]):
                    useful[counter:last_pos+1] = ['v_flu_a_h3']+['connecting']*(last_pos-counter)
                elif 'a' in flu_types:
                    useful[counter:last_pos+1] = ['v_flu_a']+['connecting']*(last_pos-counter)                                                                  
            elif token.endswith('aa'):
                useful[counter] = 'v_flu_a'
            elif token.endswith('ab'):
                useful[counter] = 'v_flu_b'
            else:
                useful[counter] = 'v_flu'

        #RSV
        elif any([pattern in token for pattern in hard_virus_dict['v_rsv']]):
            rsv_extra = []
            look_forward = 2
            max_forward = min(counter+look_forward, tokenized_length-1) 
            rsv_extra = [(tokenized[rsv_pos], rsv_pos) for rsv_pos in range(counter+1, max_forward+1)\
                       if tokenized[rsv_pos] in ('a','b')]

            if len(rsv_extra) > 0:
                last_pos = max([x[1] for x in rsv_extra])
                rsv_types = [x[0] for x in rsv_extra]
                if 'a' in rsv_types and 'b' in rsv_types:
                    useful[counter:last_pos+1] = ['v_rsv_a_b']+['connecting']*(last_pos-counter)
                elif 'a' in rsv_types:
                    useful[counter:last_pos+1] = ['v_rsv_a']+['connecting']*(last_pos-counter)
                elif 'b' in rsv_types:
                    useful[counter:last_pos+1] = ['v_rsv_b']+['connecting']*(last_pos-counter)
            else:
                useful[counter] = 'v_rsv'

        elif (tokenized_length > counter+2) and ((token.startswith('resp')\
        and tokenized[counter+1].startswith('syn') and tokenized[counter+2].startswith('vi'))\
        or (token == 'r' and tokenized[counter+1] == 's' and tokenized[counter+2] == 'v')):
            rsv_extra = []
            look_forward = 4
            max_forward = min(counter+look_forward, tokenized_length-1) 
            rsv_extra = [(tokenized[rsv_pos], rsv_pos) for rsv_pos in range(counter+3, max_forward+1)\
                       if tokenized[rsv_pos] in ('a','b')]

            if len(rsv_extra) > 0:
                last_pos = max([x[1] for x in rsv_extra])
                rsv_types = [x[0] for x in rsv_extra]
                if 'a' in rsv_types and 'b' in rsv_types:
                    useful[counter:last_pos+1] = ['v_rsv_a_b']+['connecting']*(last_pos-counter)
                elif 'a' in rsv_types:
                    useful[counter:last_pos+1] = ['v_rsv_a']+['connecting']*(last_pos-counter)
                elif 'b' in rsv_types:
                    useful[counter:last_pos+1] = ['v_rsv_b']+['connecting']*(last_pos-counter)
            else:
                useful[counter:counter+3] = ['v_rsv', 'connecting', 'connecting']

        #UNKNOWN VIRUS
        elif (token.startswith('vir') or token.startswith('viu')):
            #extra rule for virus culture
            if (tokenized_length > counter+2) and tokenized[counter+1].startswith('cult')\
            and 'request' in tokenized[counter+2]:
                useful[counter:counter+3] = ['connecting']*3
            elif (tokenized_length > counter+1) and tokenized[counter+1].startswith('cult'):
                useful[counter:counter+2] = ['t_oth']*2
            else:
                useful[counter] = 'v_unk'

        #extra terms to treat as an "unknown virus" for purpose of algorithm
        elif token in ('by','further','specimen','specimens','test','sample','considered'):
            useful[counter] = 'v_unk'

    # loop over the record again
    for counter, token in enumerate(tokenized):

        #skip if already assigned
        if useful[counter]:
            continue

        #culture tests  
        if token.startswith('cult') and not ((tokenized_length > counter+1) and 'request' in tokenized[counter+1]):
            useful[counter] = 't_oth'

        #additional "direct" tests
        elif token == 'direct' and (tokenized_length > counter+1):
            if tokenized[counter+1] in ('kit', 'enzyme', 'test', 'testing', 'eia', 'antigen', 'ict'):
                useful[counter:counter+2] = ['t_oth']*2
            elif tokenized[counter+1] in ('influenza',):
                useful[counter] = 't_oth'

        #condition for mention of pos/neg
        elif token in ('negative','neg','positive','pos','detected','organism')\
        and (tokenized_length > counter+1)\
        and ((tokenized[counter-1] in ('a','original','or','level','of','the','tested','was','false','had','antibodies','antibody') 
              and tokenized[counter+1] in ('test','result','covid','new','at','note','sars')) 
             or tokenized[counter+1] in ('or','swab','to','contact','workers','retest','results',
                                         'son','person','patients','travel','individual','admission',
                                         'roommate','rapid','coworker','co','cultures')):
            useful[counter-1:counter+2] = [None]*3
        elif token in ('negative','neg','positive','pos','detected','organism','posivtive')\
        and (tokenized_length > 1)\
        and (tokenized[counter-2] in ('previous','previously','contact','worker','depot','targets',
                                      'being','unless','patient','law','due','exposure','needs','if',
                                      'swab','who','psw','known','must','mother')
             or tokenized[counter-1] in ('previous','previously','known','unit','first','second',
                                         'needs','need','requires','considered','swab','if',
                                         'depot','employee','gram','cx','member','coworker','shows',
                                         'father','contact','both','and','confirm','despite','provide',
                                         'mom','verify','particles')):
            useful[counter-1:counter+1] = [None]*2
        elif token in ('negative','neg','positive','pos','detected','organism')\
        and (tokenized_length > 3)\
        and (tokenized[counter-3] in ('mom','him','father','which','sister','partner','contact','who')
            or tokenized[counter-4] in ('who',)):
            useful[counter-2:counter+1] = [None]*3 

        #condition for word before no
        elif token == 'no' and (tokenized[counter-1] in ('by','lab','specimen','accession',
                                                         'sample','order','please','phl',
                                                         'with','bipap','pain','ord')
                                or any([pattern in tokenized[counter-1] for pattern in ('out','break','inv')]))\
        and tokenized[counter+1:counter+2] != ['virus'] and counter > 0:
            useful[counter-1:counter+1] = [None]*2

        #condition for word after no (skip)
        elif token == 'no' and (tokenized_length > counter+1)\
        and tokenized[counter+1] in ('fever','answer','longer','patient','second','grh','afb',
                                     'exposure','appetite','outbreak','symptoms','symmptoms',
                                     'show','2nd','transfer','requisition','evidence','dob',
                                     'response','name','unexplained','lts','hc','hcn','paperwork',
                                     'further','pick','time','call','other','viral', 'need', 'salmonella', 
                                     'date', 'submission', 'health','subsitute','cough','two','identifying','match',
                                     'growth','birthday'):
            useful[counter] = 'skip'

        #condition for word after no (cancel)
        elif token == 'no' and (tokenized_length > counter+1)\
        and tokenized[counter+1] in ('specimen','reportable','done','gene','result',
                                     'media','liquid','sample','swab','nasopharyngeal','record','fluid',
                                     'patient','second','results','testing','eluate','option','chose',
                                     'speicmen','label','validated','culture','volume','saliva','requisiton',
                                     'naso','confirmatory','dry'): 
            useful[counter] = 'r_can'

        #condition for due to
        elif tokenized[counter:counter+2] in [['due','to'],['for','result']] and 'new' not in tokenized[counter+2:counter+4]:
            useful[counter:counter+2] = ['stop']*2

        #condition for word after not (skip)
        elif token == 'not' and (tokenized_length > counter+1)\
        and tokenized[counter+1] in ('test','been','suspicious','validated','valildated','the','admitted',
                                     'preclude','intended','likely','given','coming','verified','ha','covid',
                                     'for','signed','on','recommended','retrieve','corssing','swabbed',
                                     'beingberecollected','at','eligible','vaccinated','put', 'leaking', 'per',
                                     'approved','c','nose','only','informed'):
            useful[counter:counter+2] = ['skip']*2


        #condition for word after not (cancel)
        elif token == 'not' and (tokenized_length > counter+1) and \
        tokenized[counter+1] in ('tested','tessted','perform','performed','process','processed', 
                                 'transmit','suitable','done','doen','be','reported','received', 
                                 'match','needed','labelled','available','symptomatic','forwared',
                                 'met','specified','indicated','returned','sufficient',
                                 'valid','required','able','needed','contain','ordered','recieved',
                                 'labeled','a','provided','appropriate','sent','send','remove',
                                 'report','rapid','found','applicable','rec','used','order',
                                 'matched','labled','proccessed','accepted','receivd','completed',
                                 'recollect','preformed','appearing','in','collected','obtained',
                                 'acceptable','capped','requested','enough','an','clearly','midturbinate',
                                 'refrigerated','refrigirated'):
            useful[counter:counter+2] = ['r_can']*2

        #condition for word before not
        elif token == 'not' and tokenized[counter-1] in ('does','did','please','done','over','swab','but','do','can','or'): #can?
            useful[counter-1:counter+1] = ['skip']*2

        #condition for errors
        elif tokenized[counter:counter+3] in (['ordered','in','error'], ['positive','in','error'],
                                             ['no','covid','result'], ['pos','in','error'],
                                             ['sent','under','incorrect'], ['no','covid','order'],
                                             ['s','already','positive']): 
            useful[counter:counter+3] = ['r_can']*3
        elif tokenized[counter:counter+3] in (['added','in','error'], ['the','wrong','patient'],['reported','in','error']):
            useful[counter:counter+3] = ['reset']*3
        elif tokenized[counter:counter+2] in (['processing','error'], ['in','error'], ['same','test'],
                                              ['labelling','error']):
            useful[counter:counter+2] = ['r_can']*2
        elif tokenized[counter:counter+4] in (['report','please','disregard','covid'],
                                              ['patient','please','disregard','results'],
                                              ['report','please','disregard','report'],
                                              ['individual', 'target', 'result', 'interpretation'],
                                              ['individual', 'target', 'results', 'interpretation'],
                                              ['requesting', 'negative', 'covid' ,'swab'],
                                              ['detected', 'cycle', 'threshold' ,'35'],
                                              ['does','not','belong','to'],
                                              ['outbreak', 'no', 'bdpoc', 'valid'],
                                              ['father', 'tested', 'positive', 'for'],
                                              ['multiplex', 'covid', 'flu', 'rspending'],
                                              ['report', 'positive', 'family','member'],
                                              ['organism', 'quantitation', 'of', 'growth'],
                                              ['please', 'disregard', 'covid', '19'],
                                              ['was', 'chosen', 'in', 'error']):
            useful[counter:counter+4] = ['end']*4
        elif tokenized[counter:counter+4] in (['please','remove','previous','copies'],):
            useful[counter:counter+4] = ['v_covid','r_can','r_can','r_can']

        #condition for target rna and disregard
        elif tokenized[counter:counter+2] in (['target','rna'],['patient','disregard'] ): 
            useful[counter:counter+2] = ['end']*2

        #condition for mother positive 
        elif token == 'mother' and (tokenized_length > counter+1)\
        and tokenized[counter+1] in ('positive'):
            useful[counter:counter+2] = ['skip']*2


        #condition for previous
        elif 'previous' in token and ('reported' in tokenized[counter+1:counter+3] or
                                      'specimen' in tokenized[counter+1:counter+2] or
                                      (tokenized[counter+1:counter+3] == ['report','covid'] and
                                           tokenized[counter-1] == 'the') or
                                      tokenized[counter+1:counter+3] in (['report','of'],
                                                                         ['reports','of'],
                                                                         ['reportof','covid'],
                                                                         ['result','of'],
                                                                         ['covid','19'],
                                                                         ['entered','covid'],
                                                                         ['report','as'],
                                                                         ['result','was'],
                                                                         ['report','that'])):
            useful[counter:counter+2] = ['end']*2

        #unable and indeterminate
        elif tokenized[counter:counter+5] in (['unable','to','be','completed','indeterminate'],
                                             ['please','disregard','previous','indeterminate','result'],
                                             ['interpretation','possible','low','viral','load'],
                                             ['all','positive','and','indeterminate','results'],
                                             ['19','positive','e','e','ab'],
                                             ['repeat', 'gx', 'e', 'neg', 'n'],
                                             ['for', 'clinical', 'use', 'indeterminate', 'for'],
                                             ['indeterminate', 'cycle', 'threshold','99', 'specimen'],
                                             ['in', 'low', 'has', 'positive','covid'],
                                            ['rejection','interface','error','specimen','not'],
                                              ['husband', 'swabbed', 'positive', 'for', 'covid'],
                                              ['born', 'to', 'covid', 'positive', 'mother'],
                                              ['newborn', 'to', 'covid', 'positive', 'mother'],
                                              ['to', 'covid', '19', 'positive','mother'],
                                              ['roommate', 'was', 'covid', 'positive', 'day'],
                                              ['delivered', 'to', 'covid', 'positive', 'mother'],
                                              ['exposed', 'to', 'a', 'positive', 'case'],
                                              ['exposed', 'to', 'covid', 'positive', 'case'],
                                              ['need', 'confirmation', 'of', 'negatvie', 'swab'],
                                              ['icu', 'admission', 'no', 'covid', 'swab'],
                                              ['positive', 'patient', 'sample', 'submitted', 'for']
                                            ):

            useful[counter:counter+4] = ['connecting']*4

        #upon further investigation
        elif tokenized[counter:counter+3] in (['upon','further','investigation'],):

            useful[counter-2:counter] = ['reset']*2

        #exclude antibody and reordered
        elif tokenized[counter:counter+8] in (['negative','for','anti','sars','cov','2','igg','antibodies'],
                                              ['negative','for','anti','sars','cov','2','iga','antibodies'],
                                             ['positive', 'for', 'anti', 'sars', 'cov' ,'2', 'igg', 'antibodies'],
                                             ['positive', 'for', 'anti', 'sars', 'cov' ,'2', 'iga', 'antibodies'],
                                             ['campylobacter', 'yersinia', 'or', 'e', 'coli', '0157', 'h7', 'isolated'],
                                             ['client', 'disclosed', 'chosen', 'not', 'to', 'vaccinat', 'for', 'covid'],
                                             ['forwarded', 'to', 'public', 'health', 'for', 'covid', 'flu', 'and'],
                                             ['label','on','specimen','not','matching','please','re','collect'],
                                             ['cepheid', 'multiplex', 'covid', 'flu', 'rsfinal', 'test', 'not', 'performed'],
                                             ['and', 'covidscr', 'are', 'ordered', 'on', 'the', 'same', 'swab'],
                                             ['neg', 'pos', 'rpt','pos', 'further', 'report', 'to', 'follow'],
                                             ['disregard', 'previous', 'result', 'stating', 'covid', '19', 'virus', 'detected'],
                                              ['the', 'university', 'health', 'covid', '19', 'virus', 'not', 'detected'],
                                              ['detected', 'sars', 'cov', '2', 'n', 'gene', 'low', 'positive'],
                                              ['to', 'covid', '19', 'positive', 'case', 'daughter', 'visited', 'yesterday'],
                                              ['of', 'dry', 'coughing', 'and', 'no', 'covid', 'test', 'in'],
                                              ['admitted', 'to', 'nicu', 'exposed', 'to', 'covid', 'positive', 'mother']
                                             ):

            useful[counter:counter+8] = ['None']*8

        #assign pending
        elif tokenized_length==3 and tokenized[counter:counter+3] == ['see','scanned','result']: 
            useful[counter:counter+3] = ['r_pen']*3 

        #exclude accidently picked-up negatives
        elif 'inneg' in token or 'lineag' in token:
            useful[counter] = 'connecting'

        else:
            #indirect_matches dictionary
            for term, patterns in indirect_matches_dict.items():
                if any([pattern in token for pattern in patterns]):
                    useful[counter] = term
                    break

            #direct_matches dictionary
            for term, patterns in direct_matches_dict.items():
                if any([pattern == token for pattern in patterns]):
                    useful[counter] = term
                    break

            #test_type dictionary
            for test, patterns in test_type_dict.items():
                if any([pattern == token for pattern in patterns]):
                    useful[counter] = test
                    break

    return useful

#interpret text to get initial results
def interpret(useful):

    def save(b):
        #presumptive modifier
        if b[1] == 'r_pos' and modifier[1]:
            b[1] = 'r_pre'

        #end modifier (skips a save)
        if not modifier[2] or modifier[0]:
            output.append([b[0] if b[0] else 'v_unk', 
                           b[1] if b[1] else 'r_neg', 
                           b[2] if b[2] else 't_unk', 
                           modifier[0]]) #final modifier

        b[0] = None
        b[1] = None
        modifier[0:4] = [False, False, False, False]
        return

    sentence = useful[:]
    output = []

    #bundle for current virus/result/test
    #0 = virus, 1 = result, 2 = test
    bundle = [None, None, None]

    #modifiers
    #0 = final, 1 = presumptive, 2 = end, 3 = skip
    modifier = [False, False, False, False]

    none_counter = 0 #counter for hitting consecutive irrelevant words
    virus_counter = 0 #counter for different viruses in same segment

    #xml field processing
    xml_pos = [i for i, x in enumerate(sentence) if x == 'xml']
    num = len(xml_pos)//2
    for i in range(num):
        xml_start_pos = xml_pos[i*2]
        xml_end_pos = xml_pos[i*2+1]
        for j in range(xml_start_pos, xml_end_pos + 1):
            if sentence[j] and sentence[j].startswith('v_') and sentence[j] != 'v_unk':
                bundle[0] = sentence[j]
                bundle[1] = 'r_pos'
                save(bundle)

    #add result to output if result in first 3 words
    if len(sentence) > 3 and not any(['v_' in s for s in sentence[0:3] if s]):
        for s in sentence[0:3]:
            if s and 'r_' in s:
                output.append(['v_unk', s, 't_unk', False])
                break
            elif s and s == 'connecting':
                pass
            else:
                break

    #if there is mention of retest but no final result flag, assign final flag to start
    if ('retest' in sentence or (len(sentence) > 0 and sentence[0] == 'r_ind')) and 'final' not in sentence :
        modifier[0] = True

    #loop on words in sentence
    for word in sentence:

        if word: #relevant term
            none_counter = 0 #restart counter

            #set current virus 
            if word.startswith('v_'):
                #different virus
                if word != 'v_unk' and word != bundle[0]:
                    #save current result if hitting a different virus
                    if bundle[0] and bundle[0] != 'v_unk':
                        #skip modifier
                        if modifier[3]:
                            modifier[3] = None #reset skip modifier
                            bundle[1] = None
                        else:
                            save(bundle)
                            virus_counter += 1 #increase counter if different virus in segment     
                    bundle[0] = word
                #same virus
                elif word != 'v_unk' and word == bundle[0]:
                    #save current result if there is one
                    if bundle[1]:
                        save(bundle)
                    bundle[0] = word
                #only set to general virus if there's no current virus
                elif word == 'v_unk' and not bundle[0]:
                    bundle[0] = word

            #set current result
            elif word.startswith('r_'):
                if word == 'r_ind':
                    if bundle[1]: 
                        save(bundle)
                    bundle[1] = word
                elif word == 'r_neg' and bundle[1] not in ('r_ind',):
                    if bundle[1]: 
                        save(bundle)
                    bundle[1] = word
                elif word == 'r_pos' and bundle[1] not in ('r_ind', 'r_neg'):
                    bundle[1] = word

                elif word in ('r_rej', 'r_can', 'r_pen') and bundle[1] not in ('r_ind', 'r_neg', 'r_pos'):
                    if word == 'r_rej':
                        bundle[1] = word
                    elif word == 'r_can' and bundle[1] not in ('r_rej',):
                        bundle[1] = word
                    elif word == 'r_pen' and bundle[1] not in ('r_rej', 'r_can'):
                        bundle[1] = word

            #set current test
            elif word.startswith('t_'):
                bundle[2] = word

            #final modifier
            elif word == 'final':
                if bundle[0] and bundle[1]:
                    save(bundle)
                modifier[0] = True
                bundle[1] = None #reset result

            #presumptive modifier
            elif word == 'presumptive':
                modifier[1] = True

            #end modifier/word
            elif word == 'end':
                #end early only if there is already result
                if len([o for o in output if o[1] in ('r_ind', 'r_neg', 'r_pos')]) > 0: 
                    return output
                if bundle[0] and bundle[1]:
                    save(bundle)
                modifier[0:4] = [False, False, True, False] #end modifier skips next save
                #end early only if there is already result
                if len(output) > 0:
                    return output

            #skip modifier
            elif word == 'skip':
                if bundle[0] and bundle[1]:
                    save(bundle)
                modifier[3] = True
                bundle[0] = None
                bundle[1] = None

            #stop word
            elif word == 'stop':
                if bundle[0] and bundle[1]:
                    save(bundle)
                modifier[0:4] = [False, False, False, False]
                bundle[0] = None
                bundle[1] = None           

            #reset word
            elif word == 'reset':
                modifier[0:4] = [False, False, False, False]
                bundle[0] = None
                bundle[1] = None

        else: #word is None
            none_counter += 1

            if none_counter == 2: #can change threshold
                #save if there is current virus and result
                if bundle[0] and bundle[1]:
                    save(bundle)
                #save the last virus if multiple were listed
                elif bundle[0] and bundle[0] != 'v_unk' and virus_counter > 1:
                    if modifier[3]:
                        modifier[3] = None #reset skip modifier
                    else:
                        save(bundle)
                #reset
                none_counter = 0 
                virus_counter = 0
                bundle[0] = None
                bundle[1] = None
                modifier[0:4] = [False, False, False, False]

    #if there is still a remaining result
    if bundle[1]: 
        save(bundle)

    #if there is an extra virus listed at the end
    elif bundle[0] and bundle[0] != 'v_unk' and virus_counter > 1 and not modifier[3]:
        save(bundle)

    return output
# %%
def assign_test_virus_types(filename):

    df_loinc_trcodes = readin_TR_LOINC_file(filename)
    mappings = {np.NaN : 'unk','--':'unk', 'culture':'cult', 'other':'oth', 'entero_rhino_D68':'entero_rhino'}

    df_loincs = df_loinc_trcodes.filter(items=['observationcode','virus_type','test_type']).drop_duplicates()
    df_tr_codes = df_loinc_trcodes.filter(items=['testrequestcode','virus_type','test_type']).drop_duplicates()
    #cleaning the categories to match previously defined ones
    df_loincs = df_loincs.replace(mappings)
    df_loincs['virus_type'] = df_loincs['virus_type'].apply(lambda x: 'coronavirus' if 'corona' in x else x)
    df_loincs['virus_type'] = df_loincs['virus_type'].apply(lambda x: 'v_' + x)
    df_loincs['test_type'] = df_loincs['test_type'].apply(lambda x: 't_' + x)

    #assign LOINCs to virus and test type
    loincs_by_v = {}
    loincs_by_t = {}
    for index, row in df_loincs.iterrows():
        loincs_by_v.setdefault(row['virus_type'], [])
        loincs_by_v[row['virus_type']].append(row['observationcode'])
        loincs_by_t.setdefault(row['test_type'], [])
        loincs_by_t[row['test_type']].append(row['observationcode'])

    #remove the unk ones
    try:
        del loincs_by_v['v_unk']
        del loincs_by_t['t_unk']
    except KeyError:
        print(' Loinc v/t_unk not found')

    #use reference excel to assign TR codes to virus and test type
    #added COVID19 TR codes

    #cleaning the categories to match previously defined ones
    df_tr_codes = df_tr_codes.replace(mappings)
    df_tr_codes['virus_type'] = df_tr_codes['virus_type'].apply(lambda x: 'coronavirus' if 'corona' in x else x)
    df_tr_codes['virus_type'] = df_tr_codes['virus_type'].apply(lambda x: 'v_' + x)
    df_tr_codes['test_type'] = df_tr_codes['test_type'].apply(lambda x: 't_' + x)

    #assign LOINCs to virus and test type
    tr_codes_by_v = {}
    tr_codes_by_t = {}
    for index, row in df_tr_codes.iterrows():
        tr_codes_by_v.setdefault(row['virus_type'], [])
        tr_codes_by_v[row['virus_type']].append(row['testrequestcode'])
        tr_codes_by_t.setdefault(row['test_type'], [])
        tr_codes_by_t[row['test_type']].append(row['testrequestcode'])

    #remove the unk ones
    try :
        del tr_codes_by_v['v_unk']
        del tr_codes_by_t['t_unk']
    except KeyError:
        print( f'v_unk/t_unk not found' )

    return [df_loinc_trcodes,loincs_by_t, loincs_by_v,tr_codes_by_v, tr_codes_by_t]

def process_result(tokens, testrequestcode, observationcode, results, loincs_by_v, loincs_by_t, tr_codes_by_v, tr_codes_by_t):
    dd = {}
    update_t_pcr_flag = False

    ###extra conditions

    #remove voc 
    if any([t in ['voc','vocs','variant','variants'] for t in tokens[0:7]]):
        return dd

#         #LOINC/TR exclusions
#         if (observationcode in loinc_exclusions) or (testrequestcode in tr_exclusions):
#             return dd

    for i in range(len(tokens)):
        #exclude antibody tests
        if tokens[i:i+3] in (['covid','19','igg'],['cov','2','antibodies'],):
            return dd
        #delete all results for irrelevant phrases
        if tokens[i:i+5] in (['swab', 'is', 'required', 'for', 'both'],
                             ['is', 'unable', 'to', 'go', 'until'],
                             ['human','herpes','simplex','virus','type'],
                             ['registration','error','please','disregard','result'],
                             ['was','exposed','to','caregiver','with'],
                             ['corrected','report','specimen','sent','to']):
            return dd
        #make presumptive-positive if test is investigational
        if tokens[i:i+3] in (['not', 'been', 'established'], 
                             ['is', 'considered', 'investigational'], 
                             ['a', 'retrospective', 'review']):
            for r in results:
                if (r[0] == 'v_covid' or r[0] == 'v_unk') and r[1] == 'r_pos':
                    r[1] = 'r_pre' 
        #change negative to pending if there are results to follow
        if tokens[i:i+3] == ['to', 'follow', 'tested']:
            for r in results:
                if r[1] in ('r_neg','r_can','r_rej') and not r[3]:
                    r[1] = 'r_pen'
        if tokens[i] == 'naat' or tokens[i:i+4] == ['isothermal', 'nucleic', 'acid', 'amplification'] or tokens[i:i+5] == ['confirmatory', 'pcr', 'testing', 'is', 'required'] or tokens[i:i+3] == ['pcr', 'not', 'collected']:
            update_t_pcr_flag = True
        if tokens[i:i+2] == ['id', 'now'] and 'detected' in tokens:
            update_t_pcr_flag = True

    #change negative to indeterminate for indeterminate multiplex
    if len(set([v for (v,r,t,f) in results])) > 4:
        if ('indeterminate' in tokens[0:3] or results[0][0:2] == ['v_unk','r_ind']): 
            for r in results:
                if r[1] == 'r_neg':
                    r[1] = 'r_ind'
        elif ('duplicate' in tokens[0:3]): 
            for r in results:
                if r[1] == 'r_neg':
                    r[1] = 'r_can'

    #if there is already a covid result, remove v_unk
    if any([(r[0] == 'v_covid' and r[1] in ['r_pos', 'r_pre', 'r_ind', 'r_neg']) for r in results]):
        results = [r for r in results if r[0] != 'v_unk']

    #remove pcr info if it is a rapid test
    if testrequestcode == 'TR12946-0':
        if update_t_pcr_flag:
            for i in range(len(results)):
                if results[i][2] == 't_pcr':
                    results[i][2] = 't_unk' 
        else:
            results = [r for r in results if r[2] != 't_pcr']

    ###determine virus or test based on LOINC or TR
    v_from_loinc = [loinc_vir for loinc_vir, loincs in loincs_by_v.items() if observationcode in loincs]
    v_from_tr = [tr_codes_vir for tr_codes_vir, tr_codes in tr_codes_by_v.items() if testrequestcode in tr_codes]
    t_from_loinc = [loinc_test for loinc_test, loincs in loincs_by_t.items() if observationcode in loincs]
    t_from_tr = [tr_codes_test for tr_codes_test, tr_codes in tr_codes_by_t.items() if testrequestcode in tr_codes]

    #determine if there are any final/interpretation results
    viruses_with_final = [v for (v,r,t,f) in results if r in ('r_pos', 'r_pre', 'r_ind', 'r_neg', 'r_rej') and f]
    results_final = results
    #remove the non-final/interpretation results for viruses with final/interpretation
    for vf in viruses_with_final:
        results_final = [(v,r,t,f) for (v,r,t,f) in results if not (v in vf and not f)]

    for v, r, t, f in results_final:
        #fill in unknown virus
        if v == 'v_unk':
            if len(v_from_loinc) > 0:
                v = v_from_loinc[0]
            elif len(v_from_tr) > 0:
                v = v_from_tr[0]

        #fill in unknown test
        if t == 't_unk':
            if len(t_from_loinc) > 0:
                t = t_from_loinc[0]
            elif len(t_from_tr) > 0:
                t = t_from_tr[0]

        #fill in pcr if there is a pcr term in text
        if t == 't_unk' and 'pcr' in tokens: 
            t = 't_pcr'

        #remove unknown virus results
        if v != 'v_unk':
            v, r, t = v[2:], r[2:], t[2:]
            #all tests that aren't pcr are oth
            #t = t if t == 'pcr' else 'oth'

            #ASSUME EVERYTHING PCR FOR COVID DATASET
            t = 'pcr'

            dd.setdefault(t, [])

            #compiling results with hierarchy: S (presumptive positive) > P (positive) > I (indeterminate) 
            #                                  > N (negative) > D (pending) > R (invalid) > C (cancelled) 
            same_vir = False
            for i in range(len(dd[t])):
                if v == dd[t][i][0]:
                    same_vir = True
                    if r == 'pre':
                        dd[t][i] = (v,r)
                    elif r == 'pos' and dd[t][i][1] not in ('pre',):
                        dd[t][i] = (v,r)
                    elif r == 'ind' and dd[t][i][1] not in ('pre', 'pos'):
                        dd[t][i] = (v,r)
                    elif r == 'neg' and dd[t][i][1] not in ('pre', 'pos', 'ind'):
                        dd[t][i] = (v,r)
                    elif r == 'pen' and dd[t][i][1] not in ('pre', 'pos', 'ind', 'neg'):
                        dd[t][i] = (v,r)
                    elif r == 'rej' and dd[t][i][1] not in ('pre', 'pos', 'ind', 'neg', 'pen'):
                        dd[t][i] = (v,r)
                    elif r == 'can':
                        pass
            if not same_vir:
                dd[t].append((v,r))

    return dd

#create output as character value for each virus and test type
result_char = {'pre':'S', 'pos': 'P', 'ind':'I', 'neg':'N', 'pen':'D', 'can':'C', 'rej':'R'}

def char_output(results, ind, df_results):

    #loop through each test type and virus
    for t, pairs in results.items(): #need to update if there are multiple test types
        for v, r in pairs:
            if v in ('adenovirus', 'bocavirus', 'coronavirus', 'entero_rhino', 'hmv', 'covid'):
                df_results.at[ind, v] = result_char[r]

            elif v.startswith('para'):
                df_results.at[ind, 'para'] = result_char[r]

            elif v.startswith('flu'):
                df_results.at[ind, 'flu'] = result_char[r]
                if '_a' in v:
                    df_results.at[ind, 'flu_a'] = result_char[r]
                if '_h1' in v:
                    df_results.at[ind, 'flu_a_h1'] = result_char[r]
                if '_h3' in v:
                    df_results.at[ind, 'flu_a_h3'] = result_char[r]
                if '_b' in v:
                    df_results.at[ind, 'flu_b'] = result_char[r]

            elif v.startswith('rsv'):
                df_results.at[ind, 'rsv'] = result_char[r]
                if '_a' in v:
                    df_results.at[ind, 'rsv_a'] = result_char[r]
                if '_b' in v:
                    df_results.at[ind, 'rsv_b'] = result_char[r]

    return

def readin_IntermediateFile(filename, test_type):

    df = filename
    df.columns = [x.lower() for x in df.columns]
    if sum(df.columns == 'virus') ==0:
        df['virus'] = test_type
    df.cleaned_value = df.cleaned_value.str.lower().str.strip()

    return(df)

#  calculate missing 
def calc_miss(df1, checkcols = flursvcols):
    missdata = (df1[df1[checkcols].isna()
                      .all(axis=1)][['cleaned_value','observationcode','testrequestcode']]
                      )
    overallmissing = df1[checkcols].isna().all(axis=1).value_counts()/df1.shape[0]
    # print(f'number of tests {df1.shape[0]}')
    print (f'\n overall missing info {np.round(overallmissing[True]*100,2)}%')
    
    # if writeflag :
    #     missdata.cleaned_value.value_counts().reset_index().to_csv(output_path + f'\..\missingness.csv')

    return [missdata, overallmissing]

# Read in Kamil's mapping of the test based on the value
    ## read Kamil's mapping of the cleaned-values
    ## and proces it to apply the results to the respective columns
def readin_ValueClassification(filename):
    
    out = pd.read_csv(filename, sep=",",header=0,index_col=None).iloc[:,:4]
    out.columns = ['cleaned_value','counts','result', 'name']
    out.result = out.result.str.lower().str.strip()
    out.name = out.name.str.lower().str.strip()
    out.cleaned_value = out.cleaned_value.str.lower().str.strip()
    # print(out.head())
    def assign_result(x, resultcol, microcols):
        # print(f'resultcol : {resultcol}, x-= {x}')
        foundSeries = pd.Series([np.NaN]*len(micro_org_cols ),index = micro_org_cols)
        if x.notna()['name'] :
            foundlist = x['name'].split()
            # print(foundlist)
            absence = [ all(virus != names for names in micro_org_cols) for virus in foundlist]
            # print(absence)
            foundlist = ['others' if absence[i] else foundlist[i] for i in range(len(foundlist))]
            foundSeries[foundlist] = x[resultcol]

        return foundSeries
     
    results = out.apply(assign_result, resultcol="result", microcols = micro_org_cols, axis=1)
    resultmap ={'positive':'P', 'negative':'N', 'unknown':'U', 
             'cancelled':'C' , 'invalid':'R', 'pending':'P' , 'indeterminate':'I'}
    for key in resultmap:
        results[micro_org_cols] = results[micro_org_cols].replace(key, resultmap[key])
    return [out,results]

# read in combined virus _codes mapped.
def readin_TR_LOINC_file(filename):
  
    dataf = pd.read_csv(filename,sep=",",header=0)
    dataf.loinc = np.where(dataf['trcode'].notna(), np.nan, dataf['loinc'])
    # forward fill the missing trcode by copying.
    dataf.trcode.ffill(inplace=True)
    # rename and replace TR_ANY by Null
    dataf = (dataf.dropna(subset=['loinc'])
            .rename(columns={'loinc':'observationcode','trcode':'testrequestcode'})
            .replace('TR_ANY',np.nan)
            )
    # print(dataf.virus_type.value_counts(dropna=False))
    # convert and strip the end spaces 
    dataf.virus_type = dataf.virus_type.str.strip()

    return dataf

def positivity(df1, checkcols=flursvcols):
    Positivity_rate = df1[checkcols].apply(lambda x: x.value_counts(dropna=False))
    # if writeflag:
    #     Positivity_rate.to_csv(output_path + f'\..\Positivity_rate.csv')
    print( " Positivity Rate: " , Positivity_rate)
    return Positivity_rate

# this program maps the virus type to it actual name and then maps it to the symbols
# for each row based on the "result" for the.
def set_value(x):

    resultmap ={'positive':'P', 'negative':'N', 'unknown':'U', 
               'cancelled':'C' , 'invalid':'R', 'pending':'P' , 'indeterminate':'I'}
    
    test_dict = dict(zip ( 
        ['Resipratory Virus, Multiplex', 'RSV', 'Flu A', 'Flu A + Flu B', 'Flu',
         'Flu A + Flu B + RSV', 'Flu B', 'Flu A H1', 'Flu A H3','RSV B','RSV A + RSV B',
         'RSV A'], 
        ['rsv', 'rsv','flu_a',['flu_a','flu_b'], 'flu',['flu_a','flu_b','rsv'],
            'flu_b','flu_a_h1','flu_a_h3','rsv_b', ['rsv_a','rsv_b'],'rsv_a']
        ))
    cols = None
    resultcols = pd.Series([np.NaN]*len(micro_org_cols),index = micro_org_cols)
    try : 
        cols = test_dict[x['virus_type']]
        if  type(cols) == 'str' :
            cols = [cols]
    
    except Exception as e: 
        obs_tr_code_not_found.setdefault( x['testrequestcode'], set()).add(x['observationcode'])

        print (x['virus_type'])
        print('error in cols generation...' )
        print(e)

    try :
        if len(cols) >0:
            # print(f'col is {cols}')
            resultcols[cols] = resultmap[x.result]
    
    except Exception as e:
        # obscode_not_found.add(x['observationcode'])
        obs_tr_code_not_found.setdefault( x['testrequestcode'], set()).add(x['observationcode'])

        print (x['virus_type'])
        print('error in assignment of result ...')
        print(e)
    
    return  resultcols

def add_micro_org_cols(df):
    absentcols = [ all(x != e for e in df.columns ) for x in micro_org_cols]
    absentcols = [micro_org_cols[i] for i in range(len(micro_org_cols)) if absentcols[i]]
    df = df.reindex(df.columns.tolist() + absentcols, axis=1)
    df.head()
    calc_miss(df, checkcols = micro_org_cols)
    positivity(df, checkcols= micro_org_cols)

    return df

def merge (Olisdata:pd.DataFrame = None, codesData:pd.DataFrame = None, join_type:str='left'):

    """this is customized  merge function to merge our list of TR/LOINC codes file with that of the dataset

    Args:
        Olisdata (pd.DataFrame): dataframe with least these columns: 
            'testrequestcode': test request field
            'observationcode' loinc codes field
        codesData (pd.DataFrame): our dataset of the TR and LOINC codes read from the file; contains following columsn
            testrequestcode, 
            observationcode :
            virus_type : 

        join_type (str,optional): _description_. Defaults to 'left'.
            other options are as per the pd.merge function : only 'inner' is taken
        should be inner if you want to filter out the data set that has non/ICES LOINC/TR codes.

    Returns:
        pd.DataFrame: pandas DataFrame with columns same as input Olisdata, but with added columns from the
            mapping table
    """

    DwCodes = Olisdata.merge( codesData[codesData.testrequestcode.notna()], how=join_type,\
                        on=['testrequestcode','observationcode'] )
    if (join_type == 'inner'):
        DwCodes1 = Olisdata.merge(codesData[codesData.testrequestcode.isna()].drop(columns=['testrequestcode'])\
                            .drop_duplicates(), how=join_type,on=['observationcode'] ).drop_duplicates()
        DwCodes = pd.concat([DwCodes,DwCodes1],axis=0, ignore_index=True ).drop_duplicates()
    
    if (join_type == 'left'):
        DwCodes = DwCodes.merge( codesData[codesData.testrequestcode.isna()].drop(columns=['testrequestcode'])\
                                .drop_duplicates(), how=join_type,on=['observationcode'] ).drop_duplicates()
        assert( DwCodes.shape[0] == Olisdata.shape[0])
        DwCodes['virus_type'] = DwCodes.virus_type_y.fillna(DwCodes.virus_type_x)
        DwCodes['virus'] = DwCodes.virus_y.fillna(DwCodes.virus_x)
        DwCodes.drop(columns=['virus_type_y','virus_type_x','virus_x','virus_y'], inplace=True)

    DwCodes.columns = [x.lower() for x in DwCodes.columns]

    # calc_miss(DwCodes, checkcols=micro_org_cols) # Not change will happen.. that' is correct.
    # positivity(DwCodes, checkcols=micro_org_cols)

    return DwCodes

# %%
def main_process():

    ## 1. read in TR request code mapping file to identify the virus its associated with.
    mapping = readin_TR_LOINC_file(combined_virus_codes)
    print( "read in : ",combined_virus_codes)
    ## 2. read in sas dataset or from red-shift
    df = read_input(input_path)

    ## 3. filter out the required rows only with LOINcs in mapping datasets;
    mapped_df = merge(df, mapping, join_type = 'inner');

    print("filtered # rows: ", len(mapped_df))
    df, df_gp = process_input(mapped_df)

    # read in loinc and tr codes with their assignment types;
    df_loinc_trcodes, loincs_by_t, loincs_by_v,tr_codes_by_v, tr_codes_by_t = assign_test_virus_types(combined_virus_codes)

    #clean values
    df_gp["cleaned_value"] = df_gp["value"].apply(clean)

    #group by unique records (org, TR code, Obs code, cleaned text) and store original indexes as tuple
    df_gp = df_gp.reset_index()
    groupby_vars = ['patientid','ordersid','observationdatetime','observationreleasets','reportinglaborgname', 'testrequestcode', 'observationcode','cleaned_value']
    df_gp = df_gp.groupby(groupby_vars).agg({'value': 'count', 
                                                    'original_indexes': lambda x: tuple([i for tup in x for i in tup])}).reset_index()
    df_gp = df_gp.rename(columns={'value':'count'})

    df_gp = df_gp.sort_values(by=['count'], ascending=False).reset_index(drop=True)
    print('unique records after cleaning:', len(df_gp))

    #tokenize
    df_gp["cleaned_tokenized_value"] = df_gp["cleaned_value"].apply(tokenize)

    #assign labels using dictionary
    df_gp["useful_tokens"] = df_gp["cleaned_tokenized_value"].apply(assign_labels)

    #interpret the labelled tokens
    df_gp["initial_results"] = df_gp["useful_tokens"].apply(interpret)

    # Post proecssing of the results
    # fill in unknown viruses based on LOINC or TR code, roll up results to one test type
    final_results = []
    for i in range(len(df_gp)):
        final_results.append(process_result(df_gp["cleaned_tokenized_value"][i],
                                            df_gp["testrequestcode"][i], df_gp["observationcode"][i], 
                                            df_gp["initial_results"][i], loincs_by_v, loincs_by_t, tr_codes_by_v, tr_codes_by_t))

    #translate results to 1-character format
    col_virus = ['covid', 'adenovirus', 'bocavirus', 'coronavirus', 'flu', 'flu_a', 'flu_a_h1', 'flu_a_h3', 'flu_b',
            'entero_rhino', 'hmv', 'para', 'rsv', 'rsv_a', 'rsv_b']

    #create empty df to fill in results
    df_results = pd.DataFrame(index=np.arange(len(df_gp)), columns=['original_indexes']+col_virus)
    df_results['original_indexes'] = df_gp['original_indexes']

    #fill in results
    for i in range(len(df_gp)):
        char_output(final_results[i], i, df_results)

    output = [None]*len(df)

    #order results based on original_indexes
    for row in df_results.itertuples():
        for i in row[1]: #original_indexes
            output[i] = tuple(row[2:])

    if output_flag == 1:                
        df_output = pd.concat([df, pd.DataFrame(output, columns=col_virus)], axis=1)

    #FINAL DATASET TO OUTPUT
    df_output.describe()

    int_output_cols = ['patientid','ordersid','observationdatetime','observationreleasets','count', 'reportinglaborgname', 'testrequestcode', 'observationcode', 'cleaned_value']
    df_final = df_gp[int_output_cols].join(df_results)

    ## 1. read kamils file
    valuemap = readin_ValueClassification(cleaned_value_classification)

    df_final.columns = [x.lower() for x in df_final.columns]
    # if sum(df.columns == 'virus') ==0:
    #     df['virus'] = test_type
    df_final.cleaned_value = df_final.cleaned_value.str.lower().str.strip()
    print ( " Kamil's file read in ")
    ## 2. calculated missing percentage
    calc_miss(df_final)  

    # add the columns of micro organism that doesn't exist
    df_final = add_micro_org_cols(df_final)

    valuemap = pd.concat([valuemap[0],valuemap[1]], axis=1)
    
    ###
    df_wnulls = df_final[df_final[micro_org_cols].isna().all(axis=1)].drop(columns=micro_org_cols)\
        .merge(valuemap, how='left', on ='cleaned_value')

    df_wonulls = df_final[df_final[micro_org_cols].notna().any(axis=1)]


    df2= pd.concat([df_wonulls.reset_index(drop=True), df_wnulls.reset_index(drop=True)]).reset_index(drop=True)
    
    # this it make sure that NaN from two parts are same
    for cols in micro_org_cols:
        df2[cols][df2[cols].isna()] = np.nan

    calc_miss(df2, checkcols = micro_org_cols) # 15%
    positivity(df2, checkcols= micro_org_cols)

    print(" after concatenation : ",df2.shape)
    
    #merge the mapping information with the data on trrequestcode and observationcode
    mapped_df = merge(df2, mapping)

    # fill the mapped test columns based on LOINC & Test request code.
    filled_df = ( mapped_df.loc[mapped_df.result.notna(),
                ['cleaned_value','virus_type', 'observationcode','testrequestcode','result']]
                .apply(set_value,axis=1))
    
    # obscode_not_found_list = list(obscode_not_found)
    print("The following observation codes were not found:", obs_tr_code_not_found)

    mapped_df.loc[mapped_df.result.notna(),micro_org_cols] = filled_df[micro_org_cols].copy()

    missdata, missigness = calc_miss(mapped_df, checkcols=micro_org_cols) # not its 0%
    positivity(mapped_df, micro_org_cols)
    

    return mapped_df

# %%
# df_gp[int_output_cols][df_gp.index.isin(df_tracker_delta.index)].join(df_results.drop(columns=['original_indexes'])).to_csv(f'intermediate_updated_output_delta.csv')


# %%
if __name__ == '__main__':

    global cleaned_value_classification
    global combined_virus_codes
    global obs_tr_code_not_found
    cleaned_value_classification = "cleaned_value_classification.csv"
    combined_virus_codes = 'combined_virus_codes.csv'
    obs_tr_code_not_found = {}
    #1.  read in arguments()
    # %%

    #help command 
    parser = argparse.ArgumentParser(description= 'Provide the input path, for example: "..\\input\\flu_rsv_set.sas7bdat" \n'
                                     'and the output file path, for example: "..\\output\\mapped_flu_rsv.csv" \n\n'
                                      'NOTE: It reads in two files \n'
                                    '------------------------------- \n'
                                     '1. combined_virus_codes.csv: Name has to remain same and should be in the directory: "indata" \n'
                                        'under current working directory. This file should contain following columns : \n'
                                        '\ta. trcode: test request codes. \n'
                                        '\tb. loinc: observation code found in OLIS observation table \n'
                                        '\tc. virus:  name of the virus or pathogen for which test is being conducted, e.g. Flu, RSV etc.. \n'
                                        '\td. virus_type: sub type of the virus/pathogen that is be tested for based on the LOINCS. E.g. FLU, \n'
                                        '\t   FLU A, FLU A + FLU B, RSV, RSV A, RSV A + RSV B. \n'
                                        '\te. test_type: mainly used by ICES methodology part corresponds to test methodology. E.g. PCR etc. \n\n'
                                     '2. cleaned_value_classification.csv: this file is provided by HDSB, MOH. specifically the format can be seen \n'
                                        'by opening the file, which is fairly large and classifies cleaned-value manually \n\n'
                                    '------------------------------- \n'
                                    'NOTE: if you see any issues please feel free to reach us at : hdsb@ontario.ca \n'
                                     , formatter_class=RawTextHelpFormatter)
    parser.add_argument('-i', '--input', type=str, help='input file w/path')
    parser.add_argument('-o', '--output', type=str, help='output file w/path')
    
    args = parser.parse_args()

    #take values from command line
    input_path = args.input
    output_path = args.output

    # figure out input path from input_path
    # TODO : [...] by default it take current working directory 
    # file_path = ...
    spare_file_path = file_path / "indata"
    #spare_file_path = os.path.join(file_path,"indata")
    print(f"other input files:\n\t cleaned_value_classification.csv\n\tcombined_virus_codes.csv\n\t\
    to be read from : {spare_file_path.absolute()}\n")
    
    cleaned_value_classification = spare_file_path.absolute() / cleaned_value_classification
    combined_virus_codes = spare_file_path.absolute() / combined_virus_codes
    # %%
    mapped_df = main_process()

    if writeflag:
        # also check for the existence of outcome_result.csv file 
        mapped_df.to_csv(output_path)
    


# %%
