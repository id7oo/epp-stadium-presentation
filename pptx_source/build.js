// King Salman Stadium — PowerPoint edition of the 3D web presentation.
// Same content and theme (night green, gold, import orange), with 3D renders of the
// stadium as section backdrops. Run: node build.js OUT.pptx
const pptxgen = require('pptxgenjs');
const fs = require('fs'), path = require('path');
const { applyTheme } = require(process.env.PPTX_SKILL + '/scripts/apply_theme.js');
const META = JSON.parse(fs.readFileSync(path.join(__dirname, 'meta.json'), 'utf8'));
const IMG = (n) => path.join(__dirname, 'img', n);
const OUT = process.argv[2] || 'deck.pptx';

const THEME = {
  name: 'King Salman Night', headFontFace: 'Calibri', bodyFontFace: 'Calibri',
  colors: { dk1: '0B1115', lt1: 'EEF4F4', dk2: '04090B', lt2: 'A0B3B6',
    accent1: '19C37D', accent2: 'DCA84A', accent3: 'E0632E', accent4: '3987E5', accent5: 'C98500', accent6: '6D8186',
    hlink: '19C37D', folHlink: 'A0B3B6' },
};
const HEX = { surface: '0B1115', surface2: '121C21', line: '1F2F36', fg: 'EEF4F4', fg2: 'A0B3B6', fg3: '6D8186',
  green: '19C37D', gold: 'DCA84A', imp: 'E0632E', blue: '3987E5', credit: 'C98500', other: '5C6F63', bg: '04090B' };

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';            // 13.333 x 7.5 in
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = 'Building King Salman Stadium: how much of the money stays in Saudi Arabia?';
pres.author = 'Group 8 · MBSC EMBA';
pres.company = 'MBSC EMBA · ECN 511';
const C = pres.SchemeColor;
const W = 13.333, Hh = 7.5, MX = 0.6;

// ── layouts ──────────────────────────────────────────────────────────────
pres.defineSlideMaster({
  title: 'CONTENT', background: { path: IMG('bg.png') },
  objects: [
    { text: { text: 'Building King Salman Stadium  ·  Group 8  ·  ECN 511', options: { x: MX, y: 7.02, w: 6, h: 0.3, fontSize: 10, color: C.accent6, margin: 0 } } },
    { placeholder: { options: { name: 'title', type: 'title', x: MX, y: 0.88, w: 12.1, h: 0.95, fontSize: 28, bold: true, color: C.background1, valign: 'top', align: 'left', margin: 0, fontFace: 'Calibri' }, text: '' } },
  ],
  slideNumber: { x: 12.33, y: 7.02, w: 0.4, h: 0.3, fontSize: 10, color: C.accent6, align: 'right' },
});
pres.defineSlideMaster({
  title: 'DIVIDER', background: { color: HEX.bg },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', x: MX, y: 3.0, w: 9.5, h: 1.3, fontSize: 54, bold: true, color: C.background1, valign: 'top', align: 'left', margin: 0 }, text: '' } },
  ],
});
pres.defineSlideMaster({ title: 'COVER', background: { color: HEX.bg }, objects: [] });

// ── helpers ──────────────────────────────────────────────────────────────
const shadow = () => ({ type: 'outer', color: '000000', blur: 18, offset: 6, angle: 90, opacity: 0.45 });
function T(slide, text, o) { slide.addText(text, Object.assign({ isTextBox: true, margin: 0, fontSize: 14, color: C.background2, valign: 'top' }, o)); }
function card(slide, x, y, w, h, o = {}) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12,
    fill: { color: o.fill || HEX.surface2, transparency: o.tr == null ? 8 : o.tr },
    line: { color: o.line || HEX.line, width: o.lw || 1 }, shadow: o.flat ? undefined : shadow(), objectName: o.name });
}
function eyebrow(slide, text, x = MX, y = 0.42) {
  const w = Math.min(0.32 + text.length * 0.085, 8);
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.32, rectRadius: 0.16, fill: { color: HEX.gold, transparency: 88 }, line: { color: HEX.gold, width: 0.75, transparency: 40 } });
  slide.addShape(pres.shapes.OVAL, { x: x + 0.13, y: y + 0.125, w: 0.07, h: 0.07, fill: { color: HEX.gold }, line: { color: HEX.gold, width: 0 } });
  T(slide, text, { x: x + 0.27, y, w: w - 0.3, h: 0.32, fontSize: 11, bold: true, color: C.accent2, valign: 'middle' });
}
const SPK = { 'Abdulmajeed Alajlan': ['AA', '19C37D'], 'Salman Alfaris': ['SA', '3987E5'], 'Abdulaziz Alweheab': ['AW', 'E0632E'],
  'Mohammed Alghamdi': ['MA', 'DCA84A'], 'Abdulrahman Aldahlawi': ['AD', '2BB6C4'], 'Haifa Binnafisah': ['HB', 'C26BD6'], 'Nada Alyahya': ['NA', 'E85A8A'] };
function presenter(slide, title) {
  const m = META[title]; if (!m || !SPK[m.who]) return;
  const [ini, col] = SPK[m.who];
  const tail = (m.sec && +m.sec ? '  ·  ' + m.sec + 's' : '') + (m.no && m.no !== '·' ? '  ·  ' + m.no + ' / 12' : '');
  const txt = m.who + tail, w = 0.55 + txt.length * 0.075;
  const x = W - MX - w, y = 0.4;
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.36, rectRadius: 0.18, fill: { color: HEX.surface2, transparency: 10 }, line: { color: HEX.line, width: 1 } });
  slide.addShape(pres.shapes.OVAL, { x: x + 0.05, y: y + 0.05, w: 0.26, h: 0.26, fill: { color: col }, line: { color: col, width: 0 } });
  T(slide, ini, { x: x + 0.05, y: y + 0.05, w: 0.26, h: 0.26, fontSize: 8, bold: true, color: '04120B', align: 'center', valign: 'middle' });
  T(slide, [{ text: m.who, options: { bold: true, color: C.background1 } }, { text: tail, options: { color: C.accent6 } }],
    { x: x + 0.38, y, w: w - 0.42, h: 0.36, fontSize: 10.5, valign: 'middle' });
}
function notes(slide, title) {
  const m = META[title] || {};
  const head = m.who && SPK[m.who] ? m.who + (m.sec && +m.sec ? ' · ' + m.sec + ' seconds' : '') + '\n\n' : '';
  slide.addNotes(head + (m.notes || ''));
}
function src(slide, text, y = 6.62) { T(slide, text, { x: MX, y, w: 12.1, h: 0.34, fontSize: 9.5, color: C.accent6 }); }
function tile(slide, x, y, w, h, v, k, col, o = {}) {
  card(slide, x, y, w, h, o);
  T(slide, v, { x: x + 0.22, y: y + 0.18, w: w - 0.44, h: o.vh || 0.62, fontSize: o.vs || 30, bold: true, color: col || C.background1, fit: 'shrink' });
  T(slide, k, { x: x + 0.22, y: y + 0.18 + (o.vh || 0.62) + 0.04, w: w - 0.44, h: h - (o.vh || 0.62) - 0.36, fontSize: o.ks || 12.5, color: C.background2 });
}
// "Follow the riyal": the money chain, lit up to the current step
const THREAD = [['SAR 4.5bn', 'scenario', ''], ['SAR 2,143m', 'purchases', ''], ['SAR 421m', 'the leak', 'imp'], ['SAR 177m', 'chem + metals', 'imp'],
  ['SAR 84m', 'EP credit', 'credit'], ['SAR 44m', 'Saudi buying', 'green'], ['~SAR 36m', 'activity', 'green']];
