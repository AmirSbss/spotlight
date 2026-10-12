// spotlight render kit. Every frame is a pure function of t (see SKILL.md, "The page").
// timeline.js loads first and sets:
//   window.SPOTLIGHT = { width, height, duration, end, grain, fonts, shots: [...] }
// shots, in order, each { a, b } in seconds plus one of:
//   clip: "frames/s01", n: 65          frames written by `footage.py shot`
//   still: "stills/004.jpg"            a photo, an AI image or a background still
//   web: "site/full.png", scroll: [y0, y1]   a captured page drawn at the output width and scrolled at a constant
//                          speed (output px); push, filter and grade work on it too
//   three: "three/routes.js", params: {...}   a Three.js scene (copy <skill-dir>/kit/three/ to work/three/). The module
//                          exports create(canvas, params, { width, height, css }) -> { render(tLocal, p) }; render draws
//                          synchronously and may return { anchors: { id: [x, y, alpha] } } (output px): every element
//                          with data-anchor="id" is centred there at that opacity, so labels are DOM text in any script
//   drift: [x0, x1]        horizontal drift in % of width. Stills move linearly: a photo defaults to push 1 +0.01/s;
//                          a still with a `filter` (text-card backdrop) to push 1.10 +0.08/s and drift 0 +4%/s
// and optionally:
//   panel: true            show the whole frame in a panel over a blurred copy (other-aspect media)
//   push: [from, to]       scale over the shot (clips: [1, 1.025], eased; stills: see drift); origin: "50% 64%"
//   filter: "blur(16px) brightness(.42)"   CSS filter (e.g. a dimmed background behind a text card)
//   grade: "saturate(.9) contrast(1.05)"   colour match for AI stills and photos next to footage
//   grain: 0.12            film grain for this shot (SPOTLIGHT.grain sets it for every shot)
//   dip: 0.3               a transition into this shot: a dip through black (or dipColor: "#E4B53B") over 0.3 s
//                          centred on the cut, so two busy shots never cross-dissolve into mud
// SPOTLIGHT.draw = (t) => { ... }   anything custom (a cursor, typing, a toggle), called every frame after the kit;
//                          it must be a pure function of t too
// Captions and the end card are DOM in scene.html: .cap[data-a][data-b], children [data-at]
// (absolute seconds), data-scrim="top|bottom"; #end wipes in at SPOTLIGHT.end.
// Charts sit inside a .cap: .chart[data-kind=bar|line|donut|number][data-at][data-dur] with data-values / data-labels
// (JSON arrays) or data-value (number). Values are numbers or strings ("12,400", "30.5%", "۱۲٬۴۰۰"), always shown
// exactly as given: a bar's or a part's value fades in as it settles (no in-between numbers that aren't in the data);
// a number counts up in its own digits, separators and units.
// Diagrams sit inside a .cap too: <svg class="diagram">; its path/line/polyline elements with data-at draw in over
// data-dur (default 0.6 s), and every other element with data-at fades in like a caption line.
(() => {
  const P = window.SPOTLIGHT, FPS = 30;
  const $ = (s) => document.querySelector(s);
  const clamp = (x, lo = 0, hi = 1) => Math.min(hi, Math.max(lo, x));
  const ramp = (t, a, b) => clamp((t - a) / (b - a));
  const outCubic = (x) => 1 - Math.pow(1 - x, 3);
  const inOutCubic = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);

  // one layout for every format: sizes scale with the short side, captions sit inside the platform safe zones
  const portrait = P.height > P.width, css = document.documentElement.style;
  css.setProperty("--W", `${P.width}px`);
  css.setProperty("--H", `${P.height}px`);
  css.setProperty("--k", Math.min(P.width, P.height) / 1080);
  css.setProperty("--safe-top", `${Math.round(P.height * (portrait ? 0.12 : 0.08))}px`);
  css.setProperty("--safe-bottom", `${Math.round(P.height * (portrait ? 0.2 : 0.1))}px`);
  css.setProperty("--side", `${Math.round(P.width * 0.066)}px`);

  const foot = $("#foot"), panel = $("#panel"), web = $("#web"), grain = $("#grain");
  const threes = new Map();  // shot -> { canvas, scene }: one canvas per three shot, created once at ready
  const token = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  const shown = new Map();
  async function show(img, src) {
    if (shown.get(img) === src) return;
    img.src = src;
    shown.set(img, src);
    await img.decode();
  }

  // clip frame for time t; the epsilon keeps (i/30)*30 from flooring to i-1 and repeating a frame
  const frameAt = (s, t) => Math.min(s.n, Math.floor((t - s.a) * FPS + 1e-6) + 1);

  async function drawShot(t) {
    const s = P.shots.find((s) => t >= s.a && t < s.b) || P.shots[P.shots.length - 1];
    const p = clamp((t - s.a) / (s.b - s.a));
    const e = inOutCubic(p);
    for (const [shot, x] of threes) x.canvas.style.opacity = shot === s ? 1 : 0;
    for (const el of document.querySelectorAll("[data-anchor]")) el.style.opacity = 0;
    if (s.three) {
      // a 3D scene drawn for this t; its anchors place DOM labels over it
      const out = threes.get(s).scene.render(t - s.a, p) || {};
      for (const [id, [x, y, alpha]] of Object.entries(out.anchors || {})) {
        for (const el of document.querySelectorAll(`[data-anchor="${id}"]`)) {
          Object.assign(el.style, { left: `${x}px`, top: `${y}px`, opacity: alpha });
        }
      }
      foot.style.opacity = 0;
      panel.style.opacity = 0;
      web.style.opacity = 0;
    }
    const src = s.clip ? `${s.clip}/${String(frameAt(s, t)).padStart(5, "0")}.jpg` : (s.still || s.web);
    // stills and web pages move linearly at a constant speed (an eased move stalls at both ends, and that reads as
    // frozen). A photo pushes in +0.01/s; a text-card backdrop (a still with a `filter`) pushes +0.08/s and drifts
    // +4%/s, so its overflow grows as fast as its drift and the edges stay covered (5% clearance). Measured at 1080x1920
    // on a real photo under blur(16px): cards up to ~5 s stay above the frozen threshold; longer cards zoom into the
    // blur and can measure frozen
    const card = Boolean(s.filter && s.still), len = s.b - s.a, m = s.still || s.web ? p : e;
    const [from, to] = s.push || (card ? [1.10, 1.10 + 0.08 * len] : s.still ? [1, 1 + 0.01 * len] : s.web ? [1, 1] : [1, 1.025]);
    const [dx0, dx1] = s.drift || (card ? [0, 4 * len] : [0, 0]);
    const scale = from + (to - from) * m, dx = dx0 + (dx1 - dx0) * m;
    if (s.three) {
      // drawn above
    } else if (s.web) {
      // the real page, scrolled: drawn at the output width, moving from scroll[0] to scroll[1] (output px)
      await show(web, src);
      const [y0, y1] = s.scroll || [0, 0], y = y0 + (y1 - y0) * m;
      // push zooms around `origin` within the visible part of the page (default its middle); filter and grade work
      // as on any other shot
      const [ox = "50%", oy = "50%"] = (s.origin || "").split(/\s+/).filter(Boolean);
      Object.assign(web.style, {
        opacity: 1, filter: [s.filter, s.grade].filter(Boolean).join(" ") || "none",
        transformOrigin: `${ox} ${y + (parseFloat(oy) / 100) * P.height}px`, transform: `translateY(${-y}px) scale(${scale})`,
      });
      foot.style.opacity = 0;
      panel.style.opacity = 0;
    } else if (s.panel) {
      await Promise.all([show(foot, src), show(panel, src)]);
      const fit = Math.min(P.width / panel.naturalWidth, P.height / panel.naturalHeight);
      const w = panel.naturalWidth * fit, h = panel.naturalHeight * fit;
      Object.assign(panel.style, {
        width: `${w}px`, height: `${h}px`, left: `${(P.width - w) / 2}px`, top: `${(P.height - h) / 2}px`,
        opacity: 1, transform: `scale(${scale})`, filter: s.grade || "none",
      });
      Object.assign(foot.style, { opacity: 1, filter: "blur(26px) brightness(.5)", transform: "scale(1.25)", transformOrigin: "50% 50%" });
      web.style.opacity = 0;
    } else {
      await show(foot, src);
      panel.style.opacity = 0;
      web.style.opacity = 0;
      Object.assign(foot.style, {
        opacity: 1, filter: [s.filter, s.grade].filter(Boolean).join(" ") || "none",
        transformOrigin: s.origin || "50% 50%", transform: `translateX(${dx}%) scale(${scale})`,
      });
    }
    // a dip through a colour, centred on the cut into a shot that asks for one (never on frame 0)
    let dip = 0, dipColor = "#000";
    for (const x of P.shots) {
      if (!x.dip || x.a <= 0) continue;
      const k = 1 - Math.abs(t - x.a) / (x.dip / 2);
      if (k > dip) [dip, dipColor] = [k, x.dipColor || "#000"];
    }
    Object.assign($("#dip").style, { opacity: clamp(dip), background: dipColor });
    // grain moves every frame but is still a function of t
    const f = Math.floor(t * FPS + 1e-6);
    grain.style.opacity = s.grain ?? P.grain ?? 0;
    grain.style.backgroundPosition = `${(f * 73) % 256}px ${(f * 151) % 256}px`;
  }

  // charts: the DOM is built once at ready; each frame sets its state from t. Numbers keep the source's own style
  const DIGITS = { "0": "0123456789", "۰": "۰۱۲۳۴۵۶۷۸۹", "٠": "٠١٢٣٤٥٦٧٨٩" };
  function numeric(v) {
    const text = String(v), set = /[۰-۹]/.test(text) ? DIGITS["۰"] : /[٠-٩]/.test(text) ? DIGITS["٠"] : DIGITS["0"];
    const ascii = text.replace(/[۰-۹٠-٩]/g, (d) => String(set.indexOf(d)));
    const m = ascii.match(/^(\D*?)(-?\d[\d,٬]*(?:[.٫]\d+)?)(.*)$/);
    if (!m) return { text, value: 0, fmt: () => text };
    const [, pre, num, post] = m, group = (num.match(/[,٬]/) || [""])[0], point = (num.match(/[.٫]/) || ["."])[0];
    const decimals = (num.split(/[.٫]/)[1] || "").length, value = parseFloat(num.replace(/[,٬]/g, "").replace("٫", "."));
    const fmt = (x) => {
      let [i, f] = Math.abs(x).toFixed(decimals).split(".");
      if (group) i = i.replace(/\B(?=(\d{3})+(?!\d))/g, group);
      return pre + ((x < 0 ? "-" : "") + i + (f ? point + f : "")).replace(/\d/g, (d) => set[d]) + post;
    };
    return { text, value, fmt };
  }
  const json = (el, key) => JSON.parse(el.dataset[key] || "[]");
  const SVG = "http://www.w3.org/2000/svg";
  const svg = (tag, attrs) => {
    const n = document.createElementNS(SVG, tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    return n;
  };
  const charts = new Map();
  function buildChart(el) {
    const kind = el.dataset.kind, labels = json(el, "labels");
    const vals = kind === "number" ? [numeric(el.dataset.value)] : json(el, "values").map(numeric);
    const max = +el.dataset.max || Math.max(...vals.map((v) => v.value), 1e-9);
    const neg = (kind === "bar" || kind === "donut") && vals.find((v) => v.value < 0);
    if (neg) throw new Error(`a ${kind} chart can't show ${neg.text}: bars and parts are sizes, so values must be >= 0 `
                             + "(a line chart, a number card or a list can show it)");
    const c = { kind, vals, max, at: +el.dataset.at || 0, dur: +el.dataset.dur || 1 };
    if (kind === "bar") {
      c.cols = vals.map((v, i) => {
        const col = document.createElement("div"), plot = document.createElement("div"), bar = document.createElement("div");
        const val = document.createElement("div"), lab = document.createElement("div");
        col.className = "col"; plot.className = "plot"; bar.className = "bar"; val.className = "val"; lab.className = "lab";
        lab.textContent = labels[i] ?? "";
        val.textContent = v.text;
        plot.append(bar, val); col.append(plot, lab); el.append(col);
        return { bar, val };
      });
    } else if (kind === "line") {
      // drawn in the chart's own pixels (measured once, layout is fixed), so nothing stretches in any format
      const s = el.appendChild(svg("svg", { class: "plot" })), { width: w, height: h } = s.getBoundingClientRect();
      const k = Math.min(P.width, P.height) / 1080, n = vals.length, pad = 40 * k, top = 70 * k, bottom = h - 70 * k;
      s.setAttribute("viewBox", `0 0 ${w} ${h}`);
      const lo = Math.min(0, ...vals.map((v) => v.value));  // negatives (a loss, a temperature) sit under the zero line
      c.pts = vals.map((v, i) => [n > 1 ? pad + ((w - 2 * pad) * i) / (n - 1) : w / 2, bottom - ((v.value - lo) / (max - lo)) * (bottom - top)]);
      c.line = s.appendChild(svg("polyline", { class: "ln", points: c.pts.map((p) => p.join(",")).join(" "), pathLength: 1 }));
      c.dots = c.pts.map(([x, y]) => s.appendChild(svg("circle", { class: "dot", cx: x, cy: y, r: 9 * k })));
      c.texts = c.pts.map(([x, y]) => s.appendChild(svg("text", { class: "val", x, y: y - 24 * k, "text-anchor": "middle" })));
      c.pts.forEach(([x], i) => { s.appendChild(svg("text", { class: "lab", x, y: h - 8 * k, "text-anchor": "middle" })).textContent = labels[i] ?? ""; });
    } else if (kind === "donut") {
      const s = svg("svg", { viewBox: "0 0 200 200", class: "plot" }), total = vals.reduce((a, v) => a + v.value, 0) || 1;
      c.C = 2 * Math.PI * 78;
      let start = 0;
      c.segs = vals.map((v, i) => {
        const len = (v.value / total) * c.C, seg = s.appendChild(svg("path", { class: `seg s${i % 5}`, d: "" }));
        const out = { seg, start, len };
        start += len;
        return out;
      });
      const legend = document.createElement("div");
      legend.className = "legend";
      c.legend = vals.map((v, i) => {
        const row = legend.appendChild(document.createElement("div"));
        row.innerHTML = `<i class="s${i % 5}"></i><span class="lab"></span><b class="val"></b>`;
        row.querySelector(".lab").textContent = labels[i] ?? "";
        row.querySelector(".val").textContent = v.text;
        return row.querySelector(".val");
      });
      el.append(s, legend);
    }
    charts.set(el, c);
  }
  function drawChart(el, t) {
    const c = charts.get(el), q = (delay = 0) => outCubic(clamp((t - c.at - delay) / c.dur));
    const settle = (k) => clamp((k - 0.6) / 0.4);  // a value fades in over the last stretch of its part's growth
    if (c.kind === "number") { const k = q(), v = c.vals[0]; el.textContent = k >= 1 ? v.text : v.fmt(v.value * k); }
    if (c.kind === "bar") c.cols.forEach(({ bar, val }, i) => {
      const k = q(0.1 * i), h = (c.vals[i].value / c.max) * 100 * k;
      bar.style.height = `${h}%`;
      val.style.bottom = `${h}%`;
      val.style.opacity = settle(k);
    });
    if (c.kind === "line") {
      const k = q();
      c.line.style.strokeDashoffset = 1 - k;
      c.pts.forEach(([x], i) => {
        const on = k >= (c.pts.length > 1 ? i / (c.pts.length - 1) : 0) - 1e-6 && k > 0;
        c.dots[i].style.opacity = on ? 1 : 0;
        c.texts[i].style.opacity = on ? 1 : 0;
        c.texts[i].textContent = c.vals[i].text;
      });
    }
    if (c.kind === "donut") {
      const k = q(), drawn = k * c.C;
      c.segs.forEach(({ seg, start, len }, i) => {
        const l = clamp(drawn - start, 0, len);
        // an arc path rebuilt each frame (two halves, so a whole circle draws too): Chromium under-repaints a changing
        // stroke-dasharray, and a frame kept stale pixels from whichever frame its capture worker drew before
        const a0 = (start / c.C) * 2 * Math.PI - Math.PI / 2, a1 = a0 + (l / c.C) * 2 * Math.PI;
        const pt = (a) => `${(100 + 78 * Math.cos(a)).toFixed(3)} ${(100 + 78 * Math.sin(a)).toFixed(3)}`;
        seg.setAttribute("d", l > 0 ? `M${pt(a0)}A78 78 0 0 1 ${pt((a0 + a1) / 2)}A78 78 0 0 1 ${pt(a1)}` : "");
        c.legend[i].style.opacity = settle(len ? l / len : k);
      });
    }
  }

  function animate(el, t) {
    for (const x of el.querySelectorAll("[data-at]")) {
      if (charts.has(x)) drawChart(x, t);
      if (+x.dataset.at <= 0 && !x.matches(".diagram *")) {  // text meant for frame 0 is already landed there
        x.style.opacity = 1;
        x.style.transform = "none";
        continue;
      }
      if (x.matches(".diagram :is(path, line, polyline)")) {
        const q = outCubic(ramp(t, +x.dataset.at, +x.dataset.at + (+x.dataset.dur || 0.6)));
        x.style.opacity = q > 0 ? 1 : 0;
        x.style.strokeDashoffset = 1 - q;
        continue;
      }
      const q = outCubic(ramp(t, +x.dataset.at, +x.dataset.at + 0.4));
      const dir = x.closest("[dir=rtl]") ? -1 : 1;  // list rows slide in from the reading side
      x.style.opacity = q;
      x.style.transform = x.classList.contains("row") ? `translateX(${(1 - q) * 40 * dir}px)` : `translateY(${(1 - q) * 24}px)`;
    }
  }

  function drawCaptions(t) {
    let top = 0, bottom = 0;
    for (const el of document.querySelectorAll(".cap[data-a]")) {
      const a = +el.dataset.a, b = +el.dataset.b;
      const live = t >= a - 0.05 ? 1 - ramp(t, b - 0.25, b) : 0;
      // the scrim fades in as it fades out (a one-frame snap reads as a flash); a caption on frame 0 has it already
      const shade = a <= 0 ? live : Math.min(live, ramp(t, a - 0.05, a + 0.25));
      el.style.opacity = live;
      const rule = el.querySelector(".rule");
      if (rule) rule.style.width = `calc(${outCubic(ramp(t, a, a + 0.55)) * 120}px * var(--k))`;
      animate(el, t);
      if (el.dataset.scrim === "top") top = Math.max(top, shade);
      if (el.dataset.scrim === "bottom") bottom = Math.max(bottom, shade);
    }
    $("#scrim-top").style.opacity = top;
    $("#scrim-bottom").style.opacity = bottom;
  }

  function drawEnd(t) {
    const end = $("#end");
    if (!end || P.end == null) return;
    const w = inOutCubic(ramp(t, P.end, P.end + 0.42));
    end.style.clipPath = `inset(${(1 - w) * 100}% 0 0 0)`;
    $("#edge").style.top = `${(1 - w) * P.height - 4}px`;
    $("#edge").style.opacity = w > 0 && w < 1 ? 1 : 0;
    animate(end, t);
  }

  window.render = async (t) => {
    await drawShot(t);
    drawCaptions(t);
    drawEnd(t);
    if (P.draw) await P.draw(t);
  };

  window.ready = (async () => {
    // shots must follow each other from 0 without gaps (a gap would show the wrong shot);
    // the last one may end early: it holds under the end card
    let at = 0;
    for (const s of P.shots) {
      if (Math.abs(s.a - at) > 1e-6) throw new Error(`timeline gap or overlap: a shot starts at ${s.a}s, expected ${at}s`);
      at = s.b;
    }
    for (const [font, sample] of P.fonts || []) await document.fonts.load(font, sample);  // ["600 80px Vazirmatn", "فارسی"]
    await document.fonts.ready;
    for (const s of P.shots) if (s.still) { const i = new Image(); i.src = s.still; await i.decode(); }
    for (const el of document.querySelectorAll(".chart")) buildChart(el);
    for (const x of document.querySelectorAll(".diagram :is(path, line, polyline)[data-at]")) {
      x.setAttribute("pathLength", 1);  // dash offset 1 -> 0 draws the whole line, whatever its real length
      x.style.strokeDasharray = "1 1";
    }
    for (const s of P.shots.filter((s) => s.three)) {
      const canvas = document.createElement("canvas");
      canvas.className = "three";
      canvas.width = P.width;
      canvas.height = P.height;
      grain.before(canvas);
      try {
        const mod = await import(new URL(s.three, location.href).href);
        threes.set(s, { canvas, scene: await mod.create(canvas, s.params || {}, { width: P.width, height: P.height, css: token }) });
      } catch (e) {
        throw new Error(`three shot ${s.three}: ${e.message}`);
      }
    }
    for (const i of document.images) if (i.getAttribute("src")) await i.decode();
    await window.render(0);
    return { fps: FPS, duration: P.duration, width: P.width, height: P.height };
  })();
})();
