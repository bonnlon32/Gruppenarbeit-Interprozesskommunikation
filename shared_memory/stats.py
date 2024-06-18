def calculate_stats(zahlen_liste):
    summenwert = sum(zahlen_liste)
    anzahl = len(zahlen_liste)
    durchschnitt = summenwert / anzahl if anzahl > 0 else 0
    return summenwert, durchschnitt