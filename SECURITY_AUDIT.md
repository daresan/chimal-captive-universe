# Security Audit

Stand: 22. Juli 2026

Prüfziel: Geheimnisse, lokale Informationen und unmittelbar erkennbare Sicherheitsrisiken im öffentlichen Repository **Chimal – Captive Universe**.

## Ergebnisübersicht

| Bereich | Ergebnis |
|---|---|
| API-Schlüssel, PATs, Passwörter und private Schlüssel | Keine Treffer im aktuellen Stand oder in der erreichbaren Git-Historie |
| Absolute lokale Benutzerpfade | Keine Treffer in versionierten Dateien oder erreichbarer Historie |
| Verwendete Geheimnis-Umgebungsvariablen | Keine Treffer |
| Externe Laufzeitabhängigkeiten oder Netzwerkanfragen | Keine; das Spiel lädt seine Laufzeitdateien lokal |
| PNG-Metadaten | Generische XMP-/TIFF-Daten in älteren Quelldateien, aber keine gefundenen Namen, E-Mail-Adressen oder lokalen Pfade |
| Git-Metadaten | Name und E-Mail-Adresse des Commit-Autors sind öffentlich; das ist kein Secret, aber eine bewusste Datenschutzentscheidung |
| Level-JSON/DOM | Ursprünglich Script-Injection möglich; in diesem Commit behoben |

Ein Musterscan kann nur bekannte oder strukturell erkennbare Geheimnisse ausschließen. Er ist kein mathematischer Beweis dafür, dass beliebiger Inhalt niemals sensibel sein kann. Deshalb werden Musterprüfung, manuelle Quellcodeprüfung und Metadatenprüfung kombiniert.

## Reproduzierbare Prüfungen

Die Befehle werden im Repository-Stamm in PowerShell ausgeführt. Falls `git` nicht im `PATH` liegt, ist `git` durch den absoluten Pfad zur lokalen Git-Installation zu ersetzen; dieser Installationspfad gehört nicht ins Repository.

### 1. Versionierte Dateien und Arbeitsbaum

```powershell
git status -sb
git ls-files
Get-Content .gitignore
```

Erwartung: `main` folgt `origin/main`, der Arbeitsbaum ist sauber und nur die von `git ls-files` ausgegebenen Dateien werden veröffentlicht.

### 2. Bekannte Secret-Formate

```powershell
git grep -n -I -E '(AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----|xox[baprs]-[A-Za-z0-9-]+|Authorization:[[:space:]]*(Basic|Bearer)|client_secret|access_token|refresh_token|password[[:space:]]*[:=])' HEAD -- . ':(exclude)SECURITY_AUDIT.md'
```

Erwartung: keine Ausgabe. Der Prozesscode `1` von `git grep` bedeutet in diesem Fall „keine Treffer“ und nicht „Audit fehlgeschlagen“.

### 3. Lokale Pfade und Umgebungsvariablen

```powershell
git grep -n -I -E '([A-Za-z]:\\Users\\|C:/Users/|/Users/|/home/|AppData|LOCALAPPDATA|CODEX_HOME|MAYA_GIT_PAT|CODEX_GITHUB_TOKEN|GITHUB_TOKEN|process\.env|os\.environ|getenv\(|EnvironmentVariable)' HEAD -- . ':(exclude)SECURITY_AUDIT.md'
```

Erwartung: keine Ausgabe.

### 4. Gesamte erreichbare Git-Historie

```powershell
$pattern = 'AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|PRIVATE KEY|access_token|MAYA_GIT_PAT|CODEX_GITHUB_TOKEN|[A-Za-z]:\\Users\\|C:/Users/|/Users/|/home/'
foreach ($commit in (git rev-list --all)) {
    git grep -n -I -E $pattern $commit -- . ':(exclude)SECURITY_AUDIT.md'
}
```

Erwartung: keine Ausgabe. Dies prüft alle von Branches und Tags erreichbaren Commits, nicht nur `HEAD`.

