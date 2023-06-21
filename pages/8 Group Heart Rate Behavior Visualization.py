import streamlit as st
import pickle
import altair as alt
import os

def get_line_chart(data):
    if len(data) < 0:
        return alt.LayerChart()
    chart = alt.Chart(data).mark_line(point=alt.OverlayMarkDef(filled=False, fill="white")).encode(
        alt.X('date:T',title = 'Date'),
        alt.Y('patient_num_over:Q',title = 'Patient Number Over Average Heart Rate'),
    )
    return chart.interactive()

with open(os.path.join('.','df_data','group_heart_rate_visualization.pkl'),'rb') as f:
    chart_df = pickle.load(f)

chart = get_line_chart(chart_df)
st.altair_chart(chart,use_container_width=True)