function thread(slide, n, now) {
  const x0 = 5.15, y = 6.95, step = 1.05;
  T(slide, 'FOLLOW THE RIYAL', { x: x0 - 1.32, y: y + 0.07, w: 1.25, h: 0.25, fontSize: 8, bold: true, color: C.accent2, charSpacing: 1 });
  THREAD.forEach((t, i) => {
    const lit = i < n, isNow = now && now.includes(i), x = x0 + i * step;
    const col = !lit ? HEX.fg3 : t[2] === 'imp' ? HEX.imp : t[2] === 'credit' ? HEX.credit : t[2] === 'green' ? HEX.green : HEX.fg;
    if (isNow) slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: x - 0.04, y: y - 0.02, w: step - 0.08, h: 0.42, rectRadius: 0.1, fill: { color: HEX.gold, transparency: 85 }, line: { color: HEX.gold, width: 0.75, transparency: 30 } });
    T(slide, t[0], { x, y, w: step - 0.16, h: 0.22, fontSize: 9.5, bold: true, color: col, align: 'center', transparency: lit ? 0 : 55 });
    T(slide, t[1], { x, y: y + 0.19, w: step - 0.16, h: 0.18, fontSize: 7, color: lit ? HEX.fg2 : HEX.fg3, align: 'center', transparency: lit ? 0 : 55 });
  });
}
function content(sec, title, head, eyebrowText) {
  const s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: sec });
  s.addText(head, { placeholder: 'title' });
  eyebrow(s, eyebrowText); presenter(s, title); notes(s, title);
  return s;
}
function divider(sec, part, name, line, img) {
  const s = pres.addSlide({ masterName: 'DIVIDER', sectionTitle: sec });
  s.addImage({ path: IMG(img), x: 0, y: 0, w: W, h: Hh, altText: '3D model of King Salman Stadium' });
  s.addImage({ path: IMG('ov_left.png'), x: 0, y: 0, w: W, h: Hh, altText: '' });
  T(s, part.toUpperCase(), { x: MX, y: 2.45, w: 6, h: 0.4, fontSize: 14, bold: true, color: C.accent2, charSpacing: 4 });
  s.addText(name, { placeholder: 'title' });
  T(s, line, { x: MX, y: 4.25, w: 7.2, h: 0.9, fontSize: 20, color: C.background2 });
  s.addShape(pres.shapes.LINE, { x: MX, y: 4.05, w: 1.4, h: 0, line: { color: HEX.green, width: 2.5 } });
  s.addNotes(part + ': ' + name + '. ' + line);
  return s;
}
function bullets(items, o = {}) {
  return items.map((t, i) => ({ text: t, options: { bullet: { code: '2192' }, breakLine: i < items.length - 1, paraSpaceAfter: 4, ...o } }));
}
function chartBase(extra) {
  return Object.assign({ catAxisLabelFontFace: '+mn-lt', valAxisLabelFontFace: '+mn-lt', dataLabelFontFace: '+mn-lt', titleFontFace: '+mn-lt',
    catAxisLabelColor: HEX.fg2, valAxisLabelColor: HEX.fg3, catAxisLabelFontSize: 11, valAxisLabelFontSize: 9,
    valGridLine: { color: '1F2F36', size: 0.5 }, catGridLine: { style: 'none' }, catAxisLineShow: false, valAxisLineShow: false,
    showValue: true, dataLabelColor: HEX.fg, dataLabelFontSize: 11, dataLabelFontBold: true, showLegend: false, plotArea: { fill: { color: HEX.bg, transparency: 100 } } }, extra);
}

// ══ COVER ════════════════════════════════════════════════════════════════
pres.addSection({ title: 'Opening' });
{
  const s = pres.addSlide({ masterName: 'COVER', sectionTitle: 'Opening' });
  s.addImage({ path: IMG('cover.jpg'), x: 0, y: 0, w: W, h: Hh, altText: 'King Salman Stadium concept rendering at sunset' });
  s.addImage({ path: IMG('ov_left.png'), x: 0, y: 0, w: W, h: Hh, altText: '' });
  eyebrow(s, 'MBSC EMBA · ECN 511 Economics for Managers', MX, 1.3);
  T(s, [{ text: 'Building King Salman Stadium: ', options: { color: C.background1 } }, { text: 'how much of the money stays in Saudi Arabia?', options: { color: C.accent1 } }],
    { x: MX, y: 1.95, w: 8.2, h: 2.4, fontSize: 44, bold: true, fontFace: 'Calibri' });
  T(s, [{ text: 'Construction and Infrastructure · ' }, { text: 'Topic B: ', options: { color: C.accent2, bold: true } }, { text: 'the multiplier effect of public capital spending, and where the money leaks' }],
    { x: MX, y: 4.5, w: 7.6, h: 0.8, fontSize: 16 });
  T(s, 'GROUP 8', { x: MX, y: 5.55, w: 3, h: 0.3, fontSize: 11, bold: true, color: C.accent2, charSpacing: 3 });
  T(s, 'Abdulmajeed Alajlan  ·  Abdulrahman Aldahlawi  ·  Salman Alfaris  ·  Mohammed Alghamdi  ·  Abdulaziz Alweheab  ·  Nada Alyahya  ·  Haifa Binnafisah',
    { x: MX, y: 5.88, w: 8.6, h: 0.6, fontSize: 12.5, color: C.background1 });
  T(s, 'Cover image: King Salman Stadium concept rendering © Populous', { x: MX, y: 7.0, w: 6, h: 0.25, fontSize: 9, color: C.accent6 });
  notes(s, 'Arrival');
}

// ══ PART 1 ═══════════════════════════════════════════════════════════════
const P1 = 'Part 1 · Our case';
pres.addSection({ title: P1 });
divider(P1, 'Part 1', 'Our case', 'What a World Cup stadium buys, and who supplies it', 'r_hero.jpg');
{
  const t = 'Construction and Infrastructure';
  const s = content(P1, t, 'Our case: the 2034 World Cup stadium programme', '01 · Construction and Infrastructure');
  // 3D-style photo card: gold slab behind, deep shadow
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.55, y: 2.08, w: 6.25, h: 3.55, rectRadius: 0.14, fill: { color: HEX.gold, transparency: 35 }, line: { color: HEX.gold, width: 0 } });
  s.addImage({ path: IMG('aerial.jpg'), x: 6.4, y: 1.95, w: 6.25, h: 3.52, rounding: false, altText: 'King Salman Stadium concept rendering, aerial view', shadow: shadow() });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.6, y: 4.88, w: 3.6, h: 0.44, rectRadius: 0.22, fill: { color: HEX.bg, transparency: 30 }, line: { color: 'FFFFFF', width: 0.5, transparency: 70 } });
  T(s, [{ text: '92,760 ', options: { bold: true, color: C.accent2, fontSize: 15 } }, { text: 'planned seats · King Salman Stadium, Riyadh', options: { color: C.background1 } }],
    { x: 6.75, y: 4.88, w: 3.4, h: 0.44, fontSize: 10.5, valign: 'middle' });
  T(s, 'King Salman Stadium concept rendering © Populous', { x: 6.4, y: 5.55, w: 6.25, h: 0.22, fontSize: 8.5, color: C.accent6, align: 'right' });
  T(s, 'A stadium buys civil works, materials, building systems and specialist expertise.', { x: MX, y: 2.0, w: 5.5, h: 0.95, fontSize: 18, bold: true, color: C.background1 });
  T(s, bullets(['Ministry of Sport buys the works.', 'Populous designs the stadium.', 'Contractors and specialist suppliers deliver.']), { x: MX, y: 3.05, w: 5.5, h: 1.2, fontSize: 15 });
  const ty = 4.45, tw = 1.78;
  tile(s, MX, ty, tw, 1.55, '15', 'stadiums in 5 host cities');
  tile(s, MX + tw + 0.08, ty, tw, 1.55, '7.8%', 'of Saudi value added, 2023 sector scale', C.accent1);
  tile(s, MX + 2 * (tw + 0.08), ty, tw, 1.55, 'SAR 646bn', 'gross output, 2023', C.accent4, { vs: 21 });
  src(s, 'Sources: FIFA 2034 bid evaluation; GASTAT Supply and Use Tables 2023; Ministry of Sport; Populous [R01, R05, R02–R03, R53].');
}
{
  const t = 'Who buys, who supplies';
  const s = content(P1, t, 'A World Cup stadium is a construction job inside a sector worth 7.8% of the Saudi economy', 'Part 1 · The sector');
  const tw = 2.95, ty = 1.98;
  [['7.8%', 'of Saudi value added comes from construction (SAR 338bn of SAR 4,333bn, 2023)', C.accent1],
   ['SAR 646bn', 'construction output in 2023, of which SAR 307.5bn is bought-in inputs', C.accent4],
   ['15', 'stadiums across 5 host cities in FIFA’s 2024 bid evaluation', null],
   ['92,760', 'planned seats at King Salman Stadium, Riyadh — our case', C.accent2]].forEach((d, i) =>
    tile(s, MX + i * (tw + 0.1), ty, tw, 1.42, d[0], d[1], d[2], { vs: 26, vh: 0.5, ks: 11.5 }));
  const hdr = (x) => ({ text: x, options: { bold: true, color: HEX.fg, fill: { color: '123A2C' }, fontSize: 11 } });
  const cell = (x, o = {}) => ({ text: x, options: Object.assign({ color: HEX.fg2, fontSize: 11 }, o) });
  s.addTable([
    ['Stadium', 'Seats', 'Who buys', 'Who supplies', 'Published value'].map(hdr),
    [cell('Prince Mohammed bin Salman Stadium, Qiddiya'), cell('45,000', { align: 'right' }), cell('Qiddiya Investment Co.'), cell('FCC (Spain) – Nesma (KSA); Elegancia: mechanical SAR 829m; IKK Fangda: facade SAR 997m ex-VAT'), cell('about SAR 4.0bn', { align: 'right' })],
    [cell('Aramco Stadium, Al Khobar'), cell('46,096', { align: 'right' }), cell('Saudi Aramco'), cell('Besix (Belgium) – Albawani (KSA)'), cell('about SAR 3.7bn', { align: 'right' })],
    [cell('King Salman Stadium, Riyadh — our case', { bold: true, color: HEX.fg, fill: { color: '2A2412' } }), cell('92,760', { bold: true, color: HEX.fg, align: 'right', fill: { color: '2A2412' } }),
     cell('Ministry of Sport', { fill: { color: '2A2412' } }), cell('Main works prequalification notice (Nov 2025); design by Populous', { fill: { color: '2A2412' } }), cell('Not published', { color: HEX.imp, align: 'right', bold: true, fill: { color: '2A2412' } })],
  ], { x: MX, y: 3.6, w: 12.1, colW: [2.9, 0.9, 1.9, 4.6, 1.8], border: { type: 'solid', color: HEX.line, pt: 0.75 }, fill: { color: HEX.surface }, margin: 0.06, rowH: 0.42 });
  T(s, [{ text: 'International–Saudi joint ventures deliver the main works; ' }, { text: 'specialist imported systems arrive through subcontracts.', options: { bold: true, color: C.background1 } }],
    { x: MX, y: 5.82, w: 12.1, h: 0.4, fontSize: 14 });
  src(s, 'Sources: R05 (sheet 6.3), R01, R02–R03, R57, R58, R23–R24. Calculation: construction gross value added 338.3bn ÷ total GVA 4,332.9bn = 7.81% (GASTAT 2023, sheet 6.3).');
}

