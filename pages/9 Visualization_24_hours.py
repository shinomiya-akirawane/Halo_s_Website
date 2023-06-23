import streamlit as st
import pandas as pd
import altair as alt
import welcome as tool

# preprocess dataframe
def preprocess_heart_rate_df(heart_rate_df,select_date):
    if len(heart_rate_df) == 0:
        return heart_rate_df
    heart_rate_df = heart_rate_df.loc[heart_rate_df['start_datetime'].str[:10] == select_date]
    heart_rate_df = pd.melt(heart_rate_df,id_vars=['patient_id','start_datetime','end_datetime'])
    return heart_rate_df

def preprocess_step_df(step_df,select_date):
    if len(step_df) == 0:
        return step_df
    step_df = step_df.loc[step_df['start_datetime'].str[:10] == select_date]
    step_df = pd.melt(step_df,id_vars=['patient_id','start_datetime','end_datetime'])
    return step_df

# The input bar to select patient id and bar to select date
patient_id = st.number_input('patient id',min_value=1,max_value=42)
heart_rate_df,step_df,qor_15_df =  tool.get_data_by_id(patient_id)

# Generate drop list of days that has record
select_day = st.selectbox('select_day',options=tool.extract_record_len(heart_rate_df,step_df))

# Generate dataframe to draw the graph
if select_day:
    heart_rate_df = preprocess_heart_rate_df(heart_rate_df,str(select_day[-11:]).strip())
    step_df = preprocess_step_df(step_df,str(select_day[-11:]).strip())
    graph_df = pd.concat([heart_rate_df,step_df],axis = 0)

    # Draw graph
    graph_title = st.subheader('24 hour heart rate & step record of NO. '+ str(patient_id) + ' on ' + str(select_day[-11:]).strip())
    domain_scale = alt.Scale(domain = ['min_HR','max_HR','avg_HR','steps'],range = ['#FCAF7C','#C7C7C7','#87C9C3','#04686B'])
    selection = alt.selection_single()
    chart = alt.Chart(graph_df).mark_line().encode(
            alt.X('start_datetime:T'),
            alt.Y('value'), 
            color = alt.condition(selection, 'variable:N', alt.value('grey')),
            tooltip = [
                alt.Tooltip('start_datetime:T',title = "Time"),
                alt.Tooltip('value',title = 'variable:N')
            ],
        ).configure_point(size=50)
    chart = chart.add_selection(selection)
    st.altair_chart(chart.interactive(),use_container_width=True)