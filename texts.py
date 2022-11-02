methodik = """**Beschreibung der Methodik**
Es wird eine Liste von 196'735 Personen (Basler Bevölkerung 2021) erstellt. Jede Person besetzt einen Impfstatus der per Beginn der Simulation (27.2.2020) auf Ungeimpft initialisiert ist. Zudem wird für jede Person das Datum der letzten Impfung oder der Infektion festgehalten. Für jeden Tag seit Beginn der Pandemie wird aus der Bevölkerung zufällig die Anzahl an diesem Tag Erstgeimpften Personen gezogen und ihr Status auf partiell geimpft gesetzt sowie das Impfdatum eingetragen. Anschliessend wird aus den allen Personen mit Status *Erstimpfung* die Anzahl der an diesem Tag Zweitgeimpften gezogen und deren Status auf *Vollständig geimpft* gesetzt, idem für die *Auffrischimpfungen*. Anschliessend werden die, an diesem Tag gemeldeten Infektionen wie folgt eingetragen: Status wird auf *Durch Infektion geimpft* gesetzt und Datum + 5 Tage ebenfalls eingetragen (Annahme: Infektion dauert ca. 5 Tage und Impfschutz ist erst anschliessend wirksam). Zuletzt wird in der Bevölkerung nach Personen gesucht, deren letztes Impf- oder Infektionsdatum weiter als die Wirkungsdauer von Impfung oder Infektion zurückliegt. Diese werden in den Status *Impfung abgelaufen* versetzt.
"""

beschreibung = """### Immunisierung-Modell der Basler Bevölkerung unter Berücksichtigung der durch Infektion immunisierten Personen sowie der Abnahme der Immunwirkung in Funktion der Zeit

Impf-Dashboards haben zum Ziel, Auskunft über den Impfstatus der Bevölkerung zu geben. Klassische Impfdashboards zeigen zu diesem Zweck die kumulierte Anzahl der partiell, vollständig- und Auffrisch-Geimpften. Dabei wird nicht berücksichtigt, dass ein beträchtlicher Teil der Bevölkerung durch Infektion zusätzlich geimpft wird, sowie die Tatsache, dass sich der Impfschutz mit der Zeit reduziert. Das Ignorieren dieser beiden wichtigen Angaben kann damit begründet werden, dass die genauen Daten dazu nicht vorliegen: die Dauer der wirksamkeit der Impfung ist von Person zu Person unterschiedlich und es kann auch keine scharfe Grenze (vorher geschützt, nachher nicht mehr) gezogen werden. Bei den infizierten Personen ist unbekannt, ob diese vorher ungeschützt oder bereits einen Impfstatus hatten. Für beide Faktoren kann man jedoch Annahmen treffen. 

In der vorliegenden App kann aus zwei Szenarien ausgewählt werden: Impfschutz für 1 Jahr bzw. 6 Monate. Bei den Infektionen wird angenommen, dass PErsonen ohne Impfschutz oder auf Personen, deren Imfpschutz abegelaufen vier Mal anfälliger auf eine Infektion sind als Geimpfte. Auch hier wären unterschiedliche Szenarien sinnvoll. Wichtig bei der Interpretation dieser Resultate ist das Bewusstsein, dass es sich um ein Modell handelt und dass man dessen Annahmen kennt.

Sowohl die [Impfdaten](https://data.bs.ch/explore/dataset/100162) wie die Daten der [Infektionen](https://data.bs.ch/explore/dataset/100108) werden vom OGD Portal des Kanton Basel-Stadt bezogen.
"""
fig1_title = "Impfstatus durch Impfung oder Infektion (Wirksamkeit = {})"

fig2_title = "Impfstatus durch Impfung oder Infektion (Wirksamkeit = {})"

fig3_title = "Covid19 Infektionen der Basler Bevölkerung"

fig4_title = "Kumulierte Impfzahlen Kanton Basel-Stadt"

fig1_legend = {
        '1Y': """Die Impfung beginnt im Januar 2021 und die Erstgeimpften erreichen einen Peak im Juni 2021. Die Zahl der Erstgeimpften reduziert sich durch die Zweitimpfung, welche in der Regel 2 Wochen auf die Erstimpfung erfolgt. Im Nomvember 2020 erfolgen die ersten Auffrischimpfung von Vollständig geimpften, welche dadurch den Status Auffrischimpfung annehmen. Diese erreicht im Januar 2022 ihren Peak. Die Impfung durch Infektion erfolgt hauptsächlich während der Pandemie-Wellen. 
            """, 
        '6M':"""
        """
}

fig2_legend = {
        '1Y': """
            """, 
        '6M':"""
        """
}
