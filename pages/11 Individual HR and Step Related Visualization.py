import streamlit as st
import altair as alt
import os
import pickle
import pandas as pd
patient_id = st.number_input('patient id',min_value=1,max_value=42)
def get_bar_chart(data):
    chart = alt.Chart(data).mark_bar().encode(
        alt.X('day',title = 'Day'),
        alt.Y('time_length:Q',title = 'Time Length(Hours)',stack=True),
        alt.Color('situation:N'),
        order=alt.Order('situation:N', sort='descending')
    )
    return chart.interactive()

with open(os.path.join('.','df_data','individual_HR_and_step_related_visualization.pkl'),'rb') as f:
    chart_df = pickle.load(f)
    chart_df = chart_df.loc[(chart_df['patient_id'] == patient_id) ,:]
chart = get_bar_chart(chart_df)
st.altair_chart(chart,use_container_width=True)
with open(os.path.join('.','df_data','individual_heart_rate_standard_table.pkl'),'rb') as f:
    table_arr = pickle.load(f)
st.table(pd.DataFrame(table_arr,columns = ('patient_id','Max heart rate at rest','Min heart rate at rest')).fillna(0).astype(int))