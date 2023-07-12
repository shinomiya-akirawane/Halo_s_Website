import streamlit as st
import pandas as pd
import os
import pickle


with open(os.path.join('.','df_data','wellness_HR.pkl'),'rb') as f:
    table_df = pickle.load(f)
    table_df['patient_id'] = table_df['patient_id'].astype(int)
    table_df['HR_record_coverage_num'] = table_df['HR_record_coverage_num'].astype(int)
    table_df['total_sympton_day_num'] = table_df['total_sympton_day_num'].astype(int)
st.table(table_df)