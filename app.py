import numpy as np
import pandas as pd
import streamlit as st

fund = pd.read_csv(r"/home/nivesh/startup_funding_project_streamlit/data/fund_cleaned_final.csv")
fund_investor = pd.read_csv(r"/home/nivesh/startup_funding_project_streamlit/data/fund_investor_final.csv")

# design of side bar
st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select Analysis type',['Overall analysis','Startup analysis','Investor analysis'])

if option == 'Overall analysis':
    st.title('Overall analysis')
elif option == 'Startup analysis':
    startup = st.sidebar.selectbox('Select the startup',sorted(fund['startup_clean'].unique().tolist()))
    btn1 = st.sidebar.button('perform analysis')
    if btn1:
        st.title('Startup Analysis')
else:
    investor = st.sidebar.selectbox('Select the Investor',sorted(fund_investor['investor_clean'].unique().tolist()))
    btn2 = st.sidebar.button('perform analysis')
    if btn2:
        st.title('Investor Analysis')