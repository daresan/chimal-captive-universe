# Projekt-Prompts und Entwicklungsverlauf

Dieses Dokument hält die maßgeblichen Vorgaben fest, anhand derer **Chimal – Captive Universe** gemeinsam entwickelt wurde. Die Texte wurden aus dem deutschsprachigen Arbeitsdialog übernommen und lediglich hinsichtlich Absätzen, offensichtlicher Tippfehler und Wiederholungen redaktionell geglättet. Kurze Bestätigungen und rein organisatorische Nachrichten wurden ausgelassen.

## Rollen

- **Daresan:** Idee, kreative Leitung, Produktanforderungen und Abnahme
- **OpenAI Codex:** Implementierung, technische Ausarbeitung, Dokumentation, Tests und KI-gestützte Erstellung beziehungsweise Aufbereitung der Bildassets

## 1. Spielprototyp und Hauptfigur

> Im Projektordner liegt der Prototyp für ein 2D-Jump’n’Run-Browsergame im Stil von Wonder Boy, aber mit dem Thema „Maya“. Die Spielfigur ist ein kleiner Maya-Junge. Das Spritesheet soll komplett neu erstellt beziehungsweise verbessert werden: sechs Frames mit jeweils 48 × 64 Pixeln pro Reihe, transparenter Hintergrund und ein durchgehend einheitlicher Look.
>
> Benötigte Reihen: IDLE, WALK, RUN, JUMP, ATTACK/USE, THROW, DUCK, BLOCK/SHIELD, ATTACK/USE WHILE WALKING, ATTACK/USE WHILE RUNNING, THROW WHILE WALKING, GETTING HIT/LOSE LIFE, POWERUP und DEATH/GAMEOVER.
>
> Der Prototyp soll das neue Spritesheet und alle Events mit Tastatur- und Xbox-Gamepad-Steuerung verwenden. Das Level soll einen Maya-Hintergrund mit mehreren Parallax-Z-Ebenen erhalten und von Homevillage über Dschungel, Mountainroad und Mountain bis zum MountainTop mit dem Boss Cursed Vulture führen.
>
> Gegner: Schlangen, Fledermäuse, Cougars und Evil Priests mit jeweils eigenem Verhalten. Normale Gegner besitzen einen Trefferpunkt, Evil Priests zwei und der Cursed Vulture drei. Der Spieler beginnt mit drei Trefferpunkten und drei Continues. Versteckte Schatztruhen liefern Heilung oder Power-ups für Angriff, Wurf und Block. Außerdem soll ein lokales Git-Repository samt README entstehen.

## 2. Level-Editor und Gegner-Sprites

> Als nächsten Schritt wird ein Level-Editor benötigt, mit dem fertige Levels gespeichert und anschließend im Spiel geladen werden können. Spielelemente sollen ausgewählt und per Mausklick in einem Raster platziert werden. Gegner-Spawnpunkte liegen auf einer getrennten Ebene, sodass ein Rasterfeld gleichzeitig ein Levelelement und einen Spawnpunkt enthalten kann.
>
> Die Gegner benötigen eigene Spritesheets anstelle generischer Blockgrafiken. Im Editor sollen außerdem Gegner- und Spielercharaktere sowie Einstellungen ihrer Spritesheets konfigurierbar sein.

## 3. Gegnerphysik, Boss-Arena und Theme-Paletten

> Gegner dürfen nicht durch Levelelemente gehen. Nicht fliegende Gegner sollen an Abgründen sterben und erst spawnen, wenn ihr Spawnpunkt im sichtbaren Fenster liegt. Der Cursed Vulture benötigt wegen Richtungsflackerns eine eigene IDLE_FLOAT-Sequenz. Spritegrößen sollen über alle Aktionen hinweg normalisiert werden.
>
> Ein Level darf Elemente aus mehreren Themes enthalten. Themes wie Village, Dschungel, Mountain und Tempel sollen links wählbar sein und darunter ihre Elemente anzeigen. Solange die linke Maustaste gehalten wird, wird das Element entlang des Rasters gemalt, jedoch pro Aktion nicht mehrfach auf dasselbe Feld.
>
> Übereinanderliegende Boden- und Steinreihen sollen visuell verschmelzen. Die Levellänge beginnt bei einer Bildschirmbreite und kann jeweils um eine weitere Bildschirmbreite vergrößert werden. Für den Cursed Vulture soll eine begrenzte Boss-Arena markiert werden; nur darin können Boss und Spieler einander angreifen.

## 4. Vertikale Levels, Minimap und Hintergrundeditor

