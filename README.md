# Chimal – Captive Universe

Das Spielthema ist eine Hommage an den Roman *Captive Universe* (*Welt im Fels*) von Harry Harrison.

Der Spieler schlüpft in die Rolle von Chimal, dem Sohn von Quiauh, der sich gegen die bösen Priester der Göttin Coatlicue behaupten muss und erst am Beginn seiner heldenhaften Entdeckungen steht. Welche düsteren Geheimnisse verbergen die Priester des Kults? Was will die Göttin wirklich von den Menschen?

Ein lokaler 2D-Plattformer-Prototyp im Geist klassischer Side-Scroller, mit einem eigenständigen Maya-Abenteurer, Canvas-Rendering, Parallax-Landschaft sowie Keyboard- und Xbox-Gamepad-Steuerung.

## Start

Da Browser lokale Bilddateien je nach Sicherheitseinstellung blockieren können, das Projekt über einen kleinen Webserver öffnen:

```powershell
python -m http.server 8080
```

Danach `http://localhost:8080` öffnen. Alternativ funktioniert in vielen Browsern auch ein Doppelklick auf `index.html`.

Der Level-Editor ist unter `http://localhost:8080/level-editor.html` erreichbar.

Vor dem Spielstart erscheint ein Startdialog für Spielername und Ausgabeformat. Unterstützt werden automatische Fensteranpassung sowie 960×540, 1280×720, 1600×900 und 1920×1080. Die Spiellogik bleibt auf einer stabilen internen 1280×720-Arbeitsfläche; Canvas, Sprites und Hintergründe werden gemeinsam auf die verfügbare beziehungsweise gewählte Darstellungsgröße skaliert.

## Level-Editor

