# Content-Qualitäts-Checkliste — Tag 1 (Pre-Welle 1)

> Fertig bis Tag 2 (nach Welle 1 Daten). Dient der Kalibrierung für Wellen 2/3.

---

## 1. Hook-Analyse (UVC v0.3)

### Titel-Pattern der 27 deployed Videos

| Kategorie | Titel | Hook-Typ | Bewertung |
|-----------|-------|----------|-----------|
| AI Code | AI Generated Code Is Technical Debt | Behauptung | ⭐⭐⭐ stark |
| AI Code | AI Generated Code Is Rot | Provokation | ⭐⭐⭐⭐ sehr stark |
| AI Code | AI Code Never Gets Reviewed | Behauptung | ⭐⭐⭐ stark |
| AI Code | AI Code Deployed to Prod | Horror | ⭐⭐⭐ stark |
| Code Ownership | Code Ownership Is Stupid | Provokation | ⭐⭐⭐⭐ sehr stark |
| Code Ownership | No One Owns This Code | Horror | ⭐⭐⭐ stark |
| Code Ownership | Code Ownership Kills Teams | Horror | ⭐⭐⭐ stark |
| CSS | CSS Is A Dumpster Fire | Provokation | ⭐⭐⭐⭐ sehr stark |
| CSS | CSS Frameworks Are Crutches | Behauptung | ⭐⭐⭐ stark |
| Agile | Agile Is A Cargo Cult | Provokation | ⭐⭐⭐⭐ sehr stark |
| Agile | Your Standups Are Worthless | Provokation | ⭐⭐⭐⭐ sehr stark |
| K8s | Kubernetes Is Too Complex | Behauptung | ⭐⭐⭐ stark |
| K8s | K8s YAML Is Hell | Provokation | ⭐⭐⭐⭐ sehr stark |
| Microservices | Microservices Are Not A Solution | Behauptung | ⭐⭐⭐ stark |
| Microservices | Distributed Monolith | Horror | ⭐⭐⭐ stark |
| React | React Is Bloatware | Provokation | ⭐⭐⭐⭐ sehr stark |
| React | React Devs Can't Write CSS | Provokation | ⭐⭐⭐⭐ sehr stark |
| Burnout | Burnout Is Inevitable | Horror | ⭐⭐⭐ stark |
| Burnout | Work Life Balance Is A Lie | Provokation | ⭐⭐⭐⭐ sehr stark |
| CI | CI Pipeline | Neutral | ⭐⭐ schwach |
| CI | Your CI Pipeline Sucks | Provokation | ⭐⭐⭐⭐ sehr stark |
| Docker | Docker | Neutral | ⭐⭐ schwach |
| Docker | Docker Compose Nightmare | Horror | ⭐⭐⭐ stark |
| TypeScript | You Use TypeScript Wrong | Provokation | ⭐⭐⭐⭐ sehr stark |
| TypeScript | TypeScript Made You Slower | Behauptung | ⭐⭐⭐ stark |
| GC | Your Garbage Collector is a Bonfire | Horror | ⭐⭐⭐⭐ sehr stark |
| Rust | Rust is the worst trend in development | Behauptung | ⭐⭐⭐ stark |

### Hook-Typ-Verteilung
- **Provokation** (14): 52% — dominanter Hook-Typ
- **Horror** (7): 26%
- **Behauptung** (5): 19%
- **Neutral** (2): 7% — SCHWACH, needs fix

### Identifizierte Probleme
1. **2 neutrale Titel** ("CI Pipeline", "Docker") — keine Emotion, kein Hook
2. **Keine Zahlen** — "8.7GB → 3.8GB" wirkt stärker als "AI Code Is Rot"
3. **Keine Fragen** — "Why Does Your CI Pipeline Suck?" wäre stärker

---

## 2. Verdict-to-Title Review

### UVC v0.3 Output (aus ai-catalog.json)
Jeder Video-Eintrag hat:
- `titles[]`: 3-5 Titel-Varianten (verdict-basiert)
- `tags[]`: SEO-Tags
- `seo.description`: AI-generierte Beschreibung

**Frage:** Sind die Upload-Titel (aus `meta["titles"]`) die stärksten Hooks?

### Stichprobe (5 Videos)

