// King Salman Stadium — PowerPoint edition, glass design.
// Pass 1 (PASS=spec) records every glass panel and writes spec.json; glass.py bakes
// one background per slide (blurred 3D render + frosted panels); pass 2 builds the
// deck on those backgrounds with native, editable text and shapes.
const pptxgen = require('pptxgenjs');
const fs = require('fs'), path = require('path');
const { applyTheme } = require(process.env.PPTX_SKILL + '/scripts/apply_theme.js');
const META = JSON.parse(fs.readFileSync(path.join(__dirname, 'meta.json'), 'utf8'));
const SOURCES = require('./sources_data.js');
const IMG = (n) => path.join(__dirname, 'img', n);
const PASS = process.env.PASS || 'final';
const OUT = process.argv[2] || 'deck.pptx';

const F = { body: 'Arial', semi: 'ARIAL_BOLD', black: 'ARIAL_BOLD', light: 'ARIAL_REG' };   // Arial: identical on Mac and Windows
const THEME = { name: 'King Salman Night Glass', headFontFace: 'Arial', bodyFontFace: 'Arial',
  colors: { dk1: '0B1115', lt1: 'F2F7F6', dk2: '04090B', lt2: 'B4C5C2', accent1: '22D38B', accent2: 'E2B357', accent3: 'EE6A33', accent4: '4A95F0', accent5: 'D79A1E', accent6: '7F928F', hlink: '22D38B', folHlink: 'B4C5C2' } };
const HX = { fg: 'F2F7F6', fg2: 'B4C5C2', fg3: '7F928F', green: '22D38B', gold: 'E2B357', imp: 'EE6A33', blue: '4A95F0', credit: 'D79A1E', other: '6E837C', bg: '04090B' };

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = 'Building King Salman Stadium: how much of the money stays in Saudi Arabia?';
pres.author = 'Group 8 · MBSC EMBA'; pres.company = 'MBSC EMBA · ECN 511';
const C = pres.SchemeColor;
const W = 13.333, Hh = 7.5, MX = 0.62, CW = W - 2 * MX;

pres.defineSlideMaster({ title: 'CONTENT', background: { color: HX.bg }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: MX, y: 0.98, w: CW, h: 0.95, fontSize: 26, fontFace: 'Arial', bold: true, color: C.background1, valign: 'top', align: 'left', margin: 0 }, text: '' } }],
  slideNumber: { x: 12.3, y: 7.05, w: 0.42, h: 0.25, fontSize: 9, color: C.accent6, align: 'right', fontFace: 'Arial' } });
pres.defineSlideMaster({ title: 'DIVIDER', background: { color: HX.bg }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: MX + 0.4, y: 3.05, w: 9.2, h: 1.2, fontSize: 50, fontFace: 'Arial', bold: true, color: C.background1, valign: 'top', align: 'left', margin: 0 }, text: '' } }] });
pres.defineSlideMaster({ title: 'COVER', background: { color: HX.bg }, objects: [] });

// ── slide bookkeeping and the glass spec ────────────────────────────────
const SPEC = []; let cur = null;
function newSlide(master, sec, base, mode, shade) {
  const s = pres.addSlide({ masterName: master, sectionTitle: sec });
  cur = { i: SPEC.length + 1, base, mode, shade, panels: [] }; SPEC.push(cur);
  if (PASS === 'final') s.background = { path: IMG('s_' + String(cur.i).padStart(2, '0') + '.jpg') };
  return s;
}
const glass = (x, y, w, h, o = {}) => cur.panels.push(Object.assign({ x, y, w, h }, o));

// ── text and shape helpers ──────────────────────────────────────────────
function norm(o) {
  if (!o) return o;
  if (o.fontFace === 'ARIAL_BOLD') { o.fontFace = 'Arial'; o.bold = true; }
  else if (o.fontFace === 'ARIAL_REG') { o.fontFace = 'Arial'; o.bold = false; }
  return o;
}
function T(s, text, o) {
  if (Array.isArray(text)) text.forEach((r) => norm(r.options));
  s.addText(text, norm(Object.assign({ isTextBox: true, margin: 0, fontSize: 14, fontFace: F.body, color: C.background2, valign: 'top' }, o)));
}
const run = (text, o = {}) => ({ text, options: o });
function pill(s, x, y, w, h, o = {}) { glass(x, y, w, h, Object.assign({ r: h / 2, shadow: false }, o)); }
function eyebrow(s, text, x = MX, y = 0.46) {
  const w = 0.5 + text.length * 0.098;
  pill(s, x, y, w, 0.34, { tint: 'gold', edge: 'E2B357' });
  s.addShape(pres.shapes.OVAL, { x: x + 0.15, y: y + 0.135, w: 0.07, h: 0.07, fill: { color: HX.gold }, line: { color: HX.gold, width: 0 } });
  T(s, text.toUpperCase(), { x: x + 0.3, y, w: w - 0.32, h: 0.34, fontSize: 9, fontFace: F.semi, color: C.accent2, valign: 'middle', charSpacing: 1 });
}
const SPK = { 'Abdulmajeed Alajlan': ['AA', '22D38B'], 'Salman Alfaris': ['SA', '4A95F0'], 'Abdulaziz Alweheab': ['AW', 'EE6A33'],
  'Mohammed Alghamdi': ['MA', 'E2B357'], 'Abdulrahman Aldahlawi': ['AD', '2BC2CF'], 'Haifa Binnafisah': ['HB', 'C77BDB'], 'Nada Alyahya': ['NA', 'EE6A95'] };
function presenter(s, title) {
  const m = META[title]; if (!m || !SPK[m.who]) return;
  const [ini, col] = SPK[m.who];
  const tail = (m.sec && +m.sec ? m.sec + 's' : '') + (m.no && m.no !== '·' ? '   ' + m.no + ' / 12' : '');
  const w = 0.7 + m.who.length * 0.095 + tail.length * 0.08, x = W - MX - w, y = 0.43;
  pill(s, x, y, w, 0.4);
  s.addShape(pres.shapes.OVAL, { x: x + 0.06, y: y + 0.06, w: 0.28, h: 0.28, fill: { color: col }, line: { color: 'FFFFFF', width: 0.5, transparency: 60 } });
  T(s, ini, { x: x + 0.06, y: y + 0.06, w: 0.28, h: 0.28, fontSize: 8, fontFace: F.semi, color: '061410', align: 'center', valign: 'middle' });
  T(s, [run(m.who, { color: HX.fg, fontFace: F.semi }), run(tail ? '   ' + tail : '', { color: HX.fg3 })], { x: x + 0.44, y, w: w - 0.5, h: 0.4, fontSize: 10.5, valign: 'middle' });
}
function notes(s, title) {
  const m = META[title] || {};
  s.addNotes((m.who && SPK[m.who] ? m.who + (m.sec && +m.sec ? ' · ' + m.sec + ' seconds' : '') + '\n\n' : '') + (m.notes || ''));
}
function src(s, text, y = 6.68) { T(s, text, { x: MX, y, w: CW - 0.6, h: 0.32, fontSize: 8.5, color: C.accent6 }); }
function footer(s) { T(s, 'BUILDING KING SALMAN STADIUM  ·  GROUP 8', { x: MX, y: 7.05, w: 5, h: 0.25, fontSize: 8, fontFace: F.semi, color: C.accent6, charSpacing: 2 }); }
// a glass stat tile: big number, label
function stat(s, x, y, w, h, v, k, col, o = {}) {
  glass(x, y, w, h, o.g || {});
  T(s, v, { x: x + 0.26, y: y + 0.2, w: w - 0.5, h: o.vh || 0.7, fontSize: o.vs || 34, fontFace: F.black, color: col || HX.fg, fit: 'shrink', charSpacing: -0.5 });
  T(s, k, { x: x + 0.26, y: y + 0.2 + (o.vh || 0.7) + 0.06, w: w - 0.5, h: h - (o.vh || 0.7) - 0.4, fontSize: o.ks || 12, color: C.background2 });
}
// a glowing rounded bar, like the web deck's charts
function bar(s, x, y, w, h, col, o = {}) {
  if (o.track) s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: o.track, h, rectRadius: Math.min(h / 2, 0.1), fill: { color: 'FFFFFF', transparency: 93 }, line: { color: 'FFFFFF', width: 0, transparency: 100 } });
  if (w <= 0.02 || h <= 0.02) return;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: Math.min(Math.min(w, h) / 2, o.r || 0.08), fill: { color: col },
    line: { color: col, width: 0 }, shadow: { type: 'outer', color: col, blur: 14, offset: 0, angle: 90, opacity: 0.55 }, objectName: o.name });
}
function bullets(items, o = {}) { return items.map((t, i) => ({ text: t, options: Object.assign({ bullet: { code: '2192', indent: 16 }, breakLine: i < items.length - 1, paraSpaceAfter: 5 }, o) })); }
// glass "table": a header line and one glass row per record
function grid(s, x, y, colW, head, rows, o = {}) {
  const rh = o.rh || 0.6, w = colW.reduce((a, b) => a + b, 0);
  let cx = x; head.forEach((hd, i) => { T(s, hd.toUpperCase(), { x: cx + 0.18, y, w: colW[i] - 0.25, h: 0.28, fontSize: 9, fontFace: F.semi, color: C.accent2, charSpacing: 1.5, align: o.alignR && o.alignR.includes(i) ? 'right' : 'left' }); cx += colW[i]; });
  rows.forEach((r, ri) => {
    const ry = y + 0.36 + ri * (rh + 0.09), hl = o.hl === ri;
    glass(x, ry, w, rh, { r: 0.12, tint: hl ? 'gold' : 'glass', edge: hl ? 'E2B357' : null, shadow: false });
    let cx2 = x;
    r.forEach((c, ci) => {
      const first = ci === 0;
      T(s, c, { x: cx2 + 0.18, y: ry, w: colW[ci] - 0.3, h: rh, fontSize: o.fs || 11.5, valign: 'middle', fontFace: first ? F.semi : F.body,
        color: (o.colColor && o.colColor[ci]) || (first || hl ? HX.fg : HX.fg2), align: o.alignR && o.alignR.includes(ci) ? 'right' : 'left' });
      cx2 += colW[ci];
    });
  });
}
const THREAD = [['SAR 4.5bn', 'scenario', ''], ['SAR 2,143m', 'purchases', ''], ['SAR 421m', 'the leak', 'imp'], ['SAR 177m', 'chem + metals', 'imp'],
  ['SAR 84m', 'EP credit', 'credit'], ['SAR 44m', 'Saudi buying', 'green'], ['~SAR 36m', 'activity', 'green']];
