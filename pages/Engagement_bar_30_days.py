import streamlit as st
import pickle
import altair as alt

def get_bar_chart(data):
    if len(data) < 0:
        return alt.LayerChart()
    chart = alt.Chart(data).mark_bar().encode(
        alt.X('date:T'),
        alt.Y('time_length:Q'),
        color = alt.Color('type:N'),
    )
    return chart.interactive(bind_y = False)

def get_point_chart(data):
    if len(data) < 0:
        return alt.LayerChart()
    chart = alt.Chart(data).mark_circle().encode(
        alt.X('submit_datetime:T',),
        alt.Y('dot_height'),
        color = alt.Color('type:N'),
    )
    return chart.interactive()

# page structure start here
patient_id = st.number_input('patient id',min_value=1,max_value=42)
with_zero = st.checkbox('Drop zero data')

if with_zero == True:
    with open('C:\\Users\\shinomiya_akirawane\\Desktop\\HALO-S\\HALO-S\\halo_s_website\\df_data\\Engagement_dot_30days_with_zero.pkl','rb') as f:
        dot_df = pickle.load(f)
        dot_df = dot_df.loc[(dot_df['patient_id'] == patient_id) ,:]
    with open('C:\\Users\\shinomiya_akirawane\\Desktop\\HALO-S\\HALO-S\\halo_s_website\\df_data\\Engagement_bar_30days_without_zero.pkl','rb') as f:
        bar_df = pickle.load(f)
        bar_df = bar_df.loc[(bar_df['patient_id'] == patient_id) ,:]
else:
    with open('C:\\Users\\shinomiya_akirawane\\Desktop\\HALO-S\\HALO-S\\halo_s_website\\df_data\\Engagement_dot_30days_with_zero.pkl','rb') as f:
        dot_df = pickle.load(f)
        dot_df = dot_df.loc[(dot_df['patient_id'] == patient_id) ,:]
    with open('C:\\Users\\shinomiya_akirawane\\Desktop\\HALO-S\\HALO-S\\halo_s_website\\df_data\\Engagement_bar_30days_with_zero.pkl','rb') as f:
        bar_df = pickle.load(f)
        bar_df = bar_df.loc[(bar_df['patient_id'] == patient_id) ,:]

chart = alt.layer(get_bar_chart(bar_df))
st.altair_chart(chart,use_container_width=True)
