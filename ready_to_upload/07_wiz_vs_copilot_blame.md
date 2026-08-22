# WIZ vs COPILOT BLAME GAME — Script #7

## Hook
An AI found a critical bug in Snowflake. Another AI might have written it. Then both AIs pointed fingers at each other. Welcome to software security in 2026.

## EXPLOIT TIMELINE
00:00 — Snowflake developer merges a PR in snowflake-connector-net
00:15 — Copilot Autofix is listed as co-author on the PR
00:30 — Vulnerable code goes live: unescaped issue title in GitHub Actions
00:45 — Five days pass with the flaw exposed
01:00 — Wiz Red Agent scans Snowflake public GitHub, flags the vulnerability
01:15 — Red Agent builds exploit, extracts Jira access token
01:30 — Wiz publishes research: claims Copilot Autofix wrote the bug
01:45 — GitHub fires back: human wrote it, Copilot only co-authored elsewhere
02:00 — Wiz retracts claim, updates blog post with timestamped correction
02:15 — Real realization: nobody can definitively prove who or what wrote the code
02:30 — Attribution in AI-assisted code becomes a security problem of its own

## Content
On June 18th 2025, a developer merged a pull request in Snowflakes public GitHub repository. The PR cleaned up a workflow script. GitHub Copilot Autofix was listed as a co-author. The merged code removed a safe pattern and replaced it with direct string interpolation of an issue title. No sanitization. No escaping.

Five days later, Wiz Red Agent scanned the repository. It flagged the vulnerability: an unauthenticated user could execute arbitrary commands by opening a GitHub issue with a crafted title. Red Agent built an exploit. It extracted a Jira access token with read access to Snowflakes internal engineering and security tickets.

Wiz published the research on August 17th. Their headline claim: Copilot Autofix wrote the bug. One AI writing the vulnerability, another AI finding it. A perfect narrative.

Except it was not quite right. GitHub pushed back. The vulnerable code section was attributable to a human contributor. Copilot contributed to other parts of the same pull request but not the specific lines with the flaw. Wiz updated their blog post the same day. The corrected attribution: unclear whether the vulnerable change was AI-assisted at all.

Wiz CTO Ami Luttwak said it plainly: clear attribution between humans and AI is becoming harder to establish. Just looking at co-authors of a PR is not enough.

And this is the real story. Not who wrote the bug. That the entire concept of code provenance is breaking down. When a human, Copilot Autofix, and a security scanner all touch the same pull request, who is responsible when something goes wrong?

Curl maintainer Daniel Stenberg calls it death by a thousand slops. Twenty percent of bug bounty submissions are now AI-generated garbage. His project ended its bug bounty program entirely after six and a half years. Bugcrowd tightened its rules. CISA now asks buyers to examine controls around AI-generated code.

The AI found it. The AI might have written it. Nobody can prove which. Welcome to the attribution crisis.

## Engagement
Have you ever tried to trace who actually wrote a specific line of code in a PR with AI co-authors? Drop your experience below. This problem is only getting worse.

## CTA
Do not subscribe. Forward this to your security team before they audit their next AI-generated pull request.

## Verdict
Wiz found a real vulnerability in Snowflakes infrastructure. The attribution fight is secondary. The real issue: AI tools touch code at every stage, and provenance tracking has not caught up. When AI writes code, AI reviews code, and AI finds bugs in code, the chain of custody collapses. Provenance is no longer a nice-to-have. It is a security requirement.

## TACTICAL DEBRIEF
Lesson: Code provenance in AI-assisted development is a security gap, not just an accounting problem. When your codebase includes contributions from humans, Copilot, and automated review bots all in the same PR, traditional Git blame is insufficient. Solution: log which model version contributed to which lines. Use GitHub's co-author tags with specific model identifiers. Implement automated provenance checks in your CI pipeline that track not just who committed but what generated each change. For security-critical repos, require human review of all AI-touched code paths. The question is no longer just who wrote the code. It is who is accountable when it breaks.

## Hashtags
#AISecurity #CopilotBug #WizSecurity #CodeProvenance #GitHubActions #SupplyChainSecurity #AICodeReview #SnowflakeVuln