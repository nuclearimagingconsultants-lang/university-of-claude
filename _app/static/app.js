/* University of Claude - study app.
   Reads /api/program (generated from whatever is built) and keeps per-module
   progress in /api/progress. No framework, no build step. */

let P = null;          // program index
let PROG = {modules:{}, notes:{}};
const $ = s => document.querySelector(s);
const el = (t, c, h) => { const n = document.createElement(t);
  if (c) n.className = c; if (h !== undefined) n.innerHTML = h; return n; };
const esc = s => (s || "").replace(/[&<>"]/g,
  c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const key = (code, n) => code + "/" + n;
const slugId = code => code.replace(/\s+/g, "-");

/* --------------------------------------------------------------- loading */
async function boot() {
  const [p, g] = await Promise.all([
    fetch("/api/program").then(r => r.json()),
    fetch("/api/progress").then(r => r.json()).catch(() => PROG)
  ]);
  if (p.error) { $("#main").innerHTML =
    `<div class="card"><h2>Index missing</h2><p class="muted">${esc(p.error)}</p></div>`;
    return; }
  P = p; PROG = g;
  $("#gen").textContent = "index generated " + P.generated.replace("T", " ");
  $("#brandsub").textContent =
    `${P.program.degree} · ${P.program.track}`;
  drawSide(); route();
}

/* ------------------------------------------------------------ progress io */
function statusOf(code, n) { return PROG.modules[key(code, n)] || "none"; }
function noteOf(code, n)   { return PROG.notes[key(code, n)] || ""; }

async function setStatus(code, n, state) {
  const k = key(code, n);
  if (state === "none") delete PROG.modules[k]; else PROG.modules[k] = state;
  PROG = await fetch("/api/progress", {method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({key:k, state})}).then(r => r.json());
  drawSide(); route(true);
}

let noteTimer = null;
function setNote(code, n, text) {
  clearTimeout(noteTimer);
  noteTimer = setTimeout(async () => {
    const k = key(code, n);
    PROG = await fetch("/api/progress", {method:"POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({key:k, state: PROG.modules[k] || "none",
                            note:text})}).then(r => r.json());
    toast("note saved");
  }, 700);
}

/* ------------------------------------------------------------------ open */
async function openFile(path) {
  if (!path) return;
  const r = await fetch("/api/open", {method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({path})}).then(r => r.json());
  toast(r.error ? "could not open: " + r.error : "opening " + r.opened);
}

let toastTimer = null;
function toast(msg) {
  const t = $("#toast"); t.textContent = msg; t.hidden = false;
  clearTimeout(toastTimer); toastTimer = setTimeout(() => t.hidden = true, 2200);
}

/* -------------------------------------------------------------- helpers */
function courseByCode(code) { return P.courses.find(c => c.code === code); }

function courseProgress(c) {
  if (!c.built || !c.modules.length) return {done:0, doing:0, total:0, pct:0};
  let done = 0, doing = 0;
  for (const m of c.modules) {
    const s = statusOf(c.code, m.n);
    if (s === "done") done++; else if (s === "doing") doing++;
  }
  return {done, doing, total:c.modules.length,
          pct: Math.round(100 * done / c.modules.length)};
}

function nextModule() {
  for (const c of P.courses) {
    if (!c.built) continue;
    for (const m of c.modules)
      if (statusOf(c.code, m.n) !== "done") return {c, m};
  }
  return null;
}

/* ---------------------------------------------------------------- sidebar */
function drawSide() {
  const side = $("#side"); side.innerHTML = "";
  const hash = location.hash;
  for (const s of P.semesters) {
    const inner = P.courses.filter(c => c.sem === s.n);
    const wrap = el("div", "phase-" + s.phase);
    const h = el("button", "semhead");
    h.innerHTML = `<span>S${s.n}</span><span class="lbl">${esc(s.label)}</span>` +
                  `<span class="cnt">${s.built}/${s.total}</span>`;
    const ul = el("ul", "clist");
    for (const c of inner) {
      const li = el("li");
      const a = el("a", c.built ? "" : "unbuilt");
      a.href = c.built ? "#/c/" + slugId(c.code) : "#/";
      const pr = courseProgress(c);
      a.innerHTML = `<span class="code">${esc(c.code)}</span>${esc(c.title)}` +
        (c.built && pr.done
          ? ` <span class="cnt" style="color:var(--accent2)">${pr.done}/${pr.total}</span>`
          : "");
      if (hash.startsWith("#/c/" + slugId(c.code)) ||
          hash.startsWith("#/m/" + slugId(c.code) + "/")) a.classList.add("on");
      li.appendChild(a); ul.appendChild(li);
    }
    h.onclick = () => { ul.hidden = !ul.hidden; };
    wrap.appendChild(h); wrap.appendChild(ul); side.appendChild(wrap);
  }
}

