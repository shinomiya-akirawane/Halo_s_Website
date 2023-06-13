import streamlit as st
import pickle
import altair as alt
import os
import datetime 
def get_point_chart(data):
    if len(data) < 0:
        return alt.LayerChart()
    chart = alt.Chart(data).mark_circle().encode(
        alt.X('start_date:T',title = 'date'),
        alt.Y('hoursminutes(start_time):T',title = 'time of day'),
        color = alt.Color('type:N', scale = alt.Scale(domain=['HR', 'qor15','step','adjustChart'], range=['red', 'blue','green','white']))
    )
    return chart.interactive(bind_y = False)

def get_area_chart_1(chart_df):
    chart = alt.Chart(chart_df).mark_rect().encode(
        x = alt.value(0),
        x2 = alt.value(2000),
        y = alt.value(200),
        y2 = alt.value(1000),
        color = alt.ColorValue('grey')
    )
    return chart

def get_area_chart_2(chart_df):
    chart = alt.Chart(chart_df).mark_rect().encode(
        x = alt.value(0),
        x2 = alt.value(2000),
        y = alt.value(0),
        y2 = alt.value(30),
        color = alt.ColorValue('grey')
    )
    return chart
# page strcutrue start here
patient_id = st.number_input('patient id',min_value=1,max_value=42)
with_zero = st.checkbox('Show only active periods',value = True)
displayElem = st.multiselect('Please choose heart rate or step or qor15',['heart rate','step','qor15'],default='qor15')
graph_title = st.subheader('Data availability of NO.'+ str(patient_id))
chart = alt.LayerChart()
with open(os.path.join('.','df_data','behavior_visualization_colored_area.pkl'),'rb') as f:
    chart_df = pickle.load(f)
    chart_df = chart_df.loc[(chart_df['patient_id'] == patient_id) ,:]
    del chart_df['patient_id']
    del chart_df['rect_num']
    chart = alt.layer(chart,get_area_chart_1(chart_df))
    chart = alt.layer(chart,get_area_chart_2(chart_df))
if with_zero == True:
    with open(os.path.join('.','df_data','Engagement_24_hours_date_without_zero.pkl'),'rb') as f:
        chart_df = pickle.load(f)
        chart_df = chart_df.loc[(chart_df['patient_id'] == patient_id) ,:]
else:
    with open(os.path.join('.','df_data','Engagement_24_hours_date_with_zero.pkl'),'rb') as f:
        chart_df = pickle.load(f)
        chart_df = chart_df.loc[(chart_df['patient_id'] == patient_id) ,:]
if 'heart rate' in displayElem:
    chart = alt.layer(chart,get_point_chart(chart_df.loc[(chart_df['type'] == 'HR'),:]))
if 'step' in displayElem:
    chart = alt.layer(chart,get_point_chart(chart_df.loc[(chart_df['type'] == 'step'),:]))
if 'qor15' in displayElem:
    chart = alt.layer(chart,get_point_chart(chart_df.loc[(chart_df['type'] == 'qor15'),:]))

chart = alt.layer(chart,get_point_chart(chart_df.loc[(chart_df['type'] == 'adjustChart'),:]))
st.altair_chart(chart,use_container_width=True)