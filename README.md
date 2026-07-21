# Maya Boy – Curse of the Vulture

Ein lokaler 2D-Plattformer-Prototyp im Geist klassischer Side-Scroller, mit einem eigenständigen Maya-Abenteurer, Canvas-Rendering, Parallax-Landschaft sowie Keyboard- und Xbox-Gamepad-Steuerung.

## Start

Da Browser lokale Bilddateien je nach Sicherheitseinstellung blockieren können, das Projekt über einen kleinen Webserver öffnen:

```powershell
python -m http.server 8080
```

Danach `http://localhost:8080` öffnen. Alternativ funktioniert in vielen Browsern auch ein Doppelklick auf `index.html`.

Der Level-Editor ist unter `http://localhost:8080/level-editor.html` erreichbar.

## Level-Editor

- Levelelemente und Spawnpunkte besitzen getrennte Ebenen und dürfen auf demselben Rasterfeld liegen.
- Themes werden links als Paletten gewählt: Village, Dschungel, Mountain, Tempel und Gameplay können innerhalb desselben Levels beliebig kombiniert werden.
- Linksklick und Ziehen malt das aktive Element fortlaufend ins Raster; jedes Feld wird pro Malvorgang höchstens einmal belegt. Rechtsklick löscht nur auf der aktiven Ebene.
- Eigenschaften wie Position, Breite und Höhe lassen sich numerisch bearbeiten.
- Die Levelbreite beginnt bei 1280 px und lässt sich bildschirmweise um jeweils 1280 px verlängern.
- Übereinanderliegende Boden- und Steinreihen verschmelzen visuell; nur die oberste Reihe erhält Gras beziehungsweise eine helle Steinkante.
- Eine `boss_arena` markiert den zulässigen Bewegungs- und Kampfbereich des Cursed Vulture.
- Undo/Redo, Browser-Speicher, JSON-Import und JSON-Export sind integriert.
- **Im Spiel testen** übergibt das aktuelle Level an `index.html?editorLevel=1`.
- Spieler- und Gegner-Sprites lassen sich über Pfad, Framegröße, Frameanzahl, Animationsreihe und Skalierung konfigurieren.

Das JSON-Format enthält `terrain`, `spawns` und `sprites` getrennt. Dadurch kann ein Spawnpunkt unabhängig von einem Geländeelement auf derselben Koordinate existieren.

## Gegnerphysik

- Gegner werden erst aktiviert, sobald ihr Spawnpunkt in den sichtbaren Viewport gelangt.
- Laufende Gegner kollidieren mit Levelgeometrie und sterben beim Verlassen eines begehbaren Bodens; fliegende Gegner sind davon ausgenommen.
- Der Boss behält seine Blickrichtung in der Nähe des Spielers und verwendet im Stillstand die zweite Sprite-Reihe `IDLE_FLOAT`.
- Bossbewegung und gegenseitige Treffer sind auf die im Editor gesetzte Boss-Arena begrenzt.

## Steuerung

| Aktion | Tastatur | Xbox-Gamepad |
|---|---|---|
| Gehen / Rennen | A/D; nach 0,62 s wird Gehen zu Rennen | Linker Stick bis/über 50 % |
| Ducken | S | Linker Stick nach unten |
| Springen | Leertaste | A |
| Block/Schild | Q | B |
| Angriff/Benutzen | E | X |
| Werfen | Tab | Y |

## Spielinhalt

- Levelroute: Homevillage → Dschungel → Mountainroad → Mountain → MountainTop.
- Gegner: Schlangen (Aufmerksamkeits-Sprint), Fledermäuse (Sinusflug), Cougars (Ansturm), Evil Priests (Gehen/Rennen und Fernangriff), Cursed Vulture (Boss).
- Lebenspunkte: normale Gegner 1, Priester 2, Boss 3; Spieler 3 HP und 3 Continues.
- Versteckte Truhen heilen oder verbessern Angriff, Wurf und Block.
- Mehrschichtige, prozedural gezeichnete Parallax-Landschaft mit Z-Tiefen.

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
- `tools/build_sprite.py` – deterministische Sheet-Normalisierung (Pillow)
- `tools/build_enemy_sprites.py` – erzeugt fünf transparente Gegner-Sheets aus dem generierten Atlas
- `static_maya_game_v1.html`, `static_maya_game_v2.html` – historische Prototypen

## Git-Workflow

Änderungen in einem Feature-Branch entwickeln, lokal testen, kleine thematische Commits erstellen und erst nach Review in `main` integrieren. Generierte Betriebssystemdateien und lokale Serverartefakte bleiben über `.gitignore` unversioniert.

## Asset-Hinweis

Die neue Figur wurde mit dem eingebauten OpenAI-Imagegen-Workflow auf einfarbigem Hintergrund erzeugt und lokal zu einem transparenten Pixel-Sheet verarbeitet. Der Charakter ist eine eigenständige Maya-inspirierte Gestaltung und kopiert keine geschützte Spielfigur.
