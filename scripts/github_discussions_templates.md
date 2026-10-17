# GitHub Discussions Seeding Templates

> **Skap-Freigabe nötig vor jedem Live-Post.** Templates sind Entwürfe, keine automatisierten Posts.

---

## Template 1: OpenCode — Case Study teilen

**Repo:** `anomalyco/opencode` (oder relevantes OpenCode-Repo)
**Category:** Show & Tell / General
**Hook:** 8.7GB → 3.8GB unter laufendem Betrieb

```markdown
Title: SQLite DB from 8.7GB to 3.8GB — pruning strategy for session-heavy workloads

Hey everyone,

wanted to share a real-world pruning case study from our production setup.

**Problem:** Our `opencode.db` (session data for a multi-agent coding system) grew to 8.7GB. The `event` table alone had 1.26M rows — ~633K older than 48 hours. Session list queries took 2.2s, and some sessions with 10K+ parts wouldn't load at all.

**What we did:**
- Chunked DELETE of events older than 48h (in batches of 50K, ~633K total)
- Conservative approach on NULL-time rows (kept them — couldn't verify age)
- `VACUUM INTO` as a compact safety copy before final pruning
- Verification: row-count checksums + subset checks on session/message/part tables (100% preserved)

**Result:** 8.7GB → 3.78GB (−54%), `freelist_count=0`, zero data loss, no downtime window needed.

**Key learnings:**
1. SQLite handles chunked deletes well under concurrent reads — just avoid long transactions
2. NULL-time rows are dangerous to delete without a reliable age signal
3. `VACUUM INTO` gives you a verifiable compact copy without touching the live DB

Full write-up with governance protocol (we ran this under a multi-agent consensus system with veto rights): [link to Dev.to article]

Anyone else dealing with SQLite bloat in session/telemetry systems? Curious how others approach retention.
```

---

## Template 2: SQLite — Pruning-Technik

**Repo:** `sqlite/sqlite` (or `utelle/opensqlite3`)
**Category:** General / Help
**Hook:** Pragmatische Antwort auf SQLite-Bloat

```markdown
Title: Practical pruning: 8.7GB → 3.8GB on a session DB with concurrent reads

Hi all,

ran into a real-world SQLite scaling issue and wanted to share the approach.

**Schema overview:**
- `event` table: 1.26M rows (full JSON payloads, ~3.5GB)
- `part` table: 667K rows (tool transcripts, ~5.9GB)
- `session` / `message`: small

The `event` table was the pruning target — every state change wrote a full JSON blob. ~633K rows were older than 48h and redundant.

**Approach:**
1. Chunked DELETE (50K rows/batch, ~13 batches) — keeps WAL manageable, avoids long locks
2. NULL-time handling: conservative — kept rows where age couldn't be determined
3. Post-delete: `VACUUM INTO` to create a compact verified copy
4. Verification: row-count checksums on all tables, subset checks on critical data

**Results:** −54% size, `freelist=0`, zero data loss, no downtime.

**Question for the community:** What's your preferred approach for NULL-time rows when the extraction path is ambiguous? We erred on the side of keeping them, but it means ~400K rows we couldn't safely age.

Blog post with full details: [link]
```

---

## Template 3: Cloudflare Workers — Deployment

**Repo:** `cloudflare/workers-sdk` (or `cloudflare/workers-sdk`)
**Category:** Show & Tell / General
**Hook:** SQLite-Pipeline über Cloudflare Workers deployed

```markdown
Title: Deploying a SQLite pruning pipeline via Cloudflare Workers — lessons learned

Hey everyone,

just shipped a production pipeline that runs SQLite maintenance tasks through Cloudflare Workers and wanted to share the architecture.

**What it does:**
- Scheduled Worker triggers pruning jobs on a SQLite database
- Chunked deletes (50K rows/batch) with progress tracking
- Verification step: row-count checksums before and after
- Notification via webhook on completion

**Key challenges:**
1. Workers have execution time limits — chunked approach was essential (couldn't do a single VACUUM)
2. SQLite WAL mode + concurrent reads: the chunked DELETE approach kept the DB responsive
3. Error handling: each batch is independently verifiable, so partial failures are recoverable

**Stack:** SQLite (local file via Workers), V8 isolate, cron trigger

This is part of a larger multi-agent coding system where session data grows fast. The pruning runs daily now and keeps the DB under 4GB.

Anyone else running SQLite maintenance through Workers? Curious about your timeout strategies.
```

---

## Template 4: AI/LLM — UVC Pipeline

**Repo:** `simonw/llm` (or relevant AI coding tool repo)
**Category:** Show & Tell / Plugins
**Hook:** UVC-Pipeline für AI-Katalog-Generierung

```markdown
Title: Building a metadata pipeline for AI-generated video content — UVC v0.3

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
```

---

## Template 5: Multi-Agent Systems — Governance

**Repo:** `langchain-ai/langchain` (or `microsoft/autogen`)
**Category:** General / Show & Tell
**Hook:** Multi-Agent-Verfassung mit Veto-Recht

```markdown
Title: Democratic governance for multi-agent systems — our team constitution

Hey everyone,

running a 3-agent coding system (dev, verifier, orchestrator) with a human veto. Wanted to share the governance protocol that's been working.

**Core principles:**
1. **Critical bus voting:** All 3 agents must approve before destructive actions (db changes, uploads, deploys)
2. **Human veto right:** Can block any action at any time
3. **Team consultation rule:** Before touching shared artifacts, must ask with clear options + wait window
4. **Done gate:** Machine-observed verification — no "85% confidence" shipping

**What we learned:**
- Veto power gives the human real control, not just rubber-stamping
- 30-minute response windows prevent deadlocks
- Democratic voting catches mistakes that single-agent review misses
- "Anti-reward-hacking" rule: agents can't optimize for test passing, only for real outcomes

**Concrete example:** We just pruned an 8.7GB SQLite database under consensus — all 3 agents voted, human confirmed, zero data loss.

Full protocol (MAP): [link to repo]

Anyone else experimenting with governance protocols for agent teams?
```

---

## Posting-Regeln

1. **KEIN autonomes Posten** — alle Templates brauchen Skap-Freigabe
2. **1 Discourse pro Repo** — keine Wiederholung auf gleichem Repo
3. **Kontext anpassen** — Titel/Body an das jeweilige Repo anpassen
4. **Kein Spam** — max. 1 Discussion pro Woche pro Repo
5. **Antworten beobachten** — auf Kommentare innerhalb 24h reagieren
6. **Link zur Dev.to** — nur als Quellenverweis, nicht als Spam
7. **AI-Kennzeichnung** — wo angemessen, erwähnen dass Pipeline AI-unterstützt ist

## Priorität

| Prio | Template | Ziel-Repo | Status |
|------|----------|-----------|--------|
| 1 | Case Study | anomalyco/opencode | ⏳ Skap-Freigabe |
| 2 | Pruning-Technik | sqlite/sqlite | ⏳ Skap-Freigabe |
| 3 | UVC Pipeline | simonw/llm | ⏳ Skap-Freigabe |
| 4 | CF Workers | cloudflare/workers-sdk | ⏳ Skap-Freigabe |
| 5 | Governance | langchain-ai/langchain | ⏳ Skap-Freigabe |
