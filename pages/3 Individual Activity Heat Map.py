import streamlit as st
import pickle
import altair as alt
import os

def get_point_chart(data):
    if len(data) < 0:
        return alt.LayerChart()
    chart = alt.Chart(data).mark_circle().encode(
        alt.X('fixed_period',title = 'Day'),
        alt.Y('hoursminutes(start_time):T',title = 'time of day'),
        color ='step_cnt:Q'
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

def get_cirtical_point_chart(data):
    if len(data) < 0:
        return alt.LayerChart()
    chart = alt.Chart(data).mark_circle().encode(
        alt.X('fixed_period',title = 'Day'),
        alt.Y('hoursminutes(start_time):T',title = 'time of day'),
        color = alt.ColorValue('red')
    )
    return chart.interactive(bind_y = False)
# page strcutrue start here
patient_id = st.number_input('patient id',min_value=1,max_value=42)
graph_title = st.subheader('Data availability of NO.'+ str(patient_id))
chart = alt.LayerChart()
with open(os.path.join('.','df_data','individual_acitivity_visualization_colored_area.pkl'),'rb') as f:
    chart_df = pickle.load(f)
    chart_df = chart_df.loc[(chart_df['patient_id'] == patient_id) ,:]
    del chart_df['patient_id']
    del chart_df['rect_num']
    chart = alt.layer(chart,get_area_chart_1(chart_df))
    chart = alt.layer(chart,get_area_chart_2(chart_df))
with open(os.path.join('.','df_data','individual_activity_visualization_heat_map.pkl'),'rb') as f:
    chart_df = pickle.load(f)
    chart_df = chart_df.loc[(chart_df['patient_id'] == patient_id) ,:]
chart = alt.layer(chart,get_point_chart(chart_df.loc[(chart_df['type'] == 'step'),:]))
chart = alt.layer(chart,get_cirtical_point_chart(chart_df.loc[(chart_df['type'] == 'critical'),:]))
chart = alt.layer(chart,get_point_chart(chart_df.loc[(chart_df['type'] == 'adjustChart'),:]))
st.altair_chart(chart,use_container_width=True)