// Capture a website as source material: node site.mjs <url-or-file://> <workdir> [--size WxH]
// Writes <workdir>/site/: copy.json, brand.json, page.html, screens/NN.png (output aspect), full.png, assets/.
// Best effort and bounded: 45 s to load, 90 s in total, at most 12 screens, full page capped at 12000 px.
import { mkdirSync, writeFileSync, copyFileSync, existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { launch } from "./browser.mjs";

const [arg, workdir = ".", ...rest] = process.argv.slice(2);
if (!arg) { console.error("usage: site.mjs <url-or-file://> <workdir> [--size WxH]"); process.exit(2); }
// a bare domain means https; an existing local path means that file
const url = /^(https?|file):/i.test(arg) ? arg : existsSync(arg) ? pathToFileURL(path.resolve(arg)).href : `https://${arg}`;
const size = (rest[rest.indexOf("--size") + 1] || "1080x1920").split("x").map(Number);
const [W, H] = rest.includes("--size") ? size : [1080, 1920];
const portrait = H > W;
// vertical renders the mobile layout (540 css px at 2x); landscape and square render desktop at 1x
const viewport = portrait ? { width: W / 2, height: H / 2 } : { width: W, height: H };
const scale = portrait ? 2 : 1;
const out = path.join(workdir, "site");
mkdirSync(path.join(out, "screens"), { recursive: true });
mkdirSync(path.join(out, "assets"), { recursive: true });
const deadline = Date.now() + 90_000;
// the hard cap: whatever is on disk by then is the result
setTimeout(() => { console.error("site.mjs: 90 s cap reached; keeping what was captured"); process.exit(0); }, 90_000).unref();
// every step after the load is best effort: one that throws (a page that navigates away, a screenshot that times out)
// is reported and the rest still run
const step = (name, fn) => fn().catch((e) => console.error(`site.mjs: ${name}: ${String(e.message).split("\n")[0]}`));

const browser = await launch();
const page = await browser.newPage({ viewport, deviceScaleFactor: scale });
try {
  await page.goto(url, { waitUntil: "networkidle", timeout: 45_000 });
} catch (e) {  // a slow page keeps what loaded; an address that can't be opened at all is an error
  if (e.name !== "TimeoutError") { console.error(`site.mjs: can't open ${url}: ${String(e.message).split("\n")[0]}`); process.exit(2); }
}
// stop whatever is still loading: a stalled font would otherwise hold every screenshot until it times out
await step("stop", () => page.evaluate(() => window.stop()));

// dismiss consent banners: click an accepting button inside a cookie/consent element (never a link that navigates
// away), and hide fixed overlays
await step("consent", () => page.evaluate(() => {
  const words = /accept|agree|allow|got it|^ok$|قبول|موافق|پذیرفتن|أوافق/i;
  const boxes = [...document.querySelectorAll("[id*=cookie i],[class*=cookie i],[id*=consent i],[class*=consent i],[class*=gdpr i]")];
  for (const box of boxes) {
    const btn = [...box.querySelectorAll("button,[role=button],a[href^='#'],a:not([href])")].find((b) => words.test(b.textContent.trim()));
    if (btn) btn.click();
  }
  for (const el of document.querySelectorAll("body *")) {
    const s = getComputedStyle(el);
    if ((s.position === "fixed" || s.position === "sticky") && /cookie|consent|gdpr|newsletter|popup|modal/i.test(el.id + " " + el.className)) {
      el.style.display = "none";
    }
  }
}));

// scroll once through the page so lazy and animate-on-scroll content appears (bounded for endless pages)
await step("scroll", async () => {
  for (let y = 0, i = 0; i < 40 && Date.now() < deadline; i++, y += viewport.height) {
    const h = await page.evaluate((y) => { scrollTo(0, y); return document.body.scrollHeight; }, y);
    await page.waitForTimeout(150);
    if (y > h || y > 12000 / scale) break;
  }
  await page.evaluate(() => scrollTo(0, 0));
});

const data = await step("copy and brand", () => page.evaluate(() => {
  const txt = (e) => (e.innerText || e.textContent || "").replace(/\s+/g, " ").trim();
  const meta = (n) => document.querySelector(`meta[name="${n}"],meta[property="${n}"]`)?.content || "";
  const og = {};
  for (const m of document.querySelectorAll('meta[property^="og:"]')) og[m.getAttribute("property").slice(3)] = m.content;
  const ctas = [...document.querySelectorAll("button,[role=button],a[class*=btn i],a[class*=button i],a[class*=cta i]")]
    .map((e) => ({ text: txt(e), href: e.getAttribute("href") || "" })).filter((c) => c.text && c.text.length < 60);
  // any CSS colour (rgb, oklch, color(), …) -> sRGB hex, by painting it on a 1x1 canvas; transparent -> null
  const ctx = Object.assign(document.createElement("canvas"), { width: 1, height: 1 }).getContext("2d", { willReadFrequently: true });
  const hex = (c) => {
    ctx.clearRect(0, 0, 1, 1); ctx.fillStyle = "#000"; ctx.fillStyle = c; ctx.fillRect(0, 0, 1, 1);
    const [r, g, b, a] = ctx.getImageData(0, 0, 1, 1).data; if (a === 0) return null;
    return "#" + [r, g, b].map((v) => v.toString(16).padStart(2, "0")).join("");
  };
  const bodyBg = hex(getComputedStyle(document.body).backgroundColor) || hex(getComputedStyle(document.documentElement).backgroundColor) || "#ffffff";
  // accent: the most used saturated colour on links and buttons, a filled button counting 3x; greys and the
  // browser's default link colours (unstyled links) don't count
  const sat = (c) => { const v = [1, 3, 5].map((i) => parseInt(c.slice(i, i + 2), 16)); return Math.max(...v) - Math.min(...v); };
  const counts = {};
  for (const e of document.querySelectorAll("a,button,[class*=btn i],[class*=accent i]")) {
    for (const p of ["backgroundColor", "color", "borderColor"]) {
      const c = hex(getComputedStyle(e)[p]);
      if (c && c !== bodyBg && c !== "#0000ee" && c !== "#551a8b" && sat(c) > 40) counts[c] = (counts[c] || 0) + (p === "backgroundColor" ? 3 : 1);
    }
  }
  const accent = Object.entries(counts).sort((a, b) => b[1] - a[1])[0]?.[0] || null;
  const fonts = [...new Set([document.body, document.querySelector("h1"), document.querySelector("h2")].filter(Boolean)
    .map((e) => getComputedStyle(e).fontFamily))];
  const logo = [...document.querySelectorAll("img")].find((i) => /logo/i.test(i.alt + i.className + i.src + (i.closest("header") ? " header" : "")))?.src
    || document.querySelector('link[rel*="icon"]')?.href || null;
  const images = [...document.images].filter((i) => i.naturalWidth >= 400).sort((a, b) => b.naturalWidth * b.naturalHeight - a.naturalWidth * a.naturalHeight)
    .slice(0, 6).map((i) => i.src);
  return {
    copy: {
      url: location.href, title: document.title, lang: document.documentElement.lang || "", dir: document.documentElement.dir || getComputedStyle(document.documentElement).direction,
      description: meta("description"), og,
      headings: [...document.querySelectorAll("h1,h2,h3")].map((h) => ({ level: +h.tagName[1], text: txt(h) })).filter((h) => h.text),
      paragraphs: [...document.querySelectorAll("p")].map(txt).filter(Boolean).slice(0, 40),
      ctas, nav: [...document.querySelectorAll("nav a")].map((a) => ({ text: txt(a), href: a.getAttribute("href") || "" })),
    },
    brand: { background: bodyBg, text: hex(getComputedStyle(document.body).color), accent, fonts, logo, images },
  };
}));

// download (or copy, for file://) the logo and the big images into site/assets/
async function fetchAsset(src, name) {
  try {
    const ext = (path.extname(new URL(src).pathname) || ".png").slice(0, 6);
    const dest = path.join(out, "assets", name + ext);
    if (src.startsWith("file://")) { const p = fileURLToPath(src); if (existsSync(p)) copyFileSync(p, dest); else return null; }
    else { const r = await page.request.get(src, { timeout: 15_000 }); if (!r.ok()) return null; writeFileSync(dest, await r.body()); }
    return path.join("site", "assets", name + ext);
  } catch { return null; }
}
if (data) {
  writeFileSync(path.join(out, "copy.json"), JSON.stringify(data.copy, null, 2));
  data.brand.logo = data.brand.logo ? await fetchAsset(data.brand.logo, "logo") : null;
  data.brand.images = (await Promise.all(data.brand.images.map((s, i) => fetchAsset(s, `image-${i + 1}`)))).filter(Boolean);
  writeFileSync(path.join(out, "brand.json"), JSON.stringify(data.brand, null, 2));
}
await step("page.html", async () => writeFileSync(path.join(out, "page.html"), await page.content()));

// screens at the output aspect, one per viewport of scroll, at most 12; then the full page, capped at 12000 px
let height = viewport.height;
await step("screens", async () => {
  height = await page.evaluate(() => document.body.scrollHeight);
  for (let i = 0, y = 0; i < 12 && y < height && Date.now() < deadline; i++, y += viewport.height) {
    await page.evaluate((y) => scrollTo(0, y), y);
    await page.waitForTimeout(120);
    await page.screenshot({ path: path.join(out, "screens", String(i + 1).padStart(2, "0") + ".png"), timeout: 10_000 });
  }
  await page.evaluate(() => scrollTo(0, 0));
});
const clipH = Math.min(height, Math.floor(12000 / scale));
await step("full page", () => page.screenshot({ path: path.join(out, "full.png"), fullPage: true, timeout: 15_000,
  clip: { x: 0, y: 0, width: viewport.width, height: clipH } }));
await browser.close().catch(() => {});
console.log(data ? `site captured: ${data.copy.headings.length} headings, ${data.copy.ctas.length} CTAs -> ${out}` : `site captured screens only -> ${out}`);