- Levelelemente und Spawnpunkte besitzen getrennte Ebenen und dürfen auf demselben Rasterfeld liegen.
- Themes werden links als Paletten gewählt: Village, Dschungel, Mountain, Tempel, Dungeon und Gameplay können innerhalb desselben Levels beliebig kombiniert werden.
- Linksklick und Ziehen malt das aktive Element fortlaufend ins Raster; jedes Feld wird pro Malvorgang höchstens einmal belegt. Rechtsklick löscht nur auf der aktiven Ebene.
- Vier Bearbeitungsmodi trennen Zeichnen, Auswählen, rasterweises Verschieben und Löschen. Terrain, Spawns und Hintergrundobjekte bleiben getrennt wählbar.
- Im Löschmodus bestimmt das Objekt unter dem ersten Mausklick den Typ des Löschstrichs. Solange die linke Maustaste gehalten wird, werden beim Darüberziehen ausschließlich weitere Objekte desselben Typs und derselben Ebene gelöscht. Der gesamte Strich ist ein einzelner Undo-Schritt.
- Hintergrundobjekte können zusätzlich nach Z-Depth 0–5 gefiltert, umrandet, ausgewählt, verschoben, skaliert oder gelöscht werden.
- **Level leeren** erzeugt einen vollständig leeren Level ohne Terrain, Spawns, Katalogobjekte oder Theme-Zuweisungen; **Neu** erzeugt weiterhin die kleine Startvorlage.
- Eigenschaften wie Position, Breite und Höhe lassen sich numerisch bearbeiten.
- Jedes Theme besitzt einen eigenen Aufzugstyp. Nach dem Setzen werden Richtung (horizontal, vertikal, 30° oder 45° in beide Diagonalrichtungen), Streckenlänge und Geschwindigkeit konfiguriert und bestätigt. Start und Ende dürfen in unterschiedlichen Bildschirmabschnitten liegen.
- Die Fahrstrecke wird im Editor gestrichelt dargestellt: Gelb kennzeichnet eine noch unbestätigte, Grün eine bestätigte Konfiguration.
- Ein Level beginnt bei 1280×720 px. Breite und Höhe lassen sich um exakt eine Bildschirmbreite (1280 px) beziehungsweise Bildschirmhöhe (720 px) vergrößern und wieder reduzieren.
- Die Minimap zeigt das gesamte Level; ein Klick darauf verschiebt den Arbeitsbereich horizontal und vertikal.
- Der Navigator besitzt einen Zoomregler von 35–125 %. Der Editier-Viewport bleibt unabhängig von Levelgröße und Zoom innerhalb des verfügbaren Browserfensters und kann in beide Richtungen scrollen.
- Eine eigene Hintergrundebene bietet einen erweiterbaren Katalog freigestellter Maya-Landschaftsobjekte mit einstellbarer Z-Tiefe und Skalierung.
- Das Level ist in unabhängige Abschnitte von 1280×720 px gegliedert. Jeder Abschnitt besitzt über `screenX` und `screenY` ein eigenes Village-, Jungle-, Mountain-, Temple- oder Dungeon-Theme. Damit können etwa Dorf, ein Dungeon darunter und ein Tempel- oder Wolkenabschnitt darüber im selben Level liegen.
- Direkte und weiche Übergänge funktionieren horizontal und vertikal. Nicht zugewiesene Abschnitte bleiben bewusst leer, statt das Theme eines Nachbarabschnitts über die gesamte Levelhöhe zu wiederholen.
- Jedes Theme verwendet ein bildschirmfüllendes Landschaftsbild; Tag/Nacht und Wetter werden als dynamische Licht- und Atmosphärenebenen darübergelegt.
- Pro Bildschirmausschnitt stehen Village-, Dschungel-, Mountain-, Tempel- und Dungeon-Vorlagen bereit.
- Der Horizont kann als Außenbereich mit Tag/Nacht und Wetter (klar, wolkig, Regen oder Schnee) oder als dunkler Höhlen-Innenraum konfiguriert werden.
- Übereinanderliegende Boden- und Steinreihen verschmelzen visuell; nur die oberste Reihe erhält Gras beziehungsweise eine helle Steinkante.
- Eine `boss_arena` markiert den zulässigen Bewegungs- und Kampfbereich des Cursed Vulture.
- Es dürfen mehrere Boss-Arenen existieren. Jede Arena belegt exakt einen 1280×720-Abschnitt; ein Cursed Vulture wird anhand seines Spawnpunkts seiner Arena zugeordnet.
- Zielsteine besitzen optional eine `Folgelevel-ID`. **Browser speichern** legt das Level zusätzlich unter einer aus dem Levelnamen erzeugten ID ab; alternativ können Folgelevels als `levels/ID.json` bereitgestellt werden.
- Undo/Redo, Browser-Speicher, JSON-Import und JSON-Export sind integriert.
- **Im Spiel testen** übergibt das aktuelle Level an `index.html?editorLevel=1`.
- Spieler- und Gegner-Sprites lassen sich über Pfad, Framegröße, Frameanzahl, Animationsreihe und Skalierung konfigurieren.

Das JSON-Format enthält `terrain`, `spawns` und `sprites` getrennt. Dadurch kann ein Spawnpunkt unabhängig von einem Geländeelement auf derselben Koordinate existieren.

## Gegnerphysik

- Gegner werden erst aktiviert, sobald ihr Spawnpunkt in den sichtbaren Viewport gelangt.
- Jeder Gegner-Spawn besitzt einen im Editor skalierbaren grünen IDLE-Bewegungsbereich und einen orangefarbenen ALERT-Wahrnehmungsbereich.
- In IDLE patrouillieren Gegner innerhalb ihres Bereichs. Erst wenn der Spieler den Wahrnehmungsbereich betritt, wechseln sie in ALERT und verfolgen beziehungsweise attackieren ihn.
- Während ALERT bewegt sich der Wahrnehmungsbereich mit dem Gegner. Ist der Spieler länger außerhalb oder bleibt der Weg länger blockiert, kehrt der Gegner in IDLE zurück.
- Blockierte Gegner behalten in ALERT die Blickrichtung zum Spieler; beim anschließenden Patrouillieren richten sie sich wieder nach ihrer tatsächlichen Bewegungsrichtung aus.
- Spieler und laufende Gegner kollidieren mit Hindernissen. Sie dürfen von Kanten auf tiefer gelegene Plattformen fallen und sterben erst, wenn sie ohne Landung das untere Levelende erreichen; fliegende Gegner sind davon ausgenommen.
- Der Boss behält seine Blickrichtung in der Nähe des Spielers und verwendet im Stillstand die zweite Sprite-Reihe `IDLE_FLOAT`.
- Bossbewegung und gegenseitige Treffer sind auf die im Editor gesetzte Boss-Arena begrenzt.
- Nahkampf und Körperkontakt mit Bossen bleiben an deren Arena gebunden. Spieler- und Gegnerprojektile dürfen Arenagrenzen überqueren.
- HIT und DEATH besitzen sichtbare, zeitlich abgespielte Sequenzen. Gegner verschwinden erst nach ihrer Todesanimation.
- Der Cursed Vulture verwendet für Bewegung ausschließlich die vier zusammenhängenden Flugframes. Die beiden Wurf-/Magieframes derselben Sheet-Reihe werden nicht mehr fälschlich in die Flugschleife gemischt.