// ══ PART 2 ═══════════════════════════════════════════════════════════════
const P2 = 'Part 2 · Multiplier and leakage';
pres.addSection({ title: P2 });
divider(P2, 'Part 2', 'Multiplier and leakage', 'Follow the riyal: where it is spent, and where it leaks', 'r_bowl.jpg');
{
  const t = 'The spending multiplier';
  const s = content(P2, t, 'One public payment creates income that people spend again', '02 · The spending multiplier, in simple terms');
  const bx = [MX, MX + 2.65, MX + 5.3], by = 2.3, bw = 2.35, bh = 1.75;
  const nodes = [['01', 'Public spending', 'The stadium pays a contractor.'], ['02', 'Income and spending', 'Workers and suppliers spend part of their income again.'], ['03', 'More Saudi production', 'Later spending supports additional goods and services.']];
  // re-spending loop: 03 back to 02, drawn above the boxes
  s.addShape(pres.shapes.LINE, { x: bx[2] + bw / 2, y: by - 0.42, w: 0, h: 0.4, line: { color: HEX.green, width: 1.75 } });
  s.addShape(pres.shapes.LINE, { x: bx[1] + bw / 2, y: by - 0.42, w: bx[2] - bx[1], h: 0, line: { color: HEX.green, width: 1.75 } });
  s.addShape(pres.shapes.LINE, { x: bx[1] + bw / 2, y: by - 0.42, w: 0, h: 0.38, line: { color: HEX.green, width: 1.75, endArrowType: 'triangle' } });
  T(s, 'spent again', { x: bx[1] + bw / 2, y: by - 0.7, w: bx[2] - bx[1], h: 0.25, fontSize: 11, bold: true, color: C.accent1, align: 'center' });
  nodes.forEach((n, i) => {
    card(s, bx[i], by, bw, bh, i === 2 ? { fill: '0C2A1F', line: '1F6B4A' } : {});
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: bx[i] + 0.18, y: by + 0.18, w: 0.5, h: 0.3, rectRadius: 0.15, fill: { color: HEX.gold, transparency: 85 }, line: { color: HEX.gold, width: 0.75, transparency: 40 } });
    T(s, n[0], { x: bx[i] + 0.18, y: by + 0.18, w: 0.5, h: 0.3, fontSize: 11, bold: true, color: C.accent2, align: 'center', valign: 'middle' });
    T(s, n[1], { x: bx[i] + 0.18, y: by + 0.58, w: bw - 0.36, h: 0.52, fontSize: 14.5, bold: true, color: C.background1, valign: 'bottom' });
    T(s, n[2], { x: bx[i] + 0.18, y: by + 1.14, w: bw - 0.36, h: 0.58, fontSize: 12 });
    if (i < 2) s.addShape(pres.shapes.LINE, { x: bx[i] + bw + 0.05, y: by + bh / 2, w: 0.2, h: 0, line: { color: HEX.green, width: 1.75, endArrowType: 'triangle' } });
  });
  // leak
  card(s, MX + 1.8, by + bh + 0.5, 4.6, 0.5, { fill: '2A140B', line: '7A3518', flat: true });
  T(s, 'Imports and saving reduce later rounds.', { x: MX + 1.8, y: by + bh + 0.5, w: 4.6, h: 0.5, fontSize: 14, bold: true, color: C.accent3, align: 'center', valign: 'middle' });
  [bx[1] + bw / 2, bx[2] + bw / 2].forEach((x) => s.addShape(pres.shapes.LINE, { x: Math.min(x, MX + 6.2), y: by + bh + 0.05, w: 0, h: 0.4, line: { color: HEX.imp, width: 1.25, dashType: 'dash', endArrowType: 'triangle' } }));
  // right column: formula and micro/macro
  const rx = 8.85, rw = 3.85;
  card(s, rx, 1.98, rw, 1.75, { fill: '2A2412', line: '7A6230' });
  T(s, 'GDP multiplier = extra GDP caused ÷ extra public spending', { x: rx + 0.22, y: 2.12, w: rw - 0.44, h: 0.75, fontSize: 15, bold: true, color: C.background1 });
  T(s, [{ text: 'Illustration: SAR 100m extra spending causes SAR 120m extra GDP. ' }, { text: 'Multiplier = 1.2.', options: { bold: true, color: C.accent2 } }],
    { x: rx + 0.22, y: 2.9, w: rw - 0.44, h: 0.75, fontSize: 12.5 });
  [['Micro', 'A firm chooses a supplier.'], ['Macro', 'The combined effect on GDP.'], ['Our topic', 'The spending multiplier is macroeconomics.']].forEach((c, i) => {
    const y = 3.9 + i * 0.82; card(s, rx, y, rw, 0.7, i === 2 ? { fill: '2A2412', line: '7A6230', flat: true } : { flat: true });
    T(s, c[0], { x: rx + 0.22, y, w: 1.1, h: 0.7, fontSize: 11, bold: true, color: C.accent2, valign: 'middle' });
    T(s, c[1], { x: rx + 1.3, y, w: rw - 1.45, h: 0.7, fontSize: 13, color: C.background1, valign: 'middle' });
  });
  src(s, 'Source: IMF, Fiscal Multipliers, 2014, section II [R69]. Teaching example, not a Saudi estimate.');
}
{
  const t = 'Construction and Saudi GDP';
  const s = content(P2, t, 'Our sector creates assets and adds value through Saudi production', '03 · Construction and Saudi GDP');
  card(s, MX, 1.98, 6.9, 4.45);
  T(s, 'GASTAT 2023 [R05]', { x: MX + 0.25, y: 2.12, w: 4, h: 0.25, fontSize: 10, bold: true, color: C.accent2 });
  T(s, 'Saudi construction, 2023 — SAR billion', { x: MX + 0.25, y: 2.36, w: 6.4, h: 0.35, fontSize: 15, bold: true, color: C.background1 });
  s.addChart(pres.charts.BAR, [{ name: 'SAR bn', labels: ['Gross output', 'Less: bought-in inputs', 'Construction value added'], values: [645.8, 307.5, 338.3] }],
    chartBase({ x: MX + 0.15, y: 2.75, w: 6.6, h: 3.55, barDir: 'col', barGapWidthPct: 70, chartColors: [HEX.blue, HEX.imp, HEX.green], valAxisHidden: true, dataLabelPosition: 'outEnd', dataLabelFontSize: 14, dataLabelFormatCode: '0.0', valAxisMaxVal: 750, altText: 'Column chart: gross output 645.8, bought-in inputs 307.5, value added 338.3 SAR billion' }));
  tile(s, 7.75, 1.98, 4.95, 1.45, '7.8%', 'of Saudi gross value added', C.accent1, { vs: 40, vh: 0.72 });
  card(s, 7.75, 3.55, 4.95, 1.55);
  T(s, [{ text: 'GDP counts the extra value created at each Saudi stage ' }, { text: 'once', options: { bold: true, color: C.background1 } }, { text: '. A local supplier’s full invoice also includes inputs bought from other firms.' }],
    { x: 7.97, y: 3.7, w: 4.5, h: 1.3, fontSize: 14 });
  card(s, 7.75, 5.22, 4.95, 1.2, { fill: '2A2412', line: '7A6230' });
  T(s, [{ text: 'Academy link: ', options: { bold: true, color: C.accent2 } }, { text: 'qualified local suppliers can win orders and create extra Saudi value.' }],
    { x: 7.97, y: 5.35, w: 4.5, h: 0.95, fontSize: 14 });
  src(s, 'Source: GASTAT, Supply and Use Tables 2023, sheets 6.2–6.3 [R05]. Sector share describes scale, not a GDP multiplier.');
}
{
  const t = 'How import-dependent it is';
  const s = content(P2, t, 'Construction’s two most imported inputs: basic metals (54.5%) and electrical machinery (50.3%)', 'Part 1 · How import-dependent it is');
  T(s, 'SAR 646bn construction output in 2023, of which SAR 307.5bn is bought-in inputs', { x: MX, y: 1.95, w: 12.1, h: 0.3, fontSize: 13, bold: true, color: C.background1 });
  const bw = 12.1, wi = bw * 0.197;
  s.addShape(pres.shapes.RECTANGLE, { x: MX, y: 2.3, w: wi - 0.03, h: 0.42, fill: { color: HEX.imp }, line: { color: HEX.imp, width: 0 } });
  s.addShape(pres.shapes.RECTANGLE, { x: MX + wi, y: 2.3, w: bw - wi, h: 0.42, fill: { color: HEX.green }, line: { color: HEX.green, width: 0 } });
  T(s, 'Imported 19.7% · SAR 60.5bn', { x: MX + 0.12, y: 2.3, w: wi, h: 0.42, fontSize: 11.5, bold: true, color: 'FFFFFF', valign: 'middle' });
  T(s, 'Made in Saudi Arabia 80.3% · SAR 247.0bn', { x: MX + wi + 0.12, y: 2.3, w: 6, h: 0.42, fontSize: 11.5, bold: true, color: '04120B', valign: 'middle' });
  const cats = ['Basic metals (steel, aluminium, copper)', 'Electrical machinery (cables, switchgear, transformers)', 'Wood products (timber, plywood, wooden doors)', 'Other chemical products (paints, sealants, adhesives)',
    'Rubber and plastics (PVC pipes, insulation, seals)', 'Glass and non-metallic (cement, glass, ceramic tiles)', 'Refined petroleum (diesel, asphalt, lubricants)', 'Basic chemicals (industrial gases, resins, solvents)'];
  T(s, 'Import leakage by input — as a share and as an amount (construction, 2023)', { x: MX, y: 2.88, w: 12.1, h: 0.28, fontSize: 12, bold: true, color: C.accent2 });
  const share = [54.5, 50.3, 44.7, 43.2, 32.6, 11.8, 8.0, 7.3], amt = [11.97, 2.01, 5.58, 13.43, 2.15, 4.93, 4.14, 4.33];
  const ord = (a) => a.slice().reverse();
  s.addChart(pres.charts.BAR, [{ name: 'Imported share', labels: ord(cats), values: ord(share) }], chartBase({
    x: MX - 0.05, y: 3.15, w: 7.4, h: 3.2, barDir: 'bar', barGapWidthPct: 45, showTitle: true, title: 'Share of national supply that is imported, %', titleColor: HEX.fg2, titleFontSize: 11,
    chartColors: ord([HEX.imp, HEX.imp, HEX.other, HEX.other, HEX.other, HEX.other, HEX.other, HEX.other]), valAxisHidden: true, valAxisMaxVal: 70, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0.0"%"', catAxisLabelFontSize: 10,
    altText: 'Bar chart of imported share of national supply by input' }));
  s.addChart(pres.charts.BAR, [{ name: 'Imported amount', labels: ord(cats.map(c => c.split(' (')[0])), values: ord(amt) }], chartBase({
    x: 7.55, y: 3.15, w: 5.2, h: 3.2, barDir: 'bar', barGapWidthPct: 45, showTitle: true, title: 'Imported amount in construction’s purchases, SAR bn', titleColor: HEX.fg2, titleFontSize: 11,
    chartColors: ord([HEX.imp, HEX.other, HEX.other, HEX.imp, HEX.other, HEX.other, HEX.other, HEX.other]), valAxisHidden: true, valAxisMaxVal: 17, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0.0', catAxisLabelFontSize: 10,
    altText: 'Bar chart of imported amount by input, SAR billion' }));
  T(s, [{ text: 'Metals and electrical machinery are half imported; ' }, { text: 'by amount, chemical products and metals are the largest leaks.', options: { bold: true, color: C.background1 } }],
    { x: MX, y: 6.42, w: 12.1, h: 0.25, fontSize: 12 });
  src(s, 'Source: GASTAT, Supply and Use Tables 2023 [R05] — use: sheet 6.2 col. H; import rate: sheet 6.1 Total imports (AA) ÷ Supply at basic prices (AB). National ratios applied to construction purchases.', 6.7);
}
{
  const t = 'A SAR 4.5bn stadium scenario';
  const s = content(P2, t, 'Applying a SAR 4.5bn stadium scenario', '04 · Applying the multiplier to our case');
  const tw = 3.95;
  [['about SAR 4.0bn', 'Qiddiya stadium · 45,000 seats', null, {}], ['about SAR 3.7bn', 'Aramco Stadium · 46,096 seats', null, {}],
   ['SAR 4.5bn', 'Group scenario, not a published budget or a validated cost estimate', C.accent1, { line: '1F6B4A' }]].forEach((d, i) =>
    tile(s, MX + i * (tw + 0.125), 1.98, tw, 1.45, d[0], d[1], d[2], Object.assign({ vs: 26, vh: 0.5 }, d[3])));
  card(s, MX, 3.62, 12.1, 2.85);
  T(s, 'ROUND 1', { x: MX + 0.3, y: 3.8, w: 3, h: 0.25, fontSize: 10, bold: true, color: C.accent2, charSpacing: 2 });
  T(s, 'Estimated purchases using GASTAT 2023 construction ratios', { x: MX + 0.3, y: 4.05, w: 9, h: 0.35, fontSize: 16, bold: true, color: C.background1 });
  T(s, [{ text: 'SAR 2,143m  ', options: { fontSize: 24, bold: true, color: C.background1 } }, { text: 'total purchases = 47.6% of the SAR 4.5bn', options: { fontSize: 13 } }],
    { x: MX + 0.3, y: 4.5, w: 11, h: 0.45, valign: 'middle' });
  const bx = MX + 0.3, bw2 = 11.5, wl = bw2 * 1721 / 2143;
  s.addShape(pres.shapes.RECTANGLE, { x: bx, y: 5.05, w: wl - 0.03, h: 0.5, fill: { color: HEX.green }, line: { color: HEX.green, width: 0 }, shadow: shadow() });
  s.addShape(pres.shapes.RECTANGLE, { x: bx + wl, y: 5.05, w: bw2 - wl, h: 0.5, fill: { color: HEX.imp }, line: { color: HEX.imp, width: 0 }, shadow: shadow() });
  T(s, [{ text: 'SAR 1,721m  ', options: { bold: true, color: C.accent1, fontSize: 15 } }, { text: 'Purchases inside Saudi Arabia (80.3%) → next spending round' }], { x: bx, y: 5.68, w: 7.5, h: 0.6, fontSize: 12.5 });
  T(s, [{ text: 'SAR 421m  ', options: { bold: true, color: C.accent3, fontSize: 15 } }, { text: 'Purchases from abroad (19.7%) — the first leak' }], { x: bx + 7.2, y: 5.68, w: 4.3, h: 0.6, fontSize: 12.5, align: 'right' });
  src(s, 'Sources: R57, R58 (benchmarks); GASTAT Supply and Use Tables 2023, sheets 6.1–6.2 [R05]. Group scenario using national ratios; figures are rounded.', 6.55);
  thread(s, 3, [0, 1, 2]);
}
{
  const t = 'The materials behind the leakage';
  const s = content(P2, t, 'Estimated imports in the SAR 4.5bn stadium scenario', '05 · The materials behind the import leakage');
  const cats = ['Basic metals', 'Electrical machinery', 'Wood products', 'Other chemical products', 'Rubber and plastics', 'Glass and non-metallic', 'Refined petroleum', 'Basic chemicals', 'All other inputs'];
  const vals = [83, 14, 39, 94, 15, 34, 29, 30, 83];
  const ord = (a) => a.slice().reverse();
  card(s, MX, 1.98, 7.75, 4.5);
  s.addChart(pres.charts.BAR, [{ name: 'SAR m', labels: ord(cats), values: ord(vals) }], chartBase({
    x: MX + 0.1, y: 2.05, w: 7.55, h: 4.35, barDir: 'bar', barGapWidthPct: 40, showTitle: true, title: 'Estimated stadium imports, SAR million', titleColor: HEX.fg2, titleFontSize: 11,
    chartColors: ord([HEX.imp, HEX.other, HEX.other, HEX.imp, HEX.other, HEX.other, HEX.other, HEX.other, HEX.other]), valAxisHidden: true, valAxisMaxVal: 110, dataLabelPosition: 'outEnd', catAxisLabelFontSize: 11,
    altText: 'Bar chart of estimated stadium imports by material group, SAR million' }));
  const rx = 8.55, rw = 4.15;
  card(s, rx, 1.98, rw, 1.55, { fill: '2A140B', line: '7A3518' });
  T(s, 'STADIUM IMPORTS', { x: rx + 0.22, y: 2.1, w: 3, h: 0.25, fontSize: 10, bold: true, color: C.accent3, charSpacing: 2 });
  T(s, 'SAR 421m', { x: rx + 0.22, y: 2.33, w: rw - 0.44, h: 0.55, fontSize: 30, bold: true, color: C.accent3 });
  T(s, '19.7% of the SAR 2,143m estimated purchases split by input', { x: rx + 0.22, y: 2.9, w: rw - 0.44, h: 0.55, fontSize: 12 });
  tile(s, rx, 3.65, rw, 1.35, 'SAR 177m', 'Chemicals + metals · 42% of stadium’s imports', C.accent2, { vs: 28, vh: 0.55 });
  card(s, rx, 5.12, rw, 1.36);
  T(s, 'Actual item check', { x: rx + 0.22, y: 5.24, w: rw - 0.44, h: 0.3, fontSize: 11, bold: true, color: C.accent2 });
  T(s, 'Grade, quantity, origin, certification and price from supplier schedules.', { x: rx + 0.22, y: 5.55, w: rw - 0.44, h: 0.85, fontSize: 13, color: C.background1 });
  src(s, 'Examples under each group are illustrative. Each bar retains its whole GASTAT group value. Source: GASTAT, Supply and Use Tables 2023, sheets 6.1–6.2 [R05]. National product ratios applied to construction use; group scenario, not invoices.', 6.52);
  thread(s, 4, [3]);
}