### 5. Öffentliche Commit-Identität

```powershell
git log --all --format='%h %an <%ae>'
```

Diese Ausgabe belegt, welche Autorenidentität bereits Teil der öffentlichen Historie ist. Wer keine private Adresse veröffentlichen möchte, sollte für zukünftige Commits eine GitHub-Noreply-Adresse konfigurieren. Bereits veröffentlichte Metadaten lassen sich nur durch eine bewusst koordinierte Umschreibung der Historie ändern.

### 6. PNG-Metadaten

```powershell
python -c "from pathlib import Path; from PIL import Image; [(print(p, Image.open(p).info)) for p in Path('.').rglob('*.png') if Image.open(p).info]"
```

Die Ausgabe darf technische Farb-, XMP- oder TIFF-Daten enthalten. Sie ist auf Namen, E-Mail-Adressen, GPS-Daten und absolute Pfade zu prüfen. Im Audit wurden keine solchen persönlichen Felder gefunden.

### 7. Potenziell gefährliche Browser-APIs

```powershell
git grep -n -I -E 'innerHTML|outerHTML|insertAdjacentHTML|eval\(|new Function|document\.write|https?://|WebSocket|sendBeacon|document\.cookie' HEAD
```

Erwartete verbleibende Treffer:

- Statische, nicht importabhängige `innerHTML`-Verwendung für fest definierte Paletten und den Game-over-Text.
- Lokale `http://localhost`-Adressen in der README.

Importierte Objekttypen, Sprite-Namen und Spritewerte dürfen nicht mehr in `innerHTML` interpoliert werden.

## Behobene Schwachstelle: manipulierter Levelimport

Vor der Härtung prüfte der Import nur, ob `terrain` und `spawns` Arrays waren. Werte wie Objekttypen und Spritefelder gelangten danach in HTML-Templates. Eine absichtlich manipulierte JSON-Datei konnte dadurch Markup beziehungsweise Script-Handler einschleusen.

Die Schutzmaßnahmen sind jetzt:

- Normalisierung jedes Imports und gespeicherter LocalStorage-Level
- Allowlist für Terrain-, Spawn-, Hintergrund- und Sprite-Typen
- Allowlist für Bildschirm-Themes und Übergangstypen
- Begrenzte, endliche Zahlenwerte und definierte Maximalgrößen
- Mengenbegrenzungen gegen triviale Speicher-/Render-Denial-of-Service-Dateien
- Spritepfade ausschließlich relativ unter `assets/`, ohne `..`, nur als `.png`
- Verwerfen unbekannter Felder und Neuaufbau eines kanonischen Levelobjekts
- UI-Erzeugung mit `createElement`, `textContent`, `value` und `replaceChildren`
- Öffnen der Spielvorschau mit `noopener`
- Spielername und Auflösungswahl werden mit DOM-APIs aufgebaut; der Name gelangt ausschließlich über `textContent` in die Oberfläche.

## Restrisiken

- Der Prototyp besitzt keine serverseitige Vertrauensgrenze, Benutzerkonten oder geheimen Daten. LocalStorage ist grundsätzlich durch jedes Script desselben Origins erreichbar.
- Die verbliebenen statischen `innerHTML`-Stellen sind aktuell nicht von Importdaten abhängig. Bei künftigen Änderungen darf dort keine nicht vertrauenswürdige Eingabe eingesetzt werden.
- Ohne automatischen spezialisierten Secret-Scanner können neue, unbekannte Tokenformate übersehen werden. Für spätere CI empfiehlt sich beispielsweise Gitleaks oder GitHubs Secret Scanning.
- Die öffentliche Commit-Autorenadresse bleibt eine bewusste Datenschutzentscheidung.

## Audit-Status

Nach Umsetzung der Importhärtung: **keine bekannten Secrets; zuvor identifiziertes lokales JSON-/DOM-Injection-Risiko behoben; verbleibende Hinweise niedrig beziehungsweise organisatorisch.**