> Die Cougar-Animation muss vollständig überarbeitet werden, weil sie unruhig wirkt und flackert. Figuren sollen nicht bereits an einer Stufe sterben: Sie dürfen auf einen tiefer gelegenen Boden fallen und sterben erst, wenn sie ohne Landung das untere Levelende erreichen.
>
> Levels müssen nach oben und unten um exakt eine Bildschirmhöhe vergrößerbar sein. Breite und Höhe sollen auch jeweils wieder um eine Bildschirmbreite beziehungsweise -höhe reduziert werden können. Gewünscht ist eine Übersichtsmap mit Navigator zum Verschieben des sichtbaren Bereichs.
>
> Auch im Spiel müssen Bodenreihen visuell verschmelzen. Spieler und Gegner dürfen massive Elemente wie Hütten nicht durchqueren. Figuren sollen über die Darstellung leicht vergrößert werden.
>
> Der Editor soll mehrere Hintergrundebenen und einen erweiterbaren Katalog schöner, freigestellter Maya-Landschaftssprites erhalten. Für die Horizontebene sollen Außen- oder Innenbereich, Tag oder Nacht sowie klares, wolkiges, regnerisches oder verschneites Wetter einstellbar sein. Innenräume verwenden einen dunklen Höhlenhintergrund. Hinzu kommen leuchtende Kristalle, ein Dungeon-Theme und passende Vorlagen pro Bildschirmausschnitt.

## 5. Bewegungsgefühl und Wurfphysik

> Der Spieler springt nicht hoch und weit genug und der Unterschied zwischen Gehen und Laufen ist zu gering. Beim Laufen soll er höher und weiter springen. Das geworfene Objekt soll mehr wie bei Super Mario wirken und einen etwas kürzeren Wurfbogen erhalten.

## 6. Veröffentlichung und Name

> Die erste Version ist würdig, auf GitHub veröffentlicht zu werden. Das Spiel wird in **„Chimal – Captive Universe“** umbenannt und im öffentlichen Repository `daresan/chimal-captive-universe` veröffentlicht.

## Hinweis zur Reproduzierbarkeit

Die Prompts beschreiben Ziele und Entscheidungen, sind aber kein deterministisches Build-Rezept. Der konkrete Stand ergibt sich aus Quellcode, Assets, Werkzeugskripten und Git-Historie dieses Repositories. Generative Bildausgaben können bei erneuter Erzeugung variieren; die verwendeten und normalisierten Ergebnisse sind deshalb im Repository enthalten.

## 7. Credits und öffentliche Prompt-Dokumentation

> Im README sollen Credits für die Arbeit von OpenAI Codex anhand der Prompts ergänzt werden. Die Prompts sollen in einer eigenen Datei in das Repository aufgenommen werden, damit die Entstehung öffentlich nachvollziehbar ist.

**Ergebnis:** README-Credits und dieses redaktionell geglättete Promptprotokoll wurden ergänzt und veröffentlicht. Idee, kreative Leitung und Anforderungen werden Daresan zugeordnet; Implementierung, technische Ausarbeitung, Dokumentation und KI-gestützte Asset-Aufbereitung werden OpenAI Codex zugeordnet.

## 8. Sicherheitsprüfung

> Das Repository soll darauf untersucht werden, dass es keine Secrets, lokalen Pfade, Umgebungsvariablen oder sonstige sicherheitsbedenkliche Inhalte enthält.

**Ergebnis:** Arbeitsbaum und erreichbare Git-Historie wurden nach typischen Secret- und Pfadmustern durchsucht. Es wurden keine Zugangsdaten oder lokalen Benutzerpfade gefunden. Als relevante Schwachstelle wurde die Verarbeitung nicht vertrauenswürdiger Level-JSON-Werte über `innerHTML` erkannt; außerdem wurden die öffentliche Git-Autorenadresse und harmlose XMP-Metadaten als Datenschutz-/Hygienehinweise dokumentiert.

## 9. Nachweisbarer Audit und Import-Härtung

> Die Behauptungen des Security Audits sollen überprüfbar belegt werden. Anschließend soll die JSON-Import-/DOM-Verarbeitung abgesichert, die Repository-Dokumentation einschließlich Audit und Promptliste in einem neuen Commit aktualisiert und ein Default-Prompt für den etablierten Git- und Dokumentationsworkflow erstellt werden.

**Ergebnis:** Die reproduzierbaren Prüfkommandos und ihre Bewertung stehen in `SECURITY_AUDIT.md`. Der Editor normalisiert importierte und gespeicherte Leveldaten anhand von Allowlists, Grenzen und sicheren lokalen Assetpfaden. Importabhängige Oberflächen werden ohne HTML-Interpolation erzeugt. `DEFAULT_CODEX_PROMPT.md` hält den künftigen Workflow fest.
