# Retentions-Mess-Framework — Welle 1 Kalibrierung

> Design-Doc für automatisierte KPI-Erhebung nach Uploads.
> Status: ENTWURF. Umsetzung nach Welle 1 +scheduler_jobs-Tabelle.

---

## 1. Metriken (pro Video)

| Metrik | Quelle | Zeitfenster | Bedeutung |
|--------|--------|-------------|-----------|
| **Average View Duration** | YouTube Analytics | 24h, 48h, 7d | Hook-Qualität (erste 3 Sek) |
| **Audience Retention (%)** | YouTube Analytics | 24h, 48h, 7d | Drop-off-Punkte im Video |
| **Click-Through-Rate (CTR)** | YouTube Analytics | 24h, 48h | Titel + Thumbnail-Wirksamkeit |
| **Impressions** | YouTube Analytics | 24h, 48h, 7d | Reichweite des Algorithms |
| **Likes/Dislikes** | YouTube API | 24h, 48h, 7d | Emotionale Resonanz |
| **Kommentare (Anzahl)** | YouTube API | 24h, 48h, 7d | Engagement |
| **Kommentare (Sentiment)** | AI-Analyse (optional) | 7d | Qualitative Resonanz |
| **Subscriber-Gain** | YouTube Analytics | 7d | Langzeitwert |

---

## 2. Zeitfenster-Logik

```
Upload: 09:00 MEZ (Tag 0)
├── Tag 0+24h: Erste Daten (Impressions, CTR,(avg View Duration)
├── Tag 0+48h: Retention-Kurve stabil, Likes/Kommentare sichtbar
├── Tag 0+7d: Vollständiges Bild, Subscriber-Gain, Sentiment
└── Tag 0+14d: Langzeit-Trend (optional)
```

**Empfehlung:** Hauptkalibrierung nach 48h (Tag 2), Feinabstimmung nach 7d (Tag 7).

---

## 3. Dashboard-Spezifikation

### Kacheln (pro Video)

| Kachel | Metrik | Schwellenwert | Farbe |
|--------|--------|---------------|-------|
| Hook-Score | Avg View Duration / Video-Länge | >50% = grün, >30% = gelb, <30% = rot |
| CTR | Click-Through-Rate | >5% = grün, >2% = gelb, <2% = rot |
| Engagement | Likes + Kommentare / Views | >3% = grün, >1% = gelb, <1% = rot |
| Retention | Audience Retention (Durchschnitt) | >40% = grün, >25% = gelb, <25% = rot |

### Aggregat (pro Welle)

| Kachel | Metrik | Schwellenwert |
|--------|--------|---------------|
| Welle-Ø Hook-Score | Durchschnitt aller Videos | >40% = grün |
| Beste/r Video | Höchster Hook-Score | Highlight |
|Schlechteste/r Video | Niedrigster Hook-Score | Warnung |
| Upload-Fenster-Effizienz | Uploads / verbrauchte Quota | >0.5 = grün |

---

## 4. Automatisierung (scheduler_jobs)

### Job: `retention_metrics_collector`

```yaml
name: retention_metrics_collector
schedule: "0 10,18 * * *"  # 10:00 und 18:00 MEZ täglich
payload:
  action: collect_retention_metrics
  sources:
    - youtube_analytics_api
    - youtube_data_api
  metrics:
    - avg_view_duration
    - audience_retention
    - ctr
    - impressions
    - likes
    - comments
  output:
    format: json
    path: research/retention_metrics/{video_id}_{timestamp}.json
    aggregate: research/retention_metrics/welle_{n}_summary.json
```

### Job: `hook_score_calculator`

```yaml
name: hook_score_calculator
schedule: "0 11 * * *"  # 11:00 MEZ täglich (nach Collector)
payload:
  action: calculate_hook_scores
  input: research/retention_metrics/
  output: research/hook_scores/{date}.json
  thresholds:
    green: 0.5
    yellow: 0.3
```

---

## 5. Trigger-Logik

### Für Welle 1 (5 Videos)

```
Tag 0 (heute): Upload 5 Videos → retention_metrics_collector starten
Tag 1+24h: Erste Metriken sammeln → Hook-Score berechnen
Tag 2+48h: Hauptkalibrierung → Checkliste Sektion 4 aktualisieren
Tag 7+7d: Vollständige Auswertung → Welle 2/3 Selektion anpassen
```

### Für Welle 2/3

```
Vor Upload: Hook-Score-Schwellenwert aus Welle 1 als Filter
Nach Upload: Metriken vergleichen → Optimierungen validieren
```

---

## 6. Offene Fragen

1. **YouTube Analytics API:** Brauchen wir OAuth-Credentials oder reicht API-Key?
2. **Rate Limits:** YouTube API hat Quota (10.000 Units/Tag) — passt das für 5 Videos + 2x täglich Collect?
3. **Datenbank-Schema:** Soll die Tabelle `scheduler_jobs` oder `retention_metrics` heißen?
4. **Dashboard:** Lokal (Terminal/HTML) oder integriert in bestehende Infrastruktur?

---

## Nächste Schritte

## Status (nach Welle 1)

### Upload-Status (2026-08-15 07:28)
- **4/5 Videos live:** e_paSjQDsx0, DPZO9-qyyNc, 00Lw55xpbg4, KrVieUhSboU
- **1 BLOCKED:** w34_redis_never_bottleneck_001 (1900 Units vs 1920 benötigt, morgen 09:00)
- **deployed.json:** 172 Einträge (168+4)
- **Quota:** 1900 Units verbleibend (resetted=false)

### Analytics-Status (Tag 0)
- **Cache:** 4 neue Videos NOCH NICHT im Analytics-Cache (normal, Daten erscheinen nach 24-48h)
- **Nächster Check:** Tag 0+24h (2026-08-16 09:00 MEZ) — analytics.py --fetch + --report
- **Metriken ablesbar:** CTR, Impressions, Avg View Duration (ab 24h), Retention Curve (ab 48h)

## Nächste Schritte

1. **Tag 0+24h (16.08. 09:00):** Erste Metriken aus analytics.py sammeln
2. **Tag 0+48h (17.08. 09:00):** Retention-Kurve + Hauptkalibrierung
3. **Tag 0+7d (22.08.):** Vollständige Auswertung → Welle 2/3 Selektion anpassen
4. **Scheduler-Setup:** scheduler_jobs-Tabelle definieren + Jobs implementieren
5. **Dashboard:** Einfache HTML-Tabelle als Prototyp
