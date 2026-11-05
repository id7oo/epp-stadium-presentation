// Price elasticity and access to weight-management medicines in Saudi Arabia — Group 8.
// Editorial "pharmacy label" look: ink-green, white paper, one signal-orange accent,
// capsule-shaped tags as the recurring motif. Run: node build.js OUT.pptx
const pptxgen = require('pptxgenjs');
const React = require('react');
const ReactDOMServer = require('react-dom/server');
const sharp = require('sharp');
const fa = require('react-icons/fa6');
const { applyTheme } = require(process.env.PPTX_SKILL + '/scripts/apply_theme.js');
const OUT = process.argv[2] || 'deck.pptx';

const THEME = {
  name: 'Dose Label', headFontFace: 'Cambria', bodyFontFace: 'Calibri',
  colors: { dk1: '13201F', lt1: 'FFFFFF', dk2: '1F4D47', lt2: 'EEF2EF',
    accent1: 'E8552A', accent2: '7FA896', accent3: 'D5E2DB', accent4: 'F6C9B8', accent5: '3A6B63', accent6: '6B7C77',
    hlink: 'E8552A', folHlink: '3A6B63' },
};
const H = THEME.colors;
const TEAM = ['Abdulmajeed Alajlan', 'Abdulrahman Aldahlawi', 'Salman Alfaris', 'Mohammed Alghamdi',
  'Abdulaziz Alweheab', 'Nada Alyahya', 'Haifa Binnafisah'];

const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9'; // 10 x 5.625
pres.title = 'Price Elasticity and Access to Weight-Management Medicines in Saudi Arabia';
pres.author = 'Group 8';
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

async function icon(Comp, color) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: '#' + color, size: 256 }));
  const buf = await sharp(Buffer.from(svg)).resize(256, 256).png().toBuffer();
  return 'image/png;base64,' + buf.toString('base64');
}

// ---------- layouts ----------
pres.defineSlideMaster({
  title: 'COVER', background: { color: H.dk1 },
  objects: [{ placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 1.2, w: 6.5, h: 2.2,
    fontFace: THEME.headFontFace, fontSize: 30, bold: true, color: C.background1, valign: 'top', align: 'left', margin: 0 }, text: '' } }],
});
pres.defineSlideMaster({
  title: 'CONTENT', background: { color: H.lt1 },
  margin: [0.5, 0.5, 0.5, 0.5],
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 0.62, w: 8.8, h: 0.7,
      fontFace: THEME.headFontFace, fontSize: 28, bold: true, color: C.text1, valign: 'top', align: 'left', margin: 0 }, text: '' } },
    { text: { text: 'Group 8  ·  GLP-1 access in Saudi Arabia', options: { x: 0.6, y: 5.17, w: 5, h: 0.25,
      fontSize: 9, color: C.accent6, margin: 0 } } },
  ],
  slideNumber: { x: 9.0, y: 5.17, w: 0.4, h: 0.25, fontSize: 9, color: H.accent6, align: 'right', margin: 0 },
});
pres.defineSlideMaster({
  title: 'DARK', background: { color: H.dk1 },
  objects: [{ placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 0.62, w: 8.8, h: 0.7,
    fontFace: THEME.headFontFace, fontSize: 28, bold: true, color: C.background1, valign: 'top', align: 'left', margin: 0 }, text: '' } }],
  slideNumber: { x: 9.0, y: 5.17, w: 0.4, h: 0.25, fontSize: 9, color: H.accent2, align: 'right', margin: 0 },
});

// ---------- helpers ----------
// The capsule: the deck's one motif. Rounded tag with text.
function capsule(slide, text, x, y, w, opt = {}) {
  const h = opt.h || 0.3;
  slide.addText(text, { x, y, w, h, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: h / 2,
    fill: { color: opt.fill || C.background2 }, line: opt.line ? { color: opt.line, width: 1 } : undefined,
    color: opt.color || C.text1, fontSize: opt.fontSize || 10, bold: opt.bold !== false, align: 'center',
    valign: 'middle', margin: 0, charSpacing: opt.charSpacing ?? 1, isTextBox: true, objectName: opt.name || 'capsule' });
}
// A small "section index" capsule + presenter name, top of every content slide
function kicker(slide, no, label, who, dark) {
  capsule(slide, no, 0.6, 0.2, 0.5, { fill: C.accent1, color: C.background1, fontSize: 10, name: 'index' });
  slide.addText(label.toUpperCase(), { x: 1.2, y: 0.2, w: 4.5, h: 0.3, fontSize: 10, bold: true, charSpacing: 2,
    color: dark ? C.accent2 : C.accent5, valign: 'middle', margin: 0, isTextBox: true, objectName: 'kicker' });
  if (who) slide.addText('Presenter  ' + who, { x: 5.4, y: 0.2, w: 4.0, h: 0.3, fontSize: 10, align: 'right',
    color: dark ? C.accent3 : C.accent6, valign: 'middle', margin: 0, isTextBox: true, objectName: 'presenter' });
}
const txt = (slide, text, o) => slide.addText(text, { margin: 0, isTextBox: true, valign: 'top', ...o });

