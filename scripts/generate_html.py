"""Generate index.html from src/videos.ts — standalone, no suckz deps."""
import json, re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TS_PATH = REPO / "src" / "videos.ts"
HTML_PATH = REPO / "index.html"

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

text = TS_PATH.read_text("utf-8")
entries = parse_videos_ts(text)
public_count = sum(1 for e in entries if e["public"])
private_count = len(entries) - public_count

blurbs = {
    "css": "CSS specificity wars, Tailwind dogma, and the !important pain.",
    "react": "React Hooks, VDOM myths, and frontend framework drama.",
    "rust": "Borrow checker, ownership, and the steepest learning curve alive.",
    "typescript": "Any type lies, compiler hypocrisy, and false security.",
    "python": "GIL frustration, type hint traps, and dynamic typing cost traps.",
    "go": "Error handling joke, goroutine leaks, and Go\u2019s fake simplicity.",
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
for e in entries:
    title = e["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    blurb = e["blurb"] or blurbs.get(e["topic"], f"Rage-Bait Tech Short about {e['title']}")
    blurb_esc = blurb.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    thumb_url = f"https://i.ytimg.com/vi/{e['id']}/hqdefault.jpg"
    yt_url = f"https://www.youtube.com/watch?v={e['id']}"
    thumb_inner = f'<div class="fallback"><span>#{e["topic"]}</span></div>'
    if e["thumb"]:
        thumb_inner += f'<img src="{thumb_url}" alt="{title}" loading="lazy" />'
    badge = "" if e["public"] else '<span class="badge-scheduled">Scheduled</span>'
    card_html.append(f"""    <article class="card">
      <div class="card-thumb">
        <a href="{yt_url}" target="_blank" rel="noopener">{thumb_inner}</a>
      </div>
      <div class="card-body">
        <span class="topic">#{e["topic"]}{badge}</span>
        <h3><a href="{yt_url}" target="_blank" rel="noopener">{title}</a></h3>
        <p class="blurb">{blurb_esc}</p>
        <a class="transcript-link" href="transcripts/{e['id']}.html" target="_blank">Transcript</a>
      </div>
    </article>""")
    if e["public"]:
        jsonld_items.append(f"""    {{
          "@type": "VideoObject",
          "name": "{title}",
          "description": "{blurb_esc}",
          "thumbnailUrl": "{thumb_url}",
          "uploadDate": "{e['date']}T00:00:00Z",
          "contentUrl": "{yt_url}",
          "embedUrl": "https://www.youtube.com/embed/{e['id']}",
          "author": {{ "@type": "Person", "name": "@0xRAGE.404", "url": "https://youtube.com/@0xRAGE.404" }}
        }}""")

og_image = f"https://i.ytimg.com/vi/{entries[0]['id']}/hqdefault.jpg" if entries else ""

html = f"""<!doctype html>
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
  <meta property="og:image" content="{og_image}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="@0xRAGE.404 \u2014 Rage-Bait Tech Shorts" />
  <meta name="twitter:description" content="{public_count} rage-bait tech shorts roasting everything wrong with your stack." />
  <meta name="twitter:image" content="{og_image}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Wallpoet&display=swap" rel="stylesheet" />
  <link rel="canonical" href="https://xxxn3m3s1sxxx.github.io/0xrage404-seo/" />
  <link rel="sitemap" type="application/xml" href="/0xrage404-seo/sitemap.xml" />
  <style>
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{background:#000;color:#0f0;font-family:'Wallpoet',monospace;min-height:100vh}}
    #matrix{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;opacity:.15;pointer-events:none}}
    header.banner{{position:relative;min-height:30vh;display:flex;align-items:center;justify-content:center;overflow:hidden;border-bottom:1px solid #0f033}}
    .banner-bg{{position:absolute;inset:0;background:radial-gradient(ellipse at center,#0f0,#000 70%)}}
    .banner-overlay{{position:absolute;inset:0;background:linear-gradient(180deg,transparent 60%,#000 100%)}}
    .banner-content{{position:relative;z-index:1;text-align:center;padding:2rem}}
    .banner-content h1{{font-size:5rem;letter-spacing:.15em;text-shadow:0 0 20px #0f0,0 0 40px #0f0;line-height:1}}
    .banner-content h1 .at{{font-size:.55em;vertical-align:middle;opacity:.6}}
    @media(max-width:768px){{.banner-content h1{{font-size:3.2rem}}}}
    .banner-tagline{{font-size:.9rem;opacity:.6;margin-top:.5rem;letter-spacing:.08em}}
    .subscribe-btn{{display:inline-block;margin-top:1.2rem;padding:.7rem 2rem;border:1px solid #0f0;border-radius:4px;color:#0f0;text-decoration:none;font-size:.85rem;letter-spacing:.1em;transition:all .2s}}
    .subscribe-btn:hover{{background:#0f0;color:#000}}
    .counter{{font-size:.7rem;opacity:.4;margin-top:1rem}}
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
    .transcript-link{{display:inline-block;margin-top:.4rem;font-size:.65rem;color:#0a0;opacity:.6;letter-spacing:.05em;text-decoration:none}}
    .transcript-link:hover{{color:#0f0}}
    footer{{position:relative;z-index:1;text-align:center;padding:2rem;border-top:1px solid #0f033;font-size:.75rem}}
    footer a{{color:#0f0}}
  </style>
</head>
<body>
  <canvas id="matrix"></canvas>
  <header class="banner">
    <div class="banner-bg"></div>
    <div class="banner-overlay"></div>
    <div class="banner-content">
      <h1><span class="at">@</span>0xRAGE.404</h1>
      <p class="banner-tagline">Rage-Bait Tech Shorts \u2014 daily developer hate</p>
      <a href="https://youtube.com/@0xRAGE.404" target="_blank" class="subscribe-btn">\u25b6 Subscribe</a>
      <p class="counter">{public_count} public \u00b7 {private_count} scheduled</p>
    </div>
  </header>
  <main id="videos">
{"\n".join(card_html)}
  </main>
  <footer>
    <p>Follow on <a href="https://youtube.com/@0xRAGE.404" target="_blank">YouTube</a></p>
  </footer>
  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
{",\n".join(jsonld_items)}
  ]
}}
</script>
  <script type="module" src="/src/main.ts"></script>
</body>
</html>"""

HTML_PATH.write_text(html, encoding="utf-8")
print(f"Generated index.html: {public_count} public, {private_count} scheduled")
