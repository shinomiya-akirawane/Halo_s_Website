import pandas as pd
import os
import pickle
import streamlit as st
import altair as alt
def get_line_chart(data):
    if len(data) < 0:
        return alt.LayerChart()
    chart = alt.Chart(data).mark_line(point=alt.OverlayMarkDef(filled=False, fill="white")).encode(
        alt.X('fixed_period',title = 'Day'),
        alt.Y('answer:Q',title = 'Record Time Length',scale=alt.Scale(domain=(0, 11))),
        color = alt.Color('patient_id:N'),
    ).properties(
    width=1400,
    height=700
)
    return chart.interactive()
with open(os.path.join('.','df_data','qor_df_with_fixed_period.pkl'),'rb') as f:
    qor_df = pickle.load(f)
question_dict = {
    'sleep' : 4,
    'rested' : 3,
    'food' : 2,
    'breathing' : 1,
    'comfortable' : 9,
    'wellbeing' : 10,
    'worries' : 14,
    'sad' : 15,
    'moderate pain' : 11,
    'severe pain' : 12
}
questions = st.multiselect('Please choose which question to display: ',['sleep','rested','food','breathing','comfortable','wellbeing','worries','sad','pain'])
chart = alt.LayerChart()
for question in questions:
    question_id = question_dict[question]
    chart_df = qor_df.loc[qor_df['question_id'] == question_id,:]
    for patient in range(0,42):
        chart = alt.layer(chart,get_line_chart(chart_df.loc[(chart_df['patient_id'] == patient)&(chart_df['fixed_period'] < 36),:]))
st.altair_chart(chart)