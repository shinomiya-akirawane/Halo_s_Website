import streamlit as st
import sqlite3
import pandas as pd
import altair as alt

# connect to database
con = sqlite3.connect('C:\\Users\\shinomiya_akirawane\\Desktop\\halo_s')
cur = con.cursor()

# get data from database
@st.cache_data
def get_data():
    heart_rate_df = pd.read_sql("SELECT patient_id,start_datetime,end_datetime,min_HR,max_HR,avg_HR from heart_rate",con=con)
    step_df = pd.read_sql("SELECT patient_id,start_datetime,end_datetime,steps from step_count",con=con)
    qor_15_df = pd.read_sql("SELECT patient_id,submit_datetime,question_id,answer from qor_15",con=con)
    return heart_rate_df,step_df,qor_15_df
#preprcess dataframe
def datetime2date(df):
    result_df = df.copy()
    for row in range(0,len(result_df)):
        result_df.iloc[row,1] = pd.to_datetime(result_df.iloc[row,1])
        result_df.iloc[row,1] = result_df.iloc[row,1].date()
    return result_df


def preprocess_heart_rate_df(heart_rate_df:pd.DataFrame):
    result_df = pd.DataFrame(columns = ['date','avg_second_duration','complete_num','type'])
    date_values = datetime2date(heart_rate_df)['start_datetime'].drop_duplicates().values
    for date in date_values:
        day_heart_rate_df = heart_rate_df.loc[heart_rate_df['start_datetime'].str[:10] == (str(date).strip())]
        patient_num = len(day_heart_rate_df['patient_id'].drop_duplicates())
        time_duration_sum = 0
        for row in range(0,len(day_heart_rate_df)):
            time_duration_sum += int((pd.to_datetime(day_heart_rate_df.iloc[row,2]) - pd.to_datetime(day_heart_rate_df.iloc[row,1])).total_seconds())
        avg_second_duration = time_duration_sum//patient_num
        result_df.loc[len(result_df)] = [str(date),avg_second_duration,patient_num,'heart_rate']
    return result_df

def preprocess_step_df(step_df):
    result_df = pd.DataFrame(columns = ['date','avg_second_duration','complete_num','type'])
    date_values = datetime2date(step_df)['start_datetime'].drop_duplicates().values
    for date in date_values:
        day_step_df = step_df.loc[step_df['start_datetime'].str[:10] == (str(date).strip())]
        patient_num = len(day_step_df['patient_id'].drop_duplicates())
        time_duration_sum = 0
        for row in range(0,len(day_step_df)):
            time_duration_sum += int((pd.to_datetime(day_step_df.iloc[row,2]) - pd.to_datetime(day_step_df.iloc[row,1])).total_seconds())
        avg_second_duration = time_duration_sum//patient_num
        result_df.loc[len(result_df)] = [str(date),avg_second_duration,patient_num,'step']
    return result_df

def preprocess_qor_15_df(qor_15_df):
    result_df = pd.DataFrame(columns = ['date','complete_num','type'])
    date_values = datetime2date(qor_15_df)['submit_datetime'].drop_duplicates().values
    for date in date_values:
        day_qor_15_df = qor_15_df.loc[qor_15_df['submit_datetime'].str[:10] == (str(date).strip())]
        patient_num = len(day_qor_15_df['patient_id'].drop_duplicates())
        result_df.loc[len(result_df)] = [str(date),patient_num,'qor15']
    return result_df

# Generate dataframe to draw the graph
heart_rate_df,step_df,qor_15_df = get_data()
heart_rate_df = preprocess_heart_rate_df(heart_rate_df)
step_df = preprocess_step_df(step_df)
qor_15_df = preprocess_qor_15_df(qor_15_df)
graph_df = pd.concat([heart_rate_df,step_df,qor_15_df])
# Draw graph
graph_title = st.subheader('Data collection situation of whole dataset')
domain_scale = alt.Scale(domain = ['heart_rate','step','qor15'],range = ['#608595','#DFC286','#C07A92'])
chart = alt.Chart(graph_df).mark_line().encode(
        alt.X('date:T'),
        alt.Y('complete_num'),
        color = alt.Color('type:N',scale = domain_scale), 
    )
st.altair_chart(chart.interactive(),use_container_width=True)