# Default-Prompt für OpenAI Codex

Der folgende Text kann zu Beginn einer neuen Codex-Aufgabe für dieses Repository verwendet werden:

```text
Du arbeitest am öffentlichen Repository „Chimal – Captive Universe“.

Halte dich bei jeder Aufgabe an diesen Workflow:

1. Lies zuerst README.md, PROMPTS.md, SECURITY_AUDIT.md und alle vorhandenen Repository-Anweisungen. Prüfe danach mit `git status -sb`, auf welchem Branch du bist und ob fremde oder nicht abgeschlossene Änderungen vorhanden sind. Verändere oder überschreibe keine fremden Änderungen.

2. Verwende für Änderungen einen thematisch benannten Feature- oder Fix-Branch. Arbeite nicht direkt auf `main`, außer ich fordere das ausdrücklich. Stage nur Dateien, die zur aktuellen Aufgabe gehören.

3. Setze den Prompt vollständig um und prüfe die Änderung angemessen. Führe mindestens Syntax-/Formatprüfungen, `git diff --check` und die für die Änderung relevanten Laufzeit- oder Browsertests aus. Bei sicherheitsrelevanten Änderungen dokumentiere auch einen reproduzierbaren Negativtest.

4. Aktualisiere nach jedem meiner Projekt-Prompts PROMPTS.md. Erfasse dort den maßgeblichen Prompt redaktionell lesbar sowie eine knappe, sachliche Zusammenfassung des tatsächlich erreichten Ergebnisses. Erfinde keine Resultate und kennzeichne offene Punkte. Übernimm niemals Secrets, Tokens, Passwörter, private lokale Pfade oder andere sensible Daten in die Dokumentation; ersetze solche Inhalte durch `[REDACTED]`.

5. Aktualisiere außerdem alle durch die Änderung betroffenen Dokumente, insbesondere README.md und SECURITY_AUDIT.md. Dokumentation und Code sollen im selben thematischen Commit enthalten sein, sofern keine sachliche Trennung erforderlich ist.

6. Prüfe vor jedem Commit den vollständigen vorgesehenen Diff und suche nach Secrets, lokalen Benutzerpfaden und unerwünschten generierten Dateien. Erstelle anschließend einen kleinen, verständlich benannten Commit nach dem Muster `feat: ...`, `fix: ...`, `docs: ...`, `security: ...` oder `chore: ...`.

7. Führe den Branch erst nach erfolgreichen Prüfungen und meiner Freigabe per Fast-forward oder geprüftem Merge nach `main` zusammen. Pushes, Pull Requests, Releases und andere externe Schreibaktionen erfolgen nur, wenn ich sie ausdrücklich beauftragt oder im aktuellen Auftrag eindeutig freigegeben habe. Verifiziere nach einem Push, dass lokaler und entfernter Branch denselben Commit referenzieren.

8. Berichte abschließend Branch, Commit, geänderte Bereiche, ausgeführte Prüfungen, verbleibende Risiken und den Synchronisationsstatus zu GitHub.

Behandle diese Regeln als Ergänzung zu den jeweils aktuellen System-, Sicherheits- und Repository-Anweisungen. Höher priorisierte Anweisungen gehen vor.
```
