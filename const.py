from datetime import datetime

DEVELOPER_MACHINES = ['liestal']
no_vacc = 0
vacc_expired = 1
part_vacc = 2
full_vacc = 3
booster_vacc = 4
infection_vacc = 5

POPULATION_BS = 196735

INFECTIONS_FILE = './100108.csv'
RAW_DATA_FILE = './100162.csv'
HISTORY_FILE = {'1Y': './status_1Y.pkl', '6M': './status_6M.pkl'}
STATS_FILE = {'1Y': './vacc_stats_1Y.csv', '6M': './vacc_stats_6M.csv'}

vacc_effective_days = {'1Y': 365, '6M': int(365/2)}
scenario_dict = {
        '1Y': {'label': '1 Jahr', 'key': '1Y'},
        '6M': {'label': '6 Monate', 'key': '6M'}
}
url_infections = "https://data.bs.ch/explore/dataset/100108/download/?format=csv&timezone=Europe/Berlin&lang=de&use_labels_for_header=false&csv_separator=%3B"
url_vaccinations = "https://data.bs.ch/explore/dataset/100162/download/?format=csv&timezone=Europe/Berlin&lang=de&use_labels_for_header=false&csv_separator=%3B"
infection_duration = 5
first_day = datetime(2020,2,27)
last_day = datetime.today()
no_days = (last_day - first_day).days

