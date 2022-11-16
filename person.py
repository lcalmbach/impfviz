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
    def __init__(self, id:int):
        """Initializes a person with a vaccination state, id and daten when 
        last vaccinated or infected.

        Args:
            id (int): _description_
        """
        self.id = id
        self.immunity_score = 0 # 0 - 100
        self.number_of_vaccinations = 0
        self.number_of_infections = 0
        self.last_status_date = 0
        self.status = 0
        self.age_gte_65 = False

        
    def update_immunity_score(self, day:int):
        # increase or decrease immunity: if person is infected then set to 100, if person is vaccinated < 14 days ago, increase to 100 
        # until day 14, if vaccination of infection is < 6M ago, decrease by waning factor (40% in 6 Months) if infection is > 6M ago
        # decrease by 20% in 24 months
        
        if (day - self.last_status_date <= cn.peak_imm_after_first_vacc) and (self.status == cn.full_vacc):
            self.immunity_score += (100 / 14)
        elif (day - self.last_status_date > cn.vacc_effective_days):
            self.immunity_score -= cn.wane_factor2
        elif (day - self.last_status_date <= cn.vacc_effective_days):
            self.immunity_score -= cn.wane_factor1
        else:
            print(day, self.last_status_date, self.status)


    def update_status(self, day:int):
        """update the person status to expired if last status date
        is greater than the expiry duration of the vacc_effective_days period.

        Args:
            day (int): current day since start of pandemic
        """
        if (day - self.last_status_date > cn.effective_days):
            self.status = cn.vacc_expired
            self.last_status_date = day

    def vaccinate(self, day:int, sequence):
        """Person gets a vaccination and changes state based on his previous status. e.g. when status
        was no_vacc then new status is: first_vacc. last_status_date changes to today.

        Args:
            day (int): current day since start of pandemic
        """
        if (self.status == cn.no_vacc) | (sequence == 1):
            self.status = cn.part_vacc
        elif (self.status in [cn.vacc_expired, cn.part_vacc, cn.infection_vacc]) | (sequence == 2):
            self.status = cn.full_vacc
        elif (self.status in [cn.full_vacc, cn.booster_vacc]) | (sequence > 2):
            self.status = cn.booster_vacc
        self.number_of_vaccinations += 1
        self.last_status_date = day
    
    def infect(self, day):
        self.status = cn.infection_vacc
        self.number_of_infections += 1
        self.last_status_date = day + cn.infection_duration
        self.immunity_score = 100

    def reset_status(self, dt):
        if self.status != cn.no_vacc:
            self.status = cn.vacc_expired
            self.last_status_date = dt
    
    def __repr__(self):
        return f"Person: {self.id}, last_status_date: {self.last_status_date} status: {self.status}"