function thread(s, n, now) {
  const step = 1.06, x0 = W - MX - THREAD.length * step - 0.5, y = 6.98;
  pill(s, x0 - 1.75, y - 0.04, THREAD.length * step + 1.8, 0.44, { alpha: .9 });
  T(s, 'FOLLOW THE RIYAL', { x: x0 - 1.6, y, w: 1.55, h: 0.36, fontSize: 7.5, fontFace: F.semi, color: C.accent2, charSpacing: 1.5, valign: 'middle' });
  THREAD.forEach((t, i) => {
    const lit = i < n, x = x0 + i * step;
    const col = !lit ? HX.fg3 : t[2] === 'imp' ? HX.imp : t[2] === 'credit' ? HX.credit : t[2] === 'green' ? HX.green : HX.fg;
    if (now.includes(i)) pill(s, x - 0.03, y - 0.0, step - 0.06, 0.36, { tint: 'gold', edge: 'E2B357' });
    T(s, [run(t[0], { fontFace: F.semi, color: col, fontSize: 9, breakLine: true }), run(t[1], { color: lit ? HX.fg2 : HX.fg3, fontSize: 6.5 })],
      { x, y: y + 0.02, w: step - 0.12, h: 0.34, align: 'center', valign: 'middle', transparency: lit ? 0 : 50 });
  });
}
function content(sec, base, title, head, eb, o = {}) {
  const s = newSlide('CONTENT', sec, base, 'content');
  s.addText(head.length > 62 ? [{ text: head, options: { fontSize: 22 } }] : head, { placeholder: 'title' });
  eyebrow(s, eb); presenter(s, title); notes(s, title); if (!o.noFooter) footer(s);
  return s;
}
function divider(sec, num, name, line, img) {
  const s = newSlide('DIVIDER', sec, img, 'photo', 0.9);
  glass(MX, 2.05, 9.9, 3.55, { r: 0.3, tint: 'dark' });
  T(s, num, { x: MX + 0.4, y: 2.3, w: 3, h: 0.7, fontSize: 40, fontFace: F.light, color: C.accent2 });
  T(s, 'PART', { x: MX + 1.55, y: 2.45, w: 2, h: 0.4, fontSize: 12, fontFace: F.semi, color: C.accent2, charSpacing: 5 });
  s.addText(name, { placeholder: 'title' });
  T(s, line, { x: MX + 0.4, y: 4.5, w: 9.0, h: 0.9, fontSize: 21, fontFace: F.light, color: C.background1 });
  s.addNotes('Part ' + num + ': ' + name + '. ' + line);
}

// ══ COVER ════════════════════════════════════════════════════════════════
pres.addSection({ title: 'Opening' });
{
  const s = newSlide('COVER', 'Opening', 'cover.jpg', 'photo', 0.95);
  glass(MX, 0.95, 8.25, 5.6, { r: 0.32, tint: 'dark' });
  eyebrow(s, 'MBSC EMBA · ECN 511 Economics for Managers', MX + 0.45, 1.35);
  T(s, [run('Building King Salman Stadium: ', { color: HX.fg }), run('how much of the money stays in Saudi Arabia?', { color: HX.green })],
    { x: MX + 0.45, y: 1.95, w: 7.4, h: 2.4, fontSize: 34, fontFace: F.semi, charSpacing: -0.5 });
  T(s, [run('Construction and Infrastructure  ·  '), run('Topic B: ', { color: HX.gold, fontFace: F.semi }), run('the multiplier effect of public capital spending, and where the money leaks')],
    { x: MX + 0.45, y: 4.45, w: 7.3, h: 0.75, fontSize: 14.5, color: C.background1 });
  T(s, 'GROUP 8', { x: MX + 0.45, y: 5.35, w: 3, h: 0.3, fontSize: 10, fontFace: F.semi, color: C.accent2, charSpacing: 4 });
  T(s, 'Abdulmajeed Alajlan  ·  Abdulrahman Aldahlawi  ·  Salman Alfaris  ·  Mohammed Alghamdi  ·  Abdulaziz Alweheab  ·  Nada Alyahya  ·  Haifa Binnafisah',
    { x: MX + 0.45, y: 5.65, w: 7.4, h: 0.6, fontSize: 11.5, color: C.background2 });
  T(s, 'Cover image: King Salman Stadium concept rendering © Populous', { x: MX, y: 7.05, w: 6, h: 0.25, fontSize: 8, color: C.accent6 });
  notes(s, 'Arrival');
}

// ══ PART 1 ═══════════════════════════════════════════════════════════════
const P1 = 'Part 1 · Our case', B1 = 'r_hero.jpg';
pres.addSection({ title: P1 });
divider(P1, '01', 'Our case', 'What a World Cup stadium buys, and who supplies it', 'r_hero.jpg');
{
  const t = 'Construction and Infrastructure';
  const s = content(P1, B1, t, 'Our case: the 2034 World Cup stadium programme', '01 · Construction and Infrastructure');
  // the photo, framed in glass
  glass(6.35, 1.95, 6.36, 4.0, { r: 0.24 });
  s.addImage({ path: IMG('aerial.jpg'), x: 6.5, y: 2.1, w: 6.06, h: 3.41, altText: 'King Salman Stadium concept rendering, aerial view', rounding: false });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.7, y: 4.98, w: 4.5, h: 0.42, rectRadius: 0.21, fill: { color: '061210', transparency: 25 }, line: { color: 'FFFFFF', width: 0.75, transparency: 70 } });
  T(s, [run('92,760 ', { fontFace: F.black, color: HX.gold, fontSize: 14 }), run('planned seats · King Salman Stadium, Riyadh', { color: HX.fg })], { x: 6.85, y: 4.98, w: 4.3, h: 0.42, fontSize: 10, valign: 'middle' });
  T(s, 'King Salman Stadium concept rendering © Populous', { x: 6.5, y: 5.58, w: 6.06, h: 0.25, fontSize: 8, color: C.accent6, align: 'right' });
  T(s, 'A stadium buys civil works, materials, building systems and specialist expertise.', { x: MX, y: 1.98, w: 5.4, h: 1.0, fontSize: 19, fontFace: F.semi, color: C.background1 });
  T(s, bullets(['Ministry of Sport buys the works.', 'Populous designs the stadium.', 'Contractors and specialist suppliers deliver.']), { x: MX, y: 3.1, w: 5.4, h: 1.2, fontSize: 14.5 });
  const tw = 1.78, ty = 4.3;
  stat(s, MX, ty, tw, 1.68, '15', 'stadiums in 5 host cities', null, { vh: 0.62, ks: 11 });
  stat(s, MX + tw + 0.1, ty, tw, 1.68, '7.8%', 'of Saudi value added, 2023 sector scale', HX.green, { vh: 0.62, ks: 11, g: { tint: 'green' } });
  stat(s, MX + 2 * (tw + 0.1), ty, tw, 1.68, 'SAR 646bn', 'gross output, 2023', HX.blue, { vs: 16, vh: 0.62, ks: 11 });
  src(s, 'Sources: FIFA 2034 bid evaluation; GASTAT Supply and Use Tables 2023; Ministry of Sport; Populous [R01, R05, R02–R03, R53].');
}
{
  const t = 'Who buys, who supplies';
  const s = content(P1, B1, t, 'A World Cup stadium is a construction job inside a sector worth 7.8% of the Saudi economy', 'Part 1 · The sector');
  const tw = (CW - 0.36) / 4, ty = 2.02;
  [['7.8%', 'of Saudi value added comes from construction (SAR 338bn of SAR 4,333bn, 2023)', HX.green, 'green'],
   ['SAR 646bn', 'construction output in 2023, of which SAR 307.5bn is bought-in inputs', HX.blue, 'glass'],
   ['15', 'stadiums across 5 host cities in FIFA’s 2024 bid evaluation', null, 'glass'],
   ['92,760', 'planned seats at King Salman Stadium, Riyadh — our case', HX.gold, 'gold']].forEach((d, i) =>
    stat(s, MX + i * (tw + 0.12), ty, tw, 1.42, d[0], d[1], d[2], { vs: 26, vh: 0.5, ks: 10.5, g: { tint: d[3] } }));
  grid(s, MX, 3.6, [3.0, 0.95, 1.95, 4.4, 1.79], ['Stadium', 'Seats', 'Who buys', 'Who supplies', 'Published value'], [
    ['Prince Mohammed bin Salman Stadium, Qiddiya', '45,000', 'Qiddiya Investment Co.', 'FCC (Spain) – Nesma (KSA); Elegancia: mechanical SAR 829m; IKK Fangda: facade SAR 997m ex-VAT', 'about SAR 4.0bn'],
    ['Aramco Stadium, Al Khobar', '46,096', 'Saudi Aramco', 'Besix (Belgium) – Albawani (KSA)', 'about SAR 3.7bn'],
    ['King Salman Stadium, Riyadh — our case', '92,760', 'Ministry of Sport', 'Main works prequalification notice (Nov 2025); design by Populous', '']],
    { rh: 0.56, fs: 10.5, hl: 2, alignR: [1, 4], colColor: { } });
  T(s, 'Not published', { x: MX + 10.3 + 0.18, y: 3.96 + 2 * 0.65, w: 1.79 - 0.3, h: 0.56, fontSize: 10.5, fontFace: F.semi, color: HX.imp, align: 'right', valign: 'middle' });
  T(s, [run('International–Saudi joint ventures deliver the main works; '), run('specialist imported systems arrive through subcontracts.', { color: HX.fg, fontFace: F.semi })], { x: MX, y: 5.98, w: CW, h: 0.4, fontSize: 13.5 });
  src(s, 'Sources: R05 (sheet 6.3), R01, R02–R03, R57, R58, R23–R24. Calculation: construction gross value added 338.3bn ÷ total GVA 4,332.9bn = 7.81% (GASTAT 2023, sheet 6.3).');
}

