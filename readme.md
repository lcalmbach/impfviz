# Impf-viz-bs
This application estimates the actual vaccination status of the population of Basel/Switzerland based on vaccination and infections data and displays the results in a dashboard. While classic dashboards only show the number vaccinated and infected people in separate graphs, impf-viz-bs combines this data and also takes into account, that vaccination protection expires after a given time. To install this app locally, proceed as follows:

```
> python -m venv env
> env\scripts\activate
> pip install -r requirements.txt
> streamlit run app.py
```