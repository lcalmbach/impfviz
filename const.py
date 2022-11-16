from datetime import datetime

DEVELOPER_MACHINES = ['liestal']
no_vacc = 0
vacc_expired = 1
part_vacc = 2
full_vacc = 3
booster_vacc = 4
infection_vacc = 5
POPULATION_BS = 196735

url_infections = "https://data.bs.ch/explore/dataset/100108/download/?format=csv&timezone=Europe/Berlin&lang=de&use_labels_for_header=false&csv_separator=%3B"
url_vaccinations = "https://data.bs.ch/explore/dataset/100162/download/?format=csv&timezone=Europe/Berlin&lang=de&use_labels_for_header=false&csv_separator=%3B"
url_hospitalisations = "https://data.bs.ch/explore/dataset/100109/download/?format=csv&timezone=Europe/Berlin&lang=de&use_labels_for_header=false&csv_separator=%3B"
url_deaths = "https://data.bs.ch/explore/dataset/100076/download/?format=csv&timezone=Europe/Zurich&lang=de&use_labels_for_header=false&csv_separator=%3B"
infection_duration = 5
first_day = datetime(2020, 2, 27)
last_day = datetime.today()
no_days = (last_day - first_day).days
days = range(0, no_days)
dark_figure_factor = 3 # 4 times more infections than positive tests
pop_gte_65 = 38937

vacc_effective_months = 6
vacc_effective_days = int(365 / 12 * vacc_effective_months)

wane_factor1 = 40 / vacc_effective_days # 40% decrease in 6 months
wane_factor2 = 20 /  int(365 / 12 * 24) # 20% decrease in 24 months: after 6 months immunity decreases more slowly to 40%
peak_imm_after_first_vacc = 14
