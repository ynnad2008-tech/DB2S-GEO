/* DB2S-GEO Curator Workbench — UX simplificada */

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => [...document.querySelectorAll(sel)];

function setStatus(msg, kind = "") {
  const el = $("#status");
  if (!el) return;
  el.textContent = msg || "";
  el.dataset.kind = kind || "";
}

function updateCandidatesCount(count) {
  const n = Number.isFinite(Number(count)) ? Number(count) : 0;
  const nav = $("#nav-admin");
  if (nav) {
    nav.textContent = n > 0 ? `Administración (${n})` : "Administración";
  }
  const label = $("#admin-candidates-count");
  if (label) {
    label.textContent =
      n === 1 ? "1 candidato para revisión" : `${n} candidatos para revisión`;
  }
}

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { Accept: "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail || JSON.stringify(body);
    } catch (_) {}
    throw new Error(`${res.status}: ${detail}`);
  }
  return res.json();
}

function esc(s) {
  return String(s ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function pills(items) {
  if (!items || !items.length) return "—";
  return items.map((x) => `<span class="pill">${esc(x)}</span>`).join("");
}

/* ---------- UX Sprint 1: etiquetas humanas (Q1–Q3) ---------- */
const resourceTitleCache = new Map();

const REASON_EXACT = {
  "fuente oficial nacional": "Es una fuente oficial nacional de Colombia.",
};

function titleFromResourceId(resourceId) {
  const id = String(resourceId || "");
  const leaf = id.includes(":") ? id.split(":").slice(1).join(":") : id;
  return leaf
    .replace(/[-_]+/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase())
    .trim() || id;
}

async function ensureResourceTitles(sourceId) {
  if (!sourceId) return {};
  if (resourceTitleCache.has(sourceId)) return resourceTitleCache.get(sourceId);
  try {
    const data = await api(`/sources/${encodeURIComponent(sourceId)}/resources`);
    const map = {};
    for (const r of data.resources || []) {
      if (r.resource_id) map[r.resource_id] = r.title || titleFromResourceId(r.resource_id);
    }
    resourceTitleCache.set(sourceId, map);
    return map;
  } catch (_) {
    const empty = {};
    resourceTitleCache.set(sourceId, empty);
    return empty;
  }
}

function lookupResourceTitle(resourceId, titleMap) {
  if (!resourceId) return "—";
  if (titleMap && titleMap[resourceId]) return titleMap[resourceId];
  for (const map of resourceTitleCache.values()) {
    if (map[resourceId]) return map[resourceId];
  }
  return titleFromResourceId(resourceId);
}

function humanReason(raw, titleMap) {
  const text = String(raw || "").trim();
  if (!text) return "";
  if (REASON_EXACT[text]) return REASON_EXACT[text];

  let m = text.match(/^keyword\s+(.+)$/i);
  if (m) {
    const topic = m[1].replace(/_/g, " ");
    return `Coincide con el tema «${topic}».`;
  }
  m = text.match(/^recurso\s+(.+)$/i);
  if (m) {
    const title = lookupResourceTitle(m[1], titleMap);
    return `Incluye el recurso «${title}».`;
  }
  m = text.match(/^fuente\s+(.+)$/i);
  if (m) return `La fuente «${m[1]}» coincide con su consulta.`;
  m = text.match(/^dominio\s+(.+)$/i);
  if (m) {
    const d = m[1].replace(/_/g, " ");
    return `Está asociada al dominio «${d}».`;
  }
  m = text.match(/^dominio compartido\s+(.+)$/i);
  if (m) {
    const d = m[1].replace(/_/g, " ");
    return `Comparte el dominio «${d}» con su consulta.`;
  }
  m = text.match(/^keyword compartida\s+(.+)$/i);
  if (m) {
    const topic = m[1].replace(/_/g, " ");
    return `Comparte el tema «${topic}» con su consulta.`;
  }
  m = text.match(/^contiene recurso\s+(.+)$/i);
  if (m) {
    const title = lookupResourceTitle(m[1], titleMap);
    return `Contiene el recurso «${title}».`;
  }
  return text;
}

function formatResourceLabels(resourceIds, titleMap, sourceId, limit = 3) {
  const ids = (resourceIds || []).slice(0, limit);
  if (!ids.length) return "—";
  return ids
    .map((id) => {
      const title = lookupResourceTitle(id, titleMap);
      return `<a href="#recommend" class="res-link" data-resource-id="${esc(id)}" data-source-id="${esc(sourceId || "")}" title="${esc(id)}">${esc(title)}</a>`;
    })
    .join("");
}

function reasonsHtml(reasons, titleMap, limit = 4) {
  const list = (reasons || []).slice(0, limit);
  if (!list.length) return "—";
  return list
    .map((x) => `<div class="reason-line">${esc(humanReason(x, titleMap))}</div>`)
    .join("");
}

function candidateStatusBadges(c) {
  const parts = [];
  if (c.already_registered) {
    parts.push('<span class="pill badge-registered">Ya en catálogo</span>');
  }
  const curation = c.curation || "human_required";
  if (curation === "human_required" && !c.already_registered) {
    parts.push('<span class="pill badge-pending">Pendiente de revisión</span>');
  } else if (curation === "human_required" && c.already_registered) {
    /* already shown Ya en catálogo */
  } else if (curation && curation !== "human_required") {
    parts.push(`<span class="pill">${esc(curation)}</span>`);
  }
  if (!parts.length) {
    parts.push('<span class="pill badge-pending">Pendiente de revisión</span>');
  }
  return parts.join(" ");
}

function showCandidateJson(payload) {
  const wrap = $("#cand-detail-wrap");
  const box = $("#cand-detail");
  if (!wrap || !box) return;
  box.textContent = JSON.stringify(payload, null, 2);
  wrap.hidden = false;
  wrap.open = false;
  wrap.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function renderRecommendRows(items, titleMapsBySource) {
  return items
    .map((r) => {
      const titleMap = titleMapsBySource[r.source_id] || {};
      return `
        <tr>
          <td><strong>${esc(r.score)}</strong></td>
          <td>
            <strong>${esc(r.source)}</strong>
            <div class="id-secondary">${esc(r.source_id)}</div>
          </td>
          <td>${reasonsHtml(r.reason, titleMap)}</td>
          <td class="res-cell">${formatResourceLabels(r.resources, titleMap, r.source_id)}</td>
        </tr>`;
    })
    .join("");
}

function renderRecommendCards(items, titleMapsBySource) {
  return items
    .map((r) => {
      const titleMap = titleMapsBySource[r.source_id] || {};
      return `
        <article class="rec-card">
          <div class="rec-card-head">
            <span class="rec-score">${esc(r.score)}</span>
            <div>
              <strong>${esc(r.source)}</strong>
              <div class="id-secondary">${esc(r.source_id)}</div>
            </div>
          </div>
          <div class="rec-card-block">
            <div class="rec-card-label">Por qué</div>
            ${reasonsHtml(r.reason, titleMap)}
          </div>
          <div class="rec-card-block">
            <div class="rec-card-label">Recursos</div>
            <div class="res-cell">${formatResourceLabels(r.resources, titleMap, r.source_id)}</div>
          </div>
        </article>`;
    })
    .join("");
}

function navigateToResource(resourceId, sourceId) {
  if (!resourceId) return;
  // Telemetría: clic de recurso (fire-and-forget)
  const payload = {
    resource_id: resourceId,
    source_id: sourceId || (String(resourceId).includes(":") ? String(resourceId).split(":")[0] : null),
  };
  fetch("/telemetry/click", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  }).catch(() => {});

  go("recommend");
  const mode = $("#rec-mode");
  const input = $("#rec-input");
  if (mode) mode.value = "resource";
  if (input) input.value = resourceId;
  runRecommend();
}

function openAdminGraphSection() {
  go("admin");
  const advanced = $("#panel-admin details.advanced");
  if (advanced) advanced.open = true;
  $$(".chip").forEach((c) => c.classList.toggle("active", c.dataset.adv === "graph"));
  $$(".adv-pane").forEach((p) => p.classList.toggle("active", p.id === "adv-graph"));
}

async function focusGraphView(kind) {
  openAdminGraphSection();
  await loadGraphAdvanced();
  const nodesSelect = $("#nodes-type");
  const relsSelect = $("#rels-type");
  if (kind === "relations") {
    if (nodesSelect) nodesSelect.value = "";
    if (relsSelect) relsSelect.value = "";
    await loadNodes();
    await loadRelations();
    $("#rels-body")?.closest(".split")?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    setStatus("Vista de relaciones del Knowledge Graph", "ok");
    return;
  }
  const typeMap = {
    institutions: "Institution",
    sources: "Source",
    resources: "Resource",
    domains: "Domain",
    keywords: "Keyword",
  };
  const nodeType = typeMap[kind];
  if (nodesSelect && nodeType) nodesSelect.value = nodeType;
  if (relsSelect) relsSelect.value = "";
  await loadNodes();
  await loadRelations();
  $("#nodes-body")?.closest(".split")?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  setStatus(`Vista de nodos: ${nodeType}`, "ok");
}

function setNavOpen(open) {
  const topbar = $(".topbar");
  const toggle = $("#nav-toggle");
  if (!topbar || !toggle) return;
  topbar.classList.toggle("nav-open", open);
  toggle.setAttribute("aria-expanded", open ? "true" : "false");
  toggle.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
}

function closeNav() {
  setNavOpen(false);
}

function go(panel) {
  $$(".nav-btn").forEach((b) => b.classList.toggle("active", b.dataset.panel === panel));
  $$(".panel").forEach((p) => p.classList.toggle("active", p.id === `panel-${panel}`));
  closeNav();
  loadPanel(panel);
}

function initNav() {
  $$(".nav-btn").forEach((btn) => {
    btn.addEventListener("click", () => go(btn.dataset.panel));
  });
  $$("[data-go]").forEach((el) => {
    el.addEventListener("click", (e) => {
      e.preventDefault();
      go(el.dataset.go);
    });
  });
  $("#nav-toggle")?.addEventListener("click", () => {
    setNavOpen(!$(".topbar")?.classList.contains("nav-open"));
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeNav();
  });
}

function loadPanel(name) {
  const map = {
    home: loadHome,
    explore: loadSources,
    recommend: () => setStatus("Escriba un tema y pulse Recomendar."),
    monitor: loadWatcher,
    observatory: loadObservatory,
    admin: () => {
      loadCandidates();
      loadGraphAdvanced();
    },
    about: () => setStatus("Acerca de DB2S-GEO · Alpha"),
    cite: loadCite,
    author: () => setStatus("Autoría · Dany Arbey Benavides"),
    support: () => setStatus("Apoya el desarrollo · aportes voluntarios"),
  };
  (map[name] || (() => {}))();
}

function loadCite() {
  const today = new Date().toISOString().slice(0, 10);
  const el = $("#cite-today");
  if (el) el.textContent = today;
  setStatus("Cómo citar · v0.9 Alpha");
}

async function loadAppMeta() {
  try {
    const info = await api("/");
    if (info.release && $("#app-version")) {
      $("#app-version").textContent = info.release;
    }
  } catch (_) {}
}

/* ---------- Inicio ---------- */
const DOMAIN_SOFT = {
  clima: "rgba(26, 90, 140, 0.55)",
  hidrologia: "rgba(10, 107, 88, 0.58)",
  biodiversidad: "rgba(46, 125, 50, 0.55)",
  oceanos_costas: "rgba(2, 119, 140, 0.55)",
  suelos: "rgba(121, 85, 45, 0.52)",
  agricultura: "rgba(85, 139, 47, 0.55)",
  poblacion: "rgba(94, 53, 177, 0.48)",
  observacion_tierra: "rgba(21, 101, 120, 0.55)",
  default: "rgba(63, 82, 75, 0.48)",
};

let homeCloudTimer = null;
let homeCloudItems = [];

function layoutHomeCloud(items, width, height) {
  const placed = [];
  const max = Math.min(items.length, width < 640 ? 16 : 24);

  for (let i = 0; i < max; i++) {
    const item = items[i];
    const weight = Number(item.weight) || 0;
    const sizePx = 11 + weight * (width < 640 ? 13 : 18);
    const estW = Math.max(36, (item.term || "").length * sizePx * 0.5);
    const estH = sizePx * 1.3;
    let x = width / 2;
    let y = height / 2;
    let ok = false;
    for (let attempt = 0; attempt < 50; attempt++) {
      const angle = (i * 2.399 + attempt * 0.47) % (Math.PI * 2);
      const ring = 0.18 + (i % 6) * 0.1 + attempt * 0.01;
      x = width / 2 + Math.cos(angle) * (width * ring * 0.42);
      y = height / 2 + Math.sin(angle) * (height * ring * 0.4);
      x = Math.max(estW / 2 + 6, Math.min(width - estW / 2 - 6, x));
      y = Math.max(estH / 2 + 6, Math.min(height - estH / 2 - 6, y));
      const clash = placed.some(
        (p) => Math.abs(p.x - x) < (p.w + estW) * 0.4 && Math.abs(p.y - y) < (p.h + estH) * 0.52
      );
      if (!clash) {
        ok = true;
        break;
      }
    }
    if (!ok) continue;
    placed.push({
      ...item,
      x: (x / width) * 100,
      y: (y / height) * 100,
      sizePx,
      w: estW,
      h: estH,
    });
  }
  return placed;
}

function renderHomeCloud(items) {
  const host = $("#home-cloud");
  if (!host) return;
  const rect = host.getBoundingClientRect();
  const w = Math.max(rect.width || 600, 280);
  const h = Math.max(rect.height || 360, 240);
  const laid = layoutHomeCloud(items, w, h);
  host.innerHTML = laid
    .map((t, i) => {
      const color = DOMAIN_SOFT[t.domain] || DOMAIN_SOFT.default;
      const opacity = t.emerging ? 0.92 : 0.38 + (Number(t.weight) || 0) * 0.45;
      const dur = 14 + (i % 7) * 2.2;
      const delay = (i % 5) * -1.4;
      const dx = ((i % 3) - 1) * 10;
      const dy = ((i % 4) - 1.5) * 8;
      return `<button type="button" class="hc-term" data-term="${esc(t.term)}"
        style="left:${t.x.toFixed(1)}%;top:${t.y.toFixed(1)}%;font-size:${t.sizePx}px;color:${color};opacity:${opacity.toFixed(2)};--hc-dur:${dur}s;--hc-delay:${delay}s;--hc-dx:${dx}px;--hc-dy:${dy}px;--hc-size:${t.sizePx}px"
        title="${esc(t.term)} · ${esc(t.count)} consultas">${esc(t.term)}</button>`;
    })
    .join("");

  host.querySelectorAll(".hc-term").forEach((btn) => {
    btn.addEventListener("click", () => {
      const term = btn.dataset.term;
      $("#home-q").value = term;
      go("recommend");
      $("#rec-mode").value = "q";
      $("#rec-input").value = term;
      runRecommend();
    });
  });
}

async function loadHomeCloud() {
  try {
    const data = await api("/observatory/wordcloud?limit=28");
    homeCloudItems = data.items || [];
    renderHomeCloud(homeCloudItems);
  } catch (_) {
    const host = $("#home-cloud");
    if (host && !host.innerHTML) {
      host.innerHTML = "";
    }
  }
}

function startHomeCloudRefresh() {
  if (homeCloudTimer) clearInterval(homeCloudTimer);
  homeCloudTimer = setInterval(() => {
    if ($("#panel-home")?.classList.contains("active")) {
      loadHomeCloud();
    }
  }, 45000);
}

function updateCandidatesNav(count) {
  updateCandidatesCount(count);
}

async function loadHome() {
  try {
    setStatus("Cargando resumen…");
    const [sources, graph, domains, watcher, candidates] = await Promise.all([
      api("/sources"),
      api("/graph/stats"),
      api("/domains"),
      api("/watcher/info"),
      api("/source-discovery/info"),
    ]);
    $("#m-sources").textContent = sources.count ?? "—";
    $("#m-resources").textContent = graph.resources ?? "—";
    $("#m-domains").textContent = domains.count ?? "—";
    $("#m-events").textContent = watcher.events ?? "—";
    $("#m-candidates").textContent = candidates.candidates ?? "—";
    updateCandidatesCount(candidates.candidates ?? 0);
    await loadHomeCloud();
    startHomeCloudRefresh();
    setStatus("");
  } catch (err) {
    setStatus(err.message, "error");
  }
}

/* ---------- Explorar ---------- */
async function loadSources() {
  try {
    setStatus("Cargando fuentes…");
    const q = $("#sources-q").value.trim();
    const domain = $("#sources-domain").value;
    const params = new URLSearchParams();
    if (q) params.set("q", q);
    if (domain) params.set("domain", domain);
    const qs = params.toString() ? `?${params}` : "";
    const data = await api(`/sources${qs}`);

    const select = $("#sources-domain");
    if (select.options.length <= 1) {
      const domains = await api("/domains");
      (domains.domains || []).forEach((d) => {
        const opt = document.createElement("option");
        opt.value = d.domain_id;
        opt.textContent = d.label || d.domain_id;
        select.appendChild(opt);
      });
    }

    const body = $("#sources-body");
    const rows = data.sources || [];
    body.innerHTML = rows.length
      ? rows
          .map(
            (s) => `
        <tr>
          <td><strong>${esc(s.source)}</strong><div class="mono">${esc(s.source_id)}</div></td>
          <td>${esc(s.institution)}</td>
          <td>${pills(s.domains)}</td>
          <td>${pills(s.access_methods)}</td>
          <td><span class="pill">${esc(s.status || "mvp")}</span></td>
        </tr>`
          )
          .join("")
      : `<tr><td colspan="5" class="empty">Sin fuentes</td></tr>`;
    setStatus(`${data.count} fuentes registradas`, "ok");
  } catch (err) {
    setStatus(err.message, "error");
  }
}

/* ---------- Recomendaciones ---------- */
async function runRecommend() {
  try {
    const mode = $("#rec-mode").value;
    const value = $("#rec-input").value.trim();
    if (!value) {
      setStatus("Indique un valor de consulta.", "error");
      return;
    }
    setStatus("Buscando recomendaciones…");
    let path = "";
    if (mode === "q") path = `/recommend?q=${encodeURIComponent(value)}`;
    else if (mode === "domain") path = `/recommend/domain/${encodeURIComponent(value)}`;
    else if (mode === "source") path = `/recommend/source/${encodeURIComponent(value)}`;
    else path = `/recommend/resource/${encodeURIComponent(value)}`;

    const data = await api(path);
    $("#rec-meta").textContent = `${data.count || 0} resultados · recomendaciones explicables`;
    const items = data.recommendations || [];

    const titleMapsBySource = {};
    await Promise.all(
      [...new Set(items.map((r) => r.source_id).filter(Boolean))].map(async (sid) => {
        titleMapsBySource[sid] = await ensureResourceTitles(sid);
      })
    );

    const body = $("#rec-body");
    const cards = $("#rec-cards");
    if (!items.length) {
      if (body) {
        body.innerHTML = `<tr><td colspan="4" class="empty">Sin recomendaciones</td></tr>`;
      }
      if (cards) cards.innerHTML = `<p class="empty">Sin recomendaciones</p>`;
    } else {
      if (body) body.innerHTML = renderRecommendRows(items, titleMapsBySource);
      if (cards) cards.innerHTML = renderRecommendCards(items, titleMapsBySource);
    }
    setStatus("Recomendaciones listas", "ok");
  } catch (err) {
    setStatus(err.message, "error");
  }
}

/* ---------- Monitoreo ---------- */
async function loadWatcher() {
  try {
    setStatus("Cargando eventos…");
    const type = $("#watcher-filter").value;
    const source = $("#watcher-source").value.trim();
    let path = "/watcher/events?limit=100";
    if (type) path = `/watcher/events/type/${encodeURIComponent(type)}?limit=100`;
    else if (source) path = `/watcher/events/${encodeURIComponent(source)}?limit=100`;

    const data = await api(path);
    let events = data.events || [];
    if (source && type) {
      events = events.filter((e) => e.source === source.toLowerCase());
    } else if (source && !type) {
      events = events.filter((e) => e.source === source.toLowerCase());
    }

    $("#watcher-body").innerHTML = events.length
      ? events
          .map(
            (e) => `
        <tr>
          <td class="mono">${esc(e.event_type)}</td>
          <td>${esc(e.source)}</td>
          <td class="mono">${esc(e.resource || "—")}</td>
          <td><span class="pill sev-${esc(e.severity)}">${esc(e.severity)}</span></td>
          <td class="mono">${esc((e.timestamp || "").replace("T", " ").slice(0, 19))}</td>
        </tr>`
          )
          .join("")
      : `<tr><td colspan="5" class="empty">Sin eventos todavía</td></tr>`;
    setStatus(`${events.length} eventos · sin auto-aplicación`, "ok");
  } catch (err) {
    setStatus(err.message, "error");
  }
}

async function runWatcher() {
  try {
    setStatus("Ejecutando monitoreo…");
    const data = await api("/watcher/run", { method: "POST" });
    setStatus(
      `Monitoreo OK · ${data.sources_checked} fuentes · ${data.events_detected} eventos nuevos`,
      "ok"
    );
    await loadWatcher();
  } catch (err) {
    setStatus(err.message, "error");
  }
}

/* ---------- Administración / candidatos ---------- */
async function loadCandidates() {
  try {
    setStatus("Cargando candidatos…");
    const data = await api("/source-discovery/candidates");
    const items = data.candidates || [];
    $("#cand-body").innerHTML = items.length
      ? items
          .map(
            (c) => `
        <tr data-id="${esc(c.id)}">
          <td>
            <strong>${esc(c.name)}</strong>
            <div class="url-secondary">${esc(c.url)}</div>
            <a href="#cand-detail-wrap" class="text-link cand-detail-link" data-id="${esc(c.id)}">Ver detalle</a>
          </td>
          <td>${esc(c.source_type)}</td>
          <td>${esc(c.institution)}</td>
          <td>${esc(c.confidence)}</td>
          <td class="cand-status">${candidateStatusBadges(c)}</td>
        </tr>`
          )
          .join("")
      : `<tr><td colspan="5" class="empty">Sin candidatos</td></tr>`;

    $$("#cand-body .cand-detail-link").forEach((link) => {
      link.addEventListener("click", async (e) => {
        e.preventDefault();
        e.stopPropagation();
        const detail = await api(`/source-discovery/candidates/${link.dataset.id}`);
        showCandidateJson(detail);
        setStatus(`Detalle de candidato · ${detail.name || link.dataset.id}`, "ok");
      });
    });
    setStatus(`${data.count} candidatos pendientes de curaduría`, "ok");
    updateCandidatesNav(data.count);
  } catch (err) {
    setStatus(err.message, "error");
  }
}

async function analyzeCandidate() {
  try {
    const url = $("#cand-url").value.trim();
    if (!url) {
      setStatus("Indique una URL.", "error");
      return;
    }
    setStatus("Analizando URL…");
    const data = await api("/source-discovery/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, persist: true }),
    });
    showCandidateJson(data);
    setStatus(`Propuesta: ${data.name} · confianza ${data.confidence}`, "ok");
    await loadCandidates();
  } catch (err) {
    setStatus(err.message, "error");
  }
}

/* ---------- Avanzado: Knowledge Graph ---------- */
async function loadGraphAdvanced() {
  try {
    const stats = await api("/graph/stats");
    const keys = [
      ["institutions", "Instituciones"],
      ["sources", "Fuentes"],
      ["resources", "Recursos"],
      ["domains", "Dominios"],
      ["keywords", "Keywords"],
      ["relations", "Relaciones"],
    ];
    $("#graph-stats").innerHTML = keys
      .map(
        ([k, label]) => `
      <button type="button" class="stat stat-link" data-graph-view="${esc(k)}" title="Ver ${esc(label)}">
        <span class="n">${esc(stats[k] ?? 0)}</span>
        <span class="l">${label}</span>
      </button>`
      )
      .join("");
    $$("#graph-stats .stat-link").forEach((btn) => {
      btn.addEventListener("click", () => {
        focusGraphView(btn.dataset.graphView).catch((e) => setStatus(e.message, "error"));
      });
    });
    await loadNodes();
    await loadRelations();
  } catch (_) {
    /* silencioso en admin hasta abrir avanzado */
  }
}

async function loadNodes() {
  const type = $("#nodes-type").value;
  const qs = type ? `?type=${encodeURIComponent(type)}` : "";
  const data = await api(`/graph/nodes${qs}`);
  const rows = (data.nodes || []).slice(0, 150);
  $("#nodes-body").innerHTML = rows.length
    ? rows
        .map(
          (n) => `
      <tr>
        <td class="mono">${esc(n.id)}</td>
        <td>${esc(n.type)}</td>
        <td>${esc(n.label)}</td>
      </tr>`
        )
        .join("")
    : `<tr><td colspan="3" class="empty">Sin nodos</td></tr>`;
}

async function loadRelations() {
  const type = $("#rels-type").value;
  const qs = type ? `?type=${encodeURIComponent(type)}` : "";
  const data = await api(`/graph/relations${qs}`);
  const rows = (data.relations || []).slice(0, 150);
  $("#rels-body").innerHTML = rows.length
    ? rows
        .map(
          (r) => `
      <tr>
        <td class="mono">${esc(r.type)}</td>
        <td class="mono">${esc(r.from_id)}</td>
        <td class="mono">${esc(r.to_id)}</td>
      </tr>`
        )
        .join("")
    : `<tr><td colspan="3" class="empty">Sin relaciones</td></tr>`;
}

/* ---------- Observatorio ---------- */
async function loadObservatory() {
  try {
    setStatus("Cargando observatorio…");
    const data = await api("/observatory/dashboard");
    const s = data.summary || {};
    $("#obs-summary").textContent =
      `${s.total_queries || 0} consultas · ${s.without_results || 0} sin resultado · anónimo`;

    const cloud = $("#obs-cloud");
    const words = Array.isArray(data.wordcloud) ? data.wordcloud : data.wordcloud?.items || [];
    if (!words.length) {
      cloud.innerHTML = `<p class="empty">Aún no hay términos. Use Recomendaciones o Decision Support.</p>`;
    } else {
      // Posiciones deterministas (sin solapamiento extremo) para aspecto de nube
      const slots = [
        [50, 48], [22, 28], [78, 30], [35, 68], [68, 72],
        [18, 55], [82, 58], [42, 22], [60, 20], [30, 42],
        [70, 45], [48, 78], [12, 40], [88, 42], [55, 60],
        [25, 75], [75, 18], [40, 55], [62, 38], [15, 68],
        [85, 70], [33, 18], [58, 82], [45, 35], [72, 62],
        [20, 20], [80, 80], [38, 82], [65, 28], [28, 58],
        [52, 15], [18, 82], [86, 25], [10, 52], [90, 55], [48, 92],
      ];
      cloud.innerHTML = words
        .slice(0, slots.length)
        .map((w, i) => {
          const weight = Number(w.weight) || 0;
          const size = (0.85 + weight * 1.55).toFixed(2);
          const [x, y] = slots[i];
          const tone = i % 4;
          return `<span class="wc-tag tone-${tone}" style="left:${x}%;top:${y}%;font-size:${size}rem" title="${esc(w.count)} apariciones">${esc(w.term)}</span>`;
        })
        .join("");
    }
    const timeline = data.timeline || [];
    const maxC = Math.max(1, ...timeline.map((d) => d.count || 0));
    $("#obs-timeline").innerHTML = timeline.length
      ? timeline
          .map((d) => {
            const h = Math.max(2, Math.round(((d.count || 0) / maxC) * 100));
            const day = (d.date || "").slice(5);
            const cls = d.count === 0 ? "bar empty-only" : "bar";
            return `<div class="bar-wrap" title="${esc(d.date)}: ${d.count}"><div class="${cls}" style="height:${h}%"></div><span class="lbl">${esc(day)}</span></div>`;
          })
          .join("")
      : `<p class="empty">Sin serie temporal</p>`;

    const top = data.top_queries || [];
    $("#obs-top").innerHTML = top.length
      ? top.map((r) => `<tr><td>${esc(r.query)}</td><td class="mono">${esc(r.count)}</td></tr>`).join("")
      : `<tr><td colspan="2" class="empty">Sin datos</td></tr>`;

    const empty = data.empty_queries || [];
    $("#obs-empty").innerHTML = empty.length
      ? empty.map((r) => `<tr><td>${esc(r.query)}</td><td class="mono">${esc(r.count)}</td></tr>`).join("")
      : `<tr><td colspan="2" class="empty">Sin vacíos registrados</td></tr>`;

    const domains = data.domains || [];
    const maxD = Math.max(1, ...domains.map((d) => d.count || 0));
    $("#obs-domains").innerHTML = domains.length
      ? domains
          .map((d) => {
            const pct = Math.round(((d.count || 0) / maxD) * 100);
            return `<div class="rank-row"><span class="name">${esc(d.domain)}</span><div class="track"><div class="fill" style="width:${pct}%"></div></div><span class="n">${esc(d.count)}</span></div>`;
          })
          .join("")
      : `<p class="empty">Sin dominios aún</p>`;

    const emerging = data.emerging || [];
    $("#obs-emerging").innerHTML = emerging.length
      ? emerging.map((r) => `<tr><td>${esc(r.term)}</td><td class="mono">${esc(r.count)}</td></tr>`).join("")
      : `<tr><td colspan="2" class="empty">Sin señales emergentes</td></tr>`;

    setStatus("Observatorio listo · registro anónimo activo", "ok");
  } catch (err) {
    setStatus(err.message, "error");
  }
}

function initAdvancedTabs() {
  $$(".chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      $$(".chip").forEach((c) => c.classList.remove("active"));
      chip.classList.add("active");
      $$(".adv-pane").forEach((p) => p.classList.remove("active"));
      $(`#adv-${chip.dataset.adv}`).classList.add("active");
      if (chip.dataset.adv === "graph") loadGraphAdvanced();
    });
  });
}

