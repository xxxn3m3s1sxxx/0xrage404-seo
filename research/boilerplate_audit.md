# Boilerplate-Audit: Deployed Videos

> Gefunden: Task 1062 Follow-up. Videos.ts enthält systematische Description-Wiederholungen.

---

## Betroffene Videos (stichprobenartig)

### Problem 1: Identische Blurb-Felder

**Blurb:** "AI hype, LLM delusions, and the Copilot that writes worse code than your intern."

| Video | Topic | Blurb korrekt? |
|-------|-------|----------------|
| TDD religion: 83% retro fraud | ai | ❌ (TDD, nicht AI Hype) |
| Meeting Recorders Remember Everything | ai | ❌ (Privacy, nicht AI Hype) |
| Your Passwords Are Screaming | ai | ❌ (Security, nicht AI Hype) |
| 99.9% Accuracy Is Propaganda | ai | ❌ (SLO/Metrics, nicht AI Hype) |
| GPT-5.6 Is Overpriced | ai | ✅ (tatsächlich AI) |
| Apple Myths About Privacy | ai | ❌ (Apple, nicht AI Hype) |

**Ursache:** `blurb` wird automatisch aus Topic "ai" generiert, nicht aus dem individuellen Content.

### Problem 2: Identische Description-Texte

**Text:** "You wear burnout as a badge of honour. 'I worked 80 hours this week'..."

| Video | Title | Description = Burnout? |
|-------|-------|----------------------|
| Burnout Is Inevitable | Burnout | ✅ (thematisch korrekt) |
| Work-Life Balance Is a Lie | Work-Life | ✅ (thematisch korrekt) |
| Developer Burnout Is Your Fault | Burnout | ✅ (thematisch korrekt) |
| There Are No 10X Developers | 10X | ❌ (10X ≠ Burnout) |

**Ursache:** Copy-paste aus Burnout-Template für verwandte aber verschiedene Themen.

### Problem 3: Topic-Mismatch

| Video | Topic in videos.ts | Tatsächliches Thema |
|-------|-------------------|-------------------|
| There Are No 10X Developers | overengineering | Burnout (falsche Description) |
| Apple Myths About Privacy | ai | Apple/Privacy (nicht AI) |
| TDD religion: 83% retro fraud | ai | TDD/Testing (nicht AI) |

---

## Auswirkung

1. **SEO-Schaden**: YouTube erkennt Copy-paste Descriptions → lower ranking
2. **User-Verwirrung**: Description passt nicht zum Titel → höhere Bounce-Rate
3. **Brand-Schaden**: "ERR.SYS" wirkt wie Content-Mill, nicht wie qualitativ hochwertiger Kanal

---

## Empfohlene Fixes

### Fix 1: Blurb-Generierung individualisieren
- Nicht nur aus Topic, sondern aus Titel + Transcript ableiten
- `blurb = f"{title_hook}: {first_sentence_of_transcript}"`

### Fix 2: Description-Templates differenzieren
- Pro Topic-Kategorie ein eigenes Template
- Burnout ≠ 10X ≠ Apple ≠ TDD — jedes braucht eigenen Hook

### Fix 3: Topic-Tags korrigieren
- "There Are No 10X Developers" → Topic: `productivity` oder `myths`, nicht `overengineering`
- "Apple Myths" → Topic: `apple`, nicht `ai`
- "TDD religion" → Topic: `testing`, nicht `ai`

### Fix 4: Deploy-gate erweitern
- Vor Deployment: `blurb uniqueness check` (kein >50% Match mit bestehenden)
- Vor Deployment: `description != other_description` (kein Copy-paste)

---

## Priorität

| Fix | Aufwand | Impact |
|-----|---------|--------|
| Fix 1 (Blurb) | mittel | hoch |
| Fix 2 (Templates) | gering | hoch |
| Fix 3 (Topics) | gering | mittel |
| Fix 4 (Gate) | hoch | sehr hoch |

**Empfehlung:** Fix 3 sofort (Topic-Tags korrigieren), Fix 1+2 nach Welle 1 (wenn neue Videos generiert werden).
