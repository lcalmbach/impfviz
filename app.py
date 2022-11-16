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


def show_dashboard(viz_type:int):
    """shows the plots in the main content area.
    """
    def get_compare_plots():
        st.write("Vergleichsplots:")
        compare_plots = ['Infektionen', 'Impfungen kumuliert', 'Total Impfungen', 'Hospitalisierte', 'Gestorbene',]
        cols = st.columns(5)
        i = 0
        show_flags = [True] * 5
        for p in compare_plots:
            with cols[i]:
                show_flags[i] = st.checkbox(p, value = show_flags[i])
            i += 1
        return show_flags
    
    def show_main_plots(df, legend_file):
        field = 'status'
        plot = alt.Chart(df).mark_area().encode(
            x = alt.X('date:T', axis = alt.Axis(title = 'Datum', 
                format = ("%m %Y"),
                labelAngle=45)
            ),
            y = alt.Y("count:Q", title='Anzahl Personen'),
            color = alt.Color(field),
            order = alt.Order(field, sort='ascending'),
            tooltip = alt.Tooltip(['date:T', field, 'count']),
        ).properties(height = 400, title=txt.fig1_title[viz_type])
        plot = plot.configure_range(category=alt.RangeScheme(colors))
        st.altair_chart(plot, use_container_width=True)

        st.image(legend_file)
        #with st.expander('Legend Fig 1'):
        #    st.markdown(txt.fig1_legend[scenario])

        # line diagram simulation
        plot = alt.Chart(df).mark_line().encode(
            x = alt.X('date:T', axis = alt.Axis(title = 'Datum', 
                format = ("%m %Y"),
                labelAngle=45)
            ),
            y = alt.Y("count:Q", title='Anzahl Personen'),
            color=alt.Color(field, legend=None),
            order=alt.Order(field, sort='ascending'),
            tooltip = alt.Tooltip(['date:T', field, 'count'])
        ).properties(title=txt.fig2_title[viz_type])
        plot = plot.configure_range(category=alt.RangeScheme(colors))
        st.altair_chart(plot, use_container_width=True)
        #with st.expander('Legend Fig 2'):
        #    st.markdown(txt.fig2_legend[scenario])

    st.markdown("### Impfdashboard-BS")
    st.markdown(txt.text_dashboard, unsafe_allow_html=True)
    show_plot_flags = get_compare_plots()
    st.write('')
    # area diagram simulation
    colors = ['#BFD7ED','#60A3D9','#0074B7', '#003B73', 'orange', 'silver']
    
    if viz_type == 0:
        show_main_plots(population.stats, 'vacc_sim_legend.png')
    else:
        show_main_plots(population.protection_stats, 'protection_legend.png')

    if show_plot_flags[0]:
        plot = alt.Chart(population.infection_data).mark_bar(width = 2).encode(
            x = alt.X('test_datum:T', axis = alt.Axis(title = 'Datum', 
                format = ("%m %Y"),
                labelAngle=45)
            ),
            y = alt.Y("faelle_bs:Q", title='Anzahl Personen'),
            tooltip = alt.Tooltip(['test_datum:T', 'faelle_bs'])
        ).properties(title=txt.fig3_title)
        st.altair_chart(plot, use_container_width=True)
    
    if show_plot_flags[1]:
        plot = alt.Chart(population.vacc_data_melted).mark_line().encode(
            x = alt.X('datum:T', axis = alt.Axis(title = 'Datum', 
                format = ("%m %Y"),
                labelAngle=45)
            ),
            y = alt.Y("anzahl:Q", title='Anzahl Personen'),
            color = alt.Color('status', legend=None),
            tooltip = alt.Tooltip(['datum:T', 'anzahl'])
        ).properties(title=txt.fig4_title)
        st.altair_chart(plot, use_container_width=True)
        st.image('./vacc_data_legend.png')


    if show_plot_flags[2]:
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

    if show_plot_flags[3]:
        df = population.hospitalisation_data
        plot = alt.Chart(df).mark_bar(width=1).encode(
            x = alt.X('datum:T', 
                axis=alt.Axis(title = 'Datum', format = ("%m %Y"), labelAngle=45)
                #,scale=alt.Scale(domain=domain),
            ),
            y = alt.Y("current_hosp_resident:Q", title='Anzahl Hospitalisierte'),
            tooltip = alt.Tooltip(['datum:T', 'current_hosp_resident'])
        ).properties(title=txt.fig6_title)
        st.altair_chart(plot, use_container_width=True)

    if show_plot_flags[3]:
        df = population.death_data
        plot = alt.Chart(df).mark_bar(width=1).encode(
            x = alt.X('datum:T', 
                axis=alt.Axis(title = 'Datum', format = ("%m %Y"), labelAngle=45)
                #,scale=alt.Scale(domain=domain),
            ),
            y = alt.Y("num_deaths:Q", title='Anzahl Gestorbene'),
            tooltip = alt.Tooltip(['datum:T', 'num_deaths'])
        ).properties(title=txt.fig7_title)
        st.altair_chart(plot, use_container_width=True)


def show_prepare_data_buttons():
    if st.sidebar.button('Simulation ausführen'):
        population.create_history()
        population.status = population.aggregate_data()
    #if st.sidebar.button('init data'):
    #    population.sim_data()
    if st.sidebar.button('Statistik erstellen'):
        population.aggregate_data()

# Start

population = Population(cn.POPULATION_BS)
if socket.gethostname().lower() in cn.DEVELOPER_MACHINES:
    show_prepare_data_buttons()

menu_options = ['Grafik', 'Methodik']
viz_options = ['Impf-Status', 'Schutz']
sel_menu = st.sidebar.selectbox("Auswahl", options=menu_options)
sel_viz = st.sidebar.selectbox("Darstellung", options=viz_options)

if (menu_options.index(sel_menu) == 0) & (len(population.stats) > 0):
    show_dashboard(viz_options.index(sel_viz))
else:
    show_texts()
st.sidebar.markdown(APP_INFO, unsafe_allow_html=True)




