# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 18:13:14 2024

@author: ACER
"""

import pandas as pd
import streamlit as st 
import xlrd
st.set_page_config(page_title="Bank Statement Search", page_icon="bank", layout="wide")
st.title("  :bank: :red[ICICI Bank Statement Search App]")
fl = st.file_uploader(" Upload a file using 'Browse files' ", type=(["xls"])) #upload file & file type
st.button("Rerun") # Refresh data cache

 
if fl is not None:   #check only if file ploaded below code will be executed.
    @st.cache_data   #Automatic data refresh
    def load_data(fl): # Load data in data frame
        Bankdata = pd.read_excel(fl, header=12) #skipe header records 
        #print('columns ==', Bankdata.columns)
        return Bankdata
    Bankdata = load_data(fl) #call method
    #rename columns
    Bankdata.rename(columns={'Withdrawal Amount (INR )':'Withdrawals', 'Deposit Amount (INR )':'Deposits'}, inplace=True)
    #print('columns 3', Bankdata.columns)
    #print('head', Bankdata.head(7))
    Bankdata['Withdrawals']= pd.to_numeric(Bankdata['Withdrawals'], errors='coerce') #covert datatype from object 
    #Bankdata['Balance']= pd.to_numeric(Bankdata['Balance'], errors='coerce')
    Bankdata['Deposits']= pd.to_numeric(Bankdata['Deposits'],  errors='coerce') #covert datatype from object
    Bankdata = Bankdata.drop(['Unnamed: 0','Cheque Number'], axis=1) # drop unwanted columns
    Bankdata['Transaction Remarks'].fillna('', inplace=True) #if in file null value convert to empty space (char)
 
    top_5_withdrawals = Bankdata.sort_values(by='Withdrawals', ascending=False).head(5)  #get 1st 5 data rows
    #top_5_withdrawals = top_5_withdrawals.reset_index(drop=True)
    #top_5_wthdropt  = top_5_withdrawals.drop(index=0, axis=0, inplace=False) #drop Totals row
    top_5_deposits = Bankdata.sort_values(by='Deposits', ascending=False).head(5) #get 1st 5 data rows
    #top_5_deposits = top_5_deposits.reset_index(drop=True)
    #top_5_depdropt  = top_5_deposits.drop(index=0, axis=0, inplace=False)
    col1, col2 = st.columns(2)
    with col1:
       with st.expander("Top 5 Withdrawls"): #for dropdown
          st.dataframe(top_5_withdrawals)   # actual data
    with col2: 
        with st.expander("Top 5 Deposits"):  #for dropdown
           st.dataframe(top_5_deposits) #for dropdown
    stinput = st.text_input("Enter keyword to search -") #inpt for search
    #
    if len(stinput) > 0:  #process only if in input is present
       #print('stinput-1', stinput)
       #print(np.isnan(stinput))
       dfs1 = Bankdata.loc[Bankdata['Transaction Remarks'].str.contains(stinput, case=False)] #search for input string in Tran column
       def functrunc(description):
           templst = list(description.split('/')) #Customization for column transaction to substring from 3rd '/' to 5rd '/'
           return templst[3:5]
       dfs1['Transaction'] = dfs1['Transaction Remarks'].apply(functrunc) #adding a column for description
       dfs1w = dfs1['Withdrawals'].sum() #sum withdrawal amount
       dfs1d = dfs1['Deposits'].sum() #sum depopsit amount
       sumdif = dfs1w - dfs1d #difference
       st.write(f':money_with_wings: :red[WITHDRAWALS  -:  {dfs1w}]   :moneybag: :green[DEPOSITS   -:  {dfs1d}  ]') #writing to streamlit
       st.write(f':abacus: With - Dep = {sumdif}                 ') #writing to streamlit UI 
       with st.expander("View Searched Transactions"): # Searched transactions
          st.dataframe(dfs1[['Value Date','Transaction', 'Withdrawals', 'Deposits','Transaction Remarks']])    
    else:
        #print('stinput-2 ', stinput)
        dfs1d = 0
        dfs1w = 0
         
    with st.expander("View All Data"):  # all data
         st.dataframe(Bankdata[['Value Date','Withdrawals', 'Deposits','Transaction Remarks']])  