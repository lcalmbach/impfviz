from datetime import datetime

DEVELOPER_MACHINES = ['liestal']
no_vacc = 0
vacc_expired = 1
part_vacc = 2
full_vacc = 3
booster_vacc = 4
infection_vacc = 5
POPULATION_BS = 196735

vacc_effective_days = {'6M': int(365/12*6), '8M':int(365/12*8), '1Y': 365}
scenario_dict = {'6M': '6 Monate', '8M': '8 Monate', '1Y': '1 Jahr'}
url_infections = "https://data.bs.ch/explore/dataset/100108/download/?format=csv&timezone=Europe/Berlin&lang=de&use_labels_for_header=false&csv_separator=%3B"
url_vaccinations = "https://data.bs.ch/explore/dataset/100162/download/?format=csv&timezone=Europe/Berlin&lang=de&use_labels_for_header=false&csv_separator=%3B"
infection_duration = 5
first_day = datetime(2020, 2, 27)
last_day = datetime.today()
no_days = (last_day - first_day).days

