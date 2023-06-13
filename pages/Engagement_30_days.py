import streamlit as st
import pandas as pd
import altair as alt
import os
import pickle
# The input bar to select patient id
patient_id = st.number_input('patient id',min_value=1,max_value=42)

# Preprocess dataframe

# Generate Graph
def get_point_chart(data,tooltip):
    if len(data) < 0:
        return alt.LayerChart()
    domain_scale = alt.Scale(domain = ['empty','full'],range = ['#FF0000','#00CC66'])
    chart = alt.Chart(data).mark_circle().encode(
        alt.X('record_date:T'),
        alt.Y('type:N',scale = alt.Scale(padding=10)),
        color = alt.Color('is_empty:N',scale = domain_scale),  
        tooltip = tooltip,
        
    )
    return chart.interactive()

graph_title = st.subheader('Data availability of NO.'+ str(patient_id))
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
with open(os.path.join('.','df_data','Engagement_30days.pkl'),'rb') as f:
    chart_df = pickle.load(f)
    chart_df = chart_df.loc[(chart_df['patient_id'] == patient_id) ,:]
    chart = alt.layer(get_point_chart(chart_df.loc[(chart_df['type'] == 'HR') ,:],heart_tooltip),
                  get_point_chart(chart_df.loc[(chart_df['type'] == 'Step') ,:],step_tooltip),
                  get_point_chart(chart_df.loc[(chart_df['type'] == 'QoR') ,:],qor_tooltip)
                  ).configure_circle(size=100)
st.altair_chart(chart,use_container_width=True)
