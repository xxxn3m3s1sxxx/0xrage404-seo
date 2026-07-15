import { VIDEOS, type Video } from "./videos.js";
import { MatrixRain } from "./matrix.js";
import "./style.css";

new MatrixRain().attach().start();

function cardHTML(v: Video): string {
  const thumb = `https://i.ytimg.com/vi/${v.id}/hqdefault.jpg`;
  const img = v.thumb ? `<a href="https://www.youtube.com/watch?v=${v.id}" target="_blank" rel="noopener"><img src="${thumb}" alt="${v.title}" loading="lazy" /></a>` : "";
  return `<div class="card">
    <div class="card-thumb">
      <div class="fallback"><span>#${v.topic}</span></div>
      ${img}
    </div>
    <div class="card-body">
      <span class="topic">#${v.topic}</span>
      <h3><a href="https://www.youtube.com/watch?v=${v.id}" target="_blank" rel="noopener">${v.title}</a></h3>
      <p class="blurb">${v.blurb}</p>
    </div>
  </div>`;
}

function jsonld(videos: Video[]): string {
  const wrapper = {
    "@context": "https://schema.org",
    "@graph": videos.map((v) => ({
      "@type": "VideoObject",
      name: v.title,
      description: v.blurb,
      thumbnailUrl: `https://i.ytimg.com/vi/${v.id}/hqdefault.jpg`,
      uploadDate: "2026-07-15",
      contentUrl: `https://www.youtube.com/watch?v=${v.id}`,
      embedUrl: `https://www.youtube.com/embed/${v.id}`,
      author: {
        "@type": "Person",
        name: "@0xRAGE.404",
        url: "https://youtube.com/@0xRAGE.404",
      },
    })),
  };
  return `<script type="application/ld+json">${JSON.stringify(wrapper, null, 2)}<\/script>`;
}

function render() {
  const container = document.getElementById("videos")!;
  container.innerHTML = VIDEOS.map(cardHTML).join("");

  const script = document.createElement("script");
  script.type = "application/ld+json";
  script.textContent = JSON.stringify(
    {
      "@context": "https://schema.org",
      "@graph": VIDEOS.map((v) => ({
        "@type": "VideoObject",
        name: v.title,
        description: v.blurb,
        thumbnailUrl: `https://i.ytimg.com/vi/${v.id}/hqdefault.jpg`,
        uploadDate: "2026-07-15",
        contentUrl: `https://www.youtube.com/watch?v=${v.id}`,
        embedUrl: `https://www.youtube.com/embed/${v.id}`,
        author: { "@type": "Person", name: "@0xRAGE.404", url: "https://youtube.com/@0xRAGE.404" },
      })),
    },
    null,
    2
  );
  document.head.appendChild(script);
}

document.addEventListener("DOMContentLoaded", render);