## Steuerung

| Aktion | Tastatur | Xbox-Gamepad |
|---|---|---|
| Gehen / Rennen | A/D; nach 0,42 s wird Gehen zu Rennen | Linker Stick bis/über 50 % |
| Ducken | S | Linker Stick nach unten |
| Springen | Leertaste | A |
| Block/Schild | Q | B |
| Angriff/Benutzen | E | X |
| Werfen | Tab | Y |

Gehen und Rennen besitzen bewusst deutlich unterschiedliche Geschwindigkeiten. Ein Sprung aus dem Lauf ist höher und wesentlich weiter als ein Sprung aus dem Stand oder Gehen. Geworfene Feuerkugeln folgen einem kurzen Bogen, bleiben länger aktiv und können bis zu dreimal vom Boden abprallen.

## Levelabschluss und Kampagne

- Das Besiegen eines Bosses beendet das Level nicht unmittelbar. Bei mehreren Cursed Vultures müssen zuerst alle Bosse besiegt werden.
- Erst danach wird der Zielstein aktiv. Beim Betreten ertönt eine kurze Fanfare und das Finish-Fenster zählt den Score sichtbar hoch.
- Pro 1000 in diesem Level verdienten Punkten erhält der Spieler ein zusätzliches Leben beziehungsweise Continue.
- Ist am Zielstein eine Folgelevel-ID eingetragen, lädt **Weiter** das entsprechende Browser-Level oder `levels/ID.json`. Score, Spielername und verbleibende Leben werden übernommen.

## Spielinhalt

- Levelroute: Homevillage → Dschungel → Mountainroad → Mountain → MountainTop.
- Gegner: Schlangen (Aufmerksamkeits-Sprint), Fledermäuse (Sinusflug), Cougars (Ansturm), Evil Priests (Gehen/Rennen und Fernangriff), Cursed Vulture (Boss).
- Lebenspunkte: normale Gegner 1, Priester 2, Boss 3; Spieler 3 HP und 3 Continues.
- Versteckte Truhen heilen oder verbessern Angriff, Wurf und Block.
- Mehrschichtige Parallax-Landschaft mit Z-Tiefen, freigestellten Katalog-Sprites, Wetter und Höhlenbeleuchtung.
- Weltverankerte Parallaxobjekte bleiben an der im Editor gesetzten Bildschirmposition sichtbar und werden je nach Z-Tiefe mit einer näheren, präsenteren Bewegungsrate dargestellt.
- Bewegliche Plattformen tragen Chimal und nicht fliegende Gegner mit, pendeln zwischen Start und Endpunkt und kollidieren wie statische Plattformen.
- Fünf neue Terrain-Familien liefern illustrierte Böden, schmale Plattformen, Aufzüge sowie thematische Idole, Säulen, Altäre, Stege und Hindernisse für Village, Jungle, Mountain, Temple und Dungeon.
- Jede der 15 Terrain-Grafiken besitzt zusätzlich eine kronenlose Füll-/Mittelsegment-Variante. Liegt ein identischer Objekttyp direkt darüber, verwenden Editor und Spiel automatisch dieses Segment; nur die oberste Reihe zeigt Gras, Moos, Dach, Plattformkante oder dekorativen Abschluss.

## Sprite-Sheet-Vertrag

`assets/mempalace_boy_spritesheet.png` ist exakt 288×896 px (RGBA): 6 Frames à 48×64 px und 14 Reihen.

