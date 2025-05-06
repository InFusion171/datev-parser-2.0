# DATEV ASCII-Weiterverarbeitungsdatei Konvertierer 2.0

### Was ist neu
- Überarbeites GUI mit PyQt

## Übersicht
- Das Programm dient dazu, exportierte Überweisungsdaten in eine [DATEV-Weiterverarbeitungsdatei](https://apps.datev.de/help-center/documents/9226961) umzuwandeln.
- Im Programm gibt man die IBAN und die BIC des Sparda-Bank-Kontos an und wählt die exportierte Überweisungsdatei aus. Die Datei kann entweder eine .csv-Datei oder eine normale .txt-Datei sein.
- Danach drückt man auf "Generieren". Das Programm erstellt einen Ordner mit dem Namen "KONTOINHABER Überweisungen", falls der KONTOINHABER in der Datei angegeben ist.
  In dem Ordner befinden sich dann die konvertierten Dateien für DATEV, die nach den Monaten des Valutadatums strukturiert sind.
- Die Datei muss folgendes [Format](#format) haben.

## Für Entwickler
- Python 3.12 oder höher

- Zu installierende Python-Packete:
    - tk 
    - chardet
    - PySide6

## Format
Es reicht aus folgendes Format zu haben:
```
"Buchungstag";"Wertstellungstag";"Verwendungszweck";"Umsatz";"Währung"
"06.08.2024";"06.08.2024";"Verwendungszweck";"-1,00";"EUR";""
"10.08.2024";"10.08.2024";"Verwendungszweck";"1,00";"EUR";""
"1.07.2024";"2.07.2024";"Verwendungszweck";"1,00";"EUR";""
etc...
```

Empfohlen wird aber dieses Format:
```
"Kontoumsätze SpardaGiro"

"Kontoinhaber:";"Max Mustermann"
"Kundennummer:";"123"

"Umsätze ab";"Enddatum";"Kontonummer";"Saldo";"Währung"
"01.01.2024";"31.12.2024";"123";"0";"EUR"
"Weitere gewählte Suchoptionen:";"keine"


"Buchungstag";"Wertstellungstag";"Verwendungszweck";"Umsatz";"Währung"
"06.08.2024";"06.08.2024";"Verwendungszweck";"-1,00";"EUR";""
"10.08.2024";"10.08.2024";"Verwendungszweck";"1,00";"EUR";""
"1.07.2024";"2.07.2024";"Verwendungszweck";"1,00";"EUR";""
etc...

"* noch nicht ausgeführte Umsätze"
```