// ══ PART 2 ═══════════════════════════════════════════════════════════════
const P2 = 'Part 2 · Multiplier and leakage', B2 = 'r_bowl.jpg';
pres.addSection({ title: P2 });
divider(P2, '02', 'Multiplier and leakage', 'Follow the riyal: where it is spent, and where it leaks', 'r_bowl.jpg');
{
  const t = 'The spending multiplier';
  const s = content(P2, B2, t, 'One public payment creates income that people spend again', '02 · The spending multiplier, in simple terms');
  const bw = 2.38, gap = 0.3, bx = [MX, MX + bw + gap, MX + 2 * (bw + gap)], by = 2.55, bh = 1.95;
  const nodes = [['01', 'Public spending', 'The stadium pays a contractor.'], ['02', 'Income and spending', 'Workers and suppliers spend part of their income again.'], ['03', 'More Saudi production', 'Later spending supports additional goods and services.']];
  // re-spending loop 03 -> 02
  const lx1 = bx[1] + bw / 2, lx2 = bx[2] + bw / 2, ly = by - 0.42;
  s.addShape(pres.shapes.LINE, { x: lx2, y: ly, w: 0, h: 0.36, line: { color: HX.green, width: 2 } });
  s.addShape(pres.shapes.LINE, { x: lx1, y: ly, w: lx2 - lx1, h: 0, line: { color: HX.green, width: 2 } });
  s.addShape(pres.shapes.LINE, { x: lx1, y: ly, w: 0, h: 0.36, line: { color: HX.green, width: 2, endArrowType: 'triangle' } });
  T(s, 'spent again', { x: lx1, y: ly - 0.3, w: lx2 - lx1, h: 0.26, fontSize: 10.5, fontFace: F.semi, color: C.accent1, align: 'center' });
  nodes.forEach((n, i) => {
    glass(bx[i], by, bw, bh, { tint: i === 2 ? 'green' : 'glass', edge: i === 2 ? '22D38B' : null });
    pill(s, bx[i] + 0.22, by + 0.22, 0.56, 0.32, { tint: 'gold', edge: 'E2B357' });
    T(s, n[0], { x: bx[i] + 0.22, y: by + 0.22, w: 0.56, h: 0.32, fontSize: 10.5, fontFace: F.semi, color: C.accent2, align: 'center', valign: 'middle' });
    T(s, n[1], { x: bx[i] + 0.22, y: by + 0.66, w: bw - 0.44, h: 0.56, fontSize: 15, fontFace: F.semi, color: C.background1, valign: 'bottom' });
    T(s, n[2], { x: bx[i] + 0.22, y: by + 1.28, w: bw - 0.44, h: 0.62, fontSize: 11.5 });
    if (i < 2) s.addShape(pres.shapes.LINE, { x: bx[i] + bw + 0.04, y: by + bh / 2, w: gap - 0.08, h: 0, line: { color: HX.green, width: 2, endArrowType: 'triangle' } });
  });
  const leakY = by + bh + 0.55;
  glass(bx[0] + 1.3, leakY, 5.55, 0.56, { r: 0.28, tint: 'red', edge: 'EE6A33', shadow: false });
  T(s, 'Imports and saving reduce later rounds.', { x: bx[0] + 1.3, y: leakY, w: 5.55, h: 0.56, fontSize: 14, fontFace: F.semi, color: C.accent3, align: 'center', valign: 'middle' });
  [lx1, lx2 - 0.4].forEach((x) => s.addShape(pres.shapes.LINE, { x, y: by + bh + 0.06, w: 0, h: 0.45, line: { color: HX.imp, width: 1.5, dashType: 'dash', endArrowType: 'triangle' } }));
  const rx = 8.92, rw = W - MX - rx;
  glass(rx, 2.0, rw, 2.0, { tint: 'gold', edge: 'E2B357' });
  T(s, 'GDP multiplier = extra GDP caused ÷ extra public spending', { x: rx + 0.26, y: 2.18, w: rw - 0.5, h: 0.85, fontSize: 15.5, fontFace: F.semi, color: C.background1 });
  T(s, [run('Illustration: SAR 100m extra spending causes SAR 120m extra GDP. '), run('Multiplier = 1.2.', { fontFace: F.semi, color: HX.gold })], { x: rx + 0.26, y: 3.08, w: rw - 0.5, h: 0.8, fontSize: 12 });
  [['MICRO', 'A firm chooses a supplier.', 'glass'], ['MACRO', 'The combined effect on GDP.', 'glass'], ['OUR TOPIC', 'The spending multiplier is macroeconomics.', 'gold']].forEach((c, i) => {
    const y = 4.15 + i * 0.78; glass(rx, y, rw, 0.66, { r: 0.16, tint: c[2], shadow: false });
    T(s, c[0], { x: rx + 0.26, y, w: 1.1, h: 0.66, fontSize: 9, fontFace: F.semi, color: C.accent2, valign: 'middle', charSpacing: 1.5 });
    T(s, c[1], { x: rx + 1.35, y, w: rw - 1.5, h: 0.66, fontSize: 12.5, color: C.background1, valign: 'middle' });
  });
  src(s, 'Source: IMF, Fiscal Multipliers, 2014, section II [R69]. Teaching example, not a Saudi estimate.');
}
{
  const t = 'Construction and Saudi GDP';
  const s = content(P2, B2, t, 'Our sector creates assets and adds value through Saudi production', '03 · Construction and Saudi GDP');
  const gx = MX, gy = 2.0, gw = 7.0, gh = 4.45;
  glass(gx, gy, gw, gh, { r: 0.24 });
  T(s, 'GASTAT 2023 [R05]', { x: gx + 0.3, y: gy + 0.22, w: 4, h: 0.25, fontSize: 9, fontFace: F.semi, color: C.accent2, charSpacing: 1.5 });
  T(s, 'Saudi construction, 2023 — SAR billion', { x: gx + 0.3, y: gy + 0.48, w: 6.4, h: 0.4, fontSize: 15, fontFace: F.semi, color: C.background1 });
  const vals = [['Gross output', 645.8, HX.blue, '645.8'], ['Less: bought-in inputs', 307.5, HX.imp, '−307.5'], ['Construction value added', 338.3, HX.green, '338.3']];
  const base = gy + gh - 0.65, top = gy + 1.35, scale = (base - top) / 645.8, colw = gw / 3;
  s.addShape(pres.shapes.LINE, { x: gx + 0.3, y: base, w: gw - 0.6, h: 0, line: { color: 'FFFFFF', width: 0.75, transparency: 70 } });
  vals.forEach((v, i) => {
    const cx = gx + colw * i + colw / 2, bwid = 0.95, h = v[1] * scale;
    const y0 = i === 1 ? base - 645.8 * scale : base - h;      // the inputs bar hangs from the output level, a waterfall
    bar(s, cx - bwid / 2, y0, bwid, h, v[2], { r: 0.1 });
    T(s, v[3], { x: cx - 1.0, y: y0 - 0.48, w: 2.0, h: 0.42, fontSize: 18, fontFace: F.black, color: C.background1, align: 'center' });
    T(s, v[0], { x: cx - 1.1, y: base + 0.1, w: 2.2, h: 0.45, fontSize: 11, color: C.background2, align: 'center' });
  });
  [[0, 1, 645.8], [1, 2, 338.3]].forEach(([a, b, lvl]) => s.addShape(pres.shapes.LINE, { x: gx + colw * a + colw / 2 + 0.48, y: base - lvl * scale, w: colw - 0.96, h: 0, line: { color: 'FFFFFF', width: 0.75, dashType: 'dash', transparency: 55 } }));
  const rx = 7.85, rw = W - MX - rx;
  stat(s, rx, 2.0, rw, 1.5, '7.8%', 'of Saudi gross value added', HX.green, { vs: 44, vh: 0.78, g: { tint: 'green', edge: '22D38B' } });
  glass(rx, 3.65, rw, 1.45);
  T(s, [run('GDP counts the extra value created at each Saudi stage '), run('once', { fontFace: F.semi, color: HX.fg }), run('. A local supplier’s full invoice also includes inputs bought from other firms.')], { x: rx + 0.26, y: 3.82, w: rw - 0.5, h: 1.2, fontSize: 13.5 });
  glass(rx, 5.25, rw, 1.2, { tint: 'gold', edge: 'E2B357' });
  T(s, [run('Academy link: ', { fontFace: F.semi, color: HX.gold }), run('qualified local suppliers can win orders and create extra Saudi value.', { color: HX.fg })], { x: rx + 0.26, y: 5.4, w: rw - 0.5, h: 0.95, fontSize: 13.5 });
  src(s, 'Source: GASTAT, Supply and Use Tables 2023, sheets 6.2–6.3 [R05]. Sector share describes scale, not a GDP multiplier.');
}
{
  const t = 'How import-dependent it is';
  const s = content(P2, B2, t, 'Construction’s two most imported inputs: basic metals (54.5%) and electrical machinery (50.3%)', 'Part 1 · How import-dependent it is', { noFooter: true });
  glass(MX, 2.0, CW, 1.0, { r: 0.2 });
  T(s, 'SAR 646bn construction output in 2023, of which SAR 307.5bn is bought-in inputs', { x: MX + 0.26, y: 2.1, w: CW - 0.5, h: 0.28, fontSize: 11.5, fontFace: F.semi, color: C.background1 });
  const bw = CW - 0.52, wi = bw * 0.197;
  bar(s, MX + 0.26, 2.48, wi - 0.04, 0.38, HX.imp, { r: 0.19 }); bar(s, MX + 0.26 + wi, 2.48, bw - wi, 0.38, HX.green, { r: 0.19 });
  T(s, 'Imported 19.7% · SAR 60.5bn', { x: MX + 0.4, y: 2.48, w: wi, h: 0.38, fontSize: 10.5, fontFace: F.semi, color: 'FFFFFF', valign: 'middle' });
  T(s, 'Made in Saudi Arabia 80.3% · SAR 247.0bn', { x: MX + 0.4 + wi, y: 2.48, w: 6, h: 0.38, fontSize: 10.5, fontFace: F.semi, color: '04150D', valign: 'middle' });
  const rows = [['Basic metals', 'steel, aluminium, copper', 54.5, 11.97], ['Electrical machinery', 'cables, switchgear, transformers', 50.3, 2.01], ['Wood products', 'timber, plywood, wooden doors', 44.7, 5.58],
    ['Other chemical products', 'paints, sealants, adhesives', 43.2, 13.43], ['Rubber and plastics', 'PVC pipes, insulation, seals', 32.6, 2.15], ['Glass and non-metallic', 'cement, glass, ceramic tiles', 11.8, 4.93],
    ['Refined petroleum', 'diesel, asphalt, lubricants', 8.0, 4.14], ['Basic chemicals', 'industrial gases, resins, solvents', 7.3, 4.33]];
  const gy = 3.15; glass(MX, gy, CW, 3.38, { r: 0.22 });
  T(s, 'IMPORT LEAKAGE BY INPUT — AS A SHARE AND AS AN AMOUNT (CONSTRUCTION, 2023)', { x: MX + 0.26, y: gy + 0.16, w: 8, h: 0.24, fontSize: 8.5, fontFace: F.semi, color: C.accent2, charSpacing: 1.2 });
  const sx = MX + 3.55, sw = 4.0, ax = MX + 8.25, aw = 2.75, ry0 = gy + 0.78, rh = 0.315;
  T(s, 'Share of national supply that is imported', { x: sx, y: gy + 0.45, w: sw, h: 0.24, fontSize: 9.5, color: C.background2 });
  T(s, 'Imported amount, SAR bn', { x: ax, y: gy + 0.45, w: aw, h: 0.24, fontSize: 9.5, color: C.background2 });
  const top2 = [3, 0];
  rows.forEach((r, i) => {
    const y = ry0 + i * rh;
    T(s, [run(r[0], { fontFace: F.semi, color: HX.fg }), run('  ' + r[1], { color: HX.fg3, fontSize: 8.5 })], { x: MX + 0.26, y, w: 3.25, h: rh, fontSize: 10.5, valign: 'middle' });
    const hiS = i < 2, hiA = top2.includes(i);
    bar(s, sx, y + 0.07, sw * r[2] / 100, rh - 0.14, hiS ? HX.imp : HX.other, { track: sw, r: 0.09 });
    T(s, r[2].toFixed(1) + '%', { x: sx + sw * r[2] / 100 + 0.08, y, w: 0.8, h: rh, fontSize: 10.5, fontFace: F.semi, color: C.background1, valign: 'middle' });
    bar(s, ax, y + 0.07, aw * r[3] / 14, rh - 0.14, hiA ? HX.imp : HX.other, { r: 0.09 });
    T(s, r[3].toFixed(1), { x: ax + aw * r[3] / 14 + 0.08, y, w: 0.6, h: rh, fontSize: 10.5, fontFace: F.semi, color: C.background1, valign: 'middle' });
  });
  T(s, [run('Metals and electrical machinery are half imported; '), run('by amount, chemical products and metals are the largest leaks.', { fontFace: F.semi, color: HX.fg })], { x: MX, y: 6.6, w: CW, h: 0.28, fontSize: 11.5 });
  src(s, 'Source: GASTAT, Supply and Use Tables 2023 [R05] — use: sheet 6.2 col. H; import rate: sheet 6.1 Total imports (AA) ÷ Supply at basic prices (AB). National ratios applied to construction purchases.', 6.86);
}
{
  const t = 'A SAR 4.5bn stadium scenario';
  const s = content(P2, B2, t, 'Applying a SAR 4.5bn stadium scenario', '04 · Applying the multiplier to our case', { noFooter: true });
  const tw = (CW - 0.24) / 3;
  [['about SAR 4.0bn', 'Qiddiya stadium · 45,000 seats', null, {}], ['about SAR 3.7bn', 'Aramco Stadium · 46,096 seats', null, {}],
   ['SAR 4.5bn', 'Group scenario, not a published budget or a validated cost estimate', HX.green, { tint: 'green', edge: '22D38B' }]].forEach((d, i) =>
    stat(s, MX + i * (tw + 0.12), 2.0, tw, 1.42, d[0], d[1], d[2], { vs: 27, vh: 0.55, g: d[3] }));
  glass(MX, 3.6, CW, 2.9, { r: 0.26 });
  T(s, 'ROUND 1', { x: MX + 0.32, y: 3.82, w: 3, h: 0.25, fontSize: 9, fontFace: F.semi, color: C.accent2, charSpacing: 3 });
  T(s, 'Estimated purchases using GASTAT 2023 construction ratios', { x: MX + 0.32, y: 4.06, w: 9, h: 0.38, fontSize: 16, fontFace: F.semi, color: C.background1 });
  T(s, [run('SAR 2,143m   ', { fontSize: 26, fontFace: F.black, color: HX.fg }), run('total purchases = 47.6% of the SAR 4.5bn', { fontSize: 12.5 })], { x: MX + 0.32, y: 4.5, w: 11, h: 0.5, valign: 'middle' });
  const bx = MX + 0.32, bw2 = CW - 0.64, wl = bw2 * 1721 / 2143;
  bar(s, bx, 5.1, wl - 0.05, 0.5, HX.green, { r: 0.25 }); bar(s, bx + wl, 5.1, bw2 - wl, 0.5, HX.imp, { r: 0.25 });
  T(s, [run('SAR 1,721m  ', { fontFace: F.black, color: HX.green, fontSize: 15 }), run('Purchases inside Saudi Arabia (80.3%) → next spending round')], { x: bx, y: 5.74, w: 6.3, h: 0.55, fontSize: 12 });
  T(s, [run('SAR 421m  ', { fontFace: F.black, color: HX.imp, fontSize: 15 }), run('Purchases from abroad (19.7%) — the first leak')], { x: bx + 6.3, y: 5.74, w: bw2 - 6.3, h: 0.55, fontSize: 12, align: 'right' });
  src(s, 'Sources: R57, R58 (benchmarks); GASTAT Supply and Use Tables 2023, sheets 6.1–6.2 [R05]. Group scenario using national ratios; figures are rounded.', 6.58);
  thread(s, 3, [0, 1, 2]);
}
{
  const t = 'The materials behind the leakage';
  const s = content(P2, B2, t, 'Estimated imports in the SAR 4.5bn stadium scenario', '05 · The materials behind the import leakage', { noFooter: true });
  const cats = [['Basic metals', 83, 1], ['Electrical machinery', 14], ['Wood products', 39], ['Other chemical products', 94, 1], ['Rubber and plastics', 15], ['Glass and non-metallic', 34], ['Refined petroleum', 29], ['Basic chemicals', 30], ['All other inputs', 83]];
  const gx = MX, gw = 7.8; glass(gx, 2.0, gw, 4.5, { r: 0.24 });
  T(s, 'ESTIMATED STADIUM IMPORTS, SAR MILLION', { x: gx + 0.3, y: 2.18, w: 6, h: 0.24, fontSize: 8.5, fontFace: F.semi, color: C.accent2, charSpacing: 1.2 });
  const lx = gx + 2.55, lw = 4.3, rh = 0.42;
  cats.forEach((c, i) => {
    const y = 2.55 + i * rh;
    T(s, c[0], { x: gx + 0.3, y, w: 2.2, h: rh, fontSize: 11, fontFace: c[2] ? F.semi : F.body, color: c[2] ? HX.fg : HX.fg2, valign: 'middle', align: 'right' });
    bar(s, lx, y + 0.09, lw * c[1] / 100, rh - 0.18, c[2] ? HX.imp : HX.other, { track: lw, r: 0.12 });
    T(s, String(c[1]), { x: lx + lw * c[1] / 100 + 0.1, y, w: 0.6, h: rh, fontSize: 12, fontFace: F.semi, color: C.background1, valign: 'middle' });
  });
  const rx = 8.62, rw = W - MX - rx;
  glass(rx, 2.0, rw, 1.6, { tint: 'red', edge: 'EE6A33' });
  T(s, 'STADIUM IMPORTS', { x: rx + 0.26, y: 2.16, w: 3, h: 0.24, fontSize: 9, fontFace: F.semi, color: C.accent3, charSpacing: 2 });
  T(s, 'SAR 421m', { x: rx + 0.26, y: 2.4, w: rw - 0.5, h: 0.6, fontSize: 32, fontFace: F.black, color: HX.imp });
  T(s, '19.7% of the SAR 2,143m estimated purchases split by input', { x: rx + 0.26, y: 3.02, w: rw - 0.5, h: 0.52, fontSize: 11 });
  stat(s, rx, 3.74, rw, 1.32, 'SAR 177m', 'Chemicals + metals · 42% of stadium’s imports', HX.gold, { vs: 28, vh: 0.55, g: { tint: 'gold', edge: 'E2B357' } });
  glass(rx, 5.2, rw, 1.3);
  T(s, 'ACTUAL ITEM CHECK', { x: rx + 0.26, y: 5.33, w: rw - 0.5, h: 0.25, fontSize: 9, fontFace: F.semi, color: C.accent2, charSpacing: 1.5 });
  T(s, 'Grade, quantity, origin, certification and price from supplier schedules.', { x: rx + 0.26, y: 5.6, w: rw - 0.5, h: 0.8, fontSize: 12.5, color: C.background1 });
  src(s, 'Examples under each group are illustrative. Each bar retains its whole GASTAT group value. Source: GASTAT, Supply and Use Tables 2023, sheets 6.1–6.2 [R05]. National product ratios applied to construction use; group scenario, not invoices.', 6.58);
  thread(s, 4, [3]);
}

