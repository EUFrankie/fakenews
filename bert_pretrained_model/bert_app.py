#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 16:42:29 2020

@author: Myriam
"""

import pandas as pd
import numpy as np
import requests
import json
import streamlit as st

from sklearn.metrics.pairwise import cosine_similarity


#CHANGE THE PATHS OF THE FILES
GLOBAL_DATA='original_data_with_identifier.csv'
GLOBAL_BERT='identifier_bert.json'
port_num='3333' #TO RUN LOCALLY


def get_embeddings(texts):
    '''
    INPUT: list of texts
    OUTPUT: list of vectorized texts by BERT
    '''
    headers = {
        'content-type':'application/json'
    }
    data = {
        "id":123,
        "texts":texts,
        "is_tokenized": False
    }
    data = json.dumps(data)
    r = requests.post("http://localhost:" + port_num + "/encode", data=data, headers=headers).json()
    return r['result']


def get_dataset(path):
    return pd.read_csv(path)

def get_embeeds(path):
    with open(path, 'r') as f:
        return json.load(f)
    
    
def get_top_measures(text,num=5):
    #embedd the data
    embeed=get_embeddings([text])
    
    #get the data
    data=get_dataset(GLOBAL_DATA)
    bert_dict=get_embeeds(GLOBAL_BERT)
    vectors=[bert_dict[key]['BERT_vectors'] for key in bert_dict.keys()]
    
    #comput the similarity
    results=cosine_similarity(embeed,vectors)
    
    #create a dataframe
    selected=pd.DataFrame(results,columns=list(bert_dict.keys()))
    selected['input']='input'
    selected=selected.set_index('input')
    
    #get the top5
    arank = selected.apply(np.argsort, axis=1)
    ranked_cols = selected.columns[arank.values[:,::-1][:,:num]]
    new_frame = pd.DataFrame({'identifier': ranked_cols[0]})
    new_frame['score']=new_frame['identifier'].apply(lambda x: selected[x].to_list()[0])
    
    #return the merger of top with the database
    return pd.merge(data,new_frame,on='identifier')

'''
# Talk with Frankie! :dog:
'''

text=st.text_input("What fake new have you heard about recently?: ",value="")

if text!='':


    df_results=get_top_measures(text)
    
    st.write('### THIS IS WHAT WE FOUND 🤔')
    for it,row in df_results.iterrows():
        st.write('**-> FOUND:**',row['title'])
        st.write('> ',row['fact_checker'],'*say it is',row['label'],'*because:',row['explanation'])
        st.write('Here is the link:',row['url_checker'])
        st.write('\n')
    
