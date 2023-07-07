import streamlit as st
import pickle
import altair as alt
import os

def get_line_chart(data,y_title):
    if len(data) < 0:
        return alt.LayerChart()
    chart = alt.Chart(data).mark_line(point=alt.OverlayMarkDef(filled=False, fill="white")).encode(
        alt.X('fixed_period',title = 'Day'),
        alt.Y('patient_num_over:Q',title = y_title),
    )
    return chart.interactive()

with open(os.path.join('.','df_data','group_heart_rate_visualization.pkl'),'rb') as f:
    chart_df = pickle.load(f)

chart1 = get_line_chart(chart_df.loc[chart_df['with_ratio'] == 'no',:].iloc[:34,:],'Patient Number Over Average Heart Rate')
chart2 = get_line_chart(chart_df.loc[chart_df['with_ratio'] == 'yes',:].iloc[:34,:],'Ratio')

st.altair_chart(chart1,use_container_width=True)
st.altair_chart(chart2,use_container_width=True)