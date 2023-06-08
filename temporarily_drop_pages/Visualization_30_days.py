import streamlit as st
import pandas as pd
import altair as alt
import welcome as tool

# The input bar to select patient id
patient_id = st.number_input('patient id',min_value=1,max_value=42)

# preprcess dataframe
def rtn_preprocessed_heart_rate_df(heart_rate_df:pd.DataFrame):
    if len(heart_rate_df) == 0:
        return heart_rate_df
    heart_rate_df = tool.datetime2date(heart_rate_df,1)
    heart_rate_mean_df = heart_rate_df.loc[:,['start_datetime','avg_HR']].groupby(by=['start_datetime']).mean()
    heart_rate_max_df = heart_rate_df.loc[:,['start_datetime','max_HR']].groupby(by=['start_datetime']).max()
    heart_rate_min_df = heart_rate_df.loc[:,['start_datetime','min_HR']].groupby(by=['start_datetime']).min()
    heart_rate_df = pd.melt(pd.concat([heart_rate_mean_df,heart_rate_min_df,heart_rate_max_df],axis=1).reset_index(),id_vars='start_datetime')
    return heart_rate_df

def rtn_preprocessed_step_df(step_df):
    if len(step_df) == 0:
        return step_df
    step_df = tool.datetime2date(step_df,1)
    step_mean_df = step_df.loc[:,['start_datetime','steps']].groupby(by=['start_datetime']).mean()
    step_df= pd.melt(step_mean_df.reset_index(),id_vars='start_datetime')
    return step_df

def get_line_chart(data):
    selection = alt.selection_single()
    chart = alt.Chart(data).mark_line(point = True).encode(
        alt.X('start_datetime:T'),
        alt.Y('value:Q'),
        color = alt.condition(selection, 'variable:N', alt.value('grey'))
    ).add_selection(selection)
    return chart.interactive()

graph_title = st.header('heart rate & steps of NO.'+ str(patient_id) + ' patient')
heart_rate_data,step_data,qor_15_data = tool.get_data_by_id(patient_id)
heart_rate_df = rtn_preprocessed_heart_rate_df(heart_rate_data)
step_df = rtn_preprocessed_step_df(step_data)
graph_df = pd.concat([heart_rate_df,step_df],axis = 0)
chart = alt.layer(get_line_chart(graph_df)).configure_point(size=100)

st.altair_chart(chart,use_container_width=True)