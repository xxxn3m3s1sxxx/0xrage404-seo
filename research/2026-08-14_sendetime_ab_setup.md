# Sendezeit-A/B-Setup — ab Welle 2 (16.08.)

> Vorbereitung für verteilte Uploads als A/B-Test gegen Bündel-Baseline.
> Status: ENTWURF. Kein Code-Change an deploy.py. Read-only, wave-safe.

---

## 1. Slot-Design

### Bündel-Baseline (Welle 1, morgen)
```
09:00 MEZ: 5× w34 Upload (agentic_ide, ai_wearable, llm_learning, phone_server, redis_never_bottleneck)
```

### Verteilung (ab Welle 2, 16.08.)
```
--schedule-hours "0 3 6 9 12"  (relativ zum Reset-Offset)
```

**Berechnung:**
- Quota-Reset: 09:00 MEZ (= 00:00 PDT)
- Slot 1: 09:00 MEZ (0h nach Reset) → `--schedule-hours 0`
- Slot 2: 12:00 MEZ (3h nach Reset) → `--schedule-hours 3`
- Slot 3: 15:00 MEZ (6h nach Reset) → `--schedule-hours 6`
- Slot 4: 18:00 MEZ (9h nach Reset) → `--schedule-hours 9`
- Slot 5: 21:00 MEZ (12h nach Reset) → `--schedule-hours 12`

**Einheitliche Units:** 1600 Units je Video (unabhängig von Slot).

### warum diese Slots?

| Slot | MEZ | Zielgruppe | Begründung |
|------|-----|------------|-----------|
| 09:00 | Früh | EU-Developer (Morgens) | Baseline, frischer Reset |
| 12:00 | Mittag | EU + US-East (Lunch) | Mittags-Peak |
| 15:00 | Nachmittag | US-East + EU (Afternoon) | Überlappung EU/US |
| 18:00 | Abend | US-West (Afternoon) | US-Feierabend-Start |
| 21:00 | Nacht | US-West (Evening) | US-Prime-Time |

---

## 2. Metriken pro Slot

### Quellen
- **analytics.py** (`scripts/analytics.py`): Retention/CTR/Views aus YouTube Analytics API
- **analytics_cache.json** (`~/.suckz/analytics_cache.json`): Cach日期
- **analytics_daily.py** (`scripts/analytics_daily.py`): Täglicher Report + Swarm-Message

### Metriken (pro Video, ab Upload-Zeitpunkt)

| Metrik | Quelle | Zeitfenster | Slot-relevant? |
|--------|--------|-------------|----------------|
| **CTR** (Click-Through-Rate) | analytics.py --fetch | 24h, 48h, 7d | Ja — Thumbnail + Titel-Wirksamkeit je Slot |
| **Avg View Duration** | analytics.py --fetch | 24h, 48h, 7d | Ja — Hook-Qualität je Slot |
| **Audience Retention (%)** | analytics.py --midpoint | 48h, 7d | Ja — Drop-off-Punkte je Slot |
| **Impressions** | analytics.py --fetch | 24h, 48h | Ja — Algorithmus-Reichweite je Slot |
| **Likes/Comments** | analytics.py --fetch | 24h, 48h, 7d | Ja — Emotionale Resonanz je Slot |
| **Subscriber-Gain** | analytics.py --fetch | 7d | Ja — Langzeitwert je Slot |

### Ablese-Zeitpunkte

```
Upload: 09:00/12:00/15:00/18:00/21:00 MEZ
├── +24h: Erste Metriken (CTR, Impressions, Avg View Duration)
├── +48h: Retention-Kurve stabil (Hauptkalibrierung)
├── +7d: Vollständiges Bild (Subscriber-Gain, Sentiment)
└── +14d: Langzeit-Trend (optional)
```

---

## 3. Baseline sauber halten

### Frage: Welche Videos sind Baseline vs. Verteilung?

**Antwort:**
- **Baseline:** Welle 1 (5× w34, morgen 09:00 Bündel) → alle 5 im selben Slot
- **Verteilung:** Welle 2+ (5× pro Tag, --schedule-hours verteilt)

### Zuordnung in deployed.json

Jedes Video bekommt ein `upload_slot`-Feld:
```json
{
  "video_id": "abc123",
  "title": "...",
  "upload_slot": "09:00",  // oder "12:00", "15:00", "18:00", "21:00"
  "wave": 1,  // oder 2, 3, ...
  "deployed_at": "2026-08-15T09:00:00+02:00"
}
```

### Vergleichslogik

