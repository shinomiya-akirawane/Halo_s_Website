import streamlit as st
import pandas as pd
import altair as alt
import welcome as tool

# The input bar to select patient id
patient_id = st.number_input('patient id',min_value=1,max_value=42)

# Preprocess dataframe
def rtn_preprocessed_qor15_df(qor_15_df,default_start_date):
    if len(qor_15_df) == 0:
        return tool.get_empty_df_by_name('qor15',default_start_date)
    qor_15_df = tool.datetime2date(qor_15_df,1)
    qor_15_date = qor_15_df['submit_datetime'].drop_duplicates().reset_index().drop(['index'],axis = 1)
    result_df = pd.concat([qor_15_date,
                          pd.Series(data = [None for i in range(0,len(qor_15_date))],name = 'is_empty'),
                          pd.Series(data=[15 for i in range(0,len(qor_15_date))],name = 'complete_num')],axis=1)
    result_df.rename(columns={'submit_datetime':'record_date'},inplace=True)
    return tool.auto_complete_missing_time(result_df,0,1,2).assign(chart_height = 1)


def rtn_preprocessed_heart_rate_df(heart_rate_df,default_start_date):
    if len(heart_rate_df) == 0:
        return tool.get_empty_df_by_name('heart_rate',default_start_date)
    heart_rate_df = tool.datetime2date(heart_rate_df,1)
    min_HR_df = heart_rate_df.groupby(by=['start_datetime'])['min_HR'].min().reset_index()
    max_HR_df = heart_rate_df.groupby(by=['start_datetime'])['max_HR'].max().reset_index()
    avg_HR_df = heart_rate_df.groupby(by=['start_datetime'])['avg_HR'].mean().reset_index()
    avg_HR_df.iloc[:,1] = avg_HR_df.iloc[:,1].astype(int)
    result_df = pd.concat([min_HR_df['start_datetime'],
                           pd.Series(data = [None for i in range(0,len(min_HR_df))],name = 'is_empty')
                              ,min_HR_df['min_HR'],max_HR_df['max_HR'],avg_HR_df['avg_HR']],axis=1)
    result_df.rename(columns={'start_datetime':'record_date'},inplace=True)
    return tool.auto_complete_missing_time(result_df,0,1,2).assign(chart_height = 3)

def rtn_preprocessed_step_df(step_df,default_start_date):
    if len(step_df) == 0:
        return tool.get_empty_df_by_name('step',default_start_date)
    step_df = tool.datetime2date(step_df,1)
    avg_step_df = step_df.groupby(by=['start_datetime'])['steps'].mean().reset_index()
    avg_step_df.iloc[:,1] = avg_step_df.iloc[:,1].astype(int)
    result_df = pd.concat([avg_step_df['start_datetime'],
                           pd.Series(data = [None for i in range(0,len(avg_step_df))],name = 'is_empty'),
                           avg_step_df['steps']],axis = 1)
    result_df.rename(columns={'start_datetime':'record_date'},inplace=True)
    return tool.auto_complete_missing_time(result_df,0,1,2).assign(chart_height = 2)

# Generate Graph
def get_point_chart(data,tooltip):
    if len(data) < 0:
        return alt.LayerChart()
    domain_scale = alt.Scale(domain = ['empty','full'],range = ['#FF0000','#00CC66'])
    chart = alt.Chart(data).mark_circle().encode(
        alt.X('record_date:T'),
        alt.Y('chart_height:Q'),
        color = alt.Color('is_empty:N',scale = domain_scale),  
        tooltip = tooltip
    )
    return chart.interactive()

graph_title = st.subheader('Data availability of NO.'+ str(patient_id))
heart_rate_data,step_data,qor_15_data = tool.get_data_by_id(patient_id)
original_heart_rate_data = heart_rate_data.copy()
original_step_data = step_data.copy()
original_qor_15_data = qor_15_data.copy()
try:
    heart_rate_data = rtn_preprocessed_heart_rate_df(heart_rate_data,tool.get_start_datetime(original_heart_rate_data,original_step_data,original_qor_15_data))
    step_data = rtn_preprocessed_step_df(step_data,tool.get_start_datetime(original_heart_rate_data,original_step_data,original_qor_15_data))
    qor_15_data = rtn_preprocessed_qor15_df(qor_15_data,tool.get_start_datetime(original_heart_rate_data,original_step_data,original_qor_15_data))
except KeyError:
    pass
heart_tooltip = [
    alt.Tooltip('record_date:T',title = 'Date'),
    alt.Tooltip('min_HR:Q',title = 'min HR(bpm)'),
    alt.Tooltip('max_HR:Q',title = 'max HR(bpm)'),
    alt.Tooltip('avg_HR:Q',title = 'avg HR(bpm)'),
]
step_tooltip = [
    alt.Tooltip('record_date:T',title = 'Date'),
    alt.Tooltip('steps:Q',title = 'avg steps'),
                ]
qor_tooltip = [
    alt.Tooltip('record_date:T',title = 'Date'),
    alt.Tooltip('complete_num:Q',title = 'complete num'),
]
chart = alt.layer(get_point_chart(heart_rate_data,heart_tooltip),get_point_chart(step_data,step_tooltip),get_point_chart(qor_15_data,qor_tooltip)).configure_circle(size=100)
st.altair_chart(chart,use_container_width=True)