// ══ PART 3 ═══════════════════════════════════════════════════════════════
const P3 = 'Part 3 · EPP and controls';
pres.addSection({ title: P3 });
divider(P3, 'Part 3', 'EPP and controls', 'Turning the leak into an obligation', 'r_yard.jpg');
{
  const t = 'Stadium EPP at 20%';
  const s = content(P3, t, 'Assessment basis: the official April 2026 consultation framework', '06 · Stadium EPP at 20 percent, credit up to 6');
  const ex = [MX, 4.95, 9.3], ew = 3.4;
  [['SAR 421m', 'Estimated stadium imports · SAR 4.5bn scenario, slide 5', C.accent3, {}], ['20%', 'Second import tier · SAR 300m–500m per tender', C.background1, {}],
   ['SAR 84m', 'Required EP credit · 421m × 20%', C.accent5, { fill: '2A2412', line: '7A6230' }]].forEach((d, i) => tile(s, ex[i], 1.98, ew, 1.35, d[0], d[1], d[2], Object.assign({ vs: 30, vh: 0.6 }, d[3])));
  T(s, '×', { x: ex[0] + ew, y: 2.3, w: ex[1] - ex[0] - ew, h: 0.6, fontSize: 30, bold: true, color: C.accent2, align: 'center' });
  T(s, '=', { x: ex[1] + ew, y: 2.3, w: ex[2] - ex[1] - ew, h: 0.6, fontSize: 30, bold: true, color: C.accent2, align: 'center' });
  card(s, MX, 3.5, 6.6, 2.45);
  T(s, 'Import tiers (per tender) and the EP obligation', { x: MX + 0.22, y: 3.6, w: 6, h: 0.3, fontSize: 12, bold: true, color: C.accent2 });
  s.addChart(pres.charts.BAR, [{ name: 'EP obligation', labels: ['SAR 75m–300m', 'SAR 300m–500m (our SAR 421m)', 'above SAR 500m'], values: [25, 20, 15] }], chartBase({
    x: MX + 0.1, y: 3.9, w: 6.4, h: 2.0, barDir: 'col', barGapWidthPct: 30, chartColors: [HEX.other, HEX.credit, HEX.other], valAxisHidden: true, valAxisMaxVal: 30, dataLabelPosition: 'inEnd', dataLabelFormatCode: '0"%"', dataLabelFontSize: 14, catAxisLabelFontSize: 10.5,
    altText: 'EP obligation by import tier: 25%, 20%, 15%' }));
  T(s, [{ text: 'Assumption: ', options: { bold: true, color: C.accent2 } }, { text: 'one main contract with one company, so all SAR 421m counts.' }], { x: MX, y: 6.05, w: 6.6, h: 0.5, fontSize: 13 });
  const rx = 7.45, rw = 5.25;
  card(s, rx, 3.5, rw, 1.25);
  T(s, 'Draft category factors', { x: rx + 0.22, y: 3.6, w: rw, h: 0.28, fontSize: 11, bold: true, color: C.accent2 });
  T(s, [{ text: 'Knowledge transfer / localisation   ' }, { text: '1–3', options: { bold: true, color: C.background1, breakLine: true } }, { text: 'Technology transfer / exports   ' }, { text: '2–4', options: { bold: true, color: C.background1 } }],
    { x: rx + 0.22, y: 3.92, w: rw - 0.44, h: 0.75, fontSize: 13 });
  card(s, rx, 4.88, rw, 1.07, { fill: '2A2412', line: '7A6230' });
  T(s, '4 + 2 = 6', { x: rx + 0.22, y: 4.95, w: 1.7, h: 0.9, fontSize: 24, bold: true, color: C.accent2, valign: 'middle' });
  T(s, 'Qualifying base + approved bonus. Rare technology or other eligible grounds.', { x: rx + 1.95, y: 4.95, w: rw - 2.15, h: 0.9, fontSize: 12.5, valign: 'middle' });
  T(s, 'Credit differs from cash, GDP and ROI.', { x: rx, y: 6.05, w: rw, h: 0.4, fontSize: 13, bold: true, color: C.background1 });
  src(s, 'Source: LCGPA, Economic Participation Policy Update, consultation text, Articles 6–9 [R63]; DGA Group, April 2026. Imports: group scenario [R05]. Actual tender terms control the applicable version.', 6.5);
  thread(s, 5, [4]);
}
{
  const t = 'London 2012';
  const s = content(P3, t, 'A fixed event deadline made live-site learning especially valuable', '07 · London 2012 offers a construction skills lesson');
  s.addImage({ path: IMG('r_side.jpg'), x: 7.0, y: 1.98, w: 5.7, h: 3.2, altText: '3D model of the stadium', shadow: shadow() });
  tile(s, MX, 1.98, 3.0, 1.55, '3,000+', 'training places', C.accent1, { vs: 36, vh: 0.7 });
  tile(s, MX + 3.15, 1.98, 3.0, 1.55, '408', 'apprentices', null, { vs: 36, vh: 0.7 });
  card(s, MX, 3.68, 3.0, 1.5);
  T(s, '✓  What worked', { x: MX + 0.22, y: 3.8, w: 2.6, h: 0.3, fontSize: 12, bold: true, color: '0CA30C' });
  T(s, [{ text: 'Training connected to ' }, { text: 'real construction jobs', options: { bold: true, color: C.background1 } }, { text: '.' }], { x: MX + 0.22, y: 4.12, w: 2.6, h: 1.0, fontSize: 13.5 });
  card(s, MX + 3.15, 3.68, 3.0, 1.5);
  T(s, '▲  What was weaker', { x: MX + 3.37, y: 3.8, w: 2.6, h: 0.3, fontSize: 12, bold: true, color: 'FAB219' });
  T(s, [{ text: 'Encouragement ' }, { text: 'without binding targets', options: { bold: true, color: C.background1 } }, { text: ' made skills objectives harder.' }], { x: MX + 3.37, y: 4.12, w: 2.6, h: 1.0, fontSize: 13.5 });
  card(s, MX, 5.4, 12.1, 0.85, { fill: '2A2412', line: '7A6230' });
  T(s, [{ text: 'Saudi adaptation: ', options: { bold: true, color: C.accent2 } }, { text: 'paid practice, independent tests and a return-to-train commitment', options: { color: C.background1 } }],
    { x: MX + 0.3, y: 5.4, w: 11.5, h: 0.85, fontSize: 17, valign: 'middle' });
  src(s, 'Sources: UK DCMS, 2012 Games construction on track, 20 May 2012 [R12]; Crossrail Learning Legacy, 2018 [R13]. Counts do not prove retained jobs.', 6.45);
}
{
  const t = 'The controls';
  const s = content(P3, t, 'Five risks, five controls', '08 · The controls that make the solution credible');
  const rows = [['Routine training earns extra credit', 'Record existing duties. Fund new competence, rights or tooling.'], ['IP cannot be used independently', 'Agree licences, diagnostic access, trainer rights and export territory.'],
    ['Shared delivery duplicates claims', 'Keep each supplier’s approved activities, cost allocation and ledger separate.'], ['Local substitutes or bulk buying fail', 'Test grades, capacity and full cost. Use fair lots and multiple suppliers.'],
    ['Skills have no work after handover', 'Confirm placements before training and contract the next site.']];
  T(s, 'RISK', { x: MX + 0.5, y: 1.88, w: 4, h: 0.25, fontSize: 9.5, bold: true, color: C.accent6, charSpacing: 2 });
  T(s, 'PROPOSED CONTROL', { x: 5.75, y: 1.88, w: 4, h: 0.25, fontSize: 9.5, bold: true, color: C.accent6, charSpacing: 2 });
  rows.forEach((r, i) => {
    const y = 2.15 + i * 0.66; card(s, MX, y, 12.1, 0.56, { flat: true });
    T(s, '▲', { x: MX + 0.2, y, w: 0.3, h: 0.56, fontSize: 10, color: C.accent3, valign: 'middle' });
    T(s, r[0], { x: MX + 0.5, y, w: 4.5, h: 0.56, fontSize: 13.5, bold: true, color: C.background1, valign: 'middle' });
    s.addShape(pres.shapes.LINE, { x: 5.55, y: y + 0.12, w: 0, h: 0.32, line: { color: HEX.green, width: 2 } });
    T(s, r[1], { x: 5.75, y, w: 6.8, h: 0.56, fontSize: 13, valign: 'middle' });
  });
  T(s, 'Evidence at three points', { x: MX, y: 5.5, w: 4, h: 0.3, fontSize: 13, bold: true, color: C.background1 });
  const tl = [['Before', 'baseline and rights'], ['Completion', 'independent tests'], ['6 / 12 months', 'work and trainer return']];
  s.addShape(pres.shapes.LINE, { x: 2.2, y: 5.98, w: 8.9, h: 0, line: { color: HEX.green, width: 2 } });
  tl.forEach((p, i) => {
    const cx = 2.2 + i * 4.45;
    s.addShape(pres.shapes.OVAL, { x: cx - 0.11, y: 5.87, w: 0.22, h: 0.22, fill: { color: HEX.bg }, line: { color: i === 2 ? HEX.gold : HEX.green, width: 3 } });
    T(s, [{ text: p[0], options: { bold: true, color: C.background1, breakLine: true } }, { text: p[1] }], { x: cx - 1.5, y: 6.12, w: 3, h: 0.5, fontSize: 12, align: 'center' });
  });
  src(s, 'Sources: LCGPA consultation Arts. 8(3), 13–16 [R63]; WIPO licensing [R64]; OECD competition safeguards [R68]; UK additionality study [R54].', 6.68);
}