function boot() {
  initNav();
  initAdvancedTabs();

  $("#sources-refresh")?.addEventListener("click", loadSources);
  $("#sources-q")?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") loadSources();
  });
  $("#sources-domain")?.addEventListener("change", loadSources);

  $("#rec-run")?.addEventListener("click", runRecommend);
  $("#rec-input")?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") runRecommend();
  });

  $("#watcher-refresh")?.addEventListener("click", loadWatcher);
  $("#watcher-run")?.addEventListener("click", runWatcher);
  $("#watcher-filter")?.addEventListener("change", loadWatcher);

  $("#obs-refresh")?.addEventListener("click", loadObservatory);

  $("#cand-refresh")?.addEventListener("click", loadCandidates);
  $("#cand-analyze")?.addEventListener("click", analyzeCandidate);
  $("#cand-url")?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") analyzeCandidate();
  });

  $("#nodes-refresh")?.addEventListener("click", () =>
    loadNodes().catch((e) => setStatus(e.message, "error"))
  );
  $("#rels-refresh")?.addEventListener("click", () =>
    loadRelations().catch((e) => setStatus(e.message, "error"))
  );
  $("#nodes-type")?.addEventListener("change", () =>
    loadNodes().catch((e) => setStatus(e.message, "error"))
  );
  $("#rels-type")?.addEventListener("change", () =>
    loadRelations().catch((e) => setStatus(e.message, "error"))
  );

  $("#home-search-form")?.addEventListener("submit", (e) => {
    e.preventDefault();
    const q = $("#home-q")?.value.trim();
    if (!q) return;
    runHomeAdvice(q).catch((err) => setStatus(err.message, "error"));
  });

  document.addEventListener("click", (e) => {
    const resLink = e.target.closest?.(".res-link");
    if (!resLink) return;
    e.preventDefault();
    navigateToResource(resLink.dataset.resourceId, resLink.dataset.sourceId);
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 768) closeNav();
    if (homeCloudItems.length && $("#panel-home")?.classList.contains("active")) {
      renderHomeCloud(homeCloudItems);
    }
  });

  loadAppMeta();
  loadHome();
}

