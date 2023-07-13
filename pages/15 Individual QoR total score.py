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
        alt.Y('answer:Q',title = 'Record Time Length',scale=alt.Scale(domain=(0, 160)))
    )
    return chart.interactive()
with open(os.path.join('.','df_data','qor_total_score.pkl'),'rb') as f:
    qor_df = pickle.load(f)
patient_id = st.number_input('patient id',min_value=1,max_value=45)
patient_qor_df = qor_df.loc[qor_df['patient_id'] == patient_id,:]

chart = get_line_chart(patient_qor_df)
st.altair_chart(chart,use_container_width=True)