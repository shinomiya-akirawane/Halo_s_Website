import streamlit as st
import pickle
import altair as alt
import os
import pandas as pd

def get_line_chart(data,y_value:str):
    if len(data) < 0:
        return alt.LayerChart()
    chart = alt.Chart(data).mark_line(point=alt.OverlayMarkDef(filled=False, fill="white")).encode(
        alt.X('start_datetime:T',title = 'Day'),
        alt.Y(y_value,title = y_value))
    return chart.interactive()

def get_bar_chart(data):
    if len(data) < 0:
        return alt.LayerChart()
    chart = alt.Chart(data).mark_bar().encode(
        alt.X('date:T',title = 'Day'),
        alt.Y('time_length',title = 'Time length'),
        alt.Color('type:N')
    )
    return chart.interactive()
patient_id = st.number_input('patient id',min_value=1,max_value=42)
displayElem = st.multiselect('Please choose: ',['avg_HR','max_HR','min_HR'])
max_HR = st.slider('Please set up max HR: ',50,150)
min_HR = st.slider('Please set up min HR: ',30,100)
chart = alt.LayerChart()
with open(os.path.join('.','df_data','individual_heart_behavior_visualization.pkl'),'rb') as f:
    chart_df = pickle.load(f)
    chart_df = chart_df.loc[(chart_df['patient_id'] == patient_id) ,:]
if 'avg_HR' in displayElem:
    chart = alt.layer(chart,get_line_chart(chart_df,'avg_HR:Q'))
if 'max_HR' in displayElem:
    chart = alt.layer(chart,get_line_chart(chart_df,'max_HR:Q'))
if 'min_HR' in displayElem:
    chart = alt.layer(chart,get_line_chart(chart_df,'min_HR:Q'))
horizontal_max_line = alt.Chart(pd.DataFrame({'y': [max_HR]})).mark_rule(color='red').encode(
    y='y'
)
horizontal_min_line = alt.Chart(pd.DataFrame({'y': [min_HR]})).mark_rule(color='red').encode(
    y='y'
)
chart = alt.layer(chart,horizontal_max_line)
chart = alt.layer(chart,horizontal_min_line)
st.altair_chart(chart,use_container_width=True)

with open(os.path.join('.','df_data','individual_heart_behavior_visualization_bar_chart.pkl'),'rb') as f:
    chart_df = pickle.load(f)
    chart_df = chart_df.loc[(chart_df['patient_id'] == patient_id) ,:]

chart = get_bar_chart(chart_df)
st.altair_chart(chart,use_container_width=True)
