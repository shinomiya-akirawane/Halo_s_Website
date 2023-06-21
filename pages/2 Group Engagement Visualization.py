import streamlit as st
import pickle
import altair as alt
import os
def get_bar_chart(data):
    if len(data) < 0:
        return alt.LayerChart()
    chart = alt.Chart(data).mark_bar().encode(
        alt.X('date:T',title = 'Date'),
        alt.Y('patient_complete_num:Q',title = 'Engaged Patient Amount'),
        color = alt.Color('type:N',scale = alt.Scale(domain=['HR hours', 'QoR completion','Active move moment hours','adjustChart'], range=['red', 'blue','green','white'])),
    ).properties(
    width=1400,
    height=700
)
    return chart.interactive(bind_y = False)

def get_point_chart(data):
    if len(data) < 0:
        return alt.LayerChart()
    chart = alt.Chart(data).mark_circle().encode(
        alt.X('date:T',title = 'Date'),
        alt.Y('patient_complete_num',title = 'Engaged Patient Amount'),
        color = alt.Color('type:N',scale = alt.Scale(domain=['HR hours', 'QoR completion','Active move moment hours','adjustChart'], range=['red', 'blue','green','white'])),
    ).properties(
    width=1400,
    height=700
)
    return chart.interactive()

def get_line_chart(data):
    if len(data) < 0:
        return alt.LayerChart()
    chart = alt.Chart(data).mark_line(point=alt.OverlayMarkDef(filled=False, fill="white")).encode(
        alt.X('date:T',title = 'Date'),
        alt.Y('patient_complete_num:Q',title = 'Engaged Patient Amount'),
        color = alt.Color('type:N',scale = alt.Scale(domain=['HR hours', 'QoR completion','Active move moment hours','adjustChart'], range=['red', 'blue','green','white'])),
    ).properties(
    width=1400,
    height=700
)
    return chart.interactive()
# page structure start here

with_zero = st.checkbox('Show only active periods',value = True)
bar_chart_display = st.checkbox('Display bar chart',value = True)
displayElem = st.multiselect('Please choose heart rate or step or qor15',['heart rate','step','qor15'])
chart = alt.LayerChart()
with open(os.path.join('.','df_data','group_engagement.pkl'),'rb') as f:
    chart_df = pickle.load(f)
print(chart_df.loc[(chart_df['type'] == 'HR hours'),:])
if bar_chart_display:
    if 'heart rate' in displayElem:
        chart = alt.layer(chart,get_bar_chart(chart_df.loc[(chart_df['type'] == 'HR hours'),:]),get_line_chart(chart_df.loc[(chart_df['type'] == 'HR hours'),:]))
    if 'step' in displayElem:
        chart = alt.layer(chart,get_bar_chart(chart_df.loc[(chart_df['type'] == 'Active move moment hours'),:]),get_line_chart(chart_df.loc[(chart_df['type'] == 'Active move moment hours'),:]))
    if 'qor15' in displayElem:
        chart = alt.layer(chart,get_bar_chart(chart_df.loc[(chart_df['type'] == 'QoR completion'),:]),get_line_chart(chart_df.loc[(chart_df['type'] == 'QoR completion'),:]))
else:
    if 'heart rate' in displayElem:
        chart = alt.layer(chart,get_line_chart(chart_df.loc[(chart_df['type'] == 'HR hours'),:]))
    if 'step' in displayElem:
        chart = alt.layer(chart,get_line_chart(chart_df.loc[(chart_df['type'] == 'Active move moment hours'),:]))
    if 'qor15' in displayElem:
        chart = alt.layer(chart,get_line_chart(chart_df.loc[(chart_df['type'] == 'QoR completion'),:]))

chart = alt.layer(chart,get_point_chart(chart_df.loc[(chart_df['type'] == 'adjustChart'),:]))
st.altair_chart(chart,use_container_width=True)