class Population():
    def __init__(self, n:int):
        """Initializes the population of basel with 200k items of type person

        Args:
            n (int): _description_
        """
        self.total = n
        self.population = self.init_population()
        # used in first trial, where a coordinate was assigned to each person
        # self.population_df = self.init_population_df()
        self.history = pd.DataFrame()
        self.infection_data = self.get_infections()
        self.hospitalisation_data = self.get_hospitalisations()
        self.death_data = self.get_deaths()
        self.vacc_data, self.vacc_data_melted = self.get_vaccinations()
        self.stats_vacc_status_file = f'./vacc_stats.csv'
        self.stats_protection_file = f'./protection_stats.csv'
        self.history_file = f'./status.pkl'
        self.stats = self.get_stats(self.stats_vacc_status_file)
        self.protection_stats = self.get_stats(self.stats_protection_file)
        # init population >= 65
        pop_gte_65 = random.sample(self.population, cn.pop_gte_65)
        for p in pop_gte_65:
                p.age_gte_65 = True


    @st.experimental_memo
    def get_vaccinations(_self):
        url = cn.url_vaccinations
        s = requests.get(url).content
        df = pd.read_csv(io.StringIO(s.decode('utf-8')), sep=';')
        df['vacc_day'] = pd.to_datetime(df['vacc_day'])
        # add empty record on first day so date axis in diagrams plot correctly
        _df = pd.DataFrame({'vacc_day':[cn.first_day], 'vollstaendig_geimpft':[0]})
        df = pd.concat([_df, df], ignore_index=True)
        df = df.fillna(0)

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
        # df = df.rename(columns={'test_datum':'datum'}) 
        return df
    
    @st.experimental_memo
    def get_hospitalisations(_self):
        url=cn.url_hospitalisations
        s=requests.get(url).content
        df = pd.read_csv(io.StringIO(s.decode('utf-8')), sep=';')
        fields = ['date', 'current_hosp_resident', 'current_icu']
        df = df[fields]
        df['date'] = pd.to_datetime(df['date'])
        df = df.rename(columns={'date':'datum'}) 
        return df
    
    @st.experimental_memo
    def get_deaths(_self):
        url=cn.url_deaths
        s=requests.get(url).content
        df = pd.read_csv(io.StringIO(s.decode('utf-8')), sep=';')
        fields = ['date', 'newdeaths']
        df = df[fields]
        df['date'] = pd.to_datetime(df['date'])
        df = df.groupby(['date']).sum().reset_index()
        df.columns = ['datum','num_deaths']
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
            return df


    def get_stats(self, filename):
        """stats with day, status, count per row"""
        if path.exists(filename):
            """"reads the data from data.bs"""
            df = pd.read_csv(filename)
            return df
        else:
            return pd.DataFrame()


    def init_population(self):
        pop = []
        for i in range(0, self.total):
            p = Person(i)
            pop.append(p)
        return pop

    # def init_population_df(self):
    #     df = pd.DataFrame({'person_id': list(range(1, self.total+1)), 
    #         'x': [int(np.random.random() * 5000) for x in range(1, self.total+1)], 
    #         'y': [int(np.random.random() * 5000) for x in range(1, self.total+1)]}
    #     )
    #     type_dict = {'person_id':'int32', 'x':'int32', 'y':'int32'}
    #     return df.astype(type_dict)


    # def x(self):
    #     return [p.x for p in self.population]
    
    # def y(self):
    #     return [p.y for p in self.population]
    
    def aggregate_data(self):
        def assign_protection_state(_df):
            _df['status'] = 'Kein Schutz'
            _df.loc[_df['immunity_score'] > 20, 'status'] = 'Schutz gegen schwere Krankheit'
            _df.loc[_df['immunity_score'] > 60, 'status'] = 'Schutz gegen Infektion'
            return _df
        
        def add_date(_df):
            _df['first_day'] = cn.first_day
            _df['first_day'] = pd.to_datetime(_df['first_day'])
            _df['day'] = pd.to_timedelta(_df['day'], 'd')
            _df['date'] = _df['first_day'] + _df['day']
            return _df

        df = self.get_history()
        df_impf_status = df[['day', 'status','person_id']].groupby(['day', 'status']).count().reset_index()
        df_impf_status.columns = ['day', 'status', 'count']
        df_impf_status = add_date(df_impf_status)
        df_impf_status['status'] = df_impf_status['status'].replace(
            to_replace=[0,1,2,3,4,5], 
            value=['keine Immunität', 'Impfschutz abgelaufen', 'Partiell geimpft', 'Grundimmunisiert', 'Auffrischimpfung', 'durch Infektion immunisiert'])
        df_impf_status.to_csv(self.stats_vacc_status_file, index=False)

        df = assign_protection_state(df)
        df_protection_status = df[['day', 'status','person_id']].groupby(['day', 'status']).count().reset_index()
        df_protection_status.columns = ['day', 'status', 'count']
        df_protection_status = add_date(df_protection_status)
        df_protection_status.to_csv(self.stats_protection_file, index=False)
        return df_impf_status, df_protection_status


    def create_history(self):
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
                p.vaccinate(day, 1)

            #fully vaccinated
            filtered_list = list(filter(lambda p: p.status == cn.part_vacc, self.population))
            if row['neu_vollstaendig_geimpft'] < len(filtered_list):
                num=row['neu_vollstaendig_geimpft']
            else:
                num = len(filtered_list)
            random_elements = random.sample(filtered_list, num)
            for p in random_elements:
                p.vaccinate(day, 2)
            # booster
            filtered_list = list(filter(lambda p: p.status in [cn.full_vacc, cn.vacc_expired], self.population))
            if row['neu_impfung_aufgefrischt'] < len(filtered_list):
                num = row['neu_impfung_aufgefrischt']
            else:
                num = len(filtered_list)
            random_elements = random.sample(filtered_list, num)
            for p in random_elements:
                p.vaccinate(day, 3)

            # infections
            filtered_list_vaccinated = list(filter(lambda p: p.status not in [cn.no_vacc, cn.vacc_expired], self.population))
            filtered_list_no_vacc = list(filter(lambda p: p.status in [cn.no_vacc, cn.vacc_expired], self.population))
            # ratio of non vaccinated to total population
            fact = len(filtered_list_no_vacc) / cn.POPULATION_BS

            # takes into account dark figure of infections
            infections = row['faelle_bs'] * cn.dark_figure_factor
            num_non_vacc = int(fact * infections)
            num_vacc = int((infections - num_non_vacc) * 0.2) # make it 5 times more likely for non vacc persons to be infected than non vacc
            num_non_vacc = infections - num_vacc
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
            if day > cn.vacc_effective_days:
                expired_list = list(filter(lambda p: (((day - p.last_status_date) > cn.vacc_effective_days) and (p.status not in [cn.no_vacc, cn.vacc_expired])), self.population))
                for p in expired_list:
                    p.reset_status(day)
            
             # update immunity score
            person_list = list(filter(lambda p: (p.number_of_vaccinations + p.number_of_infections) > 0, self.population))
            for p in person_list:
                p.update_immunity_score(day)

            # take all persons, transform them into records and collate to big result dataframe
            _df = pd.DataFrame(
                {'day': [day] * self.total, 
                'person_id': [p.id for p in self.population],
                'status': [p.status for p in self.population],
                'immunity_score': [p.immunity_score for p in self.population],
                'number_of_vaccinations': [p.number_of_vaccinations for p in self.population],
                'number_of_infections': [p.number_of_infections for p in self.population],
                }
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
        





    