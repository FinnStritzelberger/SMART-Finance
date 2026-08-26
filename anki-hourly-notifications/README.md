# Anki Stunden-Erinnerung (iPhone)

Stündliche Erinnerung ab 07:00 Uhr, die dich so lange nervt, bis du deine Anki-Karten für den Tag gemacht hast — komplett auf dem iPhone, ohne dass ein PC laufen muss.

## Warum "Self-Report" statt automatischer Anki-Abfrage?

Kurz und ehrlich: Eine **wirklich automatische** Abfrage "hat der Nutzer noch fällige Karten?" direkt vom iPhone aus ist aktuell technisch nicht zuverlässig möglich:

- **AnkiMobile** (die iPhone-App) hat keine öffentliche Schnittstelle, die Kurzbefehle (Shortcuts) auslesen könnten.
- **AnkiConnect** (die offizielle Schnittstelle für sowas) läuft nur mit **Anki Desktop** — dafür müsste dein Windows-Rechner ständig an sein. Das wolltest du laut deiner Antwort explizit vermeiden.
- **AnkiWeb** (wo eure Geräte synchronisieren) wurde vor einiger Zeit komplett auf eine JavaScript-Web-App umgestellt. Kurzbefehle können aber kein JavaScript ausführen — ein simpler Seitenabruf liefert nur eine leere Hülle ohne die Kartenzahlen. Ein Scraping-Login wäre nur mit internen, undokumentierten Endpunkten möglich, die ich aus dieser Umgebung heraus nicht live testen kann (kein Internetzugriff auf ankiweb.net von hier aus) — das wäre also Rätselraten und würde dir vermutlich nach ein paar Wochen kommentarlos kaputtgehen.

Deshalb baue ich dir die **zuverlässige Variante**: Du bestätigst per Ein-Klick-Kurzbefehl, wenn du fertig bist, und die stündlichen Erinnerungen stoppen automatisch für den Rest des Tages. Am nächsten Morgen um 07:00 starten sie wieder von selbst. Kein Server, keine Logins, kein PC nötig — läuft 100% lokal auf deinem iPhone.

Unten (Abschnitt "Bonus") gibt es zusätzlich ein optionales Script für **echte** Anki-Anbindung über AnkiConnect, falls dein Windows-Rechner oft läuft — das kannst du später ergänzen, ist aber nicht nötig.

## Wie es funktioniert

Drei Kurzbefehle + mehrere Automationen:

1. **"Anki Einrichten"** – einmalig ausführen, legt die Status-Datei an.
2. **"Anki Erinnerung"** – läuft automatisch jede Stunde (07:00–22:00), prüft ob du heute schon fertig gemeldet hast, und schickt sonst eine Push-Benachrichtigung.
3. **"Anki Fertig"** – tippst du an, sobald du deine Karten gemacht hast. Stoppt die restlichen Erinnerungen für heute.

Der Status wird in einer kleinen Textdatei in deiner iCloud Drive gespeichert (`Shortcuts/AnkiStatus.txt`), die einfach das Datum des letzten "fertig" enthält.

## Einrichtung Schritt für Schritt

### 1. Kurzbefehl "Anki Einrichten" (einmalig)

App **Kurzbefehle** → **+** neuer Kurzbefehl → Name: `Anki Einrichten`

Aktionen:
1. **Text** → Inhalt: `1900-01-01`
2. **Datei sichern** ("Save File") → Speichern in: **iCloud Drive** → Ordner `Shortcuts` → Dateiname: `AnkiStatus.txt` → **Überschreiben: Ein**

Einmal ausführen (Play-Button) und wieder löschen kannst du ihn danach — er wird nicht mehr gebraucht.

### 2. Kurzbefehl "Anki Fertig"

Neuer Kurzbefehl, Name: `Anki Fertig`

Aktionen:
1. **Aktuelles Datum** ("Current Date")
2. **Datum formatieren** ("Format Date") → Format: **Benutzerdefiniert** → `yyyy-MM-dd` → Ergebnis in Variable `Heute` speichern (Variable festlegen)
3. **Datei sichern** → Speichern: Variable `Heute` → iCloud Drive → Ordner `Shortcuts` → Dateiname `AnkiStatus.txt` → **Überschreiben: Ein**
4. **Benachrichtigung anzeigen** ("Show Notification") → Titel: `Anki ✅` → Text: `Für heute erledigt – keine weiteren Erinnerungen mehr!`

