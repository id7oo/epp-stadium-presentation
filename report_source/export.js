// Flattened export: every page's artwork (panels, shadows, glows, photo fades, charts) is baked into one
// image, and the text is laid on top as live vector text. No PDF transparency effects remain, so the file
// looks the same in every viewer, while text stays selectable/searchable and links keep working.
// usage: node export.js  ->  writes flat/bg_NN.jpg and flat/text.pdf; then run: python3 flatten.py out.pdf
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const SCALE = 2.5;          // 794 css px * 2.5 = 1985 px across A4, about 240 dpi
const BAKE = `
  html.bake *, html.bake *::before, html.bake *::after { color: transparent !important; -webkit-text-fill-color: transparent !important; text-shadow: none !important; }
  html.bake svg text { fill: transparent !important; }`;
const TEXT = `
  html.textonly *, html.textonly *::before, html.textonly *::after { background: none !important; background-image: none !important;
    border-color: transparent !important; box-shadow: none !important; -webkit-mask-image: none !important; mask-image: none !important;
    filter: none !important; outline: none !important; }
  html.textonly, html.textonly body { background: none !important; }
  html.textonly img { visibility: hidden !important; }
  html.textonly svg * { visibility: hidden !important; }
  html.textonly svg text { visibility: visible !important; }`;

(async () => {
  const out = path.join(__dirname, 'flat');
  fs.mkdirSync(out, { recursive: true });
  const url = 'file://' + path.resolve(__dirname, 'report.html');
  const browser = await chromium.launch();

  // 1. artwork without text, one high-resolution image per page
  const ctx = await browser.newContext({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: SCALE });
  const page = await ctx.newPage();
  await page.emulateMedia({ media: 'print' });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.addStyleTag({ content: BAKE });
  await page.evaluate(() => document.documentElement.classList.add('bake'));
  const pages = await page.$$('.page');
  for (let i = 0; i < pages.length; i++) {
    await pages[i].screenshot({ path: path.join(out, `bg_${String(i + 1).padStart(2, '0')}.jpg`), type: 'jpeg', quality: 84 });
  }

  // 2. text only, as vector PDF on a transparent page
  const tp = await browser.newPage();
  await tp.goto(url, { waitUntil: 'networkidle' });
  await tp.evaluate(() => document.fonts.ready);
  await tp.addStyleTag({ content: TEXT });
  await tp.evaluate(() => document.documentElement.classList.add('textonly'));
  await tp.pdf({ path: path.join(out, 'text.pdf'), width: '210mm', height: '297mm', printBackground: false, preferCSSPageSize: true });
  console.log('pages:', pages.length);
  await browser.close();
})();