// ══ PART 3 ═══════════════════════════════════════════════════════════════
const P3 = 'Part 3 · EPP and controls', B3 = 'r_yard.jpg';
pres.addSection({ title: P3 });
divider(P3, '03', 'EPP and controls', 'Turning the leak into an obligation', 'r_yard.jpg');
{
  const t = 'Stadium EPP at 20%';
  const s = content(P3, B3, t, 'Assessment basis: the official April 2026 consultation framework', '06 · Stadium EPP at 20 percent, credit up to 6', { noFooter: true });
  const ew = 3.5, ex = [MX, MX + ew + 0.6, MX + 2 * (ew + 0.6)];
  [['SAR 421m', 'Estimated stadium imports · SAR 4.5bn scenario, slide 5', HX.imp, { tint: 'red' }], ['20%', 'Second import tier · SAR 300m–500m per tender', HX.fg, {}],
   ['SAR 84m', 'Required EP credit · 421m × 20%', HX.credit, { tint: 'gold', edge: 'E2B357' }]].forEach((d, i) => stat(s, ex[i], 2.0, ew, 1.35, d[0], d[1], d[2], { vs: 32, vh: 0.62, g: d[3] }));
  T(s, '×', { x: ex[0] + ew, y: 2.3, w: 0.6, h: 0.7, fontSize: 30, fontFace: F.light, color: C.accent2, align: 'center' });
  T(s, '=', { x: ex[1] + ew, y: 2.3, w: 0.6, h: 0.7, fontSize: 30, fontFace: F.light, color: C.accent2, align: 'center' });
  const gx = MX, gw = 6.7; glass(gx, 3.52, gw, 2.5, { r: 0.22 });
  T(s, 'IMPORT TIERS (PER TENDER) AND THE EP OBLIGATION', { x: gx + 0.28, y: 3.68, w: 6, h: 0.24, fontSize: 8.5, fontFace: F.semi, color: C.accent2, charSpacing: 1.2 });
  const tiers = [['SAR 75m–300m', 25, HX.other], ['SAR 300m–500m', 20, HX.credit, 'our SAR 421m'], ['above SAR 500m', 15, HX.other]];
  const base = 5.55, sc = 1.25 / 25, cw = (gw - 0.6) / 3;
  tiers.forEach((t2, i) => {
    const x = gx + 0.3 + i * cw, h = t2[1] * sc;
    bar(s, x + 0.25, base - h, cw - 0.5, h, t2[2], { r: 0.1 });
    T(s, t2[1] + '%', { x: x + 0.25, y: base - h + 0.08, w: cw - 0.5, h: 0.4, fontSize: 17, fontFace: F.black, color: i === 1 ? '1B1405' : 'FFFFFF', align: 'center' });
    T(s, t2[0], { x, y: base + 0.06, w: cw, h: 0.24, fontSize: 10, color: C.background2, align: 'center' });
    if (t2[3]) T(s, '▼ ' + t2[3], { x, y: base - h - 0.32, w: cw, h: 0.26, fontSize: 9.5, fontFace: F.semi, color: C.accent3, align: 'center' });
  });
  T(s, [run('Assumption: ', { fontFace: F.semi, color: HX.gold }), run('one main contract with one company, so all SAR 421m counts.')], { x: MX, y: 6.12, w: gw, h: 0.4, fontSize: 12.5 });
  const rx = 7.55, rw = W - MX - rx;
  glass(rx, 3.52, rw, 1.25);
  T(s, 'DRAFT CATEGORY FACTORS', { x: rx + 0.26, y: 3.66, w: rw, h: 0.24, fontSize: 8.5, fontFace: F.semi, color: C.accent2, charSpacing: 1.2 });
  T(s, [run('Knowledge transfer / localisation   '), run('1–3', { fontFace: F.semi, color: HX.fg, breakLine: true }), run('Technology transfer / exports   '), run('2–4', { fontFace: F.semi, color: HX.fg })], { x: rx + 0.26, y: 3.95, w: rw - 0.5, h: 0.75, fontSize: 12.5 });
  glass(rx, 4.9, rw, 1.12, { tint: 'gold', edge: 'E2B357' });
  T(s, '4 + 2 = 6', { x: rx + 0.26, y: 4.9, w: 1.9, h: 1.12, fontSize: 25, fontFace: F.black, color: HX.gold, valign: 'middle' });
  T(s, 'Qualifying base + approved bonus. Rare technology or other eligible grounds.', { x: rx + 2.15, y: 4.9, w: rw - 2.35, h: 1.12, fontSize: 11.5, valign: 'middle' });
  T(s, 'Credit differs from cash, GDP and ROI.', { x: rx, y: 6.12, w: rw, h: 0.4, fontSize: 12.5, fontFace: F.semi, color: C.background1 });
  src(s, 'Source: LCGPA, Economic Participation Policy Update, consultation text, Articles 6–9 [R63]; DGA Group, April 2026. Imports: group scenario [R05]. Actual tender terms control the applicable version.', 6.55);
  thread(s, 5, [4]);
}
{
  const t = 'London 2012';
  const s = content(P3, B3, t, 'A fixed event deadline made live-site learning especially valuable', '07 · London 2012 offers a construction skills lesson');
  glass(6.95, 2.0, W - MX - 6.95, 3.25, { r: 0.24 });
  s.addImage({ path: IMG('r_side.jpg'), x: 7.1, y: 2.15, w: W - MX - 7.25, h: 2.95, sizing: { type: 'cover', w: W - MX - 7.25, h: 2.95 }, altText: '3D model of the stadium' });
  stat(s, MX, 2.0, 3.05, 1.55, '3,000+', 'training places', HX.green, { vs: 38, vh: 0.75, g: { tint: 'green' } });
  stat(s, MX + 3.2, 2.0, 3.05, 1.55, '408', 'apprentices', null, { vs: 38, vh: 0.75 });
  glass(MX, 3.7, 3.05, 1.55);
  T(s, '✓  WHAT WORKED', { x: MX + 0.26, y: 3.86, w: 2.6, h: 0.26, fontSize: 9, fontFace: F.semi, color: '3DDB6A', charSpacing: 1.2 });
  T(s, [run('Training connected to '), run('real construction jobs', { fontFace: F.semi, color: HX.fg }), run('.')], { x: MX + 0.26, y: 4.16, w: 2.6, h: 1.0, fontSize: 13 });
  glass(MX + 3.2, 3.7, 3.05, 1.55);
  T(s, '▲  WHAT WAS WEAKER', { x: MX + 3.46, y: 3.86, w: 2.6, h: 0.26, fontSize: 9, fontFace: F.semi, color: 'FAB219', charSpacing: 1.2 });
  T(s, [run('Encouragement '), run('without binding targets', { fontFace: F.semi, color: HX.fg }), run(' made skills objectives harder.')], { x: MX + 3.46, y: 4.16, w: 2.6, h: 1.0, fontSize: 13 });
  glass(MX, 5.45, CW, 0.95, { tint: 'gold', edge: 'E2B357', r: 0.24 });
  T(s, [run('Saudi adaptation:  ', { fontFace: F.semi, color: HX.gold }), run('paid practice, independent tests and a return-to-train commitment', { color: HX.fg })], { x: MX + 0.35, y: 5.45, w: CW - 0.7, h: 0.95, fontSize: 18, fontFace: F.light, valign: 'middle' });
  src(s, 'Sources: UK DCMS, 2012 Games construction on track, 20 May 2012 [R12]; Crossrail Learning Legacy, 2018 [R13]. Counts do not prove retained jobs.');
}
{
  const t = 'The controls';
  const s = content(P3, B3, t, 'Five risks, five controls', '08 · The controls that make the solution credible');
  const rows = [['Routine training earns extra credit', 'Record existing duties. Fund new competence, rights or tooling.'], ['IP cannot be used independently', 'Agree licences, diagnostic access, trainer rights and export territory.'],
    ['Shared delivery duplicates claims', 'Keep each supplier’s approved activities, cost allocation and ledger separate.'], ['Local substitutes or bulk buying fail', 'Test grades, capacity and full cost. Use fair lots and multiple suppliers.'],
    ['Skills have no work after handover', 'Confirm placements before training and contract the next site.']];
  T(s, 'RISK', { x: MX + 0.62, y: 1.95, w: 3, h: 0.24, fontSize: 8.5, fontFace: F.semi, color: C.accent2, charSpacing: 2 });
  T(s, 'PROPOSED CONTROL', { x: 5.9, y: 1.95, w: 3, h: 0.24, fontSize: 8.5, fontFace: F.semi, color: C.accent2, charSpacing: 2 });
  rows.forEach((r, i) => {
    const y = 2.27 + i * 0.66; glass(MX, y, CW, 0.56, { r: 0.14, shadow: false });
    s.addShape(pres.shapes.OVAL, { x: MX + 0.2, y: y + 0.15, w: 0.26, h: 0.26, fill: { color: HX.imp, transparency: 75 }, line: { color: HX.imp, width: 1 } });
    T(s, String(i + 1), { x: MX + 0.2, y: y + 0.15, w: 0.26, h: 0.26, fontSize: 9, fontFace: F.semi, color: C.accent3, align: 'center', valign: 'middle' });
    T(s, r[0], { x: MX + 0.62, y, w: 4.6, h: 0.56, fontSize: 13, fontFace: F.semi, color: C.background1, valign: 'middle' });
    T(s, '→', { x: 5.45, y, w: 0.35, h: 0.56, fontSize: 14, color: C.accent1, valign: 'middle' });
    T(s, r[1], { x: 5.9, y, w: 6.7, h: 0.56, fontSize: 12.5, valign: 'middle' });
  });
  glass(MX, 5.62, CW, 0.98, { r: 0.22 });
  T(s, 'EVIDENCE AT THREE POINTS', { x: MX + 0.3, y: 5.62, w: 2.6, h: 0.98, fontSize: 9, fontFace: F.semi, color: C.accent2, charSpacing: 1.5, valign: 'middle' });
  const tl = [['Before', 'baseline and rights'], ['Completion', 'independent tests'], ['6 / 12 months', 'work and trainer return']], tx0 = 3.75, tx1 = 11.6;
  s.addShape(pres.shapes.LINE, { x: tx0, y: 5.9, w: tx1 - tx0, h: 0, line: { color: HX.green, width: 2, transparency: 20 } });
  tl.forEach((p, i) => {
    const cx = tx0 + i * (tx1 - tx0) / 2;
    s.addShape(pres.shapes.OVAL, { x: cx - 0.11, y: 5.79, w: 0.22, h: 0.22, fill: { color: HX.bg }, line: { color: i === 2 ? HX.gold : HX.green, width: 3 }, shadow: { type: 'outer', color: i === 2 ? HX.gold : HX.green, blur: 8, offset: 0, angle: 90, opacity: 0.7 } });
    T(s, [run(p[0], { fontFace: F.semi, color: HX.fg, breakLine: true }), run(p[1])], { x: cx - 1.4, y: 6.04, w: 2.8, h: 0.5, fontSize: 11, align: 'center' });
  });
  src(s, 'Sources: LCGPA consultation Arts. 8(3), 13–16 [R63]; WIPO licensing [R64]; OECD competition safeguards [R68]; UK additionality study [R54].');
}

