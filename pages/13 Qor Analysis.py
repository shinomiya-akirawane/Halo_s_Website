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
        alt.Y('answer:Q',title = 'Record Time Length'),
        color = alt.Color('question_context:N'),
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
    'pain' : 11
}
patient_id = st.number_input('patient id',min_value=1,max_value=42)
questions = st.multiselect('Please choose which question to display: ',['sleep','rested','food','breathing','comfortable','wellbeing','worries','sad','pain'])
chart = alt.LayerChart()
patient_qor_df = qor_df.loc[qor_df['patient_id'] == patient_id,:]
for question in questions:
    question_id = question_dict[question]
    chart_df = patient_qor_df.loc[patient_qor_df['question_id'] == question_id,:]
    chart = alt.layer(chart,get_line_chart(chart_df))
st.altair_chart(chart,use_container_width=True)
