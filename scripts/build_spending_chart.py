#!/usr/bin/env python3
"""Build a local, self-contained HTML spending chart from the masked CSVs.

Usage:
    python3 scripts/build_spending_chart.py [MASKED_DIR] [OUT_HTML]

Defaults: MASKED_DIR=docs/masked, OUT_HTML=docs/masked/wydatki.html.
Reads statements_masked.csv and operations_list_masked.csv (output of mask_statements.py),
classifies every row and keeps only *consumption*: loan/instalment payments, investments,
transfers to/from people or own accounts, salary, card repayments and refunds are left out
(the card's own purchases are counted, its repayments are not, so nothing is counted twice).
The page has no external resources: open it in a browser, nothing leaves the machine.
"""
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

OWN = r'\[WŁAŚCICIEL\]'
MERCHANT_RULES = [
    ('Spożywcze', r'LIDL|BIEDRONKA|ŻABKA|ZABKA|ALDI|EUROSPAR|SPAR\b|CARREFOUR|KAUFLAND|AUCHAN|DINO|STOKROTKA|NETTO|LEWIATAN|SPOŻYW|DELIKATESY|PIEKARNIA|CUKIERNIA|MARKET|ŻYWNOŚĆ|HEBE|ROSSMANN|FRESH'),
    ('Restauracje i kawiarnie', r'RESTAUR|RAMEN|SUSHI|PIZZ|BURGER|KFC|MCDONALD|STARBUCKS|CAFE|KAWIARN|KAWA|HERBAT|TAWERNA|PIANO|BAR\b|PUB\b|WOLT|GLOVO|PYSZNE|BISTRO|FEERIA|VICENTI|FOOD'),
    ('Paliwo i auto', r'ORLEN|\bBP\b|SHELL|CIRCLE K|MOYA|LOTOS|EV\+MAP|EV PLUS|PARKING|PARKOMAT|MYJNIA|AUTOSTRAD|E-TOLL|GREENWAY'),
    ('Transport', r'UBER|BOLT|JAKDOJADE|PKP|ZTM|TAXI|KOLEJE|FLIXBUS|MPK|\bLOT\b|RYANAIR|WIZZ'),
    ('Zdrowie', r'APTEKA|DENTAL|DENTYST|MEDIC|LUXMED|GEMINI|KLINIK|LEKARZ|\bDOZ\b'),
    ('Sport i rekreacja', r'MULTISPORT|SKI|KARNET|SIŁOWNIA|GYM|BASEN|FITNESS|BILET|KINO'),
    ('Zakupy online i ubrania', r'VINTED|EOBUWIE|ALLEGRO|AMAZON|ALIEXPRESS|ZALANDO|OLX|TEMU|EMPIK|RTV|MEDIA EXPERT|ZARA|H&M|RESERVED|CCC|SINSAY|DECATHLON|IKEA|LEROY|CASTORAMA'),
    ('Telekom i media', r'T-MOBILE|ORANGE|PLAY\b|NETIA|VECTRA|ENEA|PGE|TAURON|PGNIG|NETFLIX|SPOTIFY|HBO|YOUTUBE|APPLE|GOOGLE|OPENAI|ANTHROPIC|CANVA|MICROSOFT|ZEN\.COM'),
]
MERCHANT_RULES = [(c, re.compile(r, re.I)) for c, r in MERCHANT_RULES]
HOUSING = 'Mieszkanie i czynsz'
OTHER_PURCHASES = 'Inne zakupy'
# Colours follow the entity, not its rank: these six get a fixed palette slot, the rest is grey.
MAIN = [HOUSING, 'Spożywcze', 'Edukacja', 'Sport i rekreacja', 'Restauracje i kawiarnie', 'Zakupy online i ubrania']


def merchant_category(desc):
    return next((c for c, rx in MERCHANT_RULES if rx.search(desc)), None)