| Reihe | Animation |
|---:|---|
| 0–3 | IDLE, WALK, RUN, JUMP |
| 4–7 | ATTACK/USE, THROW, DUCK, BLOCK/SHIELD |
| 8–10 | ATTACK WALK, ATTACK RUN, THROW WALK |
| 11–13 | HIT/LOSE LIFE, POWERUP, DEATH/GAMEOVER |

Die generierte Chroma-Key-Quelle liegt aus Gründen der Nachvollziehbarkeit unter `assets/maya_boy_chromakey.png`. `tools/build_sprite.py` erzeugt daraus reproduzierbar das exakte Runtime-Raster und entfernt Magenta in den Alpha-Kanal.

## Technik und Struktur

- `index.html` – vollständiges Spiel ohne Build-Schritt oder externe Bibliotheken
- `level-editor.html` – rasterbasierter Level- und Sprite-Konfigurationseditor
- `assets/` – Runtime-Sheet und Generierungsquelle
- `assets/backgrounds/` – fünf bildschirmfüllende Theme-Landschaften
- `assets/terrain/` – zwei transparente 5×3-Terrain-Atlanten und 30 daraus geschnittene Abschluss- beziehungsweise Füllsegmente
- `tools/build_sprite.py` – deterministische Sheet-Normalisierung (Pillow)
- `tools/build_enemy_sprites.py` – erzeugt fünf transparente Gegner-Sheets aus dem generierten Atlas
- `tools/build_catalog_assets.py` – normalisiert das Cougar-Sheet und erzeugt den transparenten Landschaftskatalog
- `static_maya_game_v1.html`, `static_maya_game_v2.html` – historische Prototypen

## Git-Workflow

Änderungen in einem Feature-Branch entwickeln, lokal testen, kleine thematische Commits erstellen und erst nach Review in `main` integrieren. Generierte Betriebssystemdateien und lokale Serverartefakte bleiben über `.gitignore` unversioniert.

## Asset-Hinweis

Die neue Figur wurde mit dem eingebauten OpenAI-Imagegen-Workflow auf einfarbigem Hintergrund erzeugt und lokal zu einem transparenten Pixel-Sheet verarbeitet. Der Charakter ist eine eigenständige Maya-inspirierte Gestaltung und kopiert keine geschützte Spielfigur.

## Credits und Entstehung

**Konzept, kreative Leitung und iterative Anforderungen:** Daresan

**Implementierung, technische Ausarbeitung, Dokumentation und KI-gestützte Asset-Erstellung:** OpenAI Codex, auf Grundlage der Prompts von Daresan

Der Prototyp entstand in einer schrittweisen Mensch–KI-Zusammenarbeit. Daresan definierte Spielidee, Maya-Thema, Figuren, Steuerung, Gegnerverhalten, Levelstruktur sowie die Anforderungen an Sprites und Editor. OpenAI Codex setzte diese Vorgaben im lokalen Projekt um, entwickelte die Canvas-Spielmechanik und den Level-Editor, erzeugte und normalisierte Bildassets, testete die Änderungen und pflegte den Git-Verlauf.

Die maßgeblichen Nutzer-Prompts und die daraus entstandenen Entwicklungsschritte sind zur öffentlichen Nachvollziehbarkeit in [PROMPTS.md](PROMPTS.md) dokumentiert.

## Sicherheit und Entwicklungsprozess

- [SECURITY_AUDIT.md](SECURITY_AUDIT.md) dokumentiert Prüfbereich, reproduzierbare Befehle, Befunde und umgesetzte Schutzmaßnahmen.
- [DEFAULT_CODEX_PROMPT.md](DEFAULT_CODEX_PROMPT.md) enthält den vereinbarten Standard-Prompt für Git-Workflow, Dokumentationspflege und Prompt-/Ergebnisprotokoll.
- Importierte Leveldaten werden gegen bekannte Typen und zulässige Werte normalisiert. Importabhängige UI wird mit sicheren DOM-APIs aufgebaut; Spritequellen müssen lokale PNG-Dateien unter `assets/` sein.
- Folgelevel-IDs erlauben ausschließlich bis zu 60 alphanumerische Zeichen, `_` und `-`. Sie können daher weder externe URLs noch frei gewählte lokale Pfade referenzieren.