// ══ PART 4 ═══════════════════════════════════════════════════════════════
const P4 = 'Part 4 · The academy proposal', B4 = 'r_scoreboard.jpg';
pres.addSection({ title: P4 });
divider(P4, '04', 'The academy proposal', 'Turning the obligation into Saudi capability', 'r_scoreboard.jpg');
{
  const t = 'One academy, three functions';
  const s = content(P4, B4, t, 'Shared delivery across eligible stadium suppliers, with separate EP obligations', '09 · One academy with three connected functions');
  glass(MX, 2.02, CW, 0.74, { tint: 'gold', edge: 'E2B357', r: 0.2 });
  T(s, [run('Shared EPP proposal:  ', { fontFace: F.semi, color: HX.gold }), run('eligible stadium vendors jointly fund ONE academy. Each vendor contributes approved funding, trainers, equipment or licensed know-how.', { color: HX.fg })], { x: MX + 0.3, y: 2.02, w: CW - 0.6, h: 0.74, fontSize: 13, valign: 'middle' });
  const fx = [['01', 'License and train', ['Licensed manuals and software', 'HVAC rigs and coating-test kits', 'Paid practice and Saudi trainers'], 'Evidence: NITI training; WIPO licensing terms'],
    ['02', 'Qualify Saudi materials', ['Coatings, sealants and metals', 'Test specific grades and origin', 'Material passports for approvals'], 'Evidence: ALUPCO extrusion; Sika Saudi admixture production'],
    ['03', 'Buy together', ['Common performance specifications', 'Competitive framework and call-offs', 'Verify discounts and full cost'], 'Evidence: OECD purchasing efficiency and competition']];
  const fw = (CW - 0.3) / 3;
  fx.forEach((f, i) => {
    const x = MX + i * (fw + 0.15), y = 2.92; glass(x, y, fw, 2.3, { tint: 'green', edge: '22D38B' });
    s.addShape(pres.shapes.OVAL, { x: x + 0.24, y: y + 0.22, w: 0.46, h: 0.46, fill: { color: HX.green, transparency: 78 }, line: { color: HX.green, width: 1.25 } });
    T(s, f[0], { x: x + 0.24, y: y + 0.22, w: 0.46, h: 0.46, fontSize: 11, fontFace: F.semi, color: C.accent1, align: 'center', valign: 'middle' });
    T(s, f[1], { x: x + 0.82, y: y + 0.22, w: fw - 1.0, h: 0.46, fontSize: 15, fontFace: F.semi, color: C.background1, valign: 'middle' });
    T(s, bullets(f[2]), { x: x + 0.26, y: y + 0.82, w: fw - 0.5, h: 0.95, fontSize: 11.5, color: C.background1 });
    T(s, f[3], { x: x + 0.26, y: y + 1.82, w: fw - 0.5, h: 0.42, fontSize: 9.5, color: C.accent6 });
  });
  glass(MX, 5.36, (CW - 0.15) / 2, 0.92, { shadow: false });
  T(s, 'One qualified host runs the programme. Sharing trainers, equipment and demand reduces duplicated training and keeps skills available across sites.', { x: MX + 0.24, y: 5.36, w: (CW - 0.15) / 2 - 0.45, h: 0.92, fontSize: 11.5, valign: 'middle' });
  const x2 = MX + (CW - 0.15) / 2 + 0.15; glass(x2, 5.36, (CW - 0.15) / 2, 0.92, { shadow: false });
  T(s, [run('LCGPA approves vendor roles and cost allocations. '), run('Each vendor keeps its own EP obligation and ledger. Each activity earns credit once.', { fontFace: F.semi, color: HX.fg })], { x: x2 + 0.24, y: 5.36, w: (CW - 0.15) / 2 - 0.45, h: 0.92, fontSize: 11.5, valign: 'middle' });
  T(s, [run('Later: ', { fontFace: F.semi, color: HX.gold }), run('export Saudi-owned courses, licensed services and qualified products.')], { x: MX, y: 6.38, w: CW, h: 0.28, fontSize: 12 });
  src(s, 'Sources: NITI [R42]; official LCGPA draft Arts. 8–9 [R63]; WIPO [R64]; OECD [R65, R68]; ALUPCO [R66]; Sika [R67]. Candidate capabilities, not partner commitments.', 6.72);
}
{
  const t = 'Hands-on training first';
  const s = content(P4, B4, t, 'Begin inside real projects with an existing qualified training provider', '10 · Hands-on training first, academy after evidence');
  T(s, [run('Joint agreement first: ', { fontFace: F.semi, color: HX.gold }), run('vendor commitments, LCGPA-approved activities and separate credit records.')], { x: MX, y: 1.95, w: CW, h: 0.3, fontSize: 12.5 });
  const st = [['1', 'Confirm demand', 'Employers identify the skills gap and sign paid site placements. Vendor roles and funding are agreed.', 'Next-site work, budget, IP rights, tools and approvals are confirmed. Signed licences and EP cost allocations.'],
    ['2', 'Run the pilot', 'Supplier mentors teach on real equipment. Independent tests and trainer practice. Saudi trainers teach the next cohort.', 'Verify practical competence, paid deployment and unit cost. Record extra capability beyond routine duties.'],
    ['3', 'Expand if proven', 'Repeat cohorts build an academy. A permanent facility needs its own case. Use existing facilities where adequate.', 'Continuing jobs and orders, proven results and acceptable quality and cost. Track work and trainer return at 6/12 months.']];
  const sw = (CW - 0.7) / 3;
  st.forEach((p, i) => {
    const x = MX + i * (sw + 0.35), y = 2.4; glass(x, y, sw, 3.25);
    s.addShape(pres.shapes.OVAL, { x: x + 0.24, y: y + 0.24, w: 0.46, h: 0.46, fill: { color: HX.gold, transparency: 80 }, line: { color: HX.gold, width: 1.25 } });
    T(s, p[0], { x: x + 0.24, y: y + 0.24, w: 0.46, h: 0.46, fontSize: 14, fontFace: F.semi, color: C.accent2, align: 'center', valign: 'middle' });
    T(s, p[1], { x: x + 0.82, y: y + 0.24, w: sw - 1.0, h: 0.46, fontSize: 16, fontFace: F.semi, color: C.background1, valign: 'middle' });
    T(s, p[2], { x: x + 0.26, y: y + 0.86, w: sw - 0.5, h: 1.05, fontSize: 11.5 });
    glass(x + 0.18, y + 1.95, sw - 0.36, 1.14, { tint: 'green', edge: '22D38B', shadow: false, r: 0.14 });
    T(s, [run('CONDITION TO PROCEED', { fontFace: F.semi, color: HX.green, fontSize: 8, charSpacing: 1.2, breakLine: true }), run(p[3], { color: HX.fg })], { x: x + 0.34, y: y + 2.04, w: sw - 0.68, h: 1.0, fontSize: 10.5 });
    if (i < 2) T(s, '→', { x: x + sw, y: y + 0.2, w: 0.35, h: 0.5, fontSize: 20, color: C.accent2, align: 'center' });
  });
  const hw = (CW - 0.15) / 2;
  glass(MX, 5.8, hw, 0.78, { tint: 'red', edge: 'EE6A33', shadow: false });
  T(s, 'No confirmed paid demand: defer intake. Weak results: redesign or stop.', { x: MX + 0.26, y: 5.8, w: hw - 0.5, h: 0.78, fontSize: 12.5, fontFace: F.semi, color: C.background1, valign: 'middle' });
  glass(MX + hw + 0.15, 5.8, hw, 0.78, { shadow: false });
  T(s, [run('Suggested start: '), run('24 learners, 6 trainer candidates, 2 eligible sites.', { fontFace: F.semi, color: HX.fg }), run(' Targets for agreement.')], { x: MX + hw + 0.41, y: 5.8, w: hw - 0.5, h: 0.78, fontSize: 12.5, valign: 'middle' });
  src(s, 'Basis: report Sections 5–8 and Appendix F. Sources: NITI [R42], training evaluation [R54], LCGPA draft [R63], WIPO [R64]. Proposed design.');
}
{
  const t = 'Value now and after opening';
  const s = content(P4, B4, t, 'What stays after the cranes leave', '11 · Value now and after the stadium opens', { noFooter: true });
  grid(s, MX, 1.95, [2.55, 3.15, 3.15], ['Value', 'During construction', 'After handover'], [
    ['Skills and academic capability', 'Paid practice, independent tests, manuals and trainer development', 'Next-site work, returning trainers and further recognised qualifications'],
    ['Local products and IP', 'Approved local grades, tooling and usable technical rights', 'Repeat orders, deeper production and independent Saudi services'],
    ['Buyer value', 'Joint offers, less duplicated buying and comparable full-cost prices', 'Reusable specifications and resilient multi-supplier sourcing'],
    ['Export value', 'Saudi-authored content and rights prepared for later markets', 'Paid courses, licensed services and qualified products sold abroad']], { rh: 0.74, fs: 11 });
  const ix = MX + 8.85 + 0.2, iw = W - MX - ix;
  glass(ix, 2.31, iw, 3.23, { r: 0.24 });
  s.addImage({ path: IMG('r_palms.jpg'), x: ix + 0.14, y: 2.45, w: iw - 0.28, h: 2.95, sizing: { type: 'cover', w: iw - 0.28, h: 2.95 }, altText: '3D model: palms and stadium facade' });
  glass(MX, 5.72, CW, 0.78, { tint: 'gold', edge: 'E2B357', r: 0.24 });
  T(s, [run('ILLUSTRATIVE MATERIALS OPPORTUNITY     ', { fontFace: F.semi, color: HX.gold, fontSize: 8.5, charSpacing: 1.2 }), run('25% of the SAR 177m basket ≈ ', { color: HX.fg, fontFace: F.semi }), run('SAR 44m', { fontFace: F.black, color: HX.green, fontSize: 22 }), run(' more domestic purchases', { color: HX.fg, fontFace: F.semi })],
    { x: MX + 0.35, y: 5.72, w: CW - 0.7, h: 0.78, fontSize: 15, valign: 'middle' });
  src(s, 'Source: GASTAT-based group scenario [R05]. Benefits are proposals. No discount or export revenue is assumed. Domestic purchases, savings and credit are separate.', 6.58);
  thread(s, 6, [5]);
}
{
  const t = 'The decision';
  const s = content(P4, B4, t, 'A shared Materials and Systems Academy pilot', '12 · The decision for LCGPA and the buyer', { noFooter: true });
  T(s, 'Proposed joint programme for all participating eligible stadium vendors · one academy, agreed vendor contributions and individual compliance records.', { x: MX, y: 1.9, w: CW, h: 0.3, fontSize: 12 });
  const cw3 = (CW - 0.3) / 3;
  [['LCGPA', 'Approve extra activities, rights, factors and separate supplier ledgers.'], ['AUTHORISED BUYER', 'Approve competitive joint procurement and construction gates.'], ['DELIVERY PARTNERS', 'Agree paid placements, material trials, trainer return and follow-up.']].forEach((d, i) => {
    const x = MX + i * (cw3 + 0.15); glass(x, 2.3, cw3, 1.1, { tint: 'gold', edge: 'E2B357' });
    T(s, d[0], { x: x + 0.24, y: 2.42, w: cw3 - 0.5, h: 0.25, fontSize: 9, fontFace: F.semi, color: C.accent2, charSpacing: 1.5 });
    T(s, d[1], { x: x + 0.24, y: 2.7, w: cw3 - 0.5, h: 0.65, fontSize: 12, color: C.background1 });
  });
  const gx = MX, gw = 7.2; glass(gx, 3.55, gw, 2.55, { r: 0.24 });
  T(s, 'EP CREDIT PLAN', { x: gx + 0.28, y: 3.7, w: 3, h: 0.24, fontSize: 9, fontFace: F.semi, color: C.accent2, charSpacing: 2 });
  T(s, 'SAR 84m from about SAR 36m of activity (average factor 2.33; SAR 63m at low-end factors)', { x: gx + 0.28, y: 3.95, w: gw - 0.55, h: 0.5, fontSize: 12.5, fontFace: F.semi, color: C.background1 });
  const rows = [['Technology transfer', 12, 3], ['Knowledge transfer', 12, 2], ['Localisation', 12, 2]];
  const lx = gx + 2.15, lw = 4.2, sc = lw / 40;
  rows.forEach((r, i) => {
    const y = 4.6 + i * 0.47;
    T(s, [run(r[0], { fontFace: F.semi, color: HX.fg }), run('  ×' + r[2], { color: HX.gold, fontFace: F.semi })], { x: gx + 0.28, y, w: 1.85, h: 0.38, fontSize: 10.5, valign: 'middle' });
    bar(s, lx, y + 0.05, r[1] * r[2] * sc, 0.28, HX.credit, { r: 0.14 });
    bar(s, lx, y + 0.05, r[1] * sc, 0.28, HX.other, { r: 0.14 });
    T(s, r[1] + 'm → ' + r[1] * r[2] + 'm', { x: lx + r[1] * r[2] * sc + 0.1, y, w: 1.4, h: 0.38, fontSize: 10.5, fontFace: F.semi, color: C.background1, valign: 'middle' });
  });
  T(s, [run('■ ', { color: HX.other }), run('activity    '), run('■ ', { color: HX.credit }), run('EP credit')], { x: lx, y: 5.95, w: 3, h: 0.2, fontSize: 8.5 });
  const rx = gx + gw + 0.15, rw = W - MX - rx;
  stat(s, rx, 3.55, rw, 1.2, 'SAR 84m', 'EP credit = 36 + 24 + 24', HX.green, { vs: 28, vh: 0.55, g: { tint: 'green', edge: '22D38B' } });
  glass(rx, 4.88, rw, 1.22, { shadow: false });
  T(s, [run('Why these factors: ', { fontFace: F.semi, color: HX.fg }), run('LCGPA sets the final factor within each draft range. We start at the minimum and add 1 per condition met: usable licences (2→3), new skills with independent tests (1→2), approved Saudi materials with real orders (1→2). Not the maximum: no manufacturing rights, recognised qualification or new plant.')],
    { x: rx + 0.22, y: 4.95, w: rw - 0.42, h: 1.12, fontSize: 9.5, valign: 'middle' });
  T(s, 'Proposed start: 24 learners, 6 trainer candidates, 2 confirmed eligible sites', { x: MX, y: 6.2, w: CW, h: 0.3, fontSize: 13, fontFace: F.semi, color: C.accent1 });
  src(s, 'Proposal targets for agreement, not forecasts or observed results. Scale on proven skills, demand, quality, cost and licensed rights. Policy basis: LCGPA [R63].', 6.55);
  thread(s, 7, [6]);
}

