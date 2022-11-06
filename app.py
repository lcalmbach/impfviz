import streamlit as st
import numpy as np
import pandas as pd
import socket
import altair as alt
import texts as txt
from datetime import datetime

from person import Population
import const as cn

__version__ = '0.0.3' 
__author__ = 'Lukas Calmbach'
__author_email__ = 'lcalmbach@gmail.com'
VERSION_DATE = '2022-11-06'
my_name = '💉Impfviz-bs'
GIT_REPO = 'https://github.com/lcalmbach/impfviz'

APP_INFO = f"""<div style="background-color:powderblue; padding: 10px;border-radius: 15px;">
    <small>App created by <a href="mailto:{__author_email__}">{__author__}</a><br>
    data from: <a href="http://data.bs.ch">OGD Portal Kanton Basel-Stadt</a><br>
    version: {__version__} ({VERSION_DATE})<br>
    <a href="{GIT_REPO}">git-repo</a>
    """

def show_texts():
    st.markdown(txt.beschreibung)
    st.markdown(txt.methodik)

def show_dashboard():
    """shows the plots in the main content area.
    """
    st.markdown("### Impfdashboard-BS")
    st.markdown(txt.text_dashboard.format(cn.scenario_dict[scenario]), unsafe_allow_html=True)
    plot = alt.Chart(population.stats).mark_area().encode(
        x = alt.X('date:T', axis = alt.Axis(title = 'Datum', 
            format = ("%m %Y"),
            labelAngle=45)
        ),
        y = alt.Y("count:Q", title='Anzahl Personen'),
        color = alt.Color("status", legend=None),
        order = alt.Order('status', sort='ascending'),
        tooltip = alt.Tooltip(['date:T', 'status', 'count'])
    ).properties(height = 400, title=txt.fig1_title.format(cn.scenario_dict[scenario]))
    st.altair_chart(plot, use_container_width=True)
    st.image('./vacc_sim_legend.png')
    #with st.expander('Legend Fig 1'):
    #    st.markdown(txt.fig1_legend[scenario])
    
    plot = alt.Chart(population.stats).mark_line().encode(
        x = alt.X('date:T', axis = alt.Axis(title = 'Datum', 
            format = ("%m %Y"),
            labelAngle=45)
        ),
        y = alt.Y("count:Q", title='Anzahl Personen'),
        color=alt.Color("status",legend=None),
        order=alt.Order('status', sort='ascending'),
        tooltip = alt.Tooltip(['date:T', 'status', 'count'])
    ).properties(title=txt.fig2_title.format(cn.scenario_dict[scenario]))
    st.altair_chart(plot, use_container_width=True)
    #with st.expander('Legend Fig 2'):
    #    st.markdown(txt.fig2_legend[scenario])

    plot = alt.Chart(population.infection_data).mark_bar(width = 2).encode(
        x = alt.X('test_datum:T', axis = alt.Axis(title = 'Datum', 
            format = ("%m %Y"),
            labelAngle=45)
        ),
        y = alt.Y("faelle_bs:Q", title='Anzahl Personen'),
        tooltip = alt.Tooltip(['test_datum:T', 'faelle_bs'])
    ).properties(title=txt.fig3_title.format(cn.scenario_dict[scenario]))
    st.altair_chart(plot, use_container_width=True)

    plot = alt.Chart(population.vacc_data_melted).mark_line().encode(
        x = alt.X('datum:T', axis = alt.Axis(title = 'Datum', 
            format = ("%m %Y"),
            labelAngle=45)
        ),
        y = alt.Y("anzahl:Q", title='Anzahl Personen'),
        color = alt.Color('status', legend=None),
        tooltip = alt.Tooltip(['datum:T', 'anzahl'])
    ).properties(title=txt.fig4_title.format(cn.scenario_dict[scenario]))
    st.altair_chart(plot, use_container_width=True)
    st.image('./vacc_data_legend.png')

    fields = ['vacc_day', 'neu_teilweise_geimpft', 'neu_vollstaendig_geimpft', 'neu_impfung_aufgefrischt']
    df = population.vacc_data[fields]
    df['anzahl']= df['neu_teilweise_geimpft'] + df['neu_vollstaendig_geimpft'] + df['neu_impfung_aufgefrischt']
    df = df.rename(columns={'vacc_day': 'datum'})[['datum', 'anzahl']]
    
    #force time axis scale to start with first day use scale. 
    #domain = list(pd.to_datetime([cn.first_day, datetime.now().date()]).astype(int) / 10 ** 6)
    plot = alt.Chart(df).mark_bar(width=1).encode(
        x = alt.X('datum:T', 
            axis=alt.Axis(title = 'Datum', format = ("%m %Y"), labelAngle=45)
            #,scale=alt.Scale(domain=domain),
        ),
        y = alt.Y("anzahl:Q", title='Anzahl Personen'),
        tooltip = alt.Tooltip(['datum:T', 'anzahl'])
    ).properties(title=txt.fig5_title)
    st.altair_chart(plot, use_container_width=True)



def show_prepare_data_buttons(scenario):
    if st.sidebar.button('generate_history current Scenario'):
        population.create_history(scenario)
        population.status = population.aggregate_data(scenario)
    if st.sidebar.button('generate_history all'):
        for s in cn.scenario_dict:
            st.info(s)
            population.create_history(s)
            population.status = population.aggregate_data(s)
    if st.sidebar.button('init data'):
        population.sim_data()
    if st.sidebar.button('calc Status'):
        population.status = population.aggregate_data(scenario)

# Start

scenario = st.sidebar.selectbox('Szenario Wirkungsdauer Impfung', options=list(cn.scenario_dict.keys()),
                                        format_func=lambda x:cn.scenario_dict[x])

population = Population(cn.POPULATION_BS, scenario)
if socket.gethostname().lower() in cn.DEVELOPER_MACHINES:
    show_prepare_data_buttons(scenario)

menu_options = ['Grafik','Methodik']
sel_menu = st.sidebar.selectbox("Auswahl", options=menu_options)
if (menu_options.index(sel_menu) == 0) & (len(population.stats) >0):
    show_dashboard()
else:
    show_texts()
st.sidebar.markdown(APP_INFO, unsafe_allow_html=True)