// ══ PART 4 ═══════════════════════════════════════════════════════════════
const P4 = 'Part 4 · The academy proposal';
pres.addSection({ title: P4 });
divider(P4, 'Part 4', 'The academy proposal', 'Turning the obligation into Saudi capability', 'r_scoreboard.jpg');
{
  const t = 'One academy, three functions';
  const s = content(P4, t, 'Shared delivery across eligible stadium suppliers, with separate EP obligations', '09 · One academy with three connected functions');
  card(s, MX, 1.98, 12.1, 0.75, { fill: '2A2412', line: '7A6230' });
  T(s, [{ text: 'Shared EPP proposal: ', options: { bold: true, color: C.accent2 } }, { text: 'eligible stadium vendors jointly fund ONE academy. Each vendor contributes approved funding, trainers, equipment or licensed know-how.', options: { color: C.background1 } }],
    { x: MX + 0.25, y: 1.98, w: 11.6, h: 0.75, fontSize: 13.5, valign: 'middle' });
  const fx = [['01', 'License and train', ['Licensed manuals and software', 'HVAC rigs and coating-test kits', 'Paid practice and Saudi trainers'], 'Evidence: NITI training; WIPO licensing terms'],
    ['02', 'Qualify Saudi materials', ['Coatings, sealants and metals', 'Test specific grades and origin', 'Material passports for approvals'], 'Evidence: ALUPCO extrusion; Sika Saudi admixture production'],
    ['03', 'Buy together', ['Common performance specifications', 'Competitive framework and call-offs', 'Verify discounts and full cost'], 'Evidence: OECD purchasing efficiency and competition']];
  const fw = 3.95;
  fx.forEach((f, i) => {
    const x = MX + i * (fw + 0.125), y = 2.88; card(s, x, y, fw, 2.3, { fill: '0C2A1F', line: '1F6B4A' });
    s.addShape(pres.shapes.OVAL, { x: x + 0.2, y: y + 0.18, w: 0.42, h: 0.42, fill: { color: HEX.green, transparency: 80 }, line: { color: HEX.green, width: 1 } });
    T(s, f[0], { x: x + 0.2, y: y + 0.18, w: 0.42, h: 0.42, fontSize: 11, bold: true, color: C.accent1, align: 'center', valign: 'middle' });
    T(s, f[1], { x: x + 0.75, y: y + 0.18, w: fw - 0.9, h: 0.42, fontSize: 15.5, bold: true, color: C.background1, valign: 'middle' });
    T(s, bullets(f[2]), { x: x + 0.22, y: y + 0.72, w: fw - 0.44, h: 1.0, fontSize: 12.5 });
    s.addShape(pres.shapes.LINE, { x: x + 0.22, y: y + 1.78, w: fw - 0.44, h: 0, line: { color: HEX.line, width: 0.75, dashType: 'dash' } });
    T(s, f[3], { x: x + 0.22, y: y + 1.84, w: fw - 0.44, h: 0.42, fontSize: 10.5, color: C.accent6 });
  });
  card(s, MX, 5.32, 5.98, 0.9, { flat: true });
  T(s, 'One qualified host runs the programme. Sharing trainers, equipment and demand reduces duplicated training and keeps skills available across sites.', { x: MX + 0.2, y: 5.32, w: 5.6, h: 0.9, fontSize: 12, valign: 'middle' });
  card(s, 6.72, 5.32, 5.98, 0.9, { flat: true });
  T(s, [{ text: 'LCGPA approves vendor roles and cost allocations. ' }, { text: 'Each vendor keeps its own EP obligation and ledger. Each activity earns credit once.', options: { bold: true, color: C.background1 } }],
    { x: 6.92, y: 5.32, w: 5.6, h: 0.9, fontSize: 12, valign: 'middle' });
  T(s, [{ text: 'Later: ', options: { bold: true, color: C.accent2 } }, { text: 'export Saudi-owned courses, licensed services and qualified products.' }], { x: MX, y: 6.3, w: 12.1, h: 0.3, fontSize: 12.5 });
  src(s, 'Sources: NITI [R42]; official LCGPA draft Arts. 8–9 [R63]; WIPO [R64]; OECD [R65, R68]; ALUPCO [R66]; Sika [R67]. Candidate capabilities, not partner commitments.', 6.66);
}
{
  const t = 'Hands-on training first';
  const s = content(P4, t, 'Begin inside real projects with an existing qualified training provider', '10 · Hands-on training first, academy after evidence');
  T(s, [{ text: 'Joint agreement first: ', options: { bold: true, color: C.accent2 } }, { text: 'vendor commitments, LCGPA-approved activities and separate credit records.' }], { x: MX, y: 1.92, w: 12.1, h: 0.3, fontSize: 13 });
  const st = [['1', 'Confirm demand', 'Employers identify the skills gap and sign paid site placements. Vendor roles and funding are agreed.', 'Next-site work, budget, IP rights, tools and approvals are confirmed. Signed licences and EP cost allocations.'],
    ['2', 'Run the pilot', 'Supplier mentors teach on real equipment. Independent tests and trainer practice. Saudi trainers teach the next cohort.', 'Verify practical competence, paid deployment and unit cost. Record extra capability beyond routine duties.'],
    ['3', 'Expand if proven', 'Repeat cohorts build an academy. A permanent facility needs its own case. Use existing facilities where adequate.', 'Continuing jobs and orders, proven results and acceptable quality and cost. Track work and trainer return at 6/12 months.']];
  const sw = 3.85;
  st.forEach((p, i) => {
    const x = MX + i * (sw + 0.275), y = 2.35; card(s, x, y, sw, 3.25);
    s.addShape(pres.shapes.OVAL, { x: x + 0.2, y: y + 0.2, w: 0.42, h: 0.42, fill: { color: HEX.gold, transparency: 85 }, line: { color: HEX.gold, width: 1 } });
    T(s, p[0], { x: x + 0.2, y: y + 0.2, w: 0.42, h: 0.42, fontSize: 13, bold: true, color: C.accent2, align: 'center', valign: 'middle' });
    T(s, p[1], { x: x + 0.75, y: y + 0.2, w: sw - 0.9, h: 0.42, fontSize: 16, bold: true, color: C.background1, valign: 'middle' });
    T(s, p[2], { x: x + 0.22, y: y + 0.78, w: sw - 0.44, h: 1.1, fontSize: 12.5 });
    card(s, x + 0.18, y + 1.92, sw - 0.36, 1.18, { fill: '0C2A1F', line: '1F6B4A', flat: true });
    T(s, [{ text: 'Condition to proceed', options: { bold: true, color: C.accent1, fontSize: 10, breakLine: true } }, { text: p[3] }], { x: x + 0.32, y: y + 2.0, w: sw - 0.64, h: 1.05, fontSize: 11 });
    if (i < 2) T(s, '→', { x: x + sw, y: y + 0.15, w: 0.275, h: 0.5, fontSize: 18, bold: true, color: C.accent2, align: 'center' });
  });
  card(s, MX, 5.75, 5.98, 0.78, { line: '7A3518', flat: true });
  T(s, 'No confirmed paid demand: defer intake. Weak results: redesign or stop.', { x: MX + 0.2, y: 5.75, w: 5.6, h: 0.78, fontSize: 13, bold: true, color: C.background1, valign: 'middle' });
  card(s, 6.72, 5.75, 5.98, 0.78, { flat: true });
  T(s, [{ text: 'Suggested start: ' }, { text: '24 learners, 6 trainer candidates, 2 eligible sites.', options: { bold: true, color: C.background1 } }, { text: ' Targets for agreement.' }],
    { x: 6.92, y: 5.75, w: 5.6, h: 0.78, fontSize: 13, valign: 'middle' });
  src(s, 'Basis: report Sections 5–8 and Appendix F. Sources: NITI [R42], training evaluation [R54], LCGPA draft [R63], WIPO [R64]. Proposed design.', 6.6);
}
{
  const t = 'Value now and after opening';
  const s = content(P4, t, 'What stays after the cranes leave', '11 · Value now and after the stadium opens');
  const hdr = (x) => ({ text: x, options: { bold: true, color: HEX.fg, fill: { color: '123A2C' }, fontSize: 12 } });
  const c = (x, b) => ({ text: x, options: { color: b ? HEX.fg : HEX.fg2, bold: !!b, fontSize: 12 } });
  s.addTable([['Value', 'During construction', 'After handover'].map(hdr),
    [c('Skills and academic capability', 1), c('Paid practice, independent tests, manuals and trainer development'), c('Next-site work, returning trainers and further recognised qualifications')],
    [c('Local products and IP', 1), c('Approved local grades, tooling and usable technical rights'), c('Repeat orders, deeper production and independent Saudi services')],
    [c('Buyer value', 1), c('Joint offers, less duplicated buying and comparable full-cost prices'), c('Reusable specifications and resilient multi-supplier sourcing')],
    [c('Export value', 1), c('Saudi-authored content and rights prepared for later markets'), c('Paid courses, licensed services and qualified products sold abroad')]],
    { x: MX, y: 1.98, w: 8.3, colW: [2.3, 3.0, 3.0], border: { type: 'solid', color: HEX.line, pt: 0.75 }, fill: { color: HEX.surface }, margin: 0.08, rowH: 0.72 });
  s.addImage({ path: IMG('r_palms.jpg'), x: 9.1, y: 1.98, w: 3.6, h: 3.62, sizing: { type: 'cover', w: 3.6, h: 3.62 }, altText: '3D model: palms and stadium facade', shadow: shadow() });
  card(s, MX, 5.72, 12.1, 0.8, { fill: '2A2412', line: '7A6230' });
  T(s, [{ text: 'Illustrative materials opportunity   ', options: { bold: true, color: C.accent2, fontSize: 11 } }, { text: '25% of the SAR 177m basket ≈ ', options: { bold: true, color: C.background1 } }, { text: 'SAR 44m', options: { bold: true, color: C.accent1, fontSize: 20 } }, { text: ' more domestic purchases', options: { bold: true, color: C.background1 } }],
    { x: MX + 0.3, y: 5.72, w: 11.5, h: 0.8, fontSize: 15, valign: 'middle' });
  src(s, 'Source: GASTAT-based group scenario [R05]. Benefits are proposals. No discount or export revenue is assumed. Domestic purchases, savings and credit are separate.', 6.58);
  thread(s, 6, [5]);
}
{
  const t = 'The decision';
  const s = content(P4, t, 'A shared Materials and Systems Academy pilot', '12 · The decision for LCGPA and the buyer');
  T(s, 'Proposed joint programme for all participating eligible stadium vendors · one academy, agreed vendor contributions and individual compliance records.', { x: MX, y: 1.9, w: 12.1, h: 0.32, fontSize: 12.5 });
  [['LCGPA', 'Approve extra activities, rights, factors and separate supplier ledgers.'], ['Authorised buyer', 'Approve competitive joint procurement and construction gates.'], ['Delivery partners', 'Agree paid placements, material trials, trainer return and follow-up.']].forEach((d, i) => {
    const x = MX + i * 4.075; card(s, x, 2.3, 3.95, 1.1, { fill: '2A2412', line: '7A6230' });
    T(s, d[0], { x: x + 0.22, y: 2.38, w: 3.5, h: 0.3, fontSize: 12, bold: true, color: C.accent2 });
    T(s, d[1], { x: x + 0.22, y: 2.68, w: 3.5, h: 0.68, fontSize: 12.5, color: C.background1 });
  });
  card(s, MX, 3.55, 7.0, 2.5);
  T(s, 'EP CREDIT PLAN', { x: MX + 0.22, y: 3.63, w: 3, h: 0.25, fontSize: 10, bold: true, color: C.accent2, charSpacing: 2 });
  T(s, 'SAR 84m from about SAR 36m of activity (average factor 2.33; SAR 63m at low-end factors)', { x: MX + 0.22, y: 3.88, w: 6.6, h: 0.5, fontSize: 13, bold: true, color: C.background1 });
  s.addChart(pres.charts.BAR, [{ name: 'Activity, SAR m', labels: ['Localisation ×2', 'Knowledge transfer ×2', 'Technology transfer ×3'], values: [12, 12, 12] }, { name: 'EP credit, SAR m', labels: ['Localisation ×2', 'Knowledge transfer ×2', 'Technology transfer ×3'], values: [24, 24, 36] }],
    chartBase({ x: MX + 0.1, y: 4.35, w: 6.8, h: 1.65, barDir: 'bar', barGrouping: 'clustered', barGapWidthPct: 35, chartColors: [HEX.other, HEX.credit], valAxisHidden: true, valAxisMaxVal: 45, dataLabelPosition: 'outEnd', catAxisLabelFontSize: 10.5, dataLabelFontSize: 10,
      showLegend: true, legendPos: 'r', legendFontSize: 9, legendColor: HEX.fg2, legendFontFace: '+mn-lt', altText: 'EP credit plan: activity and credit by category' }));
  tile(s, 7.75, 3.55, 4.95, 1.15, 'SAR 84m', 'EP credit = 36 + 24 + 24', C.accent1, { vs: 26, vh: 0.5 });
  card(s, 7.75, 4.82, 4.95, 1.23, { flat: true });
  T(s, [{ text: 'Why these factors: ', options: { bold: true, color: C.background1 } }, { text: 'LCGPA sets the final factor within each draft range. We start at the minimum and add 1 per condition met: usable licences (2→3), new skills with independent tests (1→2), approved Saudi materials with real orders (1→2). Not the maximum: no manufacturing rights, recognised qualification or new plant.' }],
    { x: 7.92, y: 4.88, w: 4.62, h: 1.12, fontSize: 9.5 });
  T(s, 'Proposed start: 24 learners, 6 trainer candidates, 2 confirmed eligible sites', { x: MX, y: 6.12, w: 12.1, h: 0.3, fontSize: 13.5, bold: true, color: C.accent1 });
  src(s, 'Proposal targets for agreement, not forecasts or observed results. Scale on proven skills, demand, quality, cost and licensed rights. Policy basis: LCGPA [R63].', 6.45);
  thread(s, 7, [6]);
}

