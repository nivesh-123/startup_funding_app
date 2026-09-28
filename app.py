import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# =========================================================
# 1. INITIALIZATION ZONE (Always at the very top!)
# =========================================================
# set all the memory flags for different options

if 'show_overall' not in st.session_state:
    st.session_state['show_overall'] = False

if 'show_startup' not in st.session_state:
    st.session_state['show_startup'] = False

if 'show_investor' not in st.session_state:
    st.session_state['show_investor'] = False

# =========================================================
# set the page config
# =========================================================

st.set_page_config(layout='wide',page_title="Funding analysis App")

# =========================================================
# import the cleaned dataset and change datatypes and add required columns
# =========================================================

fund = pd.read_csv(r"data/fund_cleaned_final.csv")
fund_investor = pd.read_csv(r"data/fund_investor_final.csv")
fund['date'] = pd.to_datetime(fund['date'],errors='coerce')
fund_investor['date'] = pd.to_datetime(fund_investor['date'],errors='coerce')

fund.info()
fund_investor.info()
# sort the fund dataframe and extract the year, month and quarter from the date column
fund = fund.sort_values(by='date',ascending=False)
fund['year'] = fund['date'].dt.year
fund['month'] = fund['date'].dt.month
fund['quarter'] = fund['date'].dt.quarter

# sort the fund_investor dataframe and extract the year, month and quarter from the date column
fund_investor = fund_investor.sort_values(by='date',ascending=False)
fund_investor['year'] = fund_investor['date'].dt.year
fund_investor['month'] = fund_investor['date'].dt.month
fund_investor['quarter'] = fund_investor['date'].dt.quarter
# only keep the date component of the date column
fund['date'] = fund['date'].dt.date 
fund_investor['date'] = fund_investor['date'].dt.date 

# =========================================================
# function for investor analysis
# =========================================================

def investor_details(investor):
    # get the name of the investor
    st.title(investor.upper())
    # get the recent 5 investments of the investor
    st.subheader('Recent Investments')
    temp = fund_investor[fund_investor['investor_clean'].str.contains(investor)]
    st.dataframe(temp[['date','startup_clean','vertical','round_clean','amount','investor_clean','city_clean']].head())
    col1,col2 = st.columns(2)
    with col1:
        # get the biggest investments of the investor
        st.subheader('Biggest Investments')
        temp_df1 = temp.groupby('startup_clean')['amount'].sum().sort_values(ascending=False).head()
        fig1,ax1 = plt.subplots()
        ax1.bar(temp_df1.index,temp_df1.values)
        ax1.set_ylabel('Invested amount (Crores rupees)')
        ax1.grid(True,alpha=0.2)
        st.pyplot(fig1)
    with col2:
        # get the sectors of the investments of the investor
        st.subheader('Sector preference')
        temp_df2 = temp.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10)
        fig2,ax2 = plt.subplots()
        ax2.pie(temp_df2.values,labels=temp_df2.index,autopct='%0.01f%%')
        st.pyplot(fig2)
        
    col1,col2 = st.columns(2)
    with col1:
        # track of YoY investments of a investor
        st.subheader('YoY investments')
        temp_df3 = temp.groupby('year')['amount'].sum()
        fig3,ax3 = plt.subplots()
        ax3.plot(temp_df3.index,temp_df3.values,marker = 'o',markersize=3)
        ax3.grid(True,alpha=0.2)
        ax3.set_ylabel('Invested amount (crores rupees)')
        ax3.set_xticks(temp_df3.index,labels=temp_df3.index)
        st.pyplot(fig3,width='stretch')
    with col2:
        # track of rounds of investment in a company
        st.subheader('Rounds of investment')
        temp_df4 = temp.groupby('round_clean')['amount'].sum()
        fig4,ax4 = plt.subplots()
        ax4.pie(temp_df4.values,labels=temp_df4.index,autopct='%0.01f%%')
        st.pyplot(fig4,width='stretch')
    
    col1,col2 = st.columns(2)
    with col1:
        # preferred cities for investment
        st.subheader('Preferred cities for investment')
        temp_df5 = temp.groupby('city_clean')['amount'].sum().sort_values(ascending=False)
        fig5,ax5 = plt.subplots()
        ax5.pie(temp_df5.values,labels=temp_df5.index,autopct='%0.01f%%')
        st.pyplot(fig5,width='stretch')
    with col2:
        # similar investors
            # find the highest investing vertical of the investor
            st.subheader('Similar Investors')
            temp_df = fund_investor.groupby(['investor_clean','vertical'])['amount'].sum().sort_values(ascending=False).reset_index(drop=False).drop_duplicates(keep='first',subset=['investor_clean'])
            req_vertical = temp_df[temp_df['investor_clean'] == investor]['vertical'].values[0]
            temp_series = temp_df[temp_df['vertical'] == req_vertical]['investor_clean'].head()
            st.markdown("\n".join([f"* **{item}**"for item in temp_series]))
            