```
Baseline-Ø (Welle 1, 5 Videos) vs. Verteilungs-Ø (Welle 2, 5 Videos)
├── Metrik: CTR, Avg View Duration, Retention, Impressions
├── Statistik: Mittelwert, Standardabweichung, p-Wert (t-Test)
├── Signifikanz: p < 0.05 = signifikant, p < 0.01 = hochsignifikant
└── Entscheidung: Wenn Verteilung > Baseline → Welle 3 verteilt beibehalten
```

---

## 4. Umsetzung (post-Welle 1)

### Schritte

1. **Welle 1 Upload (morgen):** 5× w34 um 09:00 → Baseline-Daten sammeln
2. **Tag 2+48h:** Erste Retention-Daten aus analytics.py → Checkliste aktualisieren
3. **Tag 7:** Vollständige Baseline → Welle 2/3 Selektion anpassen
4. **Ab 16.08.:** Welle 2 mit --schedule-hours verteilen
5. **Tag 16+7d:** Vergleich Baseline vs. Verteilung

### deploy.py-Kommando (Welle 2)

```bash
python -m suckz deploy \
  --whitelist claude_code_001 code_debt_001 k8s_overengineering_001 ci_fix_001 fullstack_scam_001 \
  --schedule-hours 0 3 6 9 12
```

### Analytics-Report (nach Welle 2)

```bash
python scripts/analytics.py --fetch
python scripts/analytics.py --report
python scripts/analytics.py --csv ab_comparison.csv
```

---

## 5. Offene Fragen — BEANTWORTET

### Fr. 1: --schedule-hours Genauigkeit
**Antwort:** Relativ ab Ausfuehrzeit, NICHT absolut. deploy.py:2773 `dt = datetime.now(timezone.utc) + timedelta(hours=hrs)`. Bei 09:00-Start treffen 0/3/6/9/12 auf 09:00/12:00/15:00/18:00/21:00 UTC (=MEZ+2). Exakt nur wenn Lauf puenktlich 09:00 startet. YouTube Scheduled-Uploads sind intern praezise (Sekundenbereich), aber der Triggerpunkt ist `datetime.now()` beim Ausfuehren.

### Fr. 2: Algorithmus — Scheduled vs. Immediate
**Antwort:** KEIN Unterschied. YouTube's offizielle Position (Rene Ritchie, 2025): "The recommendation system is largely based on audience behavior. So until your video goes live, not unlisted, not private, but actually public, there's no audience behavior data for it to understand or learn from." Weitere Quellen (SocialPilot 2026, YTShark 2026, Aurascience 2026): "Publish time is not known to impact a video's long-term performance." Scheduled = Immediate in der Algorithmus-Behandlung. Timing beeinflusst Early Engagement (First Hour = 3.2x Gewicht), nicht Algorithmus-Rang.

### Fr. 3: Statistische Power (5 vs. 5)
**Antwort:** Grenzwerthig. Fuer einen t-Test brauchen wir signifikante Differenzen in CTR/Retention. Bei 5 vs. 5 Videos:
- **CTR:** Typische Standardabweichung 2-4%. Bei Mittelwert-Differenz 1.5% (z.B. 3.5% vs. 5.0%) brauchen wir n>=8 pro Gruppe fuer p<0.05 (80% Power). 5 reicht nur fuer GROSSE Effekte (>2% Differenz).
- **Retention:** Typische SD 10-15%. Bei 10% Differenz brauchen wir n>=12 pro Gruppe. 5 ist UNTERDESICHTET.
- **Empfehlung:** Primärer Vergleich: Deskriptiv (Mittelwert,Median), nicht statistisch. Signifikanztest als HYPOTHESE fuer Welle 3 (n=10+). fuer Welle 2: Richtungswert, kein p-Wert.

### Fr. 4: upload_slot-Feld
**Antwort:** deployed.json-Erweiterung (keine separate Tabelle). Gruende:
- Deployed.json ist Source-of-Truth (F3-Regel)
- upload_slot ist Video-Metadatum, kein externer State
- Einfach: `"upload_slot": "12:00"` pro Video-Eintrag
- Analytics-Mapping: upload_slot + analytics_cache.json = Slot-Metriken
- Regressionstest: upload_slot-Pflicht erst ab Welle 2 (Welle 1 hat kein Slot)

---

## Nächste Schritte

1. **Nach Welle 1 (Tag 2):** Baseline-Metriken aus analytics.py eintragen
2. **Vor Welle 2:** --schedule-hours an deploy.py übergeben (kein Code-Change nötig)
3. **Nach Welle 2 (Tag 16+7d):** Vergleich Baseline vs. Verteilung
4. **Dokumentation:** Ergebnis in research/2026-08-16_sendetime_ab_results.md
