from codecs import ignore_errors
import streamlit as st
from datetime import timedelta, datetime
from lib2to3.pgen2.pgen import DFAState
import numpy as np
import pandas as pd
import random
from os import path
import io
import requests

import const as cn
placeholder = st.empty()

class Person():
    def __init__(self, id):
        self.id = id
        self.status = 0
        self.last_status_date = 0
        
    def update_status(self, day):
        if (day - self.last_status_date > cn.effective_days):
            self.status = cn.vacc_expired
            self.last_status_date = day

    def vaccinate(self, day):
        if self.status == cn.no_vacc:
            self.status = cn.part_vacc
        elif self.status == cn.vacc_expired:
            self.status = cn.full_vacc
        elif self.status == cn.part_vacc:
            self.status = cn.full_vacc
        elif self.status == cn.full_vacc:
            self.status = cn.booster_vacc
        self.last_status_date = day
    
    def infect(self, day):
        self.status = cn.infection_vacc
        self.last_status_date = day + cn.infection_duration

    def reset_status(self, dt):
        if self.status != cn.no_vacc:
            self.status = cn.vacc_expired
            self.last_status_date = dt
    
    def __repr__(self):
        return f"Person: {self.id}, last_status_date: {self.last_status_date} status: {self.status}"

class Population():
    def __init__(self, n, scenario):
        self.scenario = scenario
        self.total = n
        self.population = self.init_population()
        # used in first trial, where a coordinate was assigned to each person
        # self.population_df = self.init_population_df()
        self.history = pd.DataFrame()
        self.infection_data = self.get_infections()
        self.vacc_data, self.vacc_data_melted = self.get_vaccinations()
        self.stats_file = f'./vacc_stats_{scenario}.csv'
        self.history_file = f'./status_{scenario}.pkl'
        self.stats = self.get_stats()

    @st.experimental_memo
    def get_vaccinations(_self):
        url = cn.url_vaccinations
        s = requests.get(url).content
        df = pd.read_csv(io.StringIO(s.decode('utf-8')), sep=';')
        df['vacc_day'] = pd.to_datetime(df['vacc_day'])
        
        fields = ['vacc_day', 'vollstaendig_geimpft', 'teilweise_geimpft', 'impfung_aufgefrischt', 'mit_mindestens_einer_dosis_geimpft']
        df_melted = df[fields]
        del fields[0]
        df_melted = pd.melt(df, id_vars=['vacc_day'], value_vars=fields)
        df_melted.columns = ['datum', 'status', 'anzahl']
        return df, df_melted

    @st.experimental_memo
    def get_infections(_self):
        url=cn.url_infections
        s=requests.get(url).content
        df = pd.read_csv(io.StringIO(s.decode('utf-8')), sep=';')
        fields = ['test_datum', 'faelle_bs']
        df = df[fields]
        df['test_datum'] = pd.to_datetime(df['test_datum'])
        return df
        
    def sim_data(self):
        """
        Generates a test dataset
        """
        li1 = []
        li2 = []
        ld = []
        for day in cn.days:
            impf1 = random.randint(200, 300)
            if day > 10:
                impf2 = random.randint(200, 300)
            else:
                impf2 = 0
            ld.append(cn.first_day + timedelta(days=day))
            li1.append(impf1)
            li2.append(impf2)
        df = pd.DataFrame({'date': ld, 'impf1': li1, 'impf2':li2})
        df = df.set_index('date')
        df.to_csv('test.dat')
        st.success('Vaccination data was initialized')


    def get_history(self):
        """data with day, personid per row. used to generate the aggregated file"""
        if path.exists(self.history_file):
            """"reads the data from data.bs"""
            df = pd.read_pickle(self.history_file)
            #type_dict = {'day':'timedelta', 'person_id':'int32', 'status':'int32', 'date':'datetime64'}
            #df = df.astype(type_dict)
            #convert timedelta to days, otherweise groupby does not work
            return df


    def get_stats(self):
        """stats with day, status, count per row"""
        if path.exists(self.stats_file):
            """"reads the data from data.bs"""
            # df = pd.read_csv('status.csv')
            df = pd.read_csv(self.stats_file)
            return df
        else:
            return pd.DataFrame()

    def init_population(self):
        pop = []
        for i in range(0, self.total):
            p = Person(i)
            pop.append(p)
        return pop

    def init_population_df(self):
        df = pd.DataFrame({'person_id': list(range(1, self.total+1)), 
            'x': [int(np.random.random() * 5000) for x in range(1, self.total+1)], 
            'y': [int(np.random.random() * 5000) for x in range(1, self.total+1)]}
        )
        type_dict = {'person_id':'int32', 'x':'int32', 'y':'int32'}
        return df.astype(type_dict)


    def x(self):
        return [p.x for p in self.population]
    
    def y(self):
        return [p.y for p in self.population]
    
    def aggregate_data(self, scenario):
        df = self.get_history()
        df = df.groupby(['day', 'status']).count().reset_index()
        df.columns = ['day', 'status', 'count']
        df['first_day'] = cn.first_day
        df['first_day'] = pd.to_datetime(df['first_day'])
        df['day'] = pd.to_timedelta(df['day'], 'd')
        df['date'] = df['first_day'] + df['day']
        df['status'] = df['status'].replace(
            to_replace=[0,1,2,3,4,5], 
            value=['kein Impfschutz', 'Impfschutz abgelaufen', 'Partiell geimpft', 'Vollständig geimpft', 'Auffrischimpfung', 'durch Infektion geimpft'])

        df.to_csv(self.stats_file, index=False)
        return df


    def create_history(self, scenario):
        def read_data():
            """"reads the data from data.bs"""
            fields = ['vacc_day','neu_teilweise_geimpft', 'neu_vollstaendig_geimpft', 'neu_impfung_aufgefrischt']
            df_vacc = self.vacc_data[fields]
            df_vacc['vacc_day'] = pd.to_datetime(df_vacc['vacc_day'])
            df_vacc.sort_values(by = ['vacc_day'], inplace=True)
            # df_vacc.set_index('vacc_day', inplace=True)
            
            df_infections = self.infection_data
            df_vacc = df_infections.merge(df_vacc, how='left', right_on='vacc_day', left_on='test_datum').set_index('test_datum')
            df_vacc = df_vacc.drop('vacc_day', axis=1).reset_index()
            df_vacc.rename(columns={'test_datum':'vacc_date'}, inplace=True)
            df_vacc = df_vacc.fillna(0).sort_values(by=['vacc_date'])
            type_dict = {'neu_teilweise_geimpft':'int32', 'neu_vollstaendig_geimpft':'int32', 'neu_impfung_aufgefrischt':'int32'}
            df_vacc = df_vacc.astype(type_dict)
            # st.write(df_vacc)
            return df_vacc

        def sim_day(day:int, row):
            #partially vaccinated
            filtered_list = list(filter(lambda p: p.status == cn.no_vacc, self.population))
            if row['neu_teilweise_geimpft'] < len(filtered_list):
                num=row['neu_teilweise_geimpft']
            else:
                num = len(filtered_list)
            random_elements = random.sample(filtered_list, num)
            for p in random_elements:
                p.vaccinate(day)

            #fully vaccinated
            filtered_list = list(filter(lambda p: p.status == cn.part_vacc, self.population))
            if row['neu_vollstaendig_geimpft'] < len(filtered_list):
                num=row['neu_vollstaendig_geimpft']
            else:
                num = len(filtered_list)
            random_elements = random.sample(filtered_list, num)
            for p in random_elements:
                p.vaccinate(day)
            # booster
            filtered_list = list(filter(lambda p: p.status in [cn.full_vacc, cn.vacc_expired], self.population))
            if row['neu_impfung_aufgefrischt'] < len(filtered_list):
                num = row['neu_impfung_aufgefrischt']
            else:
                num = len(filtered_list)
            random_elements = random.sample(filtered_list, num)
            for p in random_elements:
                p.vaccinate(day)

            # infections
            filtered_list_vaccinated = list(filter(lambda p: p.status not in [cn.no_vacc, cn.vacc_expired], self.population))
            filtered_list_no_vacc = list(filter(lambda p: p.status in [cn.no_vacc, cn.vacc_expired], self.population))
            fact = len(filtered_list_no_vacc) / cn.POPULATION_BS

            num_non_vacc = int(fact * row['faelle_bs'])
            num_vacc = int((row['faelle_bs'] - num_non_vacc) * 0.2) # make it 5 times more likely for non vacc persons to be infected than non vacc
            num_non_vacc = row['faelle_bs'] - num_vacc
            # st.write( {'vaccinated': len(filtered_list_vaccinated), 'fact': fact, 'all': row['faelle_bs'], 'vaccinated': num_vacc, 'non_vacc': num_non_vacc})

            if num_non_vacc < len(filtered_list_no_vacc):
                num = num_non_vacc
            else:
                num = len(filtered_list_no_vacc)
            random_elements = random.sample(filtered_list_no_vacc, num)
            for p in random_elements:
                p.infect(day)

            # distribute 25% of cases on vaccinated persons
            if num_vacc < len(filtered_list_vaccinated):
                num = int((1-fact) * row['faelle_bs'])
            else:
                num = len(filtered_list_vaccinated)

            random_elements = random.sample(filtered_list_vaccinated, num)
            for p in random_elements:
                p.infect(day)

            # vaccination expired 
            if day > cn.vacc_effective_days[scenario]:
                expired_list = list(filter(lambda p: (((day - p.last_status_date) > cn.vacc_effective_days[scenario]) and (p.status not in [cn.no_vacc, cn.vacc_expired])), self.population))
                for p in expired_list:
                    p.reset_status(day)
            
            # take all persons, transform them into records and collate to big result dataframe
            _df = pd.DataFrame({'day': [day] * self.total, 
                'person_id': [p.id for p in self.population],
                'status': [p.status for p in self.population]}
            )
            self.history = pd.concat([self.history, _df], ignore_index=True)

        self.data = read_data()
        for index, row in self.data.iterrows():
            day = (row['vacc_date'] - cn.first_day).days
            with placeholder.container():
                st.write(f"{row['vacc_date']}, day: {day}: memory: {int(self.history.memory_usage().sum() / (1024**2))} MB")
            sim_day(day, row)
            #if day > 20:
            #    break
        st.info("Writing results to file")
        self.history.to_pickle(self.history_file)
        st.success(f"All results have been saved to '{self.history_file}'")
        





    