**Auf den Home-Bildschirm legen:** Im Kurzbefehl-Editor auf das Symbol oben → **Teilen** → **Zum Home-Bildschirm hinzufügen**. So hast du einen Button, den du direkt nach dem Anki-Lernen antippst. Optional zusätzlich unter **Einstellungen → Siri → Diesem Kurzbefehl eine Phrase geben** z.B. "Anki fertig" hinzufügen, dann geht's auch per Sprachbefehl.

### 3. Kurzbefehl "Anki Erinnerung"

Neuer Kurzbefehl, Name: `Anki Erinnerung`

Aktionen:
1. **Aktuelles Datum** → **Datum formatieren** → `yyyy-MM-dd` → Variable `Heute`
2. **Datei abrufen** ("Get File") → iCloud Drive → Ordner `Shortcuts` → Dateiname `AnkiStatus.txt` → Option **"Fehler nicht anzeigen"** aktivieren → Ergebnis als Text interpretieren → Variable `Status`
3. **Wenn** ("If") → `Status` **ist nicht gleich** `Heute`:
   - **Benachrichtigung anzeigen** → Titel: `📚 Anki Karten fällig` → Text: `Du hast deine Karten heute noch nicht gemacht. Tippe "Anki Fertig", sobald du durch bist.`
4. **Ende der Bedingung**

### 4. Automationen für die stündliche Auslösung

Kurzbefehle-App → Tab **Automation** → **+** → **Erstelle persönliche Automation** → **Uhrzeit**.

Lege **eine Automation pro Stunde** an (07:00, 08:00, 09:00 … 22:00 — also 16 Automationen), jeweils:
- Uhrzeit: z.B. 07:00, **Täglich** wiederholen
- Aktion: **Kurzbefehl ausführen** → `Anki Erinnerung`
- Ganz wichtig: **"Vor dem Ausführen fragen" AUSSCHALTEN** (sonst musst du jedes Mal bestätigen und es kommt kein stiller Push)

Das mehrfache Anlegen ist etwas Tipparbeit, aber einmalig erledigt läuft es danach von selbst weiter — iOS unterstützt bei zeitbasierten Automationen leider kein natives "alle 1 Stunde wiederholen", nur feste Uhrzeiten.

Passe den Zeitraum (07:00–22:00) gerne an deinen Tagesrhythmus an — einfach mehr/weniger Automationen anlegen oder die Uhrzeiten ändern.

### Fertig!

Ab jetzt bekommst du ab 07:00 stündlich eine Push-Benachrichtigung, bis du "Anki Fertig" antippst. Am nächsten Tag beginnt es automatisch wieder, weil das gespeicherte Datum dann nicht mehr "heute" ist.

## Bonus (optional): Echte Anki-Anbindung über AnkiConnect

Falls dein Windows-Rechner oft läuft und Anki Desktop offen ist, kannst du zusätzlich `ankiconnect_notify.py` nutzen — das fragt **wirklich** die Anzahl fälliger Karten über die offizielle [AnkiConnect](https://foosoft.net/projects/anki-connect/)-Schnittstelle ab (statt dich manuell fertig melden zu lassen) und schickt dir bei fälligen Karten eine Push-Benachrichtigung über den kostenlosen Dienst [ntfy.sh](https://ntfy.sh) direkt auf dein iPhone.

Voraussetzungen:
1. In Anki Desktop: **Werkzeuge → Add-ons → Add-on holen** → Code `2055492159` (AnkiConnect) installieren, Anki neu starten.
2. Auf dem iPhone die kostenlose **ntfy** App aus dem App Store installieren, ein Thema (Topic) abonnieren, z.B. `dein-name-anki-erinnerung-8271` (wähle etwas Einzigartiges, Themen sind sonst öffentlich).
3. Auf dem Windows-Rechner Python installieren, dann:
   ```
   pip install -r requirements.txt
   python ankiconnect_notify.py --topic dein-name-anki-erinnerung-8271
   ```
4. Über die **Windows-Aufgabenplanung** stündlich zwischen 07:00–22:00 ausführen lassen (Trigger: "Täglich", wiederholen alle 1 Stunde für 15 Stunden).

Dieses Script ist rein optional und ergänzt die Kurzbefehl-Lösung — sie funktioniert auch komplett ohne PC.
