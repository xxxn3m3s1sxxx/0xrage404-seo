# View-Verteilungs-Analyse — 159 Videos (W33)

> Datenbasis: analytics_cache (159 Videos), deployed.json (176 Einträge)
> Stand: 2026-08-15 10:30 MEZ

---

## Zusammenfassung

| Metrik | Wert |
|--------|------|
| Total Videos | 159 (W33: 08-14 Aug) |
| Avg Views | 215 |
| Median Views | 112 |
| Retention Median | 50.3% |

---

## Views-Verteilung

| Segment | Anzahl | Anteil | Bewertung |
|---------|--------|--------|-----------|
| >=500 Views | 18 | 11% | TRAGEN den Kanal |
| 100-499 Views | 63 | 40% | Mittelmässig |
| 50-99 Views | 28 | 18% | Schwach |
| <50 Views | 50 | 31% | TOT — Content-Farm-Signal |

**Kernproblem:** 31% der Produktion (50 Videos) generiert NULL Views und verschlechtert den Algorithmus-Score des gesamten Kanals.

---

## Top 5 nach Retention (>70% = starker Hook)

| Video | Views | Retention | Bewertung |
|-------|-------|-----------|-----------|
| AI Code Deployed to Prod | 1184 | 83.8% | ⭐⭐⭐⭐⭐ |
| Your CI Sabotages You | 1046 | 76.2% | ⭐⭐⭐⭐ |
| Code Ownership Is Stupid | 1529 | 68.4% | ⭐⭐⭐⭐ |
| AI Policy Is Corporate Greed | 1032 | 59.0% | ⭐⭐⭐ |
| Docker Won't Save You | 978 | 56.6% | ⭐⭐⭐ |

---

## Bottom 5 nach Views (<30 Views = tot)

| Video | Views | Retention | Bewertung |
|-------|-------|-----------|-----------|
| AI Security Is An Illusion | 10 | 27.4% | ❌ Schlechter Hook |
| You Overengineer Everything | 10 | 43.5% | ❌ Mittel |
| Your CI Pipeline Is Working Against You | 10 | 150.5%* | ❌ (Datenfehler?) |
| Meaningless Code Comments | 15 | 51.0% | ❌ Mittel |
| Cloudflare Wants Root | 16 | 42.5% | ❌ Mittel |

*Retention >100% = Datenfehler oder YouTube-Messung

---

## Empfehlung (datenbasiert)

### 1. Upload-Frequenz: 1-2/Tag statt 5/Tag
- **Begründung:** 50 tote Videos in einer Woche = Content-Farm-Signal
- **Threshold:** Retention >50% VOR Upload (sonst skip)
- **Kadenz:** Konsistenter als "weniger, aber besser"

### 2. Tote Videos aufräumen
- **50 Videos mit <50 Views:** Auf "unlisted" setzen oder löschen
- **Begründung:** Schlechte Videos verschlechtern den Algorithmus-Score des gesamten Kanals
- **Priorität:** Die 10 schlimmsten (<20 Views, <40% Retention) zuerst

### 3. Community-Engagement vor Volume
- **54 Kommentare:** Keine einzige Antwort = 0% Engagement-Rate
- **Hebel:** Kommentar-Antworten produzieren mehr Algorithmus-Signals als neue Uploads
- **Priorität:** Task 1111 (suckz) > neue Uploads

### 4. Retention als Upload-Gate
- **Aktuell:** Kein Threshold (alles hochgeladen)
- **Vorschlag:** Retention >50% als Minimum, >60% als ideal
- **Umsetzung:** Analytics-Vorab-Check vor Upload-Freigabe

---

## Nächste Schritte

1. **Heute:** suckz startet Kommentar-Antworten (Task 1111)
2. **Morgen:** Tote Videos auf unlisted setzen (50 Videos)
3. **Ab Welle 2:** Retention-Threshold als Upload-Gate
4. **Skap-Report:** Nach 7 Tagen mit neuem Schema vergleichen
