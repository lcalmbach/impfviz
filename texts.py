text_dashboard = """Es werden nur Personen mit Wohnsitz im Kanton Basel-Stadt berücksichtigt. Es werden verschiedene Annahmen getroffen, welche in der Methodik genauer erläutert werden. Für detaillierte Angaben zur Methodik wähle das Menu `Methodik` im Seitenfenster aus.<br><br>"""

methodik = """**Beschreibung der Methodik**
Es wird eine Liste von 196'735 Personen (Basler Bevölkerung 2021) erstellt. Jede Person besetzt einen Impfstatus der per Beginn der Simulation (27.2.2020) auf Ungeimpft initialisiert ist. Zudem wird für jede Person das Datum der letzten Impfung oder der Infektion festgehalten. Für jeden Tag seit Beginn der Pandemie wird aus der Bevölkerung zufällig die Anzahl an diesem Tag Erstgeimpften Personen gezogen und ihr Status auf partiell geimpft gesetzt sowie das Impfdatum eingetragen. Anschliessend wird aus den allen Personen mit Status *Erstimpfung* die Anzahl der an diesem Tag Zweitgeimpften gezogen und deren Status auf *Vollständig geimpft* gesetzt, idem für die *Auffrischimpfungen*. Anschliessend werden die, an diesem Tag gemeldeten Infektionen wie folgt eingetragen: Status wird auf *Durch Infektion geimpft* gesetzt und Datum + 5 Tage ebenfalls eingetragen (Annahme: Infektion dauert ca. 5 Tage und Impfschutz ist erst anschliessend wirksam). Zuletzt wird in der Bevölkerung nach Personen gesucht, deren letztes Impf- oder Infektionsdatum weiter als die Wirkungsdauer von Impfung oder Infektion zurückliegt. Diese werden in den Status *Impfung abgelaufen* versetzt.
"""

