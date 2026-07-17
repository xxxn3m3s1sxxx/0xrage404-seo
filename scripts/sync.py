"""Auto-sync satellite: re-check public status & re-sort videos."""
import json, re, urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TS_PATH = REPO / "src" / "videos.ts"
HTML_PATH = REPO / "index.html"
CACHE_PATH = REPO / "data" / "public_cache.json"
CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)

cache = {}
if CACHE_PATH.exists():
    cache = json.loads(CACHE_PATH.read_text("utf-8"))

def parse_videos_ts(text):
    entries = []
    for line in text.splitlines():
        m = re.search(r'\{\s*id:\s*"([^"]+)"', line)
        if not m:
            continue
        vid = m.group(1)
        title = re.search(r'title:\s*"([^"]+)"', line)
        topic = re.search(r'topic:\s*"([^"]+)"', line)
        blurb = re.search(r'blurb:\s*"([^"]+)"', line)
        file = re.search(r'file:\s*"([^"]+)"', line)
        thumb = re.search(r'thumb:\s*(true|false)', line)
        date = re.search(r'date:\s*"([^"]+)"', line)
        pub = re.search(r'public:\s*(true|false)', line)
        entries.append({
            "id": vid,
            "title": title.group(1) if title else "",
            "topic": topic.group(1) if topic else "",
            "blurb": blurb.group(1) if blurb else "",
            "file": file.group(1) if file else "",
            "thumb": thumb.group(1) == "true" if thumb else False,
            "date": date.group(1) if date else "",
            "public": pub.group(1) == "true" if pub else False,
        })
    return entries

def is_public(vid, force=False):
    if not force and vid in cache:
        return cache[vid]
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        urllib.request.urlopen(req, timeout=10)
        cache[vid] = True
        return True
    except Exception:
        cache[vid] = False
        return False

def has_thumb(vid):
    url = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0")
    try:
        r = urllib.request.urlopen(req, timeout=5)
        return len(r.read()) > 1000
    except Exception:
        return False

def rewrite_videos_ts(entries):
    lines = [
        "// Auto-generated -- do not edit manually",
        "// Run: python scripts/sync.py",
        "",
        "export interface Video {",
        '  id: string;',
        '  title: string;',
        '  topic: string;',
        '  blurb: string;',
        '  file: string;',
        '  thumb: boolean;',
        '  date: string;',
        '  public: boolean;',
        "}",
        "",
        "export const VIDEOS: Video[] = [",
    ]
    for e in entries:
        title = e["title"].replace("\\", "\\\\").replace('"', "'")
        blurb = e["blurb"].replace("\\", "\\\\").replace('"', "'")
        lines.append(f'  {{ id: "{e["id"]}", title: "{title}", topic: "{e["topic"]}", blurb: "{blurb}", file: "{e["file"]}", thumb: {"true" if e["thumb"] else "false"}, date: "{e["date"]}", public: {"true" if e["public"] else "false"} }},')
    lines.append("];")
    lines.append("")
    TS_PATH.write_text("\n".join(lines), encoding="utf-8")