| Video | Upload-Titel | Bester UVC-Titel | Differenz |
|-------|-------------|-------------------|-----------|
| AI Generated Code Is Technical Debt | AI Generated Code Is Technical Debt | "Your AI Code Is Technical Debt" (2. Person) | +Engagement |
| Code Ownership Is Stupid | Code Ownership Is Stupid | "Code Ownership Is Dead" (Past-Tense) | +Aktualität |
| CSS Is A Dumpster Fire | CSS Is A Dumpster Fire | "CSS Is a Dumpster Fire — Here's Why" (Curiosity) | +Retention |
| Kubernetes Is Too Complex | Kubernetes Is Too Complex | "Kubernetes Is Too Complex (And You Know It)" (Validation) | +Emotional |
| Burnout Is Inevitable | Burnout Is Inevitable | "Burnout Is Inevitable — Here's How to Survive" (Lösung) | +Value |

**Empfehlung:** Für Welle 2/3: UVC-Titel-Varianten mit2. Person oder Curiosity-Hook priorisieren.

---

## 3. Fünf Optimierungen für Welle 2/3

### Opt1: Neutrale Titel ersetzen
**Betroffen:** "CI Pipeline" (ci_pipeline_001), "Docker" (docker_001)
**Aktion:** UVC v0.3重新generieren mit stärkeren Hooks
**Vorschlag:**
- "CI Pipeline" → "Your CI Pipeline Is Broken (You Just Don't Know It)"
- "Docker" → "Docker Is Eating Your Dev Time"

### Opt2: Zahlen in Titel integrieren
**Betroffen:** Alle Videos mit messbaren Metriken
**Aktion:** "8.7GB → 3.8GB" in SQLite-Related-Titeln, "633K Rows Deleted" als Social Proof

### Opt3: 2. Person für Engagement
**Betroffen:** ~50% der Titel (behauptungs-Typ)
**Aktion:** "AI Generated Code Is Technical Debt" → "Your AI Code Is Technical Debt"
**Risiko:** Kann als aggressiv empfunden werden → A/B-Test nötig

### Opt4: Curiosity-Gap schließen
**Betroffen:** Alle Horror-Titel
**Aktion:** "Here's Why" / "Here's How" Suffix hinzufügen
**Beispiel:** "CSS Is A Dumpster Fire" → "CSS Is A Dumpster Fire — Here's How We Fixed It"

### Opt5: Emotionale Validation
**Betroffen:** Behauptungs-Titel
**Aktion:** "(And You Know It)" / "(And That's Okay)" Suffix
**Beispiel:** "Kubernetes Is Too Complex" → "Kubernetes Is Too Complex (And You Know It)"

---

## 4. Retention-Feedback (nach Welle 1)

> Stand: Tag 2 (2026-08-16). Daten von YouTube Data API (basic stats). Analytics-Daten (Retention-Kurven) folgen nach 48h+.

### Metriken (Tag 2)

| Video | Views | Likes | Comments | Duration | Hook-Score | Status |
|-------|-------|-------|----------|----------|------------|--------|
| w34_agentic_ide_001 | 43 | 0 | 0 | 14s | ? | Nur Views |
| w34_ai_wearable_001 | 1 | 0 | 0 | 14s | ? | Zu neu |
| w34_llm_learning_001 | 36 | 1 | 2 | 14s | ? | Engagement da |
| w34_phone_server_001 | 31 | 0 | 0 | 15s | ? | Nur Views |

**Durchschnitt:** 27.75 Views, 0.25 Likes, 0.5 Comments

### Offene Fragen
1. Welche Hook-Typen haben die höchste Retention? — **Noch nicht beantwortbar** (Retention-Daten fehlen)
2. Gibt es einen Drop-off nach dem ersten Hook (0-3 Sek)? — **Noch nicht beantwortbar**
3. Korreliert Kommentar-Qualität mit Titel-Provokation? — **初步 Ja** (w34_llm_learning hat 2 Kommentare bei 36 Views = 5.6% Engagement)

### Nächste Schritte
1. **Tag 0+48h (17.08. 09:00):** Retention-Kurve aus YouTube Analytics API laden
2. **Tag 0+7d (22.08.):** Vollständige Auswertung mit CTR und Audience Retention
3. **Analytics-Script:** `python analytics.py --fetch` mit echten OAuth2-Credentials ausführen

### Metriken zu tracken (für spitere Wellen)
- **Average View Duration** pro Video
- **Audience Retention** Kurve (Drop-off-Punkte)
- **CTR** (Click-Through-Rate) aus Search/Impressions
- **Likes/Dislikes** Verhältnis
- **Kommentare** (Qualität, nicht Quantität)

---

## 5. Quota-Fenster-Optimierung

