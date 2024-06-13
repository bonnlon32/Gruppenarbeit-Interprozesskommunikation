import os

# Erster Entwurf für den Report-Prozess. 
def report_process():
        pipe_report = '/tmp/stat_to_report'  # Pfad zur benannten Pipe für den Report-Prozess
        
        fifo_report = open(pipe_report, 'r')

while True:
        daten = fifo_report.readlines()
        if daten:
            summenwert, durchschnitt = map(float, daten)
            print(f"Report: Summe = {summenwert}, Mittelwert = {durchschnitt}")

if __name__ == "__main__":
    report_process()