def rewrite_index_html(entries):
    topics = {
        "css": "CSS specificity wars, Tailwind dogma, and the !important pain.",
        "react": "React Hooks, VDOM myths, and frontend framework drama.",
        "rust": "Borrow checker, ownership, and the steepest learning curve alive.",
        "typescript": "Any type lies, compiler hypocrisy, and false security.",
        "python": "GIL frustration, type hint traps, and dynamic typing cost traps.",
        "go": "Error handling joke, goroutine leaks, and Go's fake simplicity.",
        "docker": "Layer caching lies, image landfills, and container illusions.",
        "kubernetes": "YAML atrocities, operator madness, and K8s overkill for 90% of teams.",
        "agile": "Scrum circus, useless standups, and Agile as a bureaucracy monster.",
        "microservices": "Distributed monoliths, service mesh, and why less is more.",
        "worksonmymachine": "Reproducibility, CI/CD, and the biggest lie in software engineering.",
        "legacycode": "Tech debt, refactoring illusions, and code nobody understands.",
        "garbagecollection": "Stop-the-world, GC pauses, and memory management truth.",
        "serverless": "Cold starts, cost explosion, and the serverless scam.",
        "promptengineer": "AI code garbage, token waste, and vibecoding madness.",
        "llm": "Local LLMs, API costs, and the Jarvis syndrome delusion.",
        "hustleculture": "Burnout, toxic productivity, and the self-optimization trap.",
        "log_dump": "Internal pipeline log dump from the suckz engine.",
        "uncategorized": "Rage-Bait Tech Short from the suckz pipeline.",
    }
    card_html = []
    jsonld_items = []
    public_count = 0
    for e in entries:
        if e["public"]:
            public_count += 1
        title = e["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        blurb = topics.get(e["topic"], f"Rage-Bait Tech Short about {e['title']}")
        blurb_esc = blurb.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        thumb_url = f"https://i.ytimg.com/vi/{e['id']}/hqdefault.jpg"
        yt_url = f"https://www.youtube.com/watch?v={e['id']}"

        thumb_inner = f'<div class="fallback"><span>#{e["topic"]}</span></div>'
        if e["thumb"]:
            thumb_inner += f'<img src="{thumb_url}" alt="{title}" loading="lazy" />'

        badge = "" if e["public"] else '<span class="badge-scheduled">Scheduled</span>'
        card = f'''    <article class="card">
      <div class="card-thumb">
        <a href="{yt_url}" target="_blank" rel="noopener">{thumb_inner}</a>
      </div>
      <div class="card-body">
        <span class="topic">#{e["topic"]}{badge}</span>
        <h3><a href="{yt_url}" target="_blank" rel="noopener">{title}</a></h3>
        <p class="blurb">{blurb_esc}</p>
      </div>
    </article>'''
        card_html.append(card)

        jsonld_items.append(f'''    {{
      "@type": "VideoObject",
      "name": "{title}",
      "description": "{blurb_esc}",
      "thumbnailUrl": "{thumb_url}",
      "uploadDate": "{e['date']}T00:00:00Z",
      "contentUrl": "{yt_url}",
      "embedUrl": "https://www.youtube.com/embed/{e['id']}",
      "author": {{ "@type": "Person", "name": "@0xRAGE.404", "url": "https://youtube.com/@0xRAGE.404" }}
    }}''')

    html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="google-site-verification" content="xowI_1e7LxcI8EgpNGb9t7IaqQA8Y-O_WXllnBjChlY" />
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-9V7E3X9ZE0"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9V7E3X9ZE0');</script>
  <title>@0xRAGE.404 \u2014 Rage-Bait Tech Shorts</title>
  <meta name="description" content="{public_count} rage-bait tech shorts roasting CSS, React, Rust, Microservices, Kubernetes, Agile, Docker, TypeScript, Python, Go, AWS, legacy code, and everything wrong with your stack. Daily developer rage from @0xRAGE.404." />
  <meta name="keywords" content="0xRAGE404, rage bait, tech shorts, programming, css, react, rust, kubernetes, microservices, agile, docker, typescript, developer rant" />
  <meta name="author" content="@0xRAGE.404" />
  <meta property="og:title" content="@0xRAGE.404 \u2014 Rage-Bait Tech Shorts" />
  <meta property="og:description" content="{public_count} rage-bait tech shorts roasting everything wrong with your stack. Daily developer hate." />
  <meta property="og:url" content="https://xxxn3m3s1sxxx.github.io/0xrage404-seo/" />
  <meta property="og:type" content="website" />
  <meta property="og:image" content="https://i.ytimg.com/vi/{entries[0]['id'] if entries else ''}/hqdefault.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="@0xRAGE.404 \u2014 Rage-Bait Tech Shorts" />
  <meta name="twitter:description" content="{public_count} rage-bait tech shorts roasting everything wrong with your stack." />
  <meta name="twitter:image" content="https://i.ytimg.com/vi/{entries[0]['id'] if entries else ''}/hqdefault.jpg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Wallpoet&display=swap" rel="stylesheet" />
  <link rel="canonical" href="https://xxxn3m3s1sxxx.github.io/0xrage404-seo/" />
  <link rel="sitemap" type="application/xml" href="/0xrage404-seo/sitemap.xml" />
  <style>
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{background:#000;color:#0f0;font-family:'Wallpoet',monospace;min-height:100vh}}
    #matrix{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;opacity:.15;pointer-events:none}}
    header{{position:relative;z-index:1;text-align:center;padding:2rem 1rem 0.5rem;border-bottom:1px solid #0f033}}
    header h1{{font-size:5rem;letter-spacing:.15em;text-shadow:0 0 20px #0f0,0 0 40px #0f0;line-height:1}}
    @media(max-width:768px){{header h1{{font-size:3.2rem}}}}
    header .at{{font-size:.55em;vertical-align:middle;opacity:.6}}
    .subtitle{{font-size:.8rem;opacity:.5;margin-top:.3rem}}
    .counter{{font-size:.7rem;opacity:.4;margin-top:.2rem}}
    main{{position:relative;z-index:1;max-width:1200px;margin:0 auto;padding:1.5rem 1rem;display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1rem}}
    .card{{background:#0a0a0a;border:1px solid #0f033;border-radius:8px;overflow:hidden;transition:border-color .2s}}
    .card:hover{{border-color:#0f0}}
    .card-thumb{{position:relative;aspect-ratio:16/9;overflow:hidden;background:#111}}
    .card-thumb a{{display:block;width:100%;height:100%}}
    .card-thumb img{{width:100%;height:100%;object-fit:cover}}
    .fallback{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#001,#010,#001);font-size:1.2rem;color:#0f0;opacity:.7}}
    .card-thumb .fallback+img{{position:relative;z-index:1}}
    .badge-scheduled{{display:inline-block;margin-left:.4rem;padding:.1rem .4rem;border:1px solid #ff0;color:#ff0;font-size:.55rem;border-radius:3px;vertical-align:middle}}
    .card-body{{padding:.8rem}}
    .topic{{font-size:.65rem;opacity:.5;text-transform:uppercase;letter-spacing:.1em}}
    .card-body h3{{margin:.3rem 0;font-size:.9rem;line-height:1.4}}
    .card-body h3 a{{color:#0f0;text-decoration:none}}
    .card-body h3 a:hover{{text-decoration:underline}}
    .blurb{{font-size:.7rem;opacity:.4;line-height:1.5}}
    footer{{position:relative;z-index:1;text-align:center;padding:2rem;border-top:1px solid #0f033;font-size:.75rem}}
    footer a{{color:#0f0}}
  </style>
</head>
<body>
  <canvas id="matrix"></canvas>
  <header>
    <h1><span class="at">@</span>0xRAGE.404</h1>
    <p class="subtitle">Rage-Bait Tech Shorts</p>
    <p class="counter">{public_count} public &middot; {len(entries) - public_count} scheduled</p>
  </header>
  <main id="videos">
{chr(10).join(card_html)}
  </main>
  <footer>
    <p>Follow on <a href="https://youtube.com/@0xRAGE.404" target="_blank">YouTube</a></p>
  </footer>
  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
{', '.join(jsonld_items)}
  ]
}}
</script>
  <script type="module" src="/src/main.ts"></script>
</body>
</html>'''
    HTML_PATH.write_text(html, encoding="utf-8")

text = TS_PATH.read_text("utf-8")
entries = parse_videos_ts(text)

changed = False
for e in entries:
    current = is_public(e["id"], force=not e["public"])
    if current != e["public"]:
        print(f"[sync] {e['id']}: public={current} (was {e['public']})")
        e["public"] = current
        e["thumb"] = has_thumb(e["id"])
        changed = True

if not changed:
    print("[sync] No changes")
    CACHE_PATH.write_text(json.dumps(cache), encoding="utf-8")
    raise SystemExit(0)

entries.sort(key=lambda e: e["date"], reverse=True)
entries.sort(key=lambda e: 0 if e["public"] else 1)

rewrite_videos_ts(entries)
rewrite_index_html(entries)
CACHE_PATH.write_text(json.dumps(cache), encoding="utf-8")
print(f"[sync] Updated: {sum(1 for e in entries if e['public'])} public / {sum(1 for e in entries if not e['public'])} scheduled")