// ══ CLOSE ════════════════════════════════════════════════════════════════
pres.addSection({ title: 'Close' });
{
  const s = newSlide('COVER', 'Close', 'r_signature.jpg', 'photo', 0.82);
  cur.shadeDir = 'bottom';
  glass(1.35, 1.05, W - 2.7, 5.45, { r: 0.4, tint: 'dark' });
  T(s, 'GROUP 8   ·   MBSC EMBA   ·   ECN 511', { x: 0, y: 1.5, w: W, h: 0.32, fontSize: 11, fontFace: F.semi, color: C.accent2, align: 'center', charSpacing: 5 });
  T(s, 'Thank you', { x: 0, y: 1.95, w: W, h: 1.45, fontSize: 84, fontFace: F.semi, color: C.background1, align: 'center', charSpacing: -2 });
  T(s, 'Questions welcome', { x: 0, y: 3.45, w: W, h: 0.45, fontSize: 19, fontFace: F.light, color: C.background2, align: 'center' });
  const team = [['AA', 'Abdulmajeed', 'Alajlan'], ['AD', 'Abdulrahman', 'Aldahlawi'], ['SA', 'Salman', 'Alfaris'], ['MA', 'Mohammed', 'Alghamdi'], ['AW', 'Abdulaziz', 'Alweheab'], ['NA', 'Nada', 'Alyahya'], ['HB', 'Haifa', 'Binnafisah']];
  const cw = 1.5, x0 = (W - team.length * cw) / 2;
  team.forEach((m, i) => {
    const x = x0 + i * cw;
    s.addShape(pres.shapes.OVAL, { x: x + cw / 2 - 0.32, y: 4.35, w: 0.64, h: 0.64, fill: { color: HX.green, transparency: 86 }, line: { color: HX.green, width: 1.5 }, shadow: { type: 'outer', color: HX.green, blur: 10, offset: 0, angle: 90, opacity: 0.5 } });
    T(s, m[0], { x: x + cw / 2 - 0.32, y: 4.35, w: 0.64, h: 0.64, fontSize: 13, fontFace: F.semi, color: C.accent1, align: 'center', valign: 'middle' });
    T(s, [run(m[1], { fontFace: F.semi, color: HX.fg, fontSize: 13, breakLine: true }), run(m[2], { color: HX.fg2, fontSize: 11 })], { x, y: 5.1, w: cw, h: 0.6, align: 'center' });
  });
  T(s, 'King Salman Stadium · Riyadh 2034', { x: 0, y: 5.95, w: W, h: 0.3, fontSize: 10, color: C.accent6, align: 'center', charSpacing: 2 });
  notes(s, 'Thank you');
}

