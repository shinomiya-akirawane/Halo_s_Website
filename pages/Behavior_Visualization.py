import streamlit as st
import pickle
import altair as alt
import os

def get_point_chart(data):
    if len(data) < 0:
        return alt.LayerChart()
    chart = alt.Chart(data).mark_circle().encode(
        alt.X('start_date:T'),
        alt.Y('hoursminutes(start_time):T',scale = alt.Scale(domain=['2012-01-01T00:00:00', '2012-01-02T00:00:00'])),
        color = alt.Color('type:N')
    )
    return chart.interactive(bind_y = False)

# page strcutrue start here
patient_id = st.number_input('patient id',min_value=1,max_value=42)
with_zero = st.checkbox('Show only active periods',disabled=True)
displayElem = st.multiselect('Please choose heart rate or step or qor15',['heart rate','step','qor15'],default=None)
graph_title = st.subheader('Data availability of NO.'+ str(patient_id))
if with_zero == True:
    with open(os.path.join('.','df_data','Engagement_24_hours_date_without_zero.pkl'),'rb') as f:
        chart_df = pickle.load(f)
        chart_df = chart_df.loc[(chart_df['patient_id'] == patient_id) ,:]
else:
    with open(os.path.join('.','df_data','Engagement_24_hours_date_with_zero.pkl'),'rb') as f:
        chart_df = pickle.load(f)
        chart_df = chart_df.loc[(chart_df['patient_id'] == patient_id) ,:]
chart = alt.LayerChart()
if 'heart rate' in displayElem:
    chart = alt.layer(chart,get_point_chart(chart_df.loc[(chart_df['type'] == 'HR'),:]))
if 'step' in displayElem:
    chart = alt.layer(chart,get_point_chart(chart_df.loc[(chart_df['type'] == 'step'),:]))
if 'qor15' in displayElem:
    chart = alt.layer(chart,get_point_chart(chart_df.loc[(chart_df['type'] == 'qor15'),:]))
st.altair_chart(chart,use_container_width=True)