async function runHomeAdvice(q) {
  const box = $("#home-advice");
  if (!box) return;
  box.hidden = false;
  box.innerHTML = `<p class="home-advice-loading">Orientando con el catálogo curado…</p>`;
  setStatus("Orientando…");
  const data = await api(`/decision-support?q=${encodeURIComponent(q)}&limit=4`);
  const routes = data.routes || [];
  if (!routes.length) {
    box.innerHTML = `
      <p class="empty">No encontré rutas claras. Pruebe con más contexto o revise el ranking de fuentes.</p>
      <button type="button" class="btn" data-go="recommend">Abrir recomendaciones</button>`;
    setStatus("Sin rutas de orientación", "error");
    return;
  }
  box.innerHTML = `
    <div class="home-advice-head">
      <h2>Orientación</h2>
      <p>${esc(data.count || routes.length)} rutas · Decision Support (explicable, sin LLM)</p>
    </div>
    <div class="home-advice-list">
      ${routes
        .map(
          (r) => `
        <article class="advice-card">
          <p class="advice-rank">#${esc(r.rank)} · ${esc(r.score ?? "—")}</p>
          <h3>${esc(r.title || r.source || r.source_id)}</h3>
          <p class="advice-what"><strong>Qué hacer:</strong> ${esc(r.what_to_do || "—")}</p>
          <p class="advice-source"><strong>Fuente:</strong> ${esc(r.source || r.source_id)} · ${esc(r.institution || "")}</p>
          <p class="advice-why"><strong>Por qué:</strong> ${esc((r.why || []).slice(0, 2).join(" · ") || "—")}</p>
          <p class="advice-res">${pills((r.resources || []).map((x) => x.resource_id || x.title).filter(Boolean).slice(0, 4))}</p>
        </article>`
        )
        .join("")}
    </div>
    <div class="home-advice-actions">
      <button type="button" class="btn" id="home-to-rec">Ver ranking completo</button>
    </div>`;
  $("#home-to-rec")?.addEventListener("click", () => {
    go("recommend");
    $("#rec-mode").value = "q";
    $("#rec-input").value = q;
    runRecommend();
  });
  setStatus("Orientación lista", "ok");
}

document.addEventListener("DOMContentLoaded", boot);