def classify_statement(desc):
    """Return a consumption category, or None when the row is not consumption."""
    u = desc.upper()
    if any(k in u for k in ('AVANQUEST', 'POLSKI FUNDUSZ ROZWOJU', 'ZWROT Z FUNDUSZU', 'WPŁATA NA RACHUNEK KARTY', 'XTB',
                            'STELLANTIS', 'MILENIUM', 'PAYPO')) or u.startswith('SPŁATA KREDYTU'):
        return None
    if re.match(r'^[^|]*\| ' + OWN + ' ' + OWN, desc) or 'REVOLUT' in u or 'DO SIEBIE' in u or u.startswith('ZWROT PŁATNOŚCI'):
        return None
    if 'URZĄD SKARBOWY' in u or 'MINISTERSTWO FIN' in u:
        return 'Podatki'
    if 'ERGO HESTIA' in u:
        return 'Ubezpieczenia'
    if any(k in u for k in ('PSM PW', 'SHED LIVING', 'ATLANTIS NIERUCHOMO')):
        return HOUSING
    if 'AUTOPAY' in u and 'WSB' in u:
        return 'Edukacja'
    if u.startswith(('WYPŁATA KARTĄ', 'WYPŁATA BLIK', 'WYPŁATA GOTÓWKI')):
        return 'Gotówka'
    if u.startswith(('REALIZACJA PŁATNOŚCI PEOPAY', 'PRZELEW')):
        return merchant_category(desc)       # a transfer to a person is not consumption
    return merchant_category(desc) or ('Opłaty bankowe' if u.startswith(('PROWIZJ', 'ROZLICZENIA')) else OTHER_PURCHASES)


def classify_card(row):
    if row['category'] in ('PROWIZJA', 'ODSETKI'):
        return 'Opłaty bankowe'
    if row['category'] == 'WYPŁATA':
        return 'Gotówka'
    if re.search('SHED LIVING', row['description'], re.I):
        return HOUSING
    return merchant_category(row['description']) or OTHER_PURCHASES


def load(path):
    with open(path, encoding='utf-8-sig') as fh:
        return list(csv.DictReader(fh))


def build(masked_dir):
    agg = defaultdict(lambda: [0.0, 0])
    for name, source in (('statements_masked.csv', 'konto'), ('operations_list_masked.csv', 'karta')):
        path = masked_dir / name
        if not path.exists():
            continue
        for r in load(path):
            category = classify_card(r) if source == 'karta' else classify_statement(r['description'])
            amount = float(r['amount'])
            if category is None or amount >= 0:
                continue
            a = agg[(r['date'][:7], source, category)]
            a[0] += -amount
            a[1] += 1
    rows = [{'m': m, 's': s, 'c': c, 'v': round(v, 2), 'n': n} for (m, s, c), (v, n) in sorted(agg.items())]
    return {'rows': rows, 'main': MAIN}


def main():
    masked = Path(sys.argv[1] if len(sys.argv) > 1 else 'docs/masked')
    out = Path(sys.argv[2] if len(sys.argv) > 2 else masked / 'wydatki.html')
    data = build(masked)
    if not data['rows']:
        sys.exit('Brak danych: uruchom najpierw scripts/mask_statements.py')
    payload = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    out.write_text(TEMPLATE.replace('/*__DATA__*/', payload), encoding='utf-8')
    total = sum(r['v'] for r in data['rows'])
    print(f'Zapisano {out} ({len(data["rows"])} agregatów, wydatki łącznie {total:,.0f} zł)')


