// Render report.html to an A4 PDF, report overflow per page, optionally write PNG previews.
// usage: node render.js out.pdf [--png dir] [--pages 3,4]
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const out = process.argv[2] || 'report.pdf';
  const pngDir = process.argv.includes('--png') ? process.argv[process.argv.indexOf('--png') + 1] : null;
  const only = process.argv.includes('--pages') ? process.argv[process.argv.indexOf('--pages') + 1].split(',').map(Number) : null;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(__dirname, 'report.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const rep = await page.evaluate(() => {
    const mm = 96 / 25.4, res = [];
    document.querySelectorAll('.page').forEach((pg, i) => {
      const b = pg.querySelector('.body'); if (!b) { res.push({ i: i + 1, ok: true, free: null }); return; }
      const br = b.getBoundingClientRect();
      let maxB = br.top;
      b.querySelectorAll('*').forEach((el) => { const r = el.getBoundingClientRect(); if (r.height > 0 && r.bottom > maxB) maxB = r.bottom; });
      const over = b.scrollHeight - b.clientHeight; let sp = 0; b.querySelectorAll('.sp').forEach((s) => { sp += s.getBoundingClientRect().height; });
      // text spilling sideways out of a panel
      const wide = [];
      b.querySelectorAll('.gl, .tag, .eb, .rail').forEach((el) => { if (el.scrollWidth > el.clientWidth + 1) wide.push(el.className + ':' + (el.textContent || '').slice(0, 30)); });
      res.push({ i: i + 1, over: +(over / mm).toFixed(1), free: +((br.bottom - maxB + sp) / mm).toFixed(1), wide });
    });
    return res;
  });
  rep.forEach((r) => console.log(`p${String(r.i).padStart(2, '0')}  ${r.over > 0 ? 'OVERFLOW ' + r.over + 'mm' : 'ok'}  free ${r.free}mm ${r.wide && r.wide.length ? ' WIDE ' + r.wide.join(' | ') : ''}`));
  await page.pdf({ path: out, width: '210mm', height: '297mm', printBackground: true, preferCSSPageSize: true });
  if (pngDir) {
    fs.mkdirSync(pngDir, { recursive: true });
    const n = await page.evaluate(() => document.querySelectorAll('.page').length);
    for (let i = 0; i < n; i++) {
      if (only && !only.includes(i + 1)) continue;
      const el = (await page.$$('.page'))[i];
      await el.screenshot({ path: path.join(pngDir, `p${String(i + 1).padStart(2, '0')}.png`) });
    }
  }
  await browser.close();
})();
