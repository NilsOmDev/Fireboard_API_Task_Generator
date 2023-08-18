# Fireboard API Task Generator
Das Programm dient als Simulationssoftware für den Alarmeingang der Fireboard Schnittstelle.
Aufträge / Einsätze werden automatisiert anhand einer Bibliothek erzeugt und an die API übergeben.
Als Simulation können so die Empfänger in der Fireboard Schnittstelle den Auftrag entgegennehmen und bearbeiten.
Der Benutzer dieser Anwendung kann, währrenddessen die Einsätze mit dokumentieren und mit weiteren Informationen sowie alarmierten Fahrzeugen hinterlegen.
Die Anwendung dient so im Bereich der Simulation und dem Training von Großschadenslagen mit dem ELW1 / ELW2 in einem Kontext von Hilfsorganisationen.

# Erste Schritte:
- Repository in lokalen Speicher forken
- Streets_Pool.xlsx mit Adressen (Straße & Ort) füllen
- Streets_Pool.csv erzeugen durch Streets_Pool.xlsx
- Task_Pools.xlsx mit Stichwörtern und Einsätzen füllen.
- Task_Pool.csv erzeugen durch Task_Pool.xlsx
- Auth-Key der Fireboard API als Alarmeingang in Main.py eintragen

# Task_Pool.csv Konfiguration:
Einsätze / Aufträge werden aus der Task_Pool.csv zufällig ausgewählt. Dabei können dort alle Möglichkeiten Arten und Varianten hinterlegt werden. 
Nach der letzten Spalte "Level" lässt sich die Häufigkeit der Vorkommnisse beeinflussen. 
Je höher das Level, umso wahrscheinlicher die Generierung des Auftrags. Am besten funktioniert eine Zahl zwischen 0 - 20.

# Menü - Bedienung:
Das Programm wird über "python3 Main.py" in einer Eingabeaufforderung / CMD gestartet. 
Danach wird immer eine Tabelle mit allen aktuellen Einsätzen gezeigt. Jetzt kann der Nutzer mit Befehlen den Ablauf steuern.

Alle Befehle werden über "help" als Befehl angezeigt.
Hier eine Kurzbeschreibung der Befehle:
1. "einsatz":
Erzeugt einen zufälligen Einsatz je nach Gewichtigung aus der Task_Pool.csv in Zusammenhang mit einer zufälligen Adresse aus Streets_Pool.csv.

2. "fzg <zeile> <rufname>"
Hinterlegt ein Fahrzeug mit entsprechenden Rufnamen in der entsprechenden Zeile. Dient der Dokumentation von aktiven Fahrzeugen im Auftrag.

3. "info <zeile> <kommentar>"
Hinterlegt in der entsprechenden Zeile bzw. dem entsprechenden Auftrag ein Kommentar als Freitext.

4. "status <zeile> <fahrzeug-rufname>"
Der Status der Fahrzeuge wechselt in folgender Reihenfolge: 2 -> 3 -> 4 -> 1. Mit dem Befehl status wechselt das Fahrzeug mit entsprechenden Rufnamen in der entsprechenden Zeile genau ein Status weiter.
Sobald alle Fahrzeuge wieder Status 1 haben, wir der Auftrag automatisch vollständig gelöscht.

5. "undo"
Löscht den vorherigen Befehl, sofern dieser "fzg" oder "info" war.

6. "exit"
Beendet das Programm.