# =========================================================
# function for overall analysis
# =========================================================

def overall_analysis():
    st.title('Overall Analysis')
    # create four cards
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric(label='Total investment',value = f"₹ {round(fund['amount'].sum()):,} Cr")
    with col2:
        st.metric(label='Max investment',value = f"₹ {round(fund['amount'].max()):,} Cr")
    with col3:
        st.metric(label='Avg. investment',value = f"₹ {round(fund['amount'].mean()):,} Cr")
    with col4:
        st.metric(label='No of investments',value = f"{fund['amount'].count():,}")
    selected_option = st.selectbox('Select type',['Total','Count'])
    if selected_option == 'Total':
        temp = fund.groupby(['year','quarter'])['amount'].sum().reset_index(drop=False)
    else:
        temp = fund.groupby(['year','quarter'])['amount'].count().reset_index(drop=False)
    # Quarter over Quarter investment
    temp_xaxis = temp['quarter'].astype('str') + '-' + temp['year'].astype('str')
    temp_yaxis = round(temp['amount'])
    fig1,ax1 = plt.subplots(figsize=(6,4))
    ax1.plot(temp_xaxis,temp_yaxis,marker='o',markersize=3)
    ax1.set_xlabel('Quarter-Year')
    ax1.grid(True,alpha=0.2)
    ax1.tick_params(axis='x', rotation=75)
    st.pyplot(fig1,width='content')

# =========================================================
# design of side bar
# =========================================================

st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select Analysis type',['Overall analysis','Startup analysis','Investor analysis'])

# =========================================================    
# resetting the session state variables
# =========================================================
if option != 'Overall analysis': st.session_state['show_overall'] = False
if option != 'Startup analysis': st.session_state['show_startup'] = False
if option != 'Investor analysis': st.session_state['show_investor'] = False

# =========================================================    
# Main routing and rendering block
# =========================================================
    
if option == 'Overall analysis':
    # render the button
    btn0 = st.sidebar.button('Perform Analysis')
    if btn0:
        st.session_state['show_overall'] = True
    if st.session_state.get('show_overall',False):
        overall_analysis()
        
elif option == 'Startup analysis':
    # render the dropdown in the startup column
    startup = st.sidebar.selectbox('Select the startup',sorted(fund['startup_clean'].unique().tolist()))
    # render the button
    btn1 = st.sidebar.button('perform analysis')
    
    if btn1:
        st.session_state['show_startup'] = True
    if st.session_state.get('show_startup',False):
        pass
else:
    # render the dropdown in the investor column
    investor = st.sidebar.selectbox('Select the Investor',sorted(fund_investor['investor_clean'].unique().tolist()))
    # render the button
    btn2 = st.sidebar.button('Get investor details')
    
    if btn2:
        st.session_state['show_investor'] = True
    if st.session_state.get('show_investor',False):
        investor_details(investor)
        