(async () => {
  const I = {
    syringe: await icon(fa.FaSyringe, H.lt1),
    scale: await icon(fa.FaWeightScale, H.lt1),
    vial: await icon(fa.FaVial, H.lt1),
    user: await icon(fa.FaUser, H.lt1),
    store: await icon(fa.FaPrescriptionBottleMedical, H.lt1),
    gov: await icon(fa.FaLandmark, H.lt1),
    pill: await icon(fa.FaCapsules, H.lt1),
    tag: await icon(fa.FaTags, H.lt1),
    gap: await icon(fa.FaMagnifyingGlassChart, H.lt1),
  };

  // ===== 1. Cover =====
  pres.addSection({ title: 'Opening' });
  let s = pres.addSlide({ masterName: 'COVER', sectionTitle: 'Opening' });
  capsule(s, 'GROUP 8', 0.6, 0.55, 1.1, { fill: C.accent1, color: C.background1, charSpacing: 2 });
  txt(s, 'ECN 511  ·  Economics for Managers', { x: 1.85, y: 0.55, w: 4, h: 0.3, fontSize: 11, color: C.accent3, valign: 'middle' });
  s.addText('Price, supply and the patient: elasticity of demand for weight-management medicines in Saudi Arabia',
    { placeholder: 'title' });
  ['Ozempic', 'Wegovy', 'Mounjaro'].forEach((n, i) =>
    capsule(s, n, 0.6 + i * 1.3, 3.75, 1.15, { fill: C.text1, line: H.accent2, color: C.background1, fontSize: 11, bold: false, charSpacing: 0 }));
  txt(s, 'November 2026', { x: 0.6, y: 4.35, w: 3, h: 0.3, fontSize: 12, color: C.accent3 });
  // team column on the right
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 7.55, y: 0.55, w: 1.95, h: 4.55, rectRadius: 0.975,
    fill: { color: C.text2 }, line: { color: C.text2 }, objectName: 'team capsule' });
  txt(s, 'THE TEAM', { x: 7.55, y: 0.95, w: 1.95, h: 0.3, fontSize: 10, bold: true, charSpacing: 2, color: C.accent1, align: 'center' });
  txt(s, TEAM.map((n, i) => ({ text: n, options: { breakLine: i < TEAM.length - 1 } })),
    { x: 7.65, y: 1.35, w: 1.75, h: 3.3, fontSize: 11, color: C.background1, align: 'center', paraSpaceAfter: 7 });
  s.addNotes('Title slide, on screen before the talk. Group 8: ' + TEAM.join(', ') + '.');

  // ===== 2. Three medicines =====
  pres.addSection({ title: 'The market' });
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'The market' });
  kicker(s, '01', 'The products', TEAM[0]);
  s.addText('Same molecule does not mean same substitute', { placeholder: 'title' });
  const meds = [
    { n: 'Ozempic', m: 'semaglutide', use: 'Adults with type 2 diabetes', ic: I.syringe, fill: C.text2 },
    { n: 'Wegovy', m: 'semaglutide', use: 'Weight management in eligible patients', ic: I.scale, fill: C.accent1 },
    { n: 'Mounjaro', m: 'tirzepatide', use: 'A different molecule, a different product', ic: I.vial, fill: C.accent5 },
  ];
  meds.forEach((d, i) => {
    const x = 0.6 + i * 2.97;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.55, w: 2.75, h: 2.45, rectRadius: 0.12,
      fill: { color: C.background2 }, line: { color: C.background2 }, objectName: d.n + ' card' });
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: x + 0.25, y: 1.8, w: 0.9, h: 0.5, rectRadius: 0.25,
      fill: { color: d.fill }, line: { color: d.fill }, objectName: d.n + ' icon capsule' });
    s.addImage({ data: d.ic, x: x + 0.53, y: 1.88, w: 0.34, h: 0.34, altText: d.n + ' icon' });
    txt(s, d.n, { x: x + 0.25, y: 2.5, w: 2.3, h: 0.45, fontFace: THEME.headFontFace, fontSize: 22, bold: true, color: C.text1 });
    txt(s, d.m, { x: x + 0.25, y: 2.95, w: 2.3, h: 0.3, fontSize: 13, italic: true, color: C.accent5 });
    txt(s, d.use, { x: x + 0.25, y: 3.3, w: 2.3, h: 0.6, fontSize: 13, color: C.text1 });
  });
  // the takeaway
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 4.25, w: 8.8, h: 0.6, rectRadius: 0.3,
    fill: { color: C.text1 }, line: { color: C.text1 }, objectName: 'takeaway capsule' });
  txt(s, [{ text: 'Why it matters:  ', options: { bold: true, color: H.accent1 } },
    { text: 'a patient can only switch to a medicine that suits their condition, so the real number of substitutes is smaller than the shelf suggests.' }],
    { x: 0.9, y: 4.25, w: 8.3, h: 0.6, fontSize: 13, color: C.background1, valign: 'middle' });
  s.addNotes('Presenter: ' + TEAM[0] + '. Ozempic and Wegovy both contain semaglutide, but they are approved for different uses: Ozempic for adults with type 2 diabetes, Wegovy for weight management in eligible patients. Mounjaro contains a different molecule, tirzepatide. This matters for elasticity, because demand is more elastic when there are close substitutes. A patient can only switch to a medicine that is clinically suitable for them, so the number of real substitutes is smaller than the number of products on the shelf.');

  // ===== 3. The decision and prices =====
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'The market' });
  kicker(s, '02', 'The decision', TEAM[1]);
  s.addText('A new option, and a threefold price gap', { placeholder: 'title' });
  capsule(s, '2025', 0.6, 1.6, 0.8, { fill: C.accent1, color: C.background1, fontSize: 12 });
  txt(s, 'SFDA registers Wegovy for weight management', { x: 0.6, y: 2.05, w: 3.3, h: 0.7,
    fontFace: THEME.headFontFace, fontSize: 18, bold: true, color: C.text1 });
  txt(s, 'Another approved option enters the Saudi market.', { x: 0.6, y: 2.8, w: 3.3, h: 0.5, fontSize: 14, color: C.text1 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 3.5, w: 3.3, h: 1.35, rectRadius: 0.1,
    fill: { color: C.background2 }, line: { color: C.background2 }, objectName: 'caveat card' });
  txt(s, [{ text: 'Listed price ≠ price paid', options: { bold: true, breakLine: true } },
    { text: 'These are listed prices for specific products. What a patient pays depends on the prescribed treatment and any coverage.' }],
    { x: 0.8, y: 3.62, w: 2.95, h: 1.15, fontSize: 12, color: C.text1, paraSpaceAfter: 3 });
  s.addChart(pres.charts.BAR, [{ name: 'Listed price (SAR)', labels: ['Ozempic pen', 'Mounjaro KwikPen 2.5 mg'], values: [418.65, 1261.40] }], {
    x: 4.3, y: 1.5, w: 5.1, h: 2.9, barDir: 'bar', chartColors: [H.accent5, H.accent1], varyColors: true,
    showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '"SAR "#,##0.00', dataLabelFontSize: 13,
    dataLabelFontBold: true, dataLabelColor: H.dk1, dataLabelFontFace: '+mn-lt',
    catAxisLabelColor: H.dk1, catAxisLabelFontSize: 12, catAxisLabelFontFace: '+mn-lt', catAxisOrientation: 'maxMin',
    valAxisHidden: true, valAxisMaxVal: 1650, valAxisMinVal: 0, valGridLine: { style: 'none' }, catGridLine: { style: 'none' },
    catAxisLineShow: false, barGapWidthPct: 55, showLegend: false,
    showTitle: true, title: 'SFDA listed price, SAR', titleFontSize: 12, titleColor: H.accent6, titleFontFace: '+mn-lt',
    objectName: 'price chart' });
  capsule(s, '≈ 3.0×  higher listed price for the Mounjaro pen', 4.6, 4.5, 4.5, { fill: C.accent4, color: C.text1, fontSize: 11, charSpacing: 0 });
  s.addNotes('Presenter: ' + TEAM[1] + '. In 2025 the Saudi Food and Drug Authority registered Wegovy for weight management, adding another approved option. The SFDA drug database lists an Ozempic pen at SAR 418.65 and the Mounjaro KwikPen 2.5 mg at SAR 1,261.40, about three times higher. Two cautions: these are listed prices for specific products, and pens differ in strength and number of doses, so this is not a like-for-like monthly cost. What a patient pays depends on the treatment prescribed and on insurance coverage.');

  // ===== 4. Elastic or inelastic =====
  pres.addSection({ title: 'The analysis' });
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'The analysis' });
  kicker(s, '03', 'The concept', TEAM[2]);
  s.addText('Who reacts to price, and who cannot', { placeholder: 'title' });
  // formula capsule
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 1.55, w: 8.8, h: 0.75, rectRadius: 0.375,
    fill: { color: C.text1 }, line: { color: C.text1 }, objectName: 'formula capsule' });
  txt(s, [{ text: 'Price elasticity  =  ', options: { color: H.accent3 } },
    { text: '% change in quantity demanded  ÷  % change in price', options: { bold: true, color: H.lt1 } }],
    { x: 0.95, y: 1.55, w: 8.2, h: 0.75, fontSize: 16, valign: 'middle', fontFace: THEME.headFontFace });
  const cols = [
    { tag: 'ELASTIC  ·  |E| > 1', fill: C.accent1, head: 'Quantity moves more than price',
      items: ['Patients paying out of pocket', 'Can delay starting treatment', 'Have another clinically suitable option'] },
    { tag: 'INELASTIC  ·  |E| < 1', fill: C.text2, head: 'Quantity moves less than price',
      items: ['Patients who rely on one particular medicine', 'Few suitable alternatives', 'Treatment that cannot easily wait'] },
  ];
  cols.forEach((c, i) => {
    const x = 0.6 + i * 4.5;
    capsule(s, c.tag, x, 2.6, 2.2, { fill: c.fill, color: C.background1, fontSize: 11 });
    txt(s, c.head, { x, y: 3.05, w: 4.2, h: 0.4, fontFace: THEME.headFontFace, fontSize: 18, bold: true, color: C.text1 });
    txt(s, c.items.map((t, k) => ({ text: t, options: { bullet: { indent: 14 }, breakLine: k < c.items.length - 1 } })),
      { x, y: 3.5, w: 4.2, h: 1.3, fontSize: 14, color: C.text1, paraSpaceAfter: 5 });
  });
  s.addNotes('Presenter: ' + TEAM[2] + '. Demand is elastic when quantity demanded changes by a larger percentage than price, and inelastic when it changes by a smaller percentage. In this market, patients paying out of pocket may be more price-sensitive if they can delay starting treatment or have another clinically suitable option. Patients who rely on a particular medicine and have few suitable alternatives may be less price-sensitive.');

  // ===== 5. Tabuk evidence — waffle of 105 =====
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'The analysis' });
  kicker(s, '04', 'The evidence', TEAM[3]);
  s.addText('Over half of Tabuk users interrupted treatment', { placeholder: 'title' });
  const COLS = 15, DOT = 0.2, GAP = 0.075, X0 = 0.6, Y0 = 1.75;
  for (let k = 0; k < 105; k++) {
    const r = Math.floor(k / COLS), c = k % COLS;
    const on = k < 57;
    s.addShape(pres.shapes.OVAL, { x: X0 + c * (DOT + GAP), y: Y0 + r * (DOT + GAP), w: DOT, h: DOT,
      fill: { color: on ? C.accent1 : C.accent3 }, line: { color: on ? C.accent1 : C.accent3, width: 0.5 }, objectName: 'respondent ' + (k + 1) });
  }
  txt(s, 'Each dot is one GLP-1 user in the survey (105)', { x: 0.6, y: 3.75, w: 4.2, h: 0.3, fontSize: 11, color: C.accent6 });
  capsule(s, 'Interrupted: 57', 0.6, 4.12, 1.6, { fill: C.accent1, color: C.background1, fontSize: 11 });
  capsule(s, 'Did not: 48', 2.35, 4.12, 1.3, { fill: C.accent3, color: C.text1, fontSize: 11 });
  // stat block
  txt(s, '57', { x: 5.3, y: 1.45, w: 1.6, h: 1.1, fontFace: THEME.headFontFace, fontSize: 66, bold: true, color: C.accent1 });
  txt(s, 'of 105', { x: 6.85, y: 1.95, w: 1.5, h: 0.5, fontFace: THEME.headFontFace, fontSize: 24, color: C.text1 });
  txt(s, 'respondents who had used GLP-1 medicines reported interrupting use', { x: 5.3, y: 2.6, w: 4.1, h: 0.6, fontSize: 14, color: C.text1 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 5.3, y: 3.35, w: 4.1, h: 1.4, rectRadius: 0.1,
    fill: { color: C.background2 }, line: { color: C.background2 }, objectName: 'limit card' });
  txt(s, [{ text: 'The catch', options: { bold: true, color: H.accent1, breakLine: true } },
    { text: 'The study groups shortages and cost into one reason, so it cannot tell us how much is price and how much is supply.' }],
    { x: 5.5, y: 3.47, w: 3.75, h: 1.2, fontSize: 13, color: C.text1, paraSpaceAfter: 3 });
  s.addNotes('Presenter: ' + TEAM[3] + '. A 2024 survey in Tabuk (Frontiers in Pharmacology, 2025) found that 57 of 105 respondents who had used GLP-1 medicines reported interrupting use. The study grouped shortages and cost together as one reason for discontinuation. So affordability and supply both affect whether patients continue treatment, but the survey does not isolate the effect of price.');

  // ===== 6. Verdict =====
  s = pres.addSlide({ masterName: 'DARK', sectionTitle: 'The analysis' });
  kicker(s, '05', 'The verdict', TEAM[4], true);
  s.addText('Price sensitivity is possible, but not proven', { placeholder: 'title' });
  txt(s, 'To actually measure elasticity, we would need:', { x: 0.6, y: 1.5, w: 8.8, h: 0.35, fontSize: 15, color: C.accent3 });
  const steps = [
    { n: '1', h: 'One medicine', b: 'Prescriptions or purchases for the same product' },
    { n: '2', h: 'A price change', b: 'Before-and-after data on the price patients actually pay' },
    { n: '3', h: 'Controls', b: 'Account for shortages and insurance coverage' },
  ];
  steps.forEach((st, i) => {
    const x = 0.6 + i * 3.0;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 2.05, w: 2.75, h: 2.1, rectRadius: 0.12,
      fill: { color: C.text2 }, line: { color: C.text2 }, objectName: 'step ' + st.n });
    capsule(s, st.n, x + 0.25, 2.3, 0.6, { fill: C.accent1, color: C.background1, fontSize: 14, h: 0.36 });
    txt(s, st.h, { x: x + 0.25, y: 2.85, w: 2.3, h: 0.4, fontFace: THEME.headFontFace, fontSize: 18, bold: true, color: C.background1 });
    txt(s, st.b, { x: x + 0.25, y: 3.28, w: 2.3, h: 0.8, fontSize: 13, color: C.accent3 });
    if (i < 2) txt(s, '→', { x: x + 2.75, y: 2.85, w: 0.25, h: 0.4, fontSize: 18, bold: true, color: C.accent1, align: 'center' });
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 4.4, w: 8.8, h: 0.55, rectRadius: 0.275,
    fill: { color: C.accent1 }, line: { color: C.accent1 }, objectName: 'verdict capsule' });
  txt(s, 'Available evidence: elastic or inelastic cannot yet be established', { x: 0.6, y: 4.4, w: 8.8, h: 0.55,
    fontSize: 14, bold: true, color: C.background1, align: 'center', valign: 'middle' });
  s.addNotes('Presenter: ' + TEAM[4] + '. Calculating elasticity would require data on how prescriptions or purchases for the same medicine changed after a price change, while accounting for factors such as shortages and insurance coverage. The available evidence supports price sensitivity as a possibility, but it does not establish whether demand was elastic or inelastic.');

  // ===== 7. Consequences =====
  pres.addSection({ title: 'Implications' });
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Implications' });
  kicker(s, '06', 'The consequences', TEAM[5]);
  s.addText('Paying and finding are different problems', { placeholder: 'title' });
  const who = [
    { ic: I.user, fill: C.accent1, h: 'Patients', b: 'Wegovy gives eligible patients another approved option, yet cost or shortages can still interrupt treatment.' },
    { ic: I.store, fill: C.text2, h: 'Companies and pharmacies', b: 'Forecast on repeat purchases and stock. A fall in refills may be a shortage, a price change, or both.' },
    { ic: I.gov, fill: C.accent5, h: 'Government and insurers', b: 'Track out-of-pocket cost, stock and refill rates separately: each problem needs a different response.' },
  ];
  who.forEach((w, i) => {
    const y = 1.55 + i * 1.15;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y, w: 8.8, h: 0.98, rectRadius: 0.49,
      fill: { color: C.background2 }, line: { color: C.background2 }, objectName: w.h + ' row' });
    s.addShape(pres.shapes.OVAL, { x: 0.75, y: y + 0.14, w: 0.7, h: 0.7, fill: { color: w.fill }, line: { color: w.fill }, objectName: w.h + ' icon disc' });
    s.addImage({ data: w.ic, x: 0.93, y: y + 0.32, w: 0.34, h: 0.34, altText: w.h + ' icon' });
    txt(s, w.h, { x: 1.7, y, w: 2.4, h: 0.98, fontFace: THEME.headFontFace, fontSize: 17, bold: true, color: C.text1, valign: 'middle' });
    txt(s, w.b, { x: 4.15, y, w: 5.0, h: 0.98, fontSize: 13, color: C.text1, valign: 'middle' });
  });
  s.addNotes('Presenter: ' + TEAM[5] + '. Patients: Wegovy’s registration gave eligible patients another approved option, but the Tabuk survey shows that continuing treatment can still be difficult when cost or shortages affect access. Pharmaceutical companies and pharmacies: when forecasting sales, managers should consider whether patients can afford repeat purchases and whether pharmacies can keep the medicine in stock; a fall in refills could reflect a shortage, a change in what patients pay, or both. Government and insurers: tracking out-of-pocket costs, stock availability and refill rates separately would show whether patients are struggling to pay for treatment or to find it. These problems call for different responses.');

  // ===== 8. What has changed since (2026) =====
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Implications' });
  kicker(s, '07', 'What has changed in 2026', TEAM[6]);
  s.addText('The market is gaining substitutes', { placeholder: 'title' });
  const tl = [
    { d: 'FEB 2026', ic: I.pill, h: 'Generic semaglutide', b: 'SFDA approval reported for a generic version of semaglutide (OneSource / Hikma).' },
    { d: 'AUG 2026', ic: I.tag, h: 'An oral option', b: 'SFDA registers Foundayo (orforglipron), a daily pill for weight management.' },
    { d: 'OCT 2026', ic: I.gap, h: 'Saudi prices compared', b: 'Al Eqtisadiah: among five countries, Saudi Arabia had the lowest official prices.' },
  ];
  // the timeline is a single capsule track with three stops
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 1.75, w: 8.8, h: 0.16, rectRadius: 0.08,
    fill: { color: C.accent3 }, line: { color: C.accent3 }, objectName: 'timeline track' });
  tl.forEach((t, i) => {
    const x = 0.6 + i * 3.0;
    capsule(s, t.d, x, 1.58, 1.3, { fill: C.accent1, color: C.background1, fontSize: 11, h: 0.5 });
    s.addShape(pres.shapes.OVAL, { x, y: 2.35, w: 0.55, h: 0.55, fill: { color: C.text2 }, line: { color: C.text2 }, objectName: t.h + ' icon disc' });
    s.addImage({ data: t.ic, x: x + 0.14, y: 2.49, w: 0.27, h: 0.27, altText: t.h + ' icon' });
    txt(s, t.h, { x, y: 3.0, w: 2.7, h: 0.4, fontFace: THEME.headFontFace, fontSize: 17, bold: true, color: C.text1 });
    txt(s, t.b, { x, y: 3.4, w: 2.7, h: 0.85, fontSize: 13, color: C.text1 });
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 4.35, w: 8.8, h: 0.55, rectRadius: 0.275,
    fill: { color: C.text1 }, line: { color: C.text1 }, objectName: 'implication capsule' });
  txt(s, [{ text: 'For elasticity:  ', options: { bold: true, color: H.accent1 } },
    { text: 'more close substitutes should make demand for any single brand more price-sensitive.' }],
    { x: 0.9, y: 4.35, w: 8.3, h: 0.55, fontSize: 13, color: C.background1, valign: 'middle' });
  s.addNotes('Presenter: ' + TEAM[6] + '. Since the report’s evidence was gathered, the market has moved. In February 2026 trade press reported SFDA approval of a generic semaglutide (OneSource with Hikma). On 2 August 2026 the SFDA registered Foundayo, orforglipron, a once-daily oral GLP-1 for weight management. In October 2026 Al Eqtisadiah compared official prices in five countries and found Saudi Arabia the cheapest, with Ozempic at SAR 418.65 and Mounjaro at SAR 1,261.40. For our question: more close substitutes should make demand for any single brand more elastic, even if demand for the class as a whole stays less sensitive.');

  // ===== 9. Conclusion =====
  pres.addSection({ title: 'Close' });
  s = pres.addSlide({ masterName: 'DARK', sectionTitle: 'Close' });
  kicker(s, '08', 'Conclusion', TEAM[6], true);
  s.addText('Three forces shape demand', { placeholder: 'title' });
  ['Price', 'Availability', 'Clinical alternatives'].forEach((t, i) =>
    capsule(s, t, 0.6 + i * 2.35, 1.6, i === 2 ? 2.4 : 2.1, { fill: i === 0 ? C.accent1 : C.text2, color: C.background1, fontSize: 15, h: 0.55, charSpacing: 0 }));
  txt(s, 'To estimate price elasticity, track how purchases of the same medicine respond when the price patients actually pay changes.',
    { x: 0.6, y: 2.55, w: 8.4, h: 1.3, fontFace: THEME.headFontFace, fontSize: 24, color: C.background1 });
  txt(s, 'SFDA listings show prices differ across products. The Tabuk survey documents treatment interruptions. Neither, alone, measures elasticity.',
    { x: 0.6, y: 4.0, w: 8.4, h: 0.7, fontSize: 13, color: C.accent3 });
  s.addNotes('Presenter: ' + TEAM[6] + '. The Saudi case shows why price, availability and clinical alternatives all matter when analysing demand for prescription medicines. The SFDA listings show that prices differ across products, and the Tabuk survey documents treatment interruptions. To estimate price elasticity, managers and policymakers would need to track how purchases of the same medicine respond when the price patients actually pay changes. Thank you; we welcome your questions.');

  // ===== 10. Sources =====
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Close' });
  s.addText('REFERENCES', { x: 0.6, y: 0.2, w: 4, h: 0.3, fontSize: 10, bold: true, charSpacing: 2, color: C.accent5, valign: 'middle', margin: 0, isTextBox: true });
  s.addText('Sources', { placeholder: 'title' });
  const src = [
    ['SFDA — semaglutide indications (DHPC, Sep 2026)', 'https://www.sfda.gov.sa/sites/default/files/2026-09/DHPC-NAION_SFDA%20%28Sep2026%29.pdf'],
    ['SFDA — drug approvals, Feb–Mar 2025 (Wegovy)', 'https://www.sfda.gov.sa/system/files/2025/SFDA-DrugApprovalsFeb-Mar.pdf'],
    ['SFDA drug database — Ozempic price listing', 'https://www.sfda.gov.sa/en/details_data?id=2701200003&nid=17582'],
    ['SFDA drug database — Mounjaro registration and price', 'https://www.sfda.gov.sa/en/details_data?id=1208245747&nid=17582&page=0'],
    ['Tabuk GLP-1 survey, Frontiers in Pharmacology (2025), Table 2', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12350480/#T2'],
    ['SFDA — Foundayo (orforglipron) registration, Aug 2026', 'https://www.sfda.gov.sa/en/news/5522078'],
    ['Generic semaglutide SFDA approval (BioSpectrum Asia)', 'https://www.biospectrumasia.com/news/123/27194/onesource-hikma-partnership-secures-approval-to-commercialise-generic-version-of-ozempic-in-saudi-arabia.html'],
    ['Al Eqtisadiah — obesity drug prices in five countries (Oct 2026)', 'https://www.aleqt.com/تقارير-وتحليلات/أدوية-السمنة-في-5-دول-السعودية-الأرخص-وأمريكا-أغلى-ب377-13102'],
  ];
  txt(s, src.map(([t, u], i) => ({ text: t, options: { hyperlink: { url: u }, color: H.dk2, bullet: { indent: 14 }, breakLine: i < src.length - 1 } })),
    { x: 0.6, y: 1.5, w: 8.8, h: 3.4, fontSize: 13, paraSpaceAfter: 6 });
  s.addNotes('References slide. Each line is a clickable link.');

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log('wrote', OUT);
})();