// ══ CLOSE ════════════════════════════════════════════════════════════════
pres.addSection({ title: 'Close' });
{
  const s = pres.addSlide({ masterName: 'COVER', sectionTitle: 'Close' });
  s.addImage({ path: IMG('r_signature.jpg'), x: 0, y: 0, w: W, h: Hh, altText: '3D model of King Salman Stadium' });
  s.addImage({ path: IMG('ov_bottom.png'), x: 0, y: 0, w: W, h: Hh, altText: '' });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: Hh, fill: { color: HEX.bg, transparency: 45 }, line: { color: HEX.bg, width: 0 } });
  T(s, 'GROUP 8  ·  MBSC EMBA  ·  ECN 511', { x: 0, y: 1.55, w: W, h: 0.35, fontSize: 13, bold: true, color: C.accent2, align: 'center', charSpacing: 5 });
  T(s, 'Thank you', { x: 0, y: 2.0, w: W, h: 1.4, fontSize: 80, bold: true, color: C.background1, align: 'center' });
  T(s, 'Questions welcome', { x: 0, y: 3.45, w: W, h: 0.45, fontSize: 20, color: C.background2, align: 'center' });
  const team = [['AA', 'Abdulmajeed', 'Alajlan'], ['AD', 'Abdulrahman', 'Aldahlawi'], ['SA', 'Salman', 'Alfaris'], ['MA', 'Mohammed', 'Alghamdi'], ['AW', 'Abdulaziz', 'Alweheab'], ['NA', 'Nada', 'Alyahya'], ['HB', 'Haifa', 'Binnafisah']];
  const cw = 1.6, x0 = (W - team.length * cw) / 2;
  team.forEach((m, i) => {
    const x = x0 + i * cw;
    s.addShape(pres.shapes.LINE, { x: x + 0.1, y: 4.45, w: cw - 0.2, h: 0, line: { color: HEX.line, width: 1.5 } });
    s.addShape(pres.shapes.OVAL, { x: x + cw / 2 - 0.3, y: 4.68, w: 0.6, h: 0.6, fill: { color: HEX.green, transparency: 88 }, line: { color: HEX.green, width: 1.5 } });
    T(s, m[0], { x: x + cw / 2 - 0.3, y: 4.68, w: 0.6, h: 0.6, fontSize: 13, bold: true, color: C.accent1, align: 'center', valign: 'middle' });
    T(s, [{ text: m[1], options: { bold: true, color: C.background1, fontSize: 14, breakLine: true } }, { text: m[2], options: { color: C.background2, fontSize: 12 } }],
      { x, y: 5.38, w: cw, h: 0.6, align: 'center' });
  });
  T(s, 'King Salman Stadium · Riyadh 2034', { x: 0, y: 6.75, w: W, h: 0.3, fontSize: 11, color: C.accent6, align: 'center', charSpacing: 2 });
  notes(s, 'Thank you');
}

