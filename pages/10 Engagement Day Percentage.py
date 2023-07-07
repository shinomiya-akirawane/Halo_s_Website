import streamlit as st
import altair as alt
import os
import pickle

def get_bar_chart(data):
    chart = alt.Chart(data).mark_bar().encode(
        alt.X('patient_id:Q',title = 'Patient ID'),
        alt.Y('engaged_day_num:Q',title = 'Number of days',stack=True),
        alt.Color('level:N'),
        order=alt.Order('level:N', sort='descending')
    ).properties(
    width=1400,
    height=700
)
    return chart.interactive()

with open(os.path.join('.','df_data','engagement_day_percentage.pkl'),'rb') as f:
    chart_df = pickle.load(f)

chart = get_bar_chart(chart_df)
st.altair_chart(chart)