import { VIDEOS, type Video } from "./videos.js";
import { MatrixRain } from "./matrix.js";
import "./style.css";

new MatrixRain().attach().start();

function jsonld(videos: Video[]): string {
  const items = videos.map((v) => ({
    "@context": "https://schema.org",
    "@type": "VideoObject",
    name: v.title,
    description: `${v.title} — Rage-Bait Tech Short von @0xRAGE404. Thema: ${v.topic}.`,
    thumbnailUrl: `https://i.ytimg.com/vi/${v.id}/hqdefault.jpg`,
    uploadDate: "2026-07-15",
    contentUrl: `https://www.youtube.com/watch?v=${v.id}`,
    embedUrl: `https://www.youtube.com/embed/${v.id}`,
    author: {
      "@type": "Person",
      name: "@0xRAGE404",
      url: "https://youtube.com/@0xRAGE404",
    },
    interactionStatistic: {
      "@type": "InteractionCounter",
      interactionType: "https://schema.org/WatchAction",
      userInteractionCount: 0,
    },
  }));
  const wrapper = {
    "@context": "https://schema.org",
    "@graph": items,
  };
  return `<script type="application/ld+json">${JSON.stringify(wrapper, null, 2)}<\/script>`;
}

function render() {
  const container = document.getElementById("videos")!;
  let html = "";
  for (const v of VIDEOS) {
    html += `<div class="card">
      <span class="topic">#${v.topic}</span>
      <h3><a href="https://www.youtube.com/watch?v=${v.id}" target="_blank" rel="noopener">${v.title}</a></h3>
    </div>`;
  }
  container.innerHTML = html;

  const script = document.createElement("script");
  script.type = "application/ld+json";
  script.textContent = JSON.stringify(
    {
      "@context": "https://schema.org",
      "@graph": VIDEOS.map((v) => ({
        "@type": "VideoObject",
        name: v.title,
        description: `${v.title} — Rage-Bait Tech Short von @0xRAGE404. Thema: ${v.topic}.`,
        thumbnailUrl: `https://i.ytimg.com/vi/${v.id}/hqdefault.jpg`,
        uploadDate: "2026-07-15",
        contentUrl: `https://www.youtube.com/watch?v=${v.id}`,
        embedUrl: `https://www.youtube.com/embed/${v.id}`,
        author: { "@type": "Person", name: "@0xRAGE404", url: "https://youtube.com/@0xRAGE404" },
      })),
    },
    null,
    2
  );
  document.head.appendChild(script);
}

document.addEventListener("DOMContentLoaded", render);