// ══ SOURCES ══════════════════════════════════════════════════════════════
const PS = 'Sources';
pres.addSection({ title: PS });
const SOURCES = [
  ['Sources 1 of 4', 'Case, sector and stadium packages', [
    ['R01', 'FIFA World Cup 2034 Bid Evaluation Report, 2024, pp 46–51', 'FIFA, 29 November 2024.', 'https://digitalhub.fifa.com/m/51d8a13714827f1d/original/FIFA-World-Cup-2034-Bid-Evaluation-Report.pdf'],
    ['R17', 'FIFA host appointment, 11 December 2024', 'Extraordinary FIFA Congress appoints hosts of 2030 and 2034 editions.', 'https://inside.fifa.com/en/news/extraordinary-congress-appoints-hosts-of-2030-and-2034-editions-of-fifa-world-cup'],
    ['R05', 'GASTAT Supply and Use Tables 2023, sheets 6.1–6.2', 'Supply and Use and Input-Output Tables by Sections 2023, released 2025; thousand SAR.', 'https://www.stats.gov.sa/documents/20117/2435267/SUT_and_IO_By_Sections_-En.xlsx_fixed_3036245/91b73a34-05e8-0e49-46e8-eda783beae16?t=1746090703771'],
    ['R02', 'MoS King Salman main works notice, 25 November 2025', 'Prequalification invitation; deadline 16 February 2026.', 'https://www.mos.gov.sa/en/media/news/2025/11/25/king-salman-stadium'],
    ['R03', 'MoS King Salman preliminary works notice, 7 April 2026', 'Prequalification invitation; deadline 28 April 2026.', 'https://www.mos.gov.sa/en/media/news/2026/04/07/king-salman-stadium'],
    ['R53', 'Populous King Salman Stadium project and concept images', 'Undated project page. Designer identity.', 'https://populous.com/projects/king-salman-stadium'],
    ['R23', 'Estithmar mechanical package announcement, 10 September 2026', 'Elegancia Arabia Trading awarded SAR 829m mechanical works, Prince Mohammed bin Salman Stadium.', 'https://www.estithmarholding.com/media/read/263'],
    ['R24', 'China Fangda facade package filing, 19 October 2026', 'Announcement 2026-41; SAR 1,146.9m incl. VAT / SAR 997.3m excl. VAT.', 'http://static.cninfo.com.cn/finalpage/2026-10-19/1225610057.PDF']],
    'Evidence basis: report updated 21 October 2026. Course material: [C1] George, R. E., Assessment Guidelines for ECN 511, MBSC, 30 September 2026; [C2] MBSC, ECN 511 Course Syllabus Modular A1, 2026; [C3] George, R. E., EPP assessment update allowing supporting localisation evidence, email received 20 October 2026. No public URLs. References and backup material sit outside the eight-minute presentation.'],
  ['Sources 2 of 4', 'Policy, benchmark and training evidence', [
    ['R09', 'LCGPA Economic Participation Policy, Unit 7, historical training material', 'PC-GEN-TM-ECP-EN-V12, pp. 4–5, 11–15, 21–22.', 'https://lcgpa.futurex.sa/pluginfile.php/2095/mod_folder/content/0/pdf%20E/Economic%20Participation%20Policy%20%281%29.pdf?forcedownload=1'],
    ['R11', 'Umm Al-Qura EPP consultation notice, 14 April 2026', 'Consultation notice; not an adoption notice.', 'https://www.uqn.gov.sa/news/reports/4000737'],
    ['R27', 'DGA analysis of the EPP consultation draft, April 2026', 'DGA Group / Albright Stonebridge Group, pp. 4–6.', 'https://dgagroup.com/wp-content/uploads/2026/04/DGA-ASG-Analysis-Updated-Version-of-Saudi-Economic-Participation-Policy-Issued-for-Public-Consultation-1.pdf'],
    ['R12', 'UK government London 2012 construction release, 20 May 2012', '2012 Games construction on track thanks to 12,000-strong workforce.', 'https://www.gov.uk/government/news/2012-games-construction-on-track-thanks-to-12-000-strong-workforce'],
    ['R13', 'Crossrail Learning Legacy, contractual skills targets, 2018', 'Eldred and Blin, 17 August 2018, section 1.2.', 'https://learninglegacy.crossrail.co.uk/documents/implementing-contractual-skills-and-employment-targets/'],
    ['R14', 'EXPRO Operations Management Introduction Guideline, 2021', 'EOM-ZO0-GL-000001, Rev. 001, sections 6.3–6.7.', 'https://expro.gov.sa/api/uploads/Operations%20Management%20Introduction%20Guideline.pdf'],
    ['R42', 'NITI Apprenticeship Program, undated brochure', 'Candidate training capability only.', 'https://www.niti.edu.sa/wp-content/themes/niti_theme/pdfs/apprenticeship-program.pdf'],
    ['R54', 'UK BIS Measuring Additionality in Apprenticeships, 2013', 'Research Paper 138, pp. 9–13.', 'https://www.gov.uk/government/publications/measuring-additionality-in-apprenticeships'],
    ['R55', 'Local content preference regulation, Resolution 245, 2019', 'Articles 4, 11–16 and 18–22.', 'https://www.mof.gov.sa/mediacenter/news/Documents/%D9%84%D8%A7%D8%A6%D8%AD%D8%A9.pdf'],
    ['R56', 'LCGPA mechanisms for government entities, Unit 2', 'PC-GOV-TM-MCI-EN-V12.', 'https://lcgpa.futurex.sa/pluginfile.php/2095/mod_folder/content/0/pdf%20E/Introduction%20to%20Local%20Content%20Mechanisms%20for%20Government%20Entities%20%283%29.pdf?forcedownload=1'],
    ['R08', 'IMF Saudi Arabia Article IV, 2024, Box 1', 'Country Report 24/280, printed p. 10.', 'https://www.imf.org/-/media/files/publications/cr/2024/english/1sauea2024001-print-pdf.pdf']],
    'AI use: ChatGPT supported research, calculations, charts and drafting. Claude supported review. No original interviews or field data are claimed. Facts, teaching assumptions and proposals remain labelled. The submitting group remains responsible for source checks and final approval.'],
  ['Sources 3 of 4', 'Updated stadium comparisons', [
    ['R57', 'Argaam, Qiddiya stadium contract, October 2024', 'Qiddiya awards SAR 4B stadium project contract to Saudi-Spanish consortium.', 'https://www.argaam.com/en/article/articledetail/id/1758470'],
    ['R58', 'MEED, Saudi Arabia selects Dammam stadium contractor, 26 February 2024', 'Besix–Albawani, est. SAR 3.7bn.', 'https://www.meed.com/saudi-arabia-selects-dammam-stadium-contractor'],
    ['R59', 'StadiumDB, Aramco Stadium design and capacity, undated', '', 'https://stadiumdb.com/designs/ksa/dammam_stadium'],
    ['R60', 'StadiumDB, Qiddiya stadium design and capacity, undated', '', 'https://stadiumdb.com/designs/ksa/qiddiya_stadium'],
    ['R69', 'IMF, Fiscal Multipliers, 2014, section II', 'Batini, Eyraud, Forni and Weber, Technical Notes and Manuals 14/04. Definition and teaching example on slide 2.', 'https://www.imf.org/external/pubs/ft/tnm/2014/tnm1404.pdf']],
    'Verification: GASTAT Supply and Use Tables 2023 downloaded 27 October 2026. The supplied ratios reproduce 60.507bn of modelled imported construction inputs by applying each national product import ratio to construction use — an estimate, not an observed industry import-use matrix. BESIX’s official project page confirms the Aramco client and BESIX–ALBAWANI JV. Official capacities are approximately 47,000; the retained 46,096 is the FIFA bid design scope. Current public procurement notices do not establish an awarded King Salman main package.'],
  ['Sources 4 of 4', 'Policy and solution evidence', [
    ['R63', 'LCGPA, Economic Participation Policy Update, April 2026 consultation, Arts. 3–19', 'Official Arabic consultation text, read 28 October 2026. Consultation text, not an adoption notice.', 'https://istitlaa.ncc.gov.sa/ar/finance/lcgpa/economicparticipationpolicyupdate/Pages/default.aspx'],
    ['R64', 'WIPO, Technology Transfer Agreements, licensing rights and scope', 'Licensing, territory, field of use and ownership.', 'https://www.wipo.int/en/web/technology-transfer/agreements'],
    ['R65', 'OECD, Government at a Glance 2025, section 11.5, centralised purchasing', '', 'https://www.oecd.org/en/publications/government-at-a-glance-2025_0efd0bcd-en/full-report/efficient-public-procurement_9420d708.html'],
    ['R66', 'ALUPCO, Aluminium, Saudi extrusion, die-making and finishing capability', 'Capability evidence, not a commitment to this proposal.', 'https://alupco.com/aluminium/'],
    ['R67', 'Sika, New Saudi admixture factory, 27 June 2018, official release', 'Historic capability evidence, not proof of every coating grade or current capacity.', 'https://www.sika.com/dms/getdocument.get/e671630e-2b9d-4256-898e-bd30c9a627fa/glo-en-media-release-saudi-arabia-27-06-2018.pdf'],
    ['R68', 'OECD, SMEs in Public Procurement, 2018, Box 2.4, competition safeguards', '', 'https://www.oecd.org/content/dam/oecd/en/publications/reports/2018/10/smes-in-public-procurement_g1g98d8f/9789264307476-en.pdf']],
    'The primary draft was read directly from the official Istitlaa consultation HTML on 28 October 2026. It is a consultation text, not an adoption notice. The supporting sources establish mechanisms and existing capabilities, not committed project partners or guaranteed performance.']];