### Aktuelles Setup
- **Reset:** 00:00 PDT = 09:00 MESZ (immer)
- **Kapazität:** 9900 Units/Tag
- **Welle 1:** 5 Uploads = ~8000 Units (81% Auslastung)

### Optimierungspotenzial

| Fenster | Vorteil | Nachteil |
|---------|---------|----------|
| 09:00-12:00 MESZ | Frischer Reset, volle Quota | Peak-Traffic (alle starten gleichzeitig) |
| 12:00-15:00 MESZ | Mid-day, menos competencia | Noch 6-9h Quota-Rest |
| 18:00-21:00 MESZ | Evening Peak (YouTube) | Quota könnte aufgebraucht sein |

**Empfehlung:** Uploads um 09:00-10:00 MESZ (nach Reset), SEO/Captions um12:00-15:00 MESZ (weniger Competition).

### Rolling-Day-Regel
- 6 Slots pro Tag
- Welle 1: 5 Uploads = 1 Slot frei (für SEO/Captions)
- Welle 2+: 4 Uploads + 2 Slots für Caption/Thumbnail-Updates

---

## 6. Trend-Signal-Analyse (Welle 2/3 Selektion)

### Stärkste Signale (2026-08-14)

| Prio | Topic | Signal | Quelle | Hook-Potenzial |
|------|-------|--------|--------|----------------|
| 1 | Claude Code | +200% Search | Google Trends | ⭐⭐⭐⭐⭐ (Provokation + Trend) |
| 2 | Code Debt | +120% Search | Google Trends | ⭐⭐⭐⭐ (Fear + Zahlen) |
| 3 | K8s Overengineering | HN-hot | HackerNews Top | ⭐⭐⭐⭐ (Community-Validation) |
| 4 | Fullstack Scam | +100% Search | Google Trends | ⭐⭐⭐ (Identity-Thema) |
| 5 | Apple SW Engineering | NEW Signal | Mixed | ⭐⭐⭐ (Nische, aber leidenschaftlich) |

### Selektionsregel für Welle 2/3
1. **Mindestens 1 Video pro Trend-Signal** (Covering der Top-3)
2. **Hook-Mix beibehalten:** 52% Provokation, 26% Horror, 19% Behauptung, 3% Frage
3. **Keine neutralen Titel** (Opt1-Pflicht)
4. **Zahlen/Perspektive in 50%+ der Titel** (Opt2+Opt3)

### Empfohlenes Welle 2/3 Paket (5 Videos)

| # | Video | Topic | Hook-Typ | Signal |
|---|-------|-------|----------|--------|
| 1 | Claude Code Is Overhyped | AI Code | Provokation | +200% |
| 2 | Code Is Technical Debt | Code Debt | Horror | +120% |
| 3 | Everyone Using K8s Is Wrong | K8s | Behauptung | HN-hot |
| 4 | Your CI Pipeline Is Broken | CI | Frage | Bestehend (Opt1) |
| 5 | Fullstack Is a Scam | Career | Provokation | +100% |

---

## 7. Content-Lücke-Analyse

### Was fehlt im aktuellen Katalog (27 Videos)

| Lücke | Video-Vorschlag | Warum |
|-------|----------------|-------|
| **Testing** | "Your Tests Are Fake" | Kein Testing-Video, aber hohes Engagement auf HN/Reddit |
| **Security** | "You're Already Hacked" | Security-Themen trenden, aber kein ERR.SYS-Video |
| **Monorepo** | "Monorepos Are A Mistake" | Starke Meinung auf Twitter, wenig Gegenrede |
| **DevOps** | "DevOps Is Just ops" | Ironie-Trigger, passt zu ERR.SYS-Ton |
| **SQL** | "SQL Is Dying (It's Not)" | Clickbait + Reality-Check, hohe Retention erwartet |

### Priorität nach Welle 1
- Erst Welle 2 (5 Videos oben) → dann Lücken-Videos in Welle 3

---

## Nächste Schritte

1. **Nach Welle 1 (Tag 2):** Retention-Daten eintragen, Hook-Bewertung aktualisieren
2. **Welle 2:** Obiges 5er-Pakert (Claude Code, Code Debt, K8s, CI-Fix, Fullstack)
3. **Welle 3:** Lücken-Videos (Testing, Security, Monorepo, DevOps, SQL)
4. **Laufend:** Quota-Fenster-Tracking, A/B-Test der Titel-Varianten
5. **Kalibrierung:** Welche Hook-Typen haben höchste Retention → Gewichtung anpassen