TEMPLATE = r"""<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Moje wydatki</title>
<style>
:root {
  color-scheme: light;
  --page: #f9f9f7; --surface: #fcfcfb; --ink: #0b0b0b; --ink2: #52514e; --muted: #898781;
  --grid: #e1e0d9; --axis: #c3c2b7; --border: rgba(11,11,11,.10); --other: #b7b5ac;
  --s1: #2a78d6; --s2: #eb6834; --s3: #1baf7a; --s4: #eda100; --s5: #e87ba4; --s6: #008300;
}
@media (prefers-color-scheme: dark) {
  :root:where(:not([data-theme="light"])) {
    color-scheme: dark;
    --page: #0d0d0d; --surface: #1a1a19; --ink: #f0efec; --ink2: #c3c2b7; --muted: #898781;
    --grid: #2c2c2a; --axis: #383835; --border: rgba(255,255,255,.10); --other: #6b6a64;
    --s1: #3987e5; --s2: #d95926; --s3: #199e70; --s4: #c98500; --s5: #d55181; --s6: #008300;
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --page: #0d0d0d; --surface: #1a1a19; --ink: #f0efec; --ink2: #c3c2b7; --muted: #898781;
  --grid: #2c2c2a; --axis: #383835; --border: rgba(255,255,255,.10); --other: #6b6a64;
  --s1: #3987e5; --s2: #d95926; --s3: #199e70; --s4: #c98500; --s5: #d55181; --s6: #008300;
}
* { box-sizing: border-box; }
[hidden] { display: none !important; }
body { margin: 0; background: var(--page); color: var(--ink); font: 14px/1.4 system-ui, -apple-system, "Segoe UI", sans-serif; }
main { max-width: 1040px; margin: 0 auto; padding: 24px 16px 48px; }
h1 { font-size: 22px; font-weight: 600; margin: 0 0 2px; }
.sub { color: var(--ink2); margin: 0 0 16px; }
.controls { display: flex; flex-wrap: wrap; gap: 12px 24px; margin-bottom: 16px; }
.group { display: flex; align-items: center; gap: 8px; color: var(--ink2); }
.seg { display: inline-flex; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; background: var(--surface); }
.seg button { font: inherit; color: var(--ink2); background: none; border: 0; padding: 6px 12px; cursor: pointer; }
.seg button + button { border-left: 1px solid var(--border); }
.seg button:hover { background: color-mix(in srgb, var(--ink) 6%, transparent); }
.seg button[aria-pressed="true"] { color: var(--ink); font-weight: 600; background: color-mix(in srgb, var(--ink) 10%, transparent); }
button:focus-visible, [tabindex]:focus-visible { outline: 2px solid var(--s1); outline-offset: 2px; }
.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; margin-bottom: 16px; }
.tile { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 14px 16px; }
.tile.hero { grid-column: 1 / -1; }
.tile .label { color: var(--ink2); }
.tile .value { font-size: 26px; font-weight: 600; margin-top: 2px; }
.tile.hero .value { font-size: 52px; line-height: 1.1; }
.tile .note { color: var(--muted); font-size: 12px; margin-top: 2px; }
.card { position: relative; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 16px; }
.card h2 { font-size: 16px; font-weight: 600; margin: 0; }
.card .desc { color: var(--ink2); margin: 2px 0 12px; }
.legend { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: 6px 16px; }
.legend li { display: flex; align-items: center; gap: 8px; }
.legend.col { flex-direction: column; flex-wrap: nowrap; gap: 8px; min-width: 260px; }
.legend.col li { justify-content: flex-start; }
.sw { width: 10px; height: 10px; border-radius: 2px; flex: none; }
.legend .v { margin-left: auto; padding-left: 16px; font-weight: 600; }
.legend .p { color: var(--ink2); min-width: 48px; text-align: right; }
.share { display: flex; flex-wrap: wrap; gap: 24px; align-items: center; justify-content: center; }
#chart { margin-top: 8px; }
svg { display: block; max-width: 100%; overflow: visible; }
svg text { font: 12px system-ui, -apple-system, "Segoe UI", sans-serif; fill: var(--ink2); }
svg .ink { fill: var(--ink); }
svg .muted { fill: var(--muted); }
svg .big { font-size: 22px; font-weight: 600; fill: var(--ink); }
[data-k].dim { opacity: .45; }
[data-k] { transition: opacity .12s; }
.tt-box { position: absolute; z-index: 5; pointer-events: none; background: var(--surface); color: var(--ink);
  border: 1px solid var(--border); border-radius: 8px; padding: 8px 10px; box-shadow: 0 4px 16px rgba(0,0,0,.14); min-width: 170px; max-width: 280px; }
.tt-box .tt { font-weight: 600; margin-bottom: 4px; }
.tt-box .tr { display: flex; align-items: center; gap: 8px; line-height: 1.6; }
.tt-box .key { width: 12px; height: 3px; border-radius: 2px; flex: none; }
.tt-box .tn { color: var(--ink2); }
.tt-box .tv { margin-left: auto; padding-left: 12px; }
.toggle { margin-top: 12px; font: inherit; color: var(--ink2); background: none; border: 1px solid var(--border); border-radius: 8px; padding: 6px 12px; cursor: pointer; }
.toggle:hover { background: color-mix(in srgb, var(--ink) 6%, transparent); }
.tablewrap { overflow-x: auto; margin-top: 12px; }
table { border-collapse: collapse; width: 100%; }
th, td { padding: 6px 10px; border-bottom: 1px solid var(--grid); text-align: right; white-space: nowrap; }
th:first-child, td:first-child { text-align: left; }
th { color: var(--ink2); font-weight: 500; }
td { font-variant-numeric: tabular-nums; }
.foot { color: var(--muted); font-size: 12px; margin-top: 16px; }
@media (forced-colors: active) { .sw, .key { forced-color-adjust: none; } }
</style>
</head>
<body>
<main>
  <h1>Moje wydatki</h1>
  <p class="sub" id="period"></p>

  <div class="controls">
    <div class="group">Źródło <div class="seg" id="src" role="group" aria-label="Źródło danych"></div></div>
    <div class="group">Widok <div class="seg" id="view" role="group" aria-label="Rodzaj wykresu"></div></div>
  </div>

  <div class="tiles" id="tiles"></div>

  <section class="card" id="card">
    <h2 id="title"></h2>
    <p class="desc" id="desc"></p>
    <ul class="legend" id="legend" hidden></ul>
    <div id="chart"></div>
    <div class="tt-box" id="tip" hidden role="status"></div>
    <button class="toggle" id="tbtn" aria-expanded="false">Pokaż tabelę</button>
    <div class="tablewrap" id="tbl" hidden></div>
  </section>

  <p class="foot">Uwzględnia zakupy i opłaty z konta oraz z karty kredytowej. Pomija spłaty kredytów i rat, inwestycje, przelewy do osób
    i własne, spłaty karty (jej zakupy są policzone osobno) oraz zwroty. Pierwszy i ostatni miesiąc mogą być niepełne.</p>
</main>

<script>
const DATA = /*__DATA__*/;
const OTHER = 'Pozostałe';
const NS = 'http://www.w3.org/2000/svg';
const $ = (s) => document.querySelector(s);
const state = { src: 'all', view: 'cat', table: false };

const nf = new Intl.NumberFormat('pl-PL', { maximumFractionDigits: 0, useGrouping: 'always' });
const zl = (n) => nf.format(Math.round(n)) + ' zł';
const compact = (n) => n >= 1000 ? (n / 1000).toLocaleString('pl-PL', { maximumFractionDigits: 1 }) + ' tys.' : nf.format(n);
const pct = (x) => (x * 100).toLocaleString('pl-PL', { maximumFractionDigits: 1 }) + '%';
const MONTHS = ['sty', 'lut', 'mar', 'kwi', 'maj', 'cze', 'lip', 'sie', 'wrz', 'paź', 'lis', 'gru'];

function S(tag, attrs, parent) {
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}
function T(tag, attrs, text, parent) {
  const e = document.createElement(tag);
  for (const k in attrs || {}) e.setAttribute(k, attrs[k]);
  if (text != null) e.textContent = text;
  if (parent) parent.appendChild(e);
  return e;
}
const colorOf = (c) => { const i = DATA.main.indexOf(c); return i >= 0 ? `var(--s${i + 1})` : 'var(--other)'; };
const fold = (c) => DATA.main.includes(c) ? c : OTHER;

const allMonths = [...new Set(DATA.rows.map((r) => r.m))].sort();
const lastYear = allMonths[allMonths.length - 1].slice(0, 4);
const monthLabel = (m, short) => MONTHS[+m.slice(5) - 1] + (!short && m.slice(0, 4) !== lastYear ? ` ’${m.slice(2, 4)}` : '');
const monthLong = (m) => `${MONTHS[+m.slice(5) - 1]} ${m.slice(0, 4)}`;

const rows = () => DATA.rows.filter((r) => state.src === 'all' || r.s === state.src);
function sumBy(keyFn, rs) {
  const m = new Map();
  for (const r of rs) {
    const k = keyFn(r), a = m.get(k) || { v: 0, n: 0 };
    a.v += r.v; a.n += r.n; m.set(k, a);
  }
  return m;
}
const byValue = (m) => [...m].filter(([, a]) => a.v > 0).sort((a, b) => b[1].v - a[1].v);

/* ---------- tooltip & hover ---------- */
const tip = $('#tip');
function hideTip() { tip.hidden = true; highlight(null); }
function showTip(title, lines, x, y) {
  tip.replaceChildren();
  T('div', { class: 'tt' }, title, tip);
  for (const l of lines) {
    const row = T('div', { class: 'tr' }, null, tip);
    const key = T('span', { class: 'key' }, null, row);
    if (l.color) key.style.background = l.color; else key.style.display = 'none';
    T('span', { class: 'tn' }, l.name, row);
    T('strong', { class: 'tv' }, l.value, row);
  }
  tip.hidden = false;
  const box = $('#card').getBoundingClientRect();
  const w = tip.offsetWidth, h = tip.offsetHeight;
  let left = x - box.left + 14, top = y - box.top + 14;
  if (left + w > box.width - 8) left = x - box.left - w - 14;
  if (top + h > box.height - 8) top = box.height - h - 8;
  tip.style.left = Math.max(8, left) + 'px';
  tip.style.top = Math.max(8, top) + 'px';
}
function highlight(k) {
  document.querySelectorAll('[data-k]').forEach((e) => e.classList.toggle('dim', k != null && e.dataset.k !== k));
}
function bind(node, content, key) {
  node.setAttribute('tabindex', '0');
  const at = (x, y) => { const c = content(); highlight(key ?? null); showTip(c.title, c.lines, x, y); };
  node.setAttribute('aria-label', (() => { const c = content(); return c.title + ': ' + c.lines.map((l) => l.name + ' ' + l.value).join(', '); })());
  node.addEventListener('pointermove', (e) => at(e.clientX, e.clientY));
  node.addEventListener('pointerleave', hideTip);
  node.addEventListener('focus', () => { const b = node.getBoundingClientRect(); at(b.left + b.width / 2, b.top); });
  node.addEventListener('blur', hideTip);
}

/* ---------- tiles ---------- */
function renderTiles() {
  const rs = rows(), total = rs.reduce((s, r) => s + r.v, 0);
  const byM = sumBy((r) => r.m, rs), ms = [...byM.keys()].sort();
  const full = ms.length >= 3 ? ms.slice(1, -1) : ms;
  const avg = full.reduce((s, m) => s + byM.get(m).v, 0) / (full.length || 1);
  const cats = byValue(sumBy((r) => r.c, rs)), topM = [...byM].sort((a, b) => b[1].v - a[1].v)[0];
  const tiles = $('#tiles'); tiles.replaceChildren();
  const add = (cls, label, value, note) => {
    const t = T('div', { class: 'tile ' + cls }, null, tiles);
    T('div', { class: 'label' }, label, t); T('div', { class: 'value' }, value, t); T('div', { class: 'note' }, note, t);
  };
  add('hero', 'Wydatki łącznie', zl(total), `${monthLong(ms[0])} – ${monthLong(ms[ms.length - 1])}`);
  add('', 'Średnio miesięcznie', zl(avg), `z ${full.length} pełnych miesięcy`);
  if (cats.length) add('', 'Największa kategoria', cats[0][0], `${zl(cats[0][1].v)} · ${pct(cats[0][1].v / total)}`);
  if (topM) add('', 'Najdroższy miesiąc', monthLong(topM[0]), zl(topM[1].v));
}

/* ---------- views ---------- */
function viewCat(box) {
  const items = byValue(sumBy((r) => r.c, rows())), total = items.reduce((s, [, a]) => s + a.v, 0);
  const W = Math.max(box.clientWidth, 300), stack = W < 560, labelW = stack ? 0 : 190, rowH = stack ? 46 : 32, valW = 130;
  const Ht = items.length * rowH + 4;
  const svg = S('svg', { width: W, height: Ht, viewBox: `0 0 ${W} ${Ht}`, role: 'group', 'aria-label': 'Wydatki wg kategorii' }, box);
  const max = items.length ? items[0][1].v : 1, bw = W - labelW - valW;
  items.forEach(([c, a], i) => {
    const y = i * rowH, g = S('g', { 'data-k': c }, svg);
    const hit = S('rect', { x: 0, y, width: W, height: rowH, fill: 'transparent' }, g);
    const by = stack ? y + 22 : y + (rowH - 16) / 2;
    const lab = S('text', { x: 0, y: stack ? y + 14 : y + rowH / 2 + 4, class: 'ink' }, g); lab.textContent = c;
    const w = Math.max(2, bw * a.v / max), x = labelW;
    if (w > 8) S('path', { d: `M${x},${by} h${w - 4} a4,4 0 0 1 4,4 v8 a4,4 0 0 1 -4,4 h-${w - 4} z`, fill: colorOf(c) }, g);
    else S('rect', { x, y: by, width: w, height: 16, fill: colorOf(c) }, g);
    const val = S('text', { x: x + w + 8, y: by + 12, class: 'ink' }, g);
    val.textContent = zl(a.v);
    const p = S('tspan', { dx: 8, class: 'muted' }, val); p.textContent = pct(a.v / total);
    bind(hit, () => ({ title: c, lines: [
      { name: 'Wydatki', value: zl(a.v), color: colorOf(c) },
      { name: 'Udział', value: pct(a.v / total) },
      { name: 'Transakcje', value: nf.format(a.n) }] }), c);
  });
  return { head: ['Kategoria', 'Kwota', 'Udział', 'Transakcje'], body: items.map(([c, a]) => [c, zl(a.v), pct(a.v / total), nf.format(a.n)]) };
}

function foldedItems() {
  const f = sumBy((r) => fold(r.c), rows());
  return byValue(f);
}
function renderLegend(items, withValues, total) {
  const ul = $('#legend'); ul.replaceChildren(); ul.hidden = false;
  ul.className = 'legend' + (withValues ? ' col' : '');
  for (const [c, a] of items) {
    const li = T('li', { 'data-k': c }, null, ul);
    const sw = T('span', { class: 'sw' }, null, li); sw.style.background = colorOf(c);
    T('span', {}, c, li);
    if (withValues) { T('span', { class: 'v' }, zl(a.v), li); T('span', { class: 'p' }, pct(a.v / total), li); }
    li.addEventListener('pointerenter', () => highlight(c));
    li.addEventListener('pointerleave', () => highlight(null));
  }
}

function viewShare(box) {
  const items = foldedItems(), total = items.reduce((s, [, a]) => s + a.v, 0);
  const wrap = T('div', { class: 'share' }, null, box);
  const size = Math.min(Math.max(box.clientWidth, 260), 320), cx = size / 2, r1 = size / 2 - 4, r0 = r1 * 0.62, rm = (r0 + r1) / 2;
  const svg = S('svg', { width: size, height: size, viewBox: `0 0 ${size} ${size}`, role: 'group', 'aria-label': 'Udział kategorii w wydatkach' }, wrap);
  const gap = 2 / rm; let a0 = -Math.PI / 2;
  const pt = (r, a) => [cx + r * Math.cos(a), cx + r * Math.sin(a)];
  for (const [c, a] of items) {
    const sweep = 2 * Math.PI * a.v / total, s = a0 + gap / 2, e = a0 + sweep - gap / 2;
    if (e > s) {
      const [x0, y0] = pt(r1, s), [x1, y1] = pt(r1, e), [x2, y2] = pt(r0, e), [x3, y3] = pt(r0, s), big = e - s > Math.PI ? 1 : 0;
      const path = S('path', { d: `M${x0},${y0} A${r1},${r1} 0 ${big} 1 ${x1},${y1} L${x2},${y2} A${r0},${r0} 0 ${big} 0 ${x3},${y3} Z`, fill: colorOf(c), 'data-k': c }, svg);
      bind(path, () => ({ title: c, lines: [
        { name: 'Wydatki', value: zl(a.v), color: colorOf(c) },
        { name: 'Udział', value: pct(a.v / total) },
        { name: 'Transakcje', value: nf.format(a.n) }] }), c);
    }
    a0 += sweep;
  }
  const t1 = S('text', { x: cx, y: cx + 2, 'text-anchor': 'middle', class: 'big' }, svg); t1.textContent = zl(total);
  const t2 = S('text', { x: cx, y: cx + 22, 'text-anchor': 'middle' }, svg); t2.textContent = 'wydatki łącznie';
  const side = T('div', {}, null, wrap); side.appendChild($('#legend'));
  renderLegend(items, true, total);
  return { head: ['Kategoria', 'Kwota', 'Udział', 'Transakcje'], body: items.map(([c, a]) => [c, zl(a.v), pct(a.v / total), nf.format(a.n)]) };
}

function viewMonth(box) {
  const series = [...DATA.main, OTHER];
  const rs = rows(), per = new Map(allMonths.map((m) => [m, new Map()]));
  for (const r of rs) { const k = fold(r.c), mm = per.get(r.m); mm.set(k, (mm.get(k) || 0) + r.v); }
  const totals = allMonths.map((m) => [...per.get(m).values()].reduce((s, v) => s + v, 0));
  const W = Math.max(box.clientWidth, 300), Hh = 340, L = 46, R = 8, Tp = 26, B = 28, ph = Hh - Tp - B;
  const step = [500, 1000, 2000, 2500, 5000, 10000].find((s) => Math.max(...totals, 1) / s <= 5) || 10000;
  const top = Math.ceil(Math.max(...totals, 1) / step) * step, y = (v) => Tp + ph - ph * v / top;
  const band = (W - L - R) / allMonths.length, bw = Math.min(24, band * 0.6);
  const svg = S('svg', { width: W, height: Hh, viewBox: `0 0 ${W} ${Hh}`, role: 'group', 'aria-label': 'Wydatki w kolejnych miesiącach' }, box);
  for (let v = 0; v <= top; v += step) {
    S('line', { x1: L, x2: W - R, y1: y(v), y2: y(v), stroke: v === 0 ? 'var(--axis)' : 'var(--grid)', 'stroke-width': 1 }, svg);
    const t = S('text', { x: L - 8, y: y(v) + 4, 'text-anchor': 'end', class: 'muted' }, svg); t.textContent = v ? compact(v) : '0';
  }
  allMonths.forEach((m, i) => {
    const cx = L + band * i + band / 2, x = cx - bw / 2, g = S('g', {}, svg);
    S('rect', { x: L + band * i, y: Tp, width: band, height: ph, fill: 'transparent' }, g);
    let acc = 0; const present = series.filter((k) => per.get(m).get(k) > 0);
    present.forEach((k, j) => {
      const v = per.get(m).get(k), y1 = y(acc), y0 = y(acc + v); acc += v;
      const lo = j === 0 ? y1 : y1 - 1, hi = y0 + (j === present.length - 1 ? 0 : 1);
      const h = lo - hi; if (h < 1) return;
      const isTop = j === present.length - 1, r = Math.min(4, h);
      S('path', { d: isTop
        ? `M${x},${lo} V${hi + r} a${r},${r} 0 0 1 ${r},-${r} h${bw - 2 * r} a${r},${r} 0 0 1 ${r},${r} V${lo} Z`
        : `M${x},${lo} V${hi} h${bw} V${lo} Z`, fill: colorOf(k), 'data-k': k }, g);
    });
    if (band >= 48 && totals[i] > 0) { const t = S('text', { x: cx, y: y(totals[i]) - 6, 'text-anchor': 'middle' }, g); t.textContent = compact(totals[i]); }
    const lab = S('text', { x: cx, y: Hh - 8, 'text-anchor': 'middle', class: 'muted' }, g); lab.textContent = monthLabel(m, band < 46);
    bind(g.firstChild, () => ({ title: monthLong(m), lines: [
      ...present.slice().reverse().map((k) => ({ name: k, value: zl(per.get(m).get(k)), color: colorOf(k) })),
      { name: 'Razem', value: zl(totals[i]) }] }), null);
  });
  renderLegend(series.filter((k) => rs.some((r) => fold(r.c) === k)).map((k) => [k, { v: 0 }]), false, 1);
  return { head: ['Miesiąc', ...series, 'Razem'],
    body: allMonths.map((m, i) => [monthLong(m), ...series.map((k) => zl(per.get(m).get(k) || 0)), zl(totals[i])]) };
}

const VIEWS = {
  cat: { label: 'Kategorie (słupkowy)', title: 'Wydatki wg kategorii', desc: 'Ile wydano w każdej kategorii, od największej.', fn: viewCat },
  share: { label: 'Udział (kołowy)', title: 'Struktura wydatków', desc: 'Udział największych kategorii; reszta zebrana w „Pozostałe”.', fn: viewShare },
  month: { label: 'Miesiące (skumulowany)', title: 'Wydatki miesiąc po miesiącu', desc: 'Suma miesięczna z podziałem na kategorie.', fn: viewMonth },
};
const SRC = { all: 'Wszystko', konto: 'Konto', karta: 'Karta kredytowa' };

function segment(el, options, key) {
  el.replaceChildren();
  for (const [k, label] of options) {
    const b = T('button', { type: 'button', 'aria-pressed': String(state[key] === k) }, label, el);
    b.addEventListener('click', () => { state[key] = k; render(); });
  }
}

function renderTable(t) {
  const wrap = $('#tbl'), btn = $('#tbtn');
  wrap.hidden = !state.table; btn.setAttribute('aria-expanded', String(state.table));
  btn.textContent = state.table ? 'Ukryj tabelę' : 'Pokaż tabelę';
  wrap.replaceChildren();
  if (!state.table) return;
  const tb = T('table', {}, null, wrap), tr = T('tr', {}, null, T('thead', {}, null, tb));
  t.head.forEach((h) => T('th', { scope: 'col' }, h, tr));
  const body = T('tbody', {}, null, tb);
  t.body.forEach((r) => { const row = T('tr', {}, null, body); r.forEach((c) => T('td', {}, c, row)); });
}

function render() {
  segment($('#src'), Object.entries(SRC), 'src');
  segment($('#view'), Object.entries(VIEWS).map(([k, v]) => [k, v.label]), 'view');
  const v = VIEWS[state.view];
  $('#title').textContent = v.title; $('#desc').textContent = v.desc;
  $('#legend').hidden = true;
  $('#card').insertBefore($('#legend'), $('#chart'));
  const box = $('#chart'); box.replaceChildren(); hideTip();
  renderTiles();
  renderTable(v.fn(box));
  const ms = allMonths; $('#period').textContent = `Dane od ${monthLong(ms[0])} do ${monthLong(ms[ms.length - 1])}`;
}
$('#tbtn').addEventListener('click', () => { state.table = !state.table; render(); });
let rt; window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(render, 120); });
render();
</script>
</body>
</html>
"""

if __name__ == '__main__':
    main()