SOURCES.forEach(([title, head, refs, foot]) => {
  const s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: PS });
  s.addText(head, { placeholder: 'title' }); eyebrow(s, title);
  const cols = refs.length > 6 ? 2 : 1, per = Math.ceil(refs.length / cols), cw = cols === 2 ? 5.95 : 12.1;
  const rowH = Math.min(0.72, 3.85 / per);
  refs.forEach((r, i) => {
    const col = Math.floor(i / per), row = i % per, x = MX + col * (cw + 0.2), y = 1.98 + row * rowH;
    T(s, r[0], { x, y, w: 0.55, h: rowH, fontSize: 11, bold: true, color: C.accent2 });
    T(s, [{ text: r[1], options: { bold: true, color: C.background1, hyperlink: { url: r[3] }, breakLine: !!r[2] } }].concat(r[2] ? [{ text: r[2], options: { color: C.background2 } }] : []),
      { x: x + 0.6, y, w: cw - 0.65, h: rowH, fontSize: 10.5 });
  });
  card(s, MX, 5.95, 12.1, 0.95, { flat: true, tr: 30 });
  T(s, foot, { x: MX + 0.2, y: 6.0, w: 11.7, h: 0.88, fontSize: 9.5, color: C.accent6, valign: 'middle' });
  s.addNotes('Source titles are clickable.');
});

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log('wrote', OUT);
})();
