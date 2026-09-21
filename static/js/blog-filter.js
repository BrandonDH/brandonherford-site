// Lightweight React "island": Preact + htm loaded from a CDN (no build step,
// ~4KB). It enhances the server-rendered blog list with instant client-side
// search and tag filtering. If this module fails to load, the server-rendered
// list stays on the page — nothing breaks.
// htm/preact "standalone" is a single self-contained ESM bundle (preact + hooks
// + htm, ~4KB) with no bare imports — no import map or build step required.
import {
  html,
  render,
  useState,
  useMemo,
} from "https://cdn.jsdelivr.net/npm/htm@3.1.1/preact/standalone.module.js";

function readJSON(id) {
  const el = document.getElementById(id);
  try { return el ? JSON.parse(el.textContent) : []; } catch (_) { return []; }
}

function BlogApp({ posts, tags }) {
  const [query, setQuery] = useState("");
  const [activeTag, setActiveTag] = useState("");

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return posts.filter((p) => {
      const matchesTag = !activeTag || (p.tags || []).includes(activeTag);
      const matchesText =
        !q ||
        p.title.toLowerCase().includes(q) ||
        (p.summary || "").toLowerCase().includes(q);
      return matchesTag && matchesText;
    });
  }, [posts, query, activeTag]);

  return html`
    <div class="filter-bar">
      <input
        class="search-input"
        type="search"
        placeholder="Search posts…"
        value=${query}
        onInput=${(e) => setQuery(e.target.value)}
        aria-label="Search posts"
      />
      <div class="chips">
        <button
          class=${"chip " + (!activeTag ? "chip-active" : "")}
          onClick=${() => setActiveTag("")}
        >All</button>
        ${tags.map(
          (t) => html`
            <button
              class=${"chip " + (activeTag === t.slug ? "chip-active" : "")}
              onClick=${() => setActiveTag(t.slug)}
            >${t.name}</button>`
        )}
      </div>
    </div>

    ${filtered.length === 0
      ? html`<p class="empty">No posts match your filter.</p>`
      : html`
        <ul class="post-list">
          ${filtered.map(
            (p) => html`
              <li class="post-row" key=${p.url}>
                <a class="post-row-link" href=${p.url}>
                  <div class="post-row-main">
                    <h3 class="post-row-title">${p.title}</h3>
                    ${p.summary && html`<p class="post-row-summary">${p.summary}</p>`}
                  </div>
                  <time class="post-row-date" datetime=${p.iso_date}>${p.date}</time>
                </a>
              </li>`
          )}
        </ul>`}
  `;
}

const mount = document.getElementById("blog-app");
if (mount) {
  const posts = readJSON("posts-data");
  const tags = readJSON("tags-data");
  // Only take over the DOM if we actually have data to render.
  if (posts.length) {
    render(html`<${BlogApp} posts=${posts} tags=${tags} />`, mount);
  }
}
