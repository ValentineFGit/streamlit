# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 18:11:55 2024

@author: MacBook Pro
"""
#!pip install streamlit
import pandas as pd
import streamlit as st 
from streamlit.web import cli as stcli
from  streamlit import runtime
import os
import warnings
warnings.filterwarnings('ignore')
#from streamlit import caching
#caching.clear_cache()
libdata = pd.read_csv('LoansDatasest.csv')
print(libdata.info())
#@st.cache(allow_output_mutation=True, suppress_st_warning=True)
st.set_page_config(page_title="global library dataser", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: global dataset")
#@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def clear_cache():
 st.runtime.legacy_caching.clear_cache()
 st.sidebar.button("Refresh Program",on_click=clear_cache)
#print(libdata.head(10))
#st.write(libdata.head(100))
df100 = libdata.head(10)
print(df100)
#choose age 
st.sidebar.header("choose your filter")
age  = st.sidebar.multiselect("pick your age", df100["customer_age"].unique())         
fil_age = df100[df100["customer_age"].isin(age)]
#print(fil_age)
#ag2 = 23
#sel_age = df100[df100["customer_age"].isin([23])]
#print(sel_age)
col1 , col2 = st.columns(2)
with col1:
    st.write(fil_age)
     #st.write(sel_age)

#if __name__ == '__main__':
#    if runtime.exists():
#        
#    else:
#        sys.argv = ["streamlit", "run", sys.argv[0]]
#        sys.exit(stcli.main())