/* ----------------------------------------------------------------- routes */
function route(keepScroll) {
  const y = keepScroll ? window.scrollY : 0;
  const h = location.hash || "#/";
  const m = h.match(/^#\/m\/([^/]+)\/(\d+)$/);
  const c = h.match(/^#\/c\/([^/]+)$/);
  if (m) viewModule(m[1].replace(/-/g, " "), +m[2]);
  else if (c) viewCourse(c[1].replace(/-/g, " "));
  else viewHome();
  drawSide();
  window.scrollTo(0, y);
}
window.addEventListener("hashchange", () => {
  // Leaving a result list for a real page: drop the query, or the box
  // claims to be filtering something it is no longer showing.
  if ($("#search").value) $("#search").value = "";
  route();
});

/* ------------------------------------------------------------------ home */
function viewHome() {
  const main = $("#main"); main.innerHTML = "";
  const st = P.stats;

  const hero = el("div", "card");
  hero.innerHTML =
    `<h2>Where you are</h2>
     <div class="statrow" style="margin-top:12px">
       <div class="stat"><b>${st.courses_built}</b><span>courses built</span></div>
       <div class="stat"><b>${st.modules}</b><span>modules</span></div>
       <div class="stat"><b>${doneCount()}</b><span>modules complete</span></div>
       <div class="stat"><b>${st.exercises}</b><span>exercises</span></div>
     </div>`;
  main.appendChild(hero);

  const nx = nextModule();
  if (nx) {
    const card = el("div", "card");
    card.innerHTML =
      `<h2>Continue</h2>
       <p class="small muted" style="margin:2px 0 0">
         ${esc(nx.c.code)} &middot; ${esc(nx.c.title)}</p>
       <h3 style="font-size:18px;margin-top:8px">
         Module ${String(nx.m.n).padStart(2,"0")} &mdash; ${esc(nx.m.title)}</h3>
       <p class="q-big">${esc(nx.m.question)}</p>
       <div class="openrow">
         <a class="open primary" href="#/m/${slugId(nx.c.code)}/${nx.m.n}">
           Go to module</a>
         <button class="open" data-open="${esc(nx.m.slides || "")}">Slides</button>
         <button class="open" data-open="${esc(nx.m.notes || "")}">Notes</button>
       </div>`;
    main.appendChild(card);
  }

  for (const phase of ["prerequisite", "degree", "continuation"]) {
    const sems = P.semesters.filter(s => s.phase === phase);
    if (!sems.length) continue;
    const card = el("div", "card");
    const label = {prerequisite:"Prerequisites", degree:"The degree — Semesters 1 to 4",
                   continuation:"Continuation — Semester 5 onward"}[phase];
    let html = `<h2>${label}</h2>`;
    for (const s of sems) {
      const cs = P.courses.filter(x => x.sem === s.n);
      const built = cs.filter(x => x.built);
      const tot = built.reduce((a, c) => a + c.modules.length, 0);
      const dn = built.reduce((a, c) => a + courseProgress(c).done, 0);
      html += `<div style="margin:14px 0 0">
        <div style="display:flex;gap:10px;align-items:baseline">
          <b>S${s.n}</b><span>${esc(s.label)}</span>
          <span class="cnt small muted" style="margin-left:auto">
            ${tot ? dn + "/" + tot + " modules" : s.built + "/" + s.total + " built"}</span>
        </div>
        <div class="bar thin" style="margin-top:6px"><i style="width:${
          tot ? Math.round(100*dn/tot) : 0}%"></i></div>
        <div class="small muted" style="margin-top:6px">${
          cs.map(c => c.built
            ? `<a href="#/c/${slugId(c.code)}">${esc(c.code)}</a>`
            : `<span style="color:var(--faint)">${esc(c.code)}</span>`).join(" &middot; ")
        }</div></div>`;
    }
    card.innerHTML = html; main.appendChild(card);
  }
}

function doneCount() {
  return Object.values(PROG.modules).filter(v => v === "done").length;
}

/* ---------------------------------------------------------------- course */
function viewCourse(code) {
  const c = courseByCode(code);
  const main = $("#main"); main.innerHTML = "";
  if (!c || !c.built) {
    main.innerHTML = `<div class="card"><h2>Not built yet</h2>
      <p class="muted">${esc(code)} is planned but has no materials.</p>
      <p><a href="#/">Back to overview</a></p></div>`;
    return;
  }
  const pr = courseProgress(c);

  const head = el("div", "card");
  head.innerHTML =
    `<div class="crumb"><a href="#/">Overview</a> &rsaquo; Semester ${c.sem}</div>
     <h2 style="font-size:22px">${esc(c.code)} &mdash; ${esc(c.title)}</h2>
     <p class="tagline">${esc(c.tagline)}</p>
     <div class="bar" style="margin:16px 0 6px"><i style="width:${pr.pct}%"></i></div>
     <p class="small muted">${pr.done} of ${pr.total} modules complete${
       pr.doing ? ", " + pr.doing + " in progress" : ""}</p>
     <dl class="meta">
       <dt>Term</dt><dd>${esc(c.term)}</dd>
       <dt>Effort</dt><dd>${esc(c.effort)}</dd>
       <dt>Prerequisites</dt><dd>${esc(c.prereqs)}</dd>
       <dt>Deliverable</dt><dd>${esc(c.deliverable)}</dd>
     </dl>
     <div class="openrow">
       <button class="open" data-open="${esc(c.syllabus || "")}">Syllabus</button>
       <button class="open" data-open="${esc(c.resource_map || "")}">Resource map</button>
     </div>`;
  main.appendChild(head);

  if (c.outcomes.length) {
    const o = el("div", "card");
    o.innerHTML = `<h2>What you will be able to do</h2>
      <ul class="tight small">${c.outcomes.map(x => `<li>${esc(x)}</li>`).join("")}</ul>`;
    main.appendChild(o);
  }

  const mod = el("div", "card");
  let rows = "";
  for (const m of c.modules) {
    const s = statusOf(c.code, m.n);
    rows += `<tr>
      <td class="n">${String(m.n).padStart(2, "0")}</td>
      <td class="ti"><a href="#/m/${slugId(c.code)}/${m.n}">${esc(m.title)}</a>
        <span class="q">${esc(m.question)}</span></td>
      <td class="st"><button class="pill ${s === "none" ? "" : s}"
        data-cycle="${esc(c.code)}|${m.n}">${
          s === "done" ? "done" : s === "doing" ? "doing" : "mark"}</button></td>
    </tr>`;
  }
  mod.innerHTML = `<h2>Modules</h2><table class="mods">${rows}</table>`;
  main.appendChild(mod);
}

/* ---------------------------------------------------------------- module */
function viewModule(code, n) {
  const c = courseByCode(code);
  const main = $("#main"); main.innerHTML = "";
  if (!c || !c.built) { location.hash = "#/"; return; }
  const m = c.modules.find(x => x.n === n);
  if (!m) { location.hash = "#/c/" + slugId(code); return; }
  const s = statusOf(c.code, m.n);
  const prev = c.modules.find(x => x.n === n - 1);
  const next = c.modules.find(x => x.n === n + 1);

  const head = el("div", "card");
  head.innerHTML =
    `<div class="crumb"><a href="#/">Overview</a> &rsaquo;
      <a href="#/c/${slugId(c.code)}">${esc(c.code)}</a> &rsaquo;
      Module ${String(m.n).padStart(2, "0")} of ${c.modules.length}</div>
     <h2 style="font-size:22px">${esc(m.title)}</h2>
     <p class="muted" style="margin-top:4px">${esc(m.subtitle)}</p>
     <p class="q-big">${esc(m.question)}</p>
     <div class="openrow">
       <button class="open primary" data-open="${esc(m.slides || "")}"
         ${m.slides ? "" : "disabled"}>Open slides &middot; ${m.n_slides}</button>
       <button class="open" data-open="${esc(m.notes || "")}"
         ${m.notes ? "" : "disabled"}>Open notes</button>
       <button class="pill ${s === "none" ? "" : s}" style="padding:9px 14px"
         data-cycle="${esc(c.code)}|${m.n}">${
           s === "done" ? "done" : s === "doing" ? "in progress" : "mark status"}</button>
     </div>`;
  main.appendChild(head);

  const cols = el("div", "cols");
  if (m.outcomes.length) {
    const a = el("div", "card");
    a.innerHTML = `<h2>Outcomes</h2><ul class="tight small">${
      m.outcomes.map(x => `<li>${esc(x)}</li>`).join("")}</ul>`;
    cols.appendChild(a);
  }
  if (m.takeaways.length) {
    const b = el("div", "card");
    b.innerHTML = `<h2>Carry forward</h2><ul class="tight small">${
      m.takeaways.map(x => `<li>${esc(x)}</li>`).join("")}</ul>`;
    cols.appendChild(b);
  }
  if (cols.children.length) main.appendChild(cols);

  if (m.selfcheck.length) {
    const sc = el("div", "card");
    sc.innerHTML = `<h2>Self-check</h2>
      <p class="small muted">Answer these without the notes open.
        ${m.n_exercises} exercises and ${m.n_resources} linked resources are in
        the deck and notes.</p>
      <ol class="tight small">${m.selfcheck.map(x => `<li>${esc(x)}</li>`).join("")}</ol>`;
    main.appendChild(sc);
  }

  const nt = el("div", "card");
  nt.innerHTML = `<h2>Your notes</h2>
    <textarea class="note" id="note" placeholder="What did you build? What is still unclear?"></textarea>
    <p class="small muted" style="margin:6px 0 0">Saved automatically to
      <code>_app/data/progress.json</code>.</p>`;
  main.appendChild(nt);
  const ta = $("#note"); ta.value = noteOf(c.code, m.n);
  ta.addEventListener("input", () => setNote(c.code, m.n, ta.value));

  const nav = el("div", "openrow");
  if (prev) nav.appendChild(mkLink("&larr; " + prev.title,
    `#/m/${slugId(c.code)}/${prev.n}`));
  if (next) nav.appendChild(mkLink(next.title + " &rarr;",
    `#/m/${slugId(c.code)}/${next.n}`));
  main.appendChild(nav);
}

function mkLink(html, href) {
  const a = el("a", "open", html); a.href = href; return a;
}

/* ---------------------------------------------------------------- search */
function doSearch(q) {
  q = q.trim().toLowerCase();
  if (!q) { route(); return; }
  const hits = [];
  for (const c of P.courses) {
    if (!c.built) continue;
    if ((c.code + " " + c.title + " " + c.tagline).toLowerCase().includes(q))
      hits.push({href:"#/c/" + slugId(c.code), t:c.code + " — " + c.title,
                 w:"Course · Semester " + c.sem});
    for (const m of c.modules) {
      const head = (m.title + " " + m.subtitle + " " + m.question).toLowerCase();
      // Fall back to the module's substance, so a term that only appears in
      // a takeaway or an outcome is still findable.
      const body = (m.takeaways.join(" ") + " " + m.outcomes.join(" ") + " " +
                    m.selfcheck.join(" ")).toLowerCase();
      if (!head.includes(q) && !body.includes(q)) continue;
      const where = head.includes(q)
        ? m.question
        : (m.takeaways.concat(m.outcomes, m.selfcheck)
             .find(t => t.toLowerCase().includes(q)) || m.question);
      hits.push({href:`#/m/${slugId(c.code)}/${m.n}`,
                 t:`M${String(m.n).padStart(2,"0")} ${m.title}`,
                 w:c.code + " · " + where});
    }
    if (hits.length > 120) break;
  }
  const main = $("#main");
  main.innerHTML = `<div class="card"><h2>${hits.length} result${
    hits.length === 1 ? "" : "s"} for “${esc(q)}”</h2>
    ${hits.map(h => `<a class="hit" href="${h.href}">${esc(h.t)}
      <span class="where">${esc(h.w)}</span></a>`).join("") ||
      '<p class="muted small">Nothing matched.</p>'}</div>`;
}

/* ----------------------------------------------------------------- events */
document.addEventListener("click", e => {
  const o = e.target.closest("[data-open]");
  if (o) { const p = o.getAttribute("data-open");
    if (p) openFile(p); else toast("no file for that yet"); return; }
  const cy = e.target.closest("[data-cycle]");
  if (cy) {
    const [code, n] = cy.getAttribute("data-cycle").split("|");
    const cur = statusOf(code, +n);
    setStatus(code, +n, cur === "none" ? "doing" : cur === "doing" ? "done" : "none");
  }
});

$("#search").addEventListener("input", e => doSearch(e.target.value));
$("#reindex").addEventListener("click", async () => {
  toast("reindexing…");
  await fetch("/api/reindex", {method:"POST"});
  await boot(); toast("index refreshed");
});
document.addEventListener("keydown", e => {
  if (e.key === "/" && document.activeElement.tagName !== "INPUT" &&
      document.activeElement.tagName !== "TEXTAREA") {
    e.preventDefault(); $("#search").focus();
  }
  if (e.key === "Escape" && document.activeElement === $("#search")) {
    $("#search").value = ""; $("#search").blur(); route();
  }
});

boot();
