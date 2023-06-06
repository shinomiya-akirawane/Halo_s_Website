import streamlit as st
import pandas as pd
import sqlite3
import datetime

st.header('Welcome to HALO-s Database visualizer')
st.subheader('Please go to sidebar to choose the visualizer mode')

# useful functions
@st.cache_data
def get_data_by_id(patient_id):
    con = sqlite3.connect('C:\\Users\\shinomiya_akirawane\\Desktop\\halo_s')
    heart_rate_df = pd.read_sql("SELECT patient_id,start_datetime,end_datetime,min_HR,max_HR,avg_HR from heart_rate where patient_id = " + str(patient_id),con=con)
    step_df = pd.read_sql("SELECT patient_id,start_datetime,end_datetime,steps from step_count where patient_id = "+str(patient_id),con=con)
    qor_15_df = pd.read_sql("SELECT patient_id,submit_datetime,question_id,answer from qor_15 where patient_id="+str(patient_id),con=con)
    return heart_rate_df,step_df,qor_15_df

def extract_record_len(heart_rate_df,step_df):
    heart_record_days = (heart_rate_df['start_datetime'].str[0:11]).drop_duplicates()
    step_record_days = (step_df['start_datetime'].str[0:11]).drop_duplicates()
    record_days = pd.concat([heart_record_days,step_record_days],axis = 0).drop_duplicates().sort_values().reset_index().drop(['index'],axis = 1)
    options = [str(row) + '. ' + str(record_days.iloc[row,0]) for row in range(0,len(record_days))]
    return options

def datetime2date(df,time_col_index):
    for row in range(0,len(df)):
        df.iloc[row,time_col_index] = pd.to_datetime(df.iloc[row,time_col_index])
        df.iloc[row,time_col_index] = df.iloc[row,time_col_index].date()
    return df

def get_start_datetime(heart_rate_df,step_df,qor15_df):
    if len(heart_rate_df) != 0:
        heart_rate_df = datetime2date(heart_rate_df,1)
        start_datetime =  heart_rate_df['start_datetime'].min()
    elif len(step_df) != 0:
        step_df = datetime2date(step_df,1)
        start_datetime =  step_df['start_datetime'].min()
    elif len(qor15_df) != 0:
        qor15_df = datetime2date(qor15_df,1)
        start_datetime =  qor15_df['start_datetime'].min()
    return start_datetime

def get_empty_df_by_name(name,start_date:datetime):
    if name == 'qor15':
        df = pd.DataFrame(columns = ['record_date','is_empty','complete_num','chart_height'])
        data_range = pd.date_range(start=start_date,end = (start_date + datetime.timedelta(days=29)),freq = "D")
        df = df.set_index('record_date').reindex(index = data_range).reset_index()
        df = df.assign(is_empty = 'empty',complete_num = '0',chart_height = 1)
        df.rename(columns={'index':'record_date'},inplace=True)
    elif name == 'heart_rate':
        df = pd.DataFrame(columns = ['record_date'])
        data_range = pd.date_range(start=start_date,end = (start_date + datetime.timedelta(days=29)),freq = "D")
        df = df.set_index('record_date').reindex(index = data_range).reset_index()
        df = df.assign(is_empty = 'empty',max_HR = '0',min_HR = '0',avg_HR = '0',chart_height = 3)
        df.rename(columns={'index':'record_date'},inplace=True)
    elif name == 'step':
        df = pd.DataFrame(columns = ['record_date'])
        data_range = pd.date_range(start=start_date,end = (start_date + datetime.timedelta(days=29)),freq = "D")
        df = df.set_index('record_date').reindex(index = data_range).reset_index()
        df = df.assign(is_empty = 'empty',steps = '0',chart_height = 2)
        df.rename(columns={'index':'record_date'},inplace=True)
    return df

def auto_complete_missing_time(df,time_col_num,empty_col_num,nan_col_num):
    for row in range(0,len(df)):
        df.iloc[row,time_col_num] = pd.to_datetime(df.iloc[row,time_col_num])
        df.iloc[row,time_col_num] = df.iloc[row,time_col_num].date()
    data_range = pd.date_range(start=df['record_date'].min(),end = (df['record_date'].min()+datetime.timedelta(days=29)),freq = "D")
    df = df.set_index('record_date').reindex(index = data_range).reset_index()
    df.rename(columns={'index':'record_date'},inplace=True)
    for row in range(0,len(df)):
        if pd.isna(df.iloc[row,nan_col_num]):
            df.iloc[row,empty_col_num] = 'empty'
        else:
            df.iloc[row,empty_col_num] = 'full'
    return df