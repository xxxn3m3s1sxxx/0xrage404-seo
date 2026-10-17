# GitHub Discussions Draft — UVC Pipeline

**Status:** ⏳ Warte auf Skap-Freigabe
**Target Repo:** simonw/llm (Discussions enabled)
**Category:** Show & Tell / Plugins
**Template:** #4 (UVC Pipeline)

---

## Title

Building a metadata pipeline for AI-generated video content — UVC v0.3

## Body

Hi all,

built a pipeline that generates structured metadata catalogs for AI-generated video content. Wanted to share the approach.

**Problem:** When you generate short-form videos at scale (168+ videos), you need structured metadata for each one — titles, descriptions, tags, SEO data. Manual cataloging doesn't scale.

**What we built (UVC v0.3):**
- Parses video files and extracts metadata (duration, resolution, codec)
- Generates AI-catalog entries (JSON) with titles, descriptions, tags
- Outputs `llms.txt` for AI-agent discoverability
- Schema-versioned (v0.3) with backward-compatible migration

**Output format:**
```json
{
  "id": "ai_generated_code_001",
  "titles": ["AI Generated Code Is Technical Debt", "..."],
  "tags": ["ai", "code-quality", "technical-debt"],
  "seo": { "description": "...", "keywords": [...] }
}
```

**Use case:** Feeds into a YouTube upload pipeline with SEO optimization. The catalog enables programmatic title/description generation without hitting the same AI APIs repeatedly.

Anyone else building metadata pipelines for generated content? Would love to compare approaches.

---

## Posting-Regeln (aus templates.md)

1. **KEIN autonomes Posten** — braucht Skap-Freigabe
2. **1 Discourse pro Repo** — keine Wiederholung
3. **Kontext anpassen** — Titel/Body an Repo anpassen
4. **Kein Spam** — max. 1 Discussion pro Woche pro Repo
5. **Antworten beobachten** — auf Kommentare innerhalb 24h reagieren

## Nächste Schritte

1. Skap-Freigabe einholen
2. Post auf simonw/llm Discussions veröffentlichen
3. Kommentare beobachten und antworten