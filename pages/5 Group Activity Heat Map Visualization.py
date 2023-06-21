import streamlit as st
import pickle
import altair as alt
import os

def get_point_chart(data):
    if len(data) < 0:
        return alt.LayerChart()
    chart = alt.Chart(data).mark_circle().encode(
        alt.X('start_date:T',title = 'date'),
        alt.Y('hoursminutes(start_time):T',title = 'time of day'),
        color ='steps:Q'
    ).properties(
    width=1400,
    height=700
)
    return chart.interactive(bind_y = False)

def get_area_chart_1(chart_df):
    chart = alt.Chart(chart_df).mark_rect().encode(
        x = alt.value(0),
        x2 = alt.value(2000),
        y = alt.value(470),
        y2 = alt.value(1400),
        color = alt.ColorValue('grey')
    ).properties(
    width=1400,
    height=700
)
    return chart

def get_area_chart_2(chart_df):
    chart = alt.Chart(chart_df).mark_rect().encode(
        x = alt.value(0),
        x2 = alt.value(2000),
        y = alt.value(0),
        y2 = alt.value(80),
        color = alt.ColorValue('grey')
    ).properties(
    width=1400,
    height=700
)
    return chart

def get_pie_chart(chart_df):
    chart = alt.Chart(chart_df).mark_arc().encode(
        alt.Theta('value:Q'),
        alt.Color('type:N')
    )
    return chart
# page strcutrue start here
chart = alt.LayerChart()
with open(os.path.join('.','df_data','individual_acitivity_visualization_colored_area.pkl'),'rb') as f:
    chart_df = pickle.load(f)
    chart_df = chart_df.loc[(chart_df['patient_id'] == 1) ,:]
    del chart_df['patient_id']
    del chart_df['rect_num']
    chart = alt.layer(chart,get_area_chart_1(chart_df))
    chart = alt.layer(chart,get_area_chart_2(chart_df))
with open(os.path.join('.','df_data','group_activity_visualization_heat_map.pkl'),'rb') as f:
    chart_df = pickle.load(f)
chart = alt.layer(chart,get_point_chart(chart_df))
st.altair_chart(chart,use_container_width=True)
with open(os.path.join('.','df_data','group_activity_visualization_pie.pkl'),'rb') as f:
    chart_df = pickle.load(f)
chart = get_pie_chart(chart_df)
st.altair_chart(chart,use_container_width=True)