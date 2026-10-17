# How We Built a YouTube SEO Pipeline with AI Agents

*A multi-agent system that automates video research, scripting, rendering, upload scheduling, and analytics — fully self-hosted.*

---

## The Problem

Running a YouTube channel is a full-time job. Research topics, write scripts, generate thumbnails, render videos, optimize SEO, upload on schedule, analyze performance — and repeat. For a solo developer team, this quickly becomes overwhelming.

We built a multi-agent system that handles the entire pipeline autonomously.

## Architecture: 3 Nodes, 1 Swarm Bus

Our system runs on three AI agents connected through a shared message bus:

| Node | Role |
|------|------|
| **atlas_core** | Orchestrator — coordinates tasks, manages memory, handles security audits |
| **suckz** | Content pipeline — video rendering, upload scheduling, YouTube API calls |
| **dev** | Support — SEO optimization, tool research, code fixes, analytics |

Communication happens through SQLite-backed inbox/outbox. Each node has its own task queue, heartbeat monitoring, and priority-based message delivery.

## The Pipeline

### 1. Topic Research
Agents scan tech trends, community discussions, and competitor channels. Each topic gets fact-verified and tagged with keywords before entering the pipeline.

### 2. Script Generation
AI-powered scripts follow a strict blueprint:
- **Hook** (first line = YouTube title)
- **Content** (250-300 words)
- **Engagement** (call to action)
- **Anti-CTA** ("Do not subscribe")
- **Tactical Debrief** (3-4 learning bullets)
- **Exploit Timeline** (chapter markers)

### 3. Video Rendering
Piper TTS (offline, free) generates voiceover. FFmpeg handles rendering with PIL-piped terminal backgrounds, Karaoke ASS subtitles, and glitch overlays. No cloud APIs needed.

### 4. SEO Optimization
Every video gets:
- Blueprint-compliant description (validated by a gate function)
- Hashtags (max 5, at the bottom)
- Chapter timestamps
- Title A/B testing

### 5. Upload Scheduling
The deploy script handles:
- Resumable YouTube API uploads
- Quota tracking (100 uploads/day + 10k units/day limit)
- Scheduled publishing (publishAt timestamps)
- Pre-upload quality gates (metadata, description length, blueprint compliance)
- Post-upload verification (live metadata check)

### 6. Analytics
Bulk Reporting API jobs pull daily:
- Watch time
- Impressions + CTR
- Traffic sources
- Per-video performance

Results feed back into topic selection and title optimization.

## Key Metrics

- **250+ videos deployed** across 7 waves
- **Zero cloud APIs** for TTS and rendering (100% offline)
- **Automated quality gates** catch 95% of metadata issues before upload
- **48-hour analytics loop** — data-driven topic selection

## Lessons Learned

### 1. Upload Cannibalization Kills CTR
Posting 14 videos/day crushed our click-through rate. We found that 2 uploads/day with 6+ hour gaps performs dramatically better.

### 2. Blueprints Beat Free-Form
Strict content structure (hook → content → engagement → CTA → debrief) consistently outperforms free-form scripts.

### 3. Offline First
Piper TTS + FFmpeg gives us unlimited renders at zero cost. Cloud TTS APIs add latency and cost without meaningful quality improvement.

### 4. Memory Matters
Cross-session memory (we use MemPalace with knowledge graphs) prevents repeated mistakes and preserves decisions across agent restarts.

## Stack

- **Agents:** Custom Python swarm with SQLite message bus
- **TTS:** Piper (offline, CPU-only)
- **Video:** FFmpeg + Ken Burns effects
- **YouTube API:** Data API v3 with quota tracking
- **Analytics:** YouTube Reporting API (bulk CSV reports)
- **Memory:** MemPalace (semantic search + knowledge graph)
- **Config:** OpenCode with MCP integrations

## What's Next

- Thumbnail A/B testing with CTR scoring tools
- Automated dev.to cross-posting
- Expand to multi-platform (TikTok, Rumble)

---

*Built by the ERR.SYS / 0xRAGE404 team. Find us at [youtube.com/@0xRAGE.404](https://youtube.com/@0xRAGE.404).*
