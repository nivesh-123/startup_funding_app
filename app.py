import numpy as np
import pandas as pd
import streamlit as st

fund = pd.read_csv(r"/home/nivesh/startup_funding_project_streamlit/startup_funding.csv")
fund['Investors Name'] = fund['Investors Name'].fillna('Undisclosed')

# design of side bar
st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select Analysis type',['Overall analysis','Startup analysis','Investor analysis'])

if option == 'Overall analysis':
    st.title('Overall analysis')
elif option == 'Startup analysis':
    startup = st.sidebar.selectbox('Select the startup',sorted(fund['Startup Name'].unique().tolist()))
    btn1 = st.sidebar.button('perform analysis')
    if btn1:
        st.title('Startup Analysis')
else:
    investor = st.sidebar.selectbox('Select the Investor',sorted(fund['Investors Name'].unique().tolist()))
    btn2 = st.sidebar.button('perform analysis')
    if btn2:
        st.title('Investor Analysis')