// ══ SOURCES ══════════════════════════════════════════════════════════════
const PS = 'Sources';
pres.addSection({ title: PS });
SOURCES.forEach(([title, head, refs, foot]) => {
  const s = newSlide('CONTENT', PS, 'r_top.jpg', 'content');
  s.addText(head, { placeholder: 'title' }); eyebrow(s, title); footer(s);
  const cols = refs.length > 6 ? 2 : 1, per = Math.ceil(refs.length / cols), cw = cols === 2 ? (CW - 0.2) / 2 : CW;
  const rowH = Math.min(0.62, (3.85 - 0.06 * per) / per);
  refs.forEach((r, i) => {
    const col = Math.floor(i / per), row = i % per, x = MX + col * (cw + 0.2), y = 1.98 + row * (rowH + 0.06);
    glass(x, y, cw, rowH, { r: 0.12, shadow: false });
    T(s, r[0], { x: x + 0.18, y, w: 0.55, h: rowH, fontSize: 10, fontFace: F.semi, color: C.accent2, valign: 'middle' });
    T(s, [run(r[1], { fontFace: F.semi, color: HX.fg, hyperlink: { url: r[3] }, breakLine: !!r[2] })].concat(r[2] ? [run(r[2], { color: HX.fg2 })] : []), { x: x + 0.75, y, w: cw - 0.9, h: rowH, fontSize: 9.5, valign: 'middle' });
  });
  glass(MX, 5.95, CW, 0.92, { shadow: false, tint: 'dark' });
  T(s, foot, { x: MX + 0.25, y: 5.95, w: CW - 0.5, h: 0.92, fontSize: 8.5, color: C.accent6, valign: 'middle' });
  s.addNotes('Source titles are clickable.');
});

(async () => {
  if (PASS === 'spec') { fs.writeFileSync(path.join(__dirname, 'spec.json'), JSON.stringify(SPEC)); console.log('spec', SPEC.length); return; }
  await pres.writeFile({ fileName: OUT }); await applyTheme(OUT, THEME);
  // turn proofing off on every run, so names like Qiddiya get no red squiggles
  const JSZip = require('jszip'); const zip = await JSZip.loadAsync(fs.readFileSync(OUT));
  for (const name of Object.keys(zip.files).filter((n) => /^ppt\/(slides|slideLayouts|slideMasters)\/[^/]+\.xml$/.test(n))) {
    let x = await zip.file(name).async('string');
    x = x.replace(/<a:(rPr|endParaRPr|defRPr)(?![^>]*noProof)(\s|>|\/>)/g, (m, tag, tail) => '<a:' + tag + ' noProof="1"' + (tail === '>' || tail === '/>' ? tail : ' '));
    zip.file(name, x);
  }
  fs.writeFileSync(OUT, await zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' }));
  console.log('wrote', OUT);
})();
