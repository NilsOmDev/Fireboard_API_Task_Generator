# Fireboard API Task Generator
Das Programm dient als Simulationssoftware für den Alarmeingang der Fireboard Schnittstelle.
Aufträge / Einsätze werden automatisiert anhand einer Bibliothek erzeugt und an die API übergeben.
Als Simulation können so die Empfänger in der Fireboard Schnittstelle den Auftrag entgegennehmen und bearbeiten.
Der Benutzer dieser Anwendung kann, währrenddessen die Einsätze mit dokumentieren und mit weiteren Informationen sowie alarmierten Fahrzeugen hinterlegen.
Die Anwendung dient so im Bereich der Simulation und dem Training von Großschadenslagen mit dem ELW1 / ELW2 in einem Kontext von Hilfsorganisationen.

# benötigte Python Pakete:
- Tkinter   'pip install tk'
- Geopy     'pip install geopy'

# Erste Schritte:
- Stelle sicher, dass Python in der Version 3 installiert ist und alle Bibliotheken verfügbar sind
- Streets_Pool.xlsx mit Adressen (Straße & Ort) füllen
- Streets_Pool.csv erzeugen durch Streets_Pool.xlsx
- Task_Pools.xlsx mit Stichwörtern und Einsätzen füllen
- Task_Pool.csv erzeugen durch Task_Pool.xlsx
- Auth-Key in Umgebungsvariablen hinterlegen (möglich über GUI Button)
- Aktiviere Schnittstelle zu Fireboard durch Entfernen des Kommentars in Zeile 35 in Menu.py

# Task_Pool.csv Konfiguration:
Einsätze / Aufträge werden aus der Task_Pool.csv zufällig ausgewählt. Dabei können dort alle Möglichkeiten Arten und Varianten hinterlegt werden. 
Nach der letzten Spalte "Level" lässt sich die Häufigkeit der Vorkommnisse beeinflussen. 
Je höher das Level, umso wahrscheinlicher die Generierung des Auftrags. Am besten funktioniert eine Zahl zwischen 0 - 20.

# Menü - Bedienung:
Das Programm wird über "python Main.py" in einer Eingabeaufforderung / CMD gestartet.
Es öffnet sich danach eine GUI welche die nötigen Informationen darstellt. 
Unten befindet sich eine Menu-Zeile über den das Programm gesteuert werden kann.


# Known-Issues:
- Die Tabelle lässt sich aktuell noch nicht scrollen


