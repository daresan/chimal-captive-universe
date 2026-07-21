# Maya Boy – Curse of the Vulture

Ein lokaler 2D-Plattformer-Prototyp im Geist klassischer Side-Scroller, mit einem eigenständigen Maya-Abenteurer, Canvas-Rendering, Parallax-Landschaft sowie Keyboard- und Xbox-Gamepad-Steuerung.

## Start

Da Browser lokale Bilddateien je nach Sicherheitseinstellung blockieren können, das Projekt über einen kleinen Webserver öffnen:

```powershell
python -m http.server 8080
```

Danach `http://localhost:8080` öffnen. Alternativ funktioniert in vielen Browsern auch ein Doppelklick auf `index.html`.

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
- `assets/` – Runtime-Sheet und Generierungsquelle
- `tools/build_sprite.py` – deterministische Sheet-Normalisierung (Pillow)
- `static_maya_game_v1.html`, `static_maya_game_v2.html` – historische Prototypen

## Git-Workflow

Änderungen in einem Feature-Branch entwickeln, lokal testen, kleine thematische Commits erstellen und erst nach Review in `main` integrieren. Generierte Betriebssystemdateien und lokale Serverartefakte bleiben über `.gitignore` unversioniert.

## Asset-Hinweis

Die neue Figur wurde mit dem eingebauten OpenAI-Imagegen-Workflow auf einfarbigem Hintergrund erzeugt und lokal zu einem transparenten Pixel-Sheet verarbeitet. Der Charakter ist eine eigenständige Maya-inspirierte Gestaltung und kopiert keine geschützte Spielfigur.
