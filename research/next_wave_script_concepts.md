# Nächste Content-Welle — Script-Konzepte

> Basierend auf Trend-Signals (2026-08-14): Claude Code +200%, Code Debt +120%, K8s Overengineering HN-hot.
> Status: ENTWURF. Keine Scripts generieren solange Task1075 läuft.

---

## 1. Claude Code (+200% Signal)

### Konzept: "Claude Code Is Overhyped"
- **Hook:** "Claude Code is the new jQuery — everyone uses it, nobody understands it"
- **Thesen:**
  - Demo ist brillant, Production ist Chaos
  - 60% der Commits sind AI-generierter Ballast
  - Code-Review wird zum Bot-Argument
  - Kosten: $20/Monat für Code, den du nicht verstehst
- **Gegen-These:** Claude Code ist ein Tool, kein Ersatz für Verstehen
- **Call-to-Action:** "If you can't explain what the AI wrote, you didn't ship code — you shipped risk"

### Betroffene Videos (bestehend):
- `ai_generated_code_001` ("AI Generated Code Is Rot") — thematisch verwandt
- `ai_generated_code_002` ("AI Code Never Gets Reviewed") — ergänzend

### Neues Video:
- `ai_claude_code_overhyped_001`: "Claude Code Is Overhyped"

---

## 2. Code Technical Debt (+120% Signal)

### Konzept: "Code Is Technical Debt Waiting to Happen"
- **Hook:** "Every line of code you write is debt. Most of you are bankrupt."
- **Thesen:**
  - Code zu schreiben ist billig. Code zu verstehen ist teuer.
  - 80% der Code-Basis ist toter Code
  - Refactoring ist kein Option, es ist Überleben
  - AI macht das Problem schlimmer (mehr Code, weniger Verstehen)
- **Gegen-These:** Gut geschriebener Code ist Investment, nicht Schuld
- **Call-to-Action:** "Delete code today. Your future self will thank you."

### Betroffene Videos (bestehend):
- `ai_generated_code_is_technical_debt_001` — direkt verwandt

### Neues Video:
- `code_debt_001`: "Code Is Technical Debt Waiting to Happen"

---

## 3. Kubernetes Overengineering (HN-hot)

### Konzept: "Everyone Using Kubernetes Is Wrong"
- **Hook:** "You don't need Kubernetes. You need a VPS and a cron job."
- **Thesen:**
  - 90% der K8s-Cluster laufen mit <10 Pods
  - YAML-Hölle: mehr Zeit in Konfiguration als in Code
  - Cloud-Rechnung: $500/Monat für etwas, das ein Docker-Compose könnte
  - K8s ist für Google, nicht für deine Startup-Saas
- **Gegen-These:** K8s ist richtig für große, komplexe Systeme
- **Call-to-Action:** "If you can't explain why you need Kubernetes, you don't need it"

### Betroffene Videos (bestehend):
- `Kubernetes_is_too_complex_001` — direkt verwandt
- `Kubernetes_is_too_complex_002` ("K8s YAML Is Hell") — ergänzend

### Neues Video:
- `k8s_overengineering_001`: "Everyone Using Kubernetes Is Wrong"

---

## 4. Fullstack Scam (+100% Signal)

### Konzept: "Fullstack Is a Complete Scam"
- **Hook:** "Fullstack developer means you're bad at two things instead of one"
- **Thesen:**
  - "Fullstack" ist ein Marketing-Term, keine Fähigkeit
  - 70% der "Fullstack"-Entwickler schreiben schlechten Frontend- UND Backend-Code
  - Spezialisierung schlägt Generalisierung in 90% der Fälle
  - Die "Fullstack-Lücke" ist ein Mythos
- **Gegen-Neither:** T-Shaped Developers (breites Verstehen, tiefe Spezialisierung) sind ideal
- **Call-to-Action:** "Pick a stack. Master it. Stop calling yourself fullstack."

### Neues Video:
- `fullstack_scam_001`: "Fullstack Is a Complete Scam"

---

## 5. Apple Ruining Software Engineering (NEW Signal)

### Konzept: "Apple Is Ruining Software Engineering"
- **Hook:** "Apple's new framework will be deprecated in 18 months. Here's why."
- **Thesen:**
  - Apple zwingt Entwickler in proprietäre Ökosysteme
  - Jedes Jahr ein neues Framework, altes wird deprecated
  - SwiftUI ist nicht production-ready, aber Apple tut so
  - Developer-Experience ist schlechter als 2015
- **Gegen-These:** Apple-Plattformen haben echte Vorteile (Performance, Security)
- **Call-to-Action:** "Stop building for Apple's roadmap. Build for your users."

### Neues Video:
- `apple_ruining_sweng_001`: "Apple Is Ruining Software Engineering"

---

## Priorität (nach Welle 1)

| Prio | Video | Signal | Hook-Stärke |
|------|-------|--------|-------------|
| 1 | Claude Code Is Overhyped | +200% | ⭐⭐⭐⭐⭐ |
| 2 | Code Is Technical Debt | +120% | ⭐⭐⭐⭐ |
| 3 | Everyone Using K8s Is Wrong | HN-hot | ⭐⭐⭐⭐ |
| 4 | Fullstack Is a Complete Scam | +100% | ⭐⭐⭐ |
| 5 | Apple Is Ruining Software Engineering | NEW | ⭐⭐⭐ |

## Nächste Schritte

1. **Nach Welle 1:** Retention-Daten auswerten → welche Hook-Typen funktionieren?
2. **Script-Generierung:** Priorität 1+2 zuerst (Claude Code, Code Debt)
3. **UVC v0.3:** Metadata für neue Videos generieren
4. **Upload:** In Welle 2 einplanen (nach Quota-Reset)