beschreibung = """### Immunisierung-Modell der Basler Bevölkerung unter Berücksichtigung der durch Infektion immunisierten Personen sowie der Abnahme der Immunwirkung in Funktion der Zeit

Die vorliegende Applikation versucht den Verlauf des Covid19-Immun-Status der Basler Bevölkerung zu eruieren, welcher aus der Kombination von Impfung und Infektionen erfolgt. Dazu wurde ein Modell entwickelt, bei welchem die publizierten Impf- und Infektionsdaten auf eine virtuelle Bevölkerung von 200'000 Personen anwendet. Verschiedene Studien zeigen, dass die Immunisierung durch Infektion oder Impfung in Funktion der Zeit abnimmt. Dieser Effekt wird ebenfalls in der Applikation berücksichtigt, indem bei jeder Impfung oder Infektion der Impfschutz der Person zuerst auf 100% gesetzt wird, und anschliessend über die Dauer von 6 Monaten auf 60% abgebaut wird, über die nöchsten 2 Jahre auf 20%. Während den 6 Monaten nach einer Immunisierung gilt die Person als gegen eine Infektion-, anschliessend gegen einen schweren Krankheitsverlauf geschützt. Es wird zudem die Dunkelziffer bei den Infektionen berücksichtigt. Die Schätzung für das Verhältnis von registrierten und tatsächlichen Infektionen variieren stark in vorliegenden Modell wurden basierend auf einer [Studie von Timothy W. Russel](https://www.watson.ch/wissen/coronavirus/571890552-coronavirus-wie-hoch-ist-die-dunkelziffer-bei-den-infektionen) eine Dunkelziffer von 76% angenommen. Damit wurden alle registrierten Infektionen am gleichen Tag mit dem Faktor 3 multipliziert. Weitere Annahmen mussten bei der Auswahl in infizierten PErsonen getroffen werden, da aus den publizierten Zahlen nicht hervorgeht, ob eine infizierte Person geimpft oder in der Vergangenheit bereits erkrankt war. Für den Impfstatus der Bevölkerung ist dies relevant, da die Infektion einer geimpften Person lediglich zu einer Affrischung einer bestehenden Immunisierung führt, während die Infektion einer nicht geimpften Person die Zahl der immunisierten Personen erhöht. Bei der Auswahl der infizierten Personen aus der Bevölkerung wurde davon ausgegangen, dass Personen, in den letzen 6 Monaten entweder geimpft oder infiziert wurden, eine 5 Mal kleinere Wahrsceinlichkeit für eine Infektion besitzen. Ist zum Beispiel in der Bevölkerung das Verhältnis geimpft/ungeimpft am Tag X 1:1 und es wurden an diesem Tag 100 Personen infiziert, so wurden im Modell für diesen Tag 2 bereits geimpfte/erkrankte und 8 ungeimpfte Personen aus dem Bevölkerungsmodell infiziert. 

Die aus dem Modell generierten Grafiken zeigen, dass seit Beginn 2022 der Grossteil der Bevölkerung gegen Infektion geschützt ist. Dieser Anteil nimmt anschliessend wieder ab, wobei der Schutz gegen schwerer Krankheit steigt. Im dritten Quartal des Jahres nimmt auch wieder die Zahl der Personen ohne Impfschutz zu. Dies sind die Personen, die am Anfang der Pandemie erkrankten und seither weder geimpft noch infiziert wurden. Da über die Langzeitdauer des Imfpschutzes gegen schwere Erkrankung bei Covid noch zu wenig Daten vorliegen, ist die im Modell gemachte Schätzung von zwei Jahren mit einer grossen Unsicherheit behaftet.

Wichtig bei der Interpretation dieser Resultate ist das Bewusstsein, dass es sich um ein noch grobes Modell handelt und dass man dessen Annahmen kennt. Es ist aber zumindest ansatzweise ein Werkzeug vorhanden, um die Wirkung von Infektionen und des Ablaufs des Imfpschutzes auf den Impfstatus abzuschätzen. Klassische Impfdashboards, welche diese Parameter ignorieren, enthalten zwar genauere Angaben zur Zahl der verschiedenen Impfungen pro Tag, sagen aber sehr wenig aus zum Impfstatus der Bevölkerung und die Angabe % Bevölkerung geimpft ist mit Vorsicht zu geniessen.

Sowohl die [Impfdaten](https://data.bs.ch/explore/dataset/100162) wie die Daten der [Infektionen](https://data.bs.ch/explore/dataset/100108) werden vom OGD Portal des Kanton Basel-Stadt bezogen.
"""

fig1_title = {0: "Impfstatus durch Impfung oder Infektion",
                1: "Schutz der Basler Bevölkerung vor Infektion/schwerer Verlauf"
}
fig2_title = {0: "Impfstatus durch Impfung oder Infektion",
                1: "Schutz der Basler Bevölkerung vor Infektion/schwerer Verlauf"
}
fig3_title = "Covid19 Infektionen der Basler Bevölkerung"
fig4_title = "Kumulierte Impfzahlen Kanton Basel-Stadt"
fig5_title = "Total Impfungen, Kanton Basel-Stadt"
fig6_title = "Hospitalisierte, Kanton Basel-Stadt"
fig7_title = "Gestorbene mit Covid-19, Kanton Basel-Stadt"

fig1_legend = {
        '1Y': """Die Impfkampagne beginnt im Januar 2021 und die Erstgeimpften erreichen einen Peak im Juni 2021. Die Zahl der Erstgeimpften reduziert sich durch die Zweitimpfung, welche in der Regel 2 Wochen auf die Erstimpfung erfolgt. Im November 2020 erfolgen die ersten Auffrischimpfungen von Vollständig geimpften, welche dadurch den Status Auffrischimpfung annehmen. Diese erreicht im Januar 2022 ihren Peak. Die Impfung durch Infektion erfolgt hauptsächlich während der Pandemie-Wellen. 
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
