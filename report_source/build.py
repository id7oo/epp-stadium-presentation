"""Build report.html (A4, King Salman Night Glass) from the Group 8 EPP report text."""
import os
import charts as C

HERE = os.path.dirname(os.path.abspath(__file__))
RUN_L = 'Group 8 <span style="opacity:.5">·</span> Economic participation in stadium construction'
PAGES = []          # (html, meta)
SECTION_START = {}


def c(s): return f'<span class="c">[{s}]</span>'


RAIL = [('SAR 4.5bn', 'scenario'), ('SAR 2,143m', 'purchases'), ('SAR 421.6m', 'the leak'), ('SAR 177m', 'chem + metals'),
        ('SAR 84.32m', 'EP obligation'), ('SAR 44.24m', 'Saudi buying'), ('SAR 36.14m', 'activity')]


def rail(on):
    parts = ['<div class="rail"><span class="rl">Follow the riyal</span>']
    for i, (v, k) in enumerate(RAIL):
        cls = 'st'
        if i <= max(on): cls += ' lit'
        if i in on: cls += ' on' + (' o' if i == 2 else '')
        parts.append(f'<span class="{cls}"><b>{v}</b><i>{k}</i></span>')
    parts.append('</div>')
    return ''.join(parts)


def spread(body):
    import re
    out, prev = [], None
    for ln in body.split('\n'):
        if re.match(r'<(h2|div|p|svg)\b', ln):
            kind = 'head' if ln.startswith(('<h2', '<div class="k', '<div class="cont-title')) else ('p' if ln.startswith('<p') else 'blk')
            if prev is not None and prev != 'head' and not (prev == 'p' and kind == 'p') and not ln.startswith('<div class="grow'):
                out.append('<i class="sp"></i>')
            prev = kind
        out.append(ln)
    return '\n'.join(out)


def page(body, sec='', bg='a', banner=None, rail_on=None, cls='', spread_on=True):
    n = len(PAGES) + 1
    if spread_on:
        body = spread(body)
    foot_l = rail(rail_on) if rail_on else '<span>Building King Salman Stadium <span style="opacity:.5">·</span> MBSC EMBA <span style="opacity:.5">·</span> ECN 511</span>'
    ban = ''
    if banner:
        img, no, title, stand = banner
        ban = (f'<div class="banner" style="background-image:url(img/{img}.jpg)"></div>'
               f'<div class="btitle"><div class="no"><b>{no}</b><span>Section</span></div><h1>{title}</h1><div class="stand">{stand}</div></div>')
    html = (f'<section class="page bg-{bg} {"has-banner" if banner else ""} {cls}">'
            f'<div class="run"><span><span class="dot"></span>{RUN_L}</span><span><b>{sec}</b></span></div>'
            f'{ban}<div class="body">{body}</div>'
            f'<div class="foot">{foot_l}<span class="pn">{n:02d}</span></div></section>')
    PAGES.append(html)
    return n


def contd(no, title):
    return f'<div class="cont-title"><b>{no}</b><h1>{title} <span>continued</span></h1></div>'


# ════════════════════════════════════════════════════════════════════════════
# COVER
# ════════════════════════════════════════════════════════════════════════════
TEAM = [('Abdulmajeed Alajlan', 'AA', '#22D38B'), ('Abdulrahman Aldahlawi', 'AD', '#2BC2CF'), ('Salman Alfaris', 'SA', '#4A95F0'),
        ('Mohammed Alghamdi', 'MA', '#E2B357'), ('Abdulaziz Alweheab', 'AW', '#EE6A33'), ('Nada Alyahya', 'NA', '#EE6A95'),
        ('Haifa Binnafisah', 'HB', '#C77BDB')]

COVER = f'''
<section class="page cover" style="background:#04090B">
  <div style="position:absolute;left:0;top:0;width:210mm;height:192mm;background:url(img/cover.jpg) center/cover;
       -webkit-mask-image:linear-gradient(180deg,#000 55%,rgba(0,0,0,.6) 78%,transparent);"></div>
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,9,11,.72) 0%,rgba(4,9,11,.1) 22%,rgba(4,9,11,0) 45%),
       radial-gradient(120mm 90mm at 80% 92%,rgba(20,110,75,.28),transparent 70%)"></div>
  <div style="position:absolute;left:16mm;top:13mm;right:16mm;display:flex;justify-content:space-between;align-items:center">
    <img src="img/mbsc_logo_dark.svg" style="height:15mm">
    <span class="eb">MBSC Executive MBA · ECN 511 Economics for Managers</span>
  </div>
  <div class="gl" style="position:absolute;left:16mm;right:16mm;top:124mm;padding:9mm 10mm 8mm;background:linear-gradient(158deg,rgba(255,255,255,.12),rgba(255,255,255,.03) 36%,rgba(255,255,255,.01)),rgba(10,24,22,.62);border-color:rgba(255,255,255,.16)">
    <span class="eb">Group report · Construction and Infrastructure · Topic B</span>
    <div style="font-size:31pt;font-weight:800;line-height:1.03;color:var(--fg);letter-spacing:-.022em;margin:5mm 0 3.6mm">
      Economic Participation in <span class="green">Saudi Stadium Construction</span></div>
    <div style="font-size:12.5pt;font-weight:500;color:var(--fg2);line-height:1.4">A practical playbook using the King Salman Stadium case</div>
    <div class="hr" style="margin:6mm 0 5mm"></div>
    <div style="display:grid;grid-template-columns:1fr auto 1fr auto 1fr;align-items:center;gap:3mm">
      <div><div class="v l">SAR 4.5bn</div><div class="kv">stadium scenario, a teaching assumption</div></div>
      <div class="arrow" style="font-size:14pt">→</div>
      <div><div class="v l" style="color:#FF8A57">SAR 421.6m</div><div class="kv">imported intermediate inputs, estimated</div></div>
      <div class="arrow" style="font-size:14pt">→</div>
      <div><div class="v l gold">SAR 84.32m</div><div class="kv">EP obligation at the 20% draft rate</div></div>
    </div>
  </div>
  <div style="position:absolute;left:16mm;right:16mm;bottom:15mm;display:flex;justify-content:space-between;align-items:flex-end">
    <div>
      <div class="k" style="letter-spacing:.32em">Group 8</div>
      <div style="display:flex;flex-wrap:wrap;gap:1.6mm 4mm;max-width:128mm;font-size:8pt;color:var(--fg2)">
        {''.join(f'<span style="display:inline-flex;align-items:center;gap:1.4mm"><i style="width:1.6mm;height:1.6mm;border-radius:50%;background:{col}"></i>{n}</span>' for n, _, col in TEAM)}
      </div>
    </div>
    <div style="text-align:right">
      <div style="font-size:15pt;font-weight:800;color:var(--fg);letter-spacing:-.01em">15 November 2026</div>
      <div class="xs fg3">MBSC Executive MBA</div>
    </div>
  </div>
  <div class="src" style="position:absolute;left:16mm;bottom:7mm;font-size:5.4pt">Cover image: King Salman Stadium concept rendering © Populous</div>
</section>'''
PAGES.append(COVER)

# ════════════════════════════════════════════════════════════════════════════
# CONTENTS (page numbers filled in after the build)
# ════════════════════════════════════════════════════════════════════════════
CONTENTS_IDX = len(PAGES)
PAGES.append(None)

# ════════════════════════════════════════════════════════════════════════════
# 1 SECTOR AT A GLANCE
# ════════════════════════════════════════════════════════════════════════════
SECTION_START[1] = len(PAGES) + 1
page(f'''
<p class="lead mb3">Lasting domestic capability can be embedded in Saudi stadium procurement when economic participation commitments focus on
imported materials and specialist services that Saudi firms can supply competitively. We recommend a shared <span class="green">Materials and Systems
Academy</span> programme, initially delivered through existing facilities and live construction sites. Each participating supplier would retain
responsibility for its approved obligations and evidence of delivery.</p>

<div class="g3 mb3">
  <div class="gl"><div class="k">Construction GVA · 2023</div><div class="v"><small>SAR</small>338.3bn</div><div class="kv">of gross value added generated by Saudi construction</div></div>
  <div class="gl green"><div class="k g">Share of the economy</div><div class="v green">7.8%</div>
    <div class="bar mt1" style="height:2mm"><i style="width:7.8%;background:var(--green)"></i></div>
    <div class="kv">of Saudi gross value added</div></div>
  <div class="gl"><div class="k">King Salman Stadium</div><div class="v">92,760</div><div class="kv">planned seats in FIFA’s 2024 bid evaluation</div></div>
</div>

<p class="mb3">Saudi Arabia’s construction sector generated SAR 338.3 billion of gross value added in 2023, equivalent to 7.8% of Saudi gross value
added. King Salman International Stadium, with 92,760 planned seats in FIFA’s 2024 bid evaluation, provides the case examined here. Demand for its
building systems, materials and technical expertise creates opportunities to develop suppliers and licensed technical services. {c('1–3')}</p>

<div class="gl" style="padding:4.5mm 5mm">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3.5mm">
    <span class="eb">From scenario to obligation</span><span class="xs fg3">squares drawn to scale by value</span></div>
  <div style="display:grid;grid-template-columns:1.4fr auto 1fr auto 1fr;gap:3mm;align-items:end">
    <div style="display:flex;gap:3.5mm;align-items:flex-end">
      <div style="width:30mm;height:30mm;border-radius:1.8mm;background:linear-gradient(135deg,rgba(180,197,194,.38),rgba(180,197,194,.10));border:.3mm solid rgba(255,255,255,.25);flex:none;position:relative">
        <div style="position:absolute;right:0;bottom:0;width:9.2mm;height:9.2mm;border-radius:1mm;border:.3mm dashed rgba(238,106,51,.8)"></div></div>
      <div><div class="v m" style="white-space:nowrap">SAR 4.5bn</div><div class="kv">stadium scenario</div></div></div>
    <div class="arrow" style="padding-bottom:5mm">→</div>
    <div style="display:flex;gap:3mm;align-items:flex-end">
      <div style="width:9.2mm;height:9.2mm;border-radius:1mm;background:var(--imp);box-shadow:0 0 3mm rgba(238,106,51,.6);flex:none"></div>
      <div><div class="v m" style="color:#FF8A57">SAR 421.6m</div><div class="kv">imported intermediate inputs</div></div></div>
    <div style="padding-bottom:5mm;text-align:center"><span class="tag y">× 20%</span></div>
    <div style="display:flex;gap:3mm;align-items:flex-end">
      <div style="width:4.1mm;height:4.1mm;border-radius:.6mm;background:var(--gold);box-shadow:0 0 2.4mm rgba(226,179,87,.7);flex:none"></div>
      <div><div class="v m gold">SAR 84.32m</div><div class="kv">EP obligations</div></div></div>
  </div>
</div>

<p class="mt3">For this scenario, we assume a stadium value of SAR 4.5 billion, which implies an estimated SAR 421.6 million of imported
intermediate inputs. The presentation also assumes that one eligible foreign supplier accounts for the full import base. Applying the draft’s 20%
obligation rate for this import band therefore produces SAR 84.32 million of EP obligations. <strong>The stadium value is a teaching
assumption;</strong> actual eligibility depends on the tender’s supplier structure and documented imported goods and services. {c('1, 2, 4')}</p>
''', sec='01 · Sector at a glance', bg='a', rail_on=[0, 2, 4],
     banner=('ban_1', '01', 'Sector at a <em>glance</em>', 'A World Cup stadium is a construction job in a sector worth 7.8% of the Saudi economy. Its imports are where the money leaks, and where capability can be built.'))

PRI = [('Establish eligibility before pricing.', 'Map imported packages to foreign suppliers, confirm the applicable policy and obtain an approved obligation calculation.', 'Eligibility'),
       ('Approve a staged shared programme.', 'Combine licensed systems training with qualification of Saudi materials, starting with paid placements and confirmed orders across two eligible sites.', 'Programme'),
       ('Award credit against additional, verifiable capability.', 'Agree the activity baseline, rights, valuation factors and evidence before investment, then measure sustained employment and repeat orders.', 'Credit')]
pri_html = ''.join(f'''
  <div class="gl {'green' if i == 1 else ''}" style="padding:5mm 5mm 5mm;display:flex;flex-direction:column">
    <div style="display:flex;justify-content:space-between;align-items:flex-start">
      <div style="font-size:30pt;font-weight:300;line-height:.9;color:var(--gold)">0{i + 1}</div><span class="tag {'g' if i == 1 else 'y'}">{t}</span></div>
    <div style="font-size:10.5pt;font-weight:800;line-height:1.25;color:var(--fg);margin:4mm 0 2mm">{a}</div>
    <div class="sm">{b}</div></div>''' for i, (a, b, t) in enumerate(PRI))

TL = [('Preceding framework', 'SAR 100m import threshold, 35% obligation', 'm'),
      ('14 April 2026', 'Consultation on the policy update announced in Umm Al-Qura', 'y'),
      ('22 April 2026', 'Consultation closed', 'y'),
      ('15 November 2026', 'Official Arabic text of the April draft accessed for this report', 'g'),
      ('Before implementation', 'Confirm contract-specific commencement and transition provisions', 'o')]
tl_html = ''.join(f'''<div style="position:relative;padding-left:6mm;margin-bottom:{0 if i == len(TL) - 1 else 3.2}mm">
  <i style="position:absolute;left:0;top:1mm;width:2.6mm;height:2.6mm;border-radius:50%;background:{ {'m': '#7F928F', 'y': '#E2B357', 'g': '#22D38B', 'o': '#EE6A33'}[k] };box-shadow:0 0 2mm {'rgba(226,179,87,.5)' if k == 'y' else 'transparent'}"></i>
  <div style="font-size:7.6pt;font-weight:800;color:var(--fg)">{d}</div><div class="xs">{t}</div></div>''' for i, (d, t, k) in enumerate(TL))

team_html = ''.join(f'''<div style="display:flex;flex-direction:column;align-items:center;text-align:center;gap:1.6mm">
  <div style="width:11mm;height:11mm;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:8pt;font-weight:800;color:{col};
    border:.4mm solid {col};background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.14),rgba(255,255,255,.02));box-shadow:0 0 3.5mm {col}55">{ini}</div>
  <div style="font-size:7pt;font-weight:700;color:var(--fg);line-height:1.2">{n.split()[0]}<br><span style="font-weight:500;color:var(--fg3)">{n.split()[1]}</span></div></div>''' for n, ini, col in TEAM)

page(f'''
{contd('01', 'Sector at a glance')}
<h2>Our three priorities</h2>
<div class="g3 mb3" style="grid-auto-rows:1fr">{pri_html}</div>

<div class="sm2 mb3">
  <div class="gl dark" style="padding:5mm">
    <div class="k">Policy basis · timeline</div>
    <div class="mt1">{tl_html}</div>
  </div>
  <div>
    <h2>Policy basis</h2>
    <p>This report analyses LCGPA’s April 2026 consultation draft, using the official Arabic text accessed on 15 November 2026, and compares it with
    the preceding framework. The consultation notice confirms the draft’s consultation history. Contract-specific commencement and transition
    provisions require confirmation before implementation. {c('4–6')}</p>
    <div class="gl gold tight mt2" style="display:flex;gap:3mm;align-items:center">
      <div class="v m gold" style="flex:none">120 days</div>
      <div class="xs">Article 19 provides for effectiveness 120 days after publication, while Article 4 preserves obligations under the rules that applied when they arose. {c('4')}</div>
    </div>
  </div>
</div>

<div class="gl" style="padding:5mm 5mm 5.5mm">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4.5mm">
    <span class="eb">Prepared by · Group 8</span><span class="xs fg3">MBSC Executive MBA · ECN 511 Economics for Managers</span></div>
  <div style="display:grid;grid-template-columns:repeat(7,1fr);gap:2mm">{team_html}</div>
  <div class="hr"></div>
  <p class="sm mb0">Prepared by Abdulmajeed Alajlan, Abdulrahman Aldahlawi, Salman Alfaris, Mohammed Alghamdi, Abdulaziz Alweheab, Nada Alyahya and
  Haifa Binnafisah. <strong>The analysis and recommendations express the group’s views, independently of DGA and LCGPA.</strong></p>
</div>
''', sec='01 · Sector at a glance', bg='b')

# ════════════════════════════════════════════════════════════════════════════
# 2 THE CURRENT SCENARIO
# ════════════════════════════════════════════════════════════════════════════
SECTION_START[2] = len(PAGES) + 1
CHAIN = [('Public buyer', 'procures the stadium'), ('Main contractor or JV', 'delivers the main works'),
         ('Specialist subcontractors', 'systems, façade, fit-out'), ('Equipment manufacturers', 'plant, controls, components')]
chain_html = ''
for i, (a, b) in enumerate(CHAIN):
    chain_html += f'''<div class="gl tight" style="flex:1;text-align:center;padding:3mm 2mm"><div class="num" style="margin:0 auto 1.6mm">{i + 1}</div>
      <div style="font-size:7.8pt;font-weight:800;color:var(--fg);line-height:1.2">{a}</div><div class="xs fg3">{b}</div></div>'''
    if i < 3:
        chain_html += '<div class="arrow" style="align-self:center;font-size:10pt">→</div>'

page(f'''
<h2>Procurement exposure and existing activity</h2>
<p>The stadium supply chain includes a public buyer, a main contractor or joint venture, specialist subcontractors and equipment manufacturers.
Imported exposure can arise in mechanical and electrical systems, façade components, control software, commissioning and foreign engineering services.
Local invoicing alone does not establish domestic origin. The draft’s definitions cover foreign services delivered through locally established
companies as well as direct imports. {c('4, Articles 1 and 3')}</p>

<div class="gl dark mt1 mb3" style="padding:4.5mm">
  <div style="display:flex;gap:2mm">{chain_html}</div>
  <div style="display:flex;align-items:center;gap:2.5mm;margin-top:3.5mm;flex-wrap:wrap">
    <span class="k o mb0" style="margin:0">Where imported exposure arises</span>
    <span class="tag o">Mechanical and electrical systems</span><span class="tag o">Façade components</span><span class="tag o">Control software</span>
    <span class="tag o">Commissioning</span><span class="tag o">Foreign engineering services</span>
  </div>
  <div class="xs mt1" style="color:#FFB08C">Local invoicing alone does not establish domestic origin.</div>
</div>

<div class="ms">
  <div>
    <p>The preceding LCGPA framework applies a SAR 100 million import threshold and a 35% obligation. Its training guidance describes direct
    foreign procurement and qualifying foreign subcontracts beneath local contractors. DGA reports that practical implementation has involved tender
    undertakings, EP proposals, negotiation of qualifying projects and performance security. This makes the actual procurement documents essential to
    assessing exposure. {c('5, pp. 4–5 and 12; 7, pp. 3–4')}</p>
    <p>The April draft lowers the single-tender threshold to SAR 75 million of imports from one foreign company, excluding VAT. Companies under one
    ultimate owner are treated together. The SAR 100 million cumulative threshold over two consecutive calendar years applies to unified purchasing.
    LCGPA may extend cumulative treatment to specified direct or agency purchases with one year’s prior notice. Framework purchase orders count as
    main contracts. {c('4, Articles 1 and 6')}</p>
  </div>
  <div style="display:flex;flex-direction:column;gap:3mm">
    <div class="gl tight" style="padding:3.6mm 4mm">
      <div class="k m">Preceding framework</div>
      <div style="display:flex;gap:5mm"><div><div class="v m">SAR 100m</div><div class="xs">import threshold</div></div>
      <div><div class="v m">35%</div><div class="xs">obligation</div></div></div>
    </div>
    <div class="gl gold tight" style="padding:3.6mm 4mm">
      <div class="k">April 2026 draft</div>
      <div style="display:flex;gap:5mm"><div><div class="v m gold">SAR 75m</div><div class="xs">single-tender threshold, one foreign company, excl. VAT</div></div>
      <div><div class="v m gold" style="white-space:nowrap">25–15%</div><div class="xs">banded obligation rate</div></div></div>
      <div class="hr" style="margin:2.4mm 0"></div>
      <div class="li"><span class="d"></span><span class="xs">One ultimate owner counts as one company</span></div>
      <div class="li"><span class="d"></span><span class="xs"><b>SAR 100m</b> cumulative over two consecutive calendar years for unified purchasing</span></div>
      <div class="li"><span class="d"></span><span class="xs">Framework purchase orders count as main contracts</span></div>
    </div>
  </div>
</div>
''', sec='02 · The current scenario', bg='c',
     banner=('ban_2', '02', 'The current <em>scenario</em>', 'Who buys, who supplies and where imports enter the stadium supply chain, then how an import base becomes an EP obligation.'))

SIT = [('Foreign contractor with an imported stadium package', 'Identify covered imports from the relevant foreign company and test the tender threshold.'),
       ('Saudi main contractor using foreign specialists', 'Trace each foreign supplier and subcontract. Include approved compliance duties in the subcontract.'),
       ('Several venues buying through a unified arrangement', 'Test the cumulative threshold and common ownership. Maintain a register of purchase orders.'),
       ('A state-owned company buying for its own project', 'Confirm its applicable procurement regime and EPP terms. Ownership alone does not establish coverage.')]
sit_html = ''.join(f'''<div class="gl tight" style="padding:3.4mm 4mm;display:grid;grid-template-columns:auto 1fr;gap:1mm 3mm">
   <div class="num" style="grid-row:span 2">{i + 1}</div>
   <div style="font-size:7.9pt;font-weight:800;color:var(--fg);line-height:1.25">{a}</div>
   <div class="xs"><span class="green" style="font-weight:800">→ </span>{b}</div></div>''' for i, (a, b) in enumerate(SIT))

SUP = [('ALUPCO', 'Aluminium', 'Saudi aluminium extrusion, die-making and finishing capabilities.', '8'),
       ('Sika', 'Construction chemicals', 'A 2018 announcement documents concrete-admixture manufacturing in Dammam.', '9'),
       ('NITI', 'Industrial training', 'Industrial training and customised programmes relevant to construction.', '10')]
sup_html = ''.join(f'''<div class="gl tight" style="padding:3.6mm 4mm"><div style="display:flex;justify-content:space-between;align-items:center">
   <div style="font-size:11pt;font-weight:800;color:var(--fg);letter-spacing:-.01em">{a}</div><span class="tag g">{b}</span></div>
   <div class="xs mt1">{t} {c(r)}</div></div>''' for a, b, t, r in SUP)

page(f'''
<div class="k">Practical EPP assessment by procurement situation</div>
<div class="g2 mb3" style="gap:3mm">{sit_html}</div>

<div class="gl dark mb3" style="padding:4.5mm 5mm 4mm">{C.stadiums()}
  <div class="src mt1">Awarded values are approximate and owner-procured; the King Salman figure is the group’s scenario. Sources: {c('20–23')}</div></div>

<p>King Salman Stadium’s budget is unpublished and its main works are unawarded, so two awarded Saudi stadiums anchor our SAR 4.5 billion scenario.
Qiddiya’s 45,000-seat stadium went to an FCC–Nesma joint venture for about SAR 4.0 billion, with mechanical (SAR 829 million) and façade
(SAR 997 million excluding VAT) packages awarded separately. Aramco’s 46,096-seat Al Khobar stadium went to BESIX–Albawani for about SAR 3.7 billion.
<strong>Both owners procured directly, so these show market structure and cost rather than EPP coverage.</strong> DGA distinguishes government EPP
procurement from state-owned localisation programmes, while the draft includes companies purchasing on behalf of government entities.
{c('4, Article 3; 7, p. 3; 20–23')}</p>

<h2 class="mt2">What Saudi suppliers already provide</h2>
<div class="g3 mb2" style="gap:3mm">{sup_html}</div>
<div class="sm2" style="gap:5mm">
  <div class="gl imp tight" style="padding:3.4mm 4mm"><div class="k o">Still requires supplier assessment</div>
    <div class="chip-row"><span class="tag o">Technical grades</span><span class="tag o">Available capacity</span><span class="tag o">Commercial terms</span><span class="tag o">Willingness to participate</span></div></div>
  <div><p>These sources establish potential capabilities. Technical grades, available capacity, commercial terms and willingness to participate still
  require supplier assessment. {c('8–10')}</p>
  <p>The public documents reviewed confirm procurement and production activity but provide little information about approved, stadium-specific
  EP agreements. We therefore propose the academy as a new programme, subject to formal supplier commitments and LCGPA approval.</p></div>
</div>
''', sec='02 · The current scenario', bg='a')

page(f'''
{contd('02', 'The current scenario')}
<h2>From imported packages to EP obligations</h2>
<p>We reproduced the presentation’s estimate using GASTAT’s 2023 supply-and-use tables. Construction output was SAR 645.816 billion and
intermediate consumption SAR 307.541 billion. For each product, we multiplied construction purchases by imports divided by national supply at basic
prices. Summing the estimates gives SAR 60.507 billion, or 19.67% of intermediate purchases. Applying these ratios to SAR 4.5 billion gives
SAR 2,142.9 million of purchases and SAR 421.6 million of estimated imports. {c('1, 2')}</p>

<div class="gl dark mt1 mb3" style="padding:4.5mm 5mm">{C.gastat()}</div>

<div class="ms" style="gap:5mm">
  <div class="gl dark" style="padding:4mm 4.5mm">
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:2.5mm">
      <div class="k mb0">Estimated stadium imports, SAR million</div><div class="xs fg3">total 421.6</div></div>
    {C.imports_chart(98)}
    <div class="src mt1">Group calculation from GASTAT 2023 supply-and-use tables; values rounded; examples are illustrative. {c('1, 2')}</div>
  </div>
  <div>
    <div class="gl imp" style="padding:4mm">
      <div class="k o">The two largest import groups</div>
      <div class="v l" style="color:#FF8A57">SAR 176.97m</div>
      <div class="kv"><b>42%</b> of estimated imports</div>
      <div class="hr" style="background:linear-gradient(90deg,rgba(238,106,51,.7),transparent)"></div>
      <div style="display:flex;justify-content:space-between"><span class="xs">Other chemical products</span><b class="xs">≈ SAR 94m</b></div>
      <div style="display:flex;justify-content:space-between"><span class="xs">Basic metals</span><b class="xs">≈ SAR 83m</b></div>
    </div>
    <p class="mt2 sm">The two largest modelled import groups are other chemical products, such as paints, coatings, sealants and adhesives (about
    SAR 94 million), and basic metals, such as steel, aluminium and copper (about SAR 83 million), together SAR 176.97 million, or 42% of
    estimated imports.</p>
  </div>
</div>

<div class="gl imp mt3" style="padding:3.8mm 4.5mm;display:grid;grid-template-columns:auto 1fr;gap:4mm;align-items:start">
  <span class="eb o">Screening estimate</span>
  <p class="sm mb0">This method assumes construction uses the national import mix within each product category. It also combines the use table’s
  purchaser-price values with supply-table import ratios. It is a screening estimate. <strong>An EPP calculation needs contractual import values
  excluding VAT, including relevant imported services, and attribution to the correct supplier.</strong> A stadium’s specialised equipment mix may
  materially change the result.</p>
</div>
''', sec='02 · The current scenario', bg='d', rail_on=[1, 2, 3])

page(f'''
<div class="ms" style="gap:5mm">
  <div class="gl dark" style="padding:4mm 4.5mm">
    <div class="k">Draft single-tender obligation rate by import band</div>
    {C.tiers(100)}
  </div>
  <div style="display:flex;flex-direction:column;gap:3mm">
    <div class="gl gold" style="padding:4mm">
      <div class="k">Our illustration</div>
      <div style="font-size:9pt;font-weight:700;color:var(--fg2)">SAR 421.61m × 20%</div>
      <div class="v l gold" style="margin-top:1mm">= SAR 84.32m</div>
      <div class="kv">EP obligation, applying the band rate to the entire import base</div>
    </div>
    <div class="gl tight" style="padding:3.6mm 4mm">{C.obligation_compare(58)}</div>
  </div>
</div>

<p class="mt3">For continuity with the presentation, our illustration applies the relevant band rate to the entire import base. Thus
SAR 421.61 million × 20% = SAR 84.32 million. <strong>Obtain LCGPA’s written confirmation of the tier calculation, including whether bands apply
incrementally, before using it in a bid.</strong> Under a 35% preceding-policy scenario, the same base implies SAR 147.56 million.
{c('4, Article 7; 5')}</p>


<h2>Categories most relevant to stadium suppliers</h2>
<div class="gl dark mb3" style="padding:4.5mm 5mm 4mm">{C.factor_chart(168)}</div>

<p>LCGPA sets each factor according to the project’s contribution. Article 9 describes category-specific criteria and potential bonuses of 1–2
for qualifying scarce capabilities, priority regions or an SME beneficiary. <strong>Our proposal assumes ordinary category factors and requests no
bonus.</strong> EP credit measures recognised fulfilment of obligations. The financial appraisal must separately measure project expenditure and
commercial returns. {c('4, Articles 8–9')}</p>
''', sec='02 · The current scenario', bg='b', rail_on=[2, 4])

# ════════════════════════════════════════════════════════════════════════════
# 3 BENCHMARK MODELS
# ════════════════════════════════════════════════════════════════════════════
SECTION_START[3] = len(PAGES) + 1
page(f'''
<div class="ms">
  <div>
    <h2>London 2012 construction and employment programmes</h2>
    <p>London 2012 offers a comparator with a fixed event deadline and a temporary concentration of construction demand. The Olympic Delivery
    Authority aimed to use that demand to expand access to employment and training, particularly for neighbouring communities. This is relevant to
    the stadium academy because both programmes must turn a finite construction period into skills that remain useful after completion.</p>
  </div>
  <div class="gl dark" style="padding:4mm"><div class="k">Benchmarks in this section</div>
    <div class="li"><span class="d"></span><span class="xs"><b>London 2012</b> · fixed deadline, temporary demand</span></div>
    <div class="li"><span class="d"></span><span class="xs"><b>Australian AIP plans</b> · fair opportunity for local suppliers</span></div>
    <div class="li"><span class="d"></span><span class="xs"><b>Crossrail</b> · contractual skills targets</span></div>
    <div class="li"><span class="d g"></span><span class="xs"><b>Aramco iktva</b> · the closest Saudi comparator</span></div>
  </div>
</div>

<div class="k g mt3">What worked</div>
<div class="g4 mb2" style="gap:2.6mm">
  <div class="gl tight"><div class="v green">3,000+</div><div class="kv">training places · UK government, 20 May 2012</div></div>
  <div class="gl tight"><div class="v">408</div><div class="kv">apprentices working on the project · same release</div></div>
  <div class="gl tight green"><div class="v green">450+</div><div class="kv">apprenticeship opportunities against a target of 350 · ODA 2011–12</div></div>
  <div class="gl tight"><div class="v">1,580</div><div class="kv">placements for previously unemployed people · ODA 2011–12</div></div>
</div>
<div class="gl tight mb3" style="display:grid;grid-template-columns:auto 1fr;gap:5mm;align-items:center;padding:3mm 4mm">
  <div class="xs fg" style="font-weight:700;width:38mm">ODA apprenticeship opportunities against target</div>
  {C.vs_target(450, 350, 118, 500, '450+ achieved', 'target 350')}
</div>
<p>A UK government release dated 20 May 2012 reported more than 3,000 training places and 408 apprentices working on the project. The ODA’s
2011–12 annual report recorded over 450 apprenticeship opportunities against a target of 350 and 1,580 placements for previously unemployed people.
<strong>These are differently scoped reporting snapshots and should be read separately.</strong> They show that a large construction programme can
organise training alongside live employment. {c('11, 12')}</p>

<p>The feature worth adapting is the connection between training and an employer’s actual work. In our proposal, a stadium systems supplier would
specify the tasks learners must perform, identify a qualified mentor and provide a paid placement. The host provider would teach the prerequisite
skills and assess progress. The learner’s next assignment would form part of the agreement before the cohort begins.</p>

<div class="gl green mt1" style="padding:4mm 4.5mm">
  <div class="k g">Our adaptation · training tied to real work</div>
  <div style="display:grid;grid-template-columns:1fr auto 1fr auto 1fr;gap:2.5mm;align-items:stretch">
    <div><div class="num g" style="margin-bottom:1.5mm">1</div><b class="sm">Supplier</b><div class="xs">specifies the tasks, names a qualified mentor and provides a paid placement</div></div>
    <div class="arrow" style="align-self:center">→</div>
    <div><div class="num g" style="margin-bottom:1.5mm">2</div><b class="sm">Host provider</b><div class="xs">teaches the prerequisite skills and assesses progress</div></div>
    <div class="arrow" style="align-self:center">→</div>
    <div><div class="num g" style="margin-bottom:1.5mm">3</div><b class="sm">Next assignment</b><div class="xs">agreed before the cohort begins</div></div>
  </div>
</div>
''', sec='03 · Benchmark models', bg='a',
     banner=('ban_3', '03', 'Benchmark <em>models</em>', 'What London 2012, Australia, Crossrail and Aramco’s iktva teach about turning a construction peak into capability that lasts.'))

page(f'''
<h2>What proved weaker</h2>
<div class="ms">
  <div>
    <p>Crossrail’s later review of the Olympic experience reports that the ODA largely relied on contractor encouragement to meet its public skills
    commitments. It records the ODA’s conclusion that binding contractual clauses would have made delivery easier. This suggests that the Saudi
    programme needs clear supplier commitments, named delivery owners and milestones attached to each approved activity. {c('13, section 1.2')}</p>
    <p>The post-Games evaluation also found difficulties converting job starts into sustained employment across the broader host-borough employment
    programme. It identified insufficient support during the first 26 and 52 weeks of employment as a contributing factor. A stadium programme should
    therefore budget for follow-up and assistance through the next paid assignment. {c('14, pp. 54–55')}</p>
  </div>
  <div class="gl imp" style="padding:4mm 4.5mm">
    <div class="k o">Where sustained employment slipped</div>
    <svg width="100%" viewBox="0 0 60 24" style="margin:2mm 0 1mm">
      <line x1="3" y1="10" x2="57" y2="10" stroke="rgba(255,255,255,.25)" stroke-width=".4"/>
      <rect x="3" y="8.6" width="54" height="2.8" rx="1.4" fill="rgba(238,106,51,.35)"/>
      <circle cx="3" cy="10" r="1.6" fill="#F2F7F6"/><circle cx="30" cy="10" r="1.6" fill="#EE6A33"/><circle cx="57" cy="10" r="1.6" fill="#EE6A33"/>
      <text x="3" y="5.4" font-size="2.4" font-weight="800" fill="#F2F7F6" text-anchor="start">Job start</text>
      <text x="30" y="5.4" font-size="2.4" font-weight="800" fill="#FF9B6E" text-anchor="middle">26 weeks</text>
      <text x="57" y="5.4" font-size="2.4" font-weight="800" fill="#FF9B6E" text-anchor="end">52 weeks</text>
      <text x="30" y="17" font-size="2.1" font-weight="500" fill="#B4C5C2" text-anchor="middle">insufficient support in the first weeks of employment</text>
    </svg>
    <div class="hr" style="background:linear-gradient(90deg,rgba(238,106,51,.7),transparent)"></div>
    <div class="li"><span class="d o"></span><span class="xs">Relied on <b>contractor encouragement</b>, not binding clauses</span></div>
    <div class="li"><span class="d g"></span><span class="xs">Our fix: <b>supplier commitments</b>, named owners and milestones for each activity</span></div>
  </div>
</div>

<h2 class="mt2">Was the activity additional</h2>
<div class="ms">
  <div>
    <p>The same evaluation estimated that 696 of 2,026 job entries in the six-host-borough project were additional. It cautioned that the underlying
    survey evidence was more robust for the overall programme than for its component projects. This estimate concerns the wider employment initiative,
    with only some jobs attributable to construction. <strong>It cannot establish an additionality rate for Saudi stadium training.</strong> {c('14, p. 55')}</p>
    <p>Our adaptation is to record each participant’s previous employment, skills and planned employer training before admission. At six and twelve
    months, the provider would verify paid employment and responsibilities using employer records. Comparable eligible workers awaiting a later intake
    could help test whether the programme improved outcomes, while recognising differences in recruitment and motivation. LCGPA would receive both the
    observed outcomes and the limitations on causal interpretation.</p>
  </div>
  <div style="display:flex;flex-direction:column;gap:3mm">
    <div class="gl" style="padding:4mm">
      <div class="k">Six-host-borough project</div>
      <div style="display:flex;align-items:baseline;gap:2mm"><div class="v l green">696</div><div class="sm fg3">of 2,026 job entries</div></div>
      <div class="kv mb2">estimated additional, about one in three</div>
      {C.proportion(696, 2026, 58, C.GREEN, 'additional · 696', 'not additional · 1,330')}
    </div>
    <div class="gl green tight" style="padding:3.4mm 4mm">
      <div class="k g">Our evidence points per learner</div>
      <div style="display:flex;justify-content:space-between;text-align:center">
        <div><div class="v s">Before</div><div class="xs">baseline</div></div><div class="arrow">→</div>
        <div><div class="v s">6 mo</div><div class="xs">paid work</div></div><div class="arrow">→</div>
        <div><div class="v s">12 mo</div><div class="xs">paid work</div></div></div>
    </div>
  </div>
</div>

<h2 class="mt2">Australian Industry Participation plans</h2>
<div class="sm2" style="gap:5mm">
  <div class="gl" style="padding:4mm">
    <div style="display:flex;align-items:baseline;gap:2mm"><div class="v l green">12</div><div class="sm fg3">of 22 surveyed proponents</div></div>
    <div class="kv mb2">reported benefits, mainly better awareness of local suppliers · 2023 evaluation</div>
    {C.dots(12, 22, 11, 1.8, 4.7)}
  </div>
  <div>
    <p>Plans for major projects, including those with capital expenditure of A$500 million or more, must give domestic suppliers a fair opportunity
    to compete. The 2023 evaluation found that 12 of 22 surveyed proponents reported benefits, mainly better awareness of local suppliers, but data
    could not establish overall outcomes or additionality. <strong>Our lesson is to publish imported opportunities early and reward new qualified local
    production, not supplier directories.</strong> {c('24')}</p>
  </div>
</div>
''', sec='03 · Benchmark models', bg='c')

page(f'''
{contd('03', 'Benchmark models')}
<h2>Crossrail contractual skills and employment targets</h2>
<p>Crossrail provides a second construction comparator because it translated employment and training goals into contractor obligations across a
complex supply chain. The two UK programmes illuminate implementation design. Saudi eligibility and valuation must follow LCGPA’s own policy.</p>

<div class="k g mt2">What worked</div>
<div class="g3 mb3" style="gap:3mm">
  <div class="gl tight green"><div class="v green">1 per £3m</div><div class="kv">one skills or employment output for every £3 million of tender value</div></div>
  <div class="gl tight"><div class="v">≥ 50%</div><div class="kv">of outputs allocated to priority activities, such as apprenticeships and unemployed job starts</div></div>
  <div class="gl tight"><div class="v">1,000+</div><div class="kv">broader apprenticeship figure, including other delivery partners and activities</div></div>
</div>
<div class="gl tight mb3" style="display:grid;grid-template-columns:auto 1fr;gap:5mm;align-items:center;padding:3mm 4mm">
  <div class="xs fg" style="font-weight:700;width:38mm">Apprenticeships on the new route and stations against the original target</div>
  {C.vs_target(710, 400, 118, 800, '710 reported in 2022', 'target 400')}
</div>
<p>Crossrail’s contracts required one skills or employment output for every £3 million of tender value, with at least half allocated to priority
activities such as apprenticeships and unemployed job starts. The 2022 construction evaluation reports 710 apprenticeships associated with the new
route and stations against an original target of 400. A broader figure above 1,000 includes other delivery partners and activities. <strong>These
figures have different populations.</strong> {c('13, section 2.1; 15, p. 41')}</p>
<p>The evaluation describes quarterly review of contractor progress, illustrating the importance of active delivery management. For Saudi stadiums,
we propose one accountable coordinator at the training host and one EP owner in each obligated firm. {c('15, p. 43')}</p>

<div class="g2 mt2" style="gap:5mm">
  <div>
    <h2>What proved weaker</h2>
    <p>The implementation review found that ambiguous workforce-training definitions allowed existing corporate programmes to qualify with little
    additional effort. Multiple outputs could also relate to one apprentice. Subcontractor participation was uneven, and extensive reporting created an
    administrative burden. {c('13, sections 3.2–3.6')}</p>
    <div class="gl imp tight" style="padding:3.4mm 4mm">
      <div class="li"><span class="d o"></span><span class="xs"><b>Ambiguous definitions</b> let existing programmes qualify</span></div>
      <div class="li"><span class="d o"></span><span class="xs"><b>Multiple outputs</b> could relate to one apprentice</span></div>
      <div class="li"><span class="d o"></span><span class="xs"><b>Uneven</b> subcontractor participation</span></div>
      <div class="li"><span class="d o"></span><span class="xs"><b>Extensive reporting</b>, an administrative burden</span></div>
    </div>
  </div>
  <div>
    <h2>Was the activity additional</h2>
    <p>The published apprenticeship totals establish programme outputs. They do not isolate how many opportunities would have existed without the
    contractual requirements. The evidence of routine training qualifying for outputs further weakens a blanket claim of additionality.</p>
    <p>For the stadium pilot, each learner would have one identifier linking baseline skills, training, assessment and paid deployment. Supplier claims
    would distinguish newly funded activity from existing corporate training commitments.</p>
    <div class="gl green tight" style="padding:3mm 4mm;display:flex;align-items:center;justify-content:space-between;gap:1.5mm">
      <span class="tag g">Baseline skills</span><span class="arrow">›</span><span class="tag g">Training</span><span class="arrow">›</span>
      <span class="tag g">Assessment</span><span class="arrow">›</span><span class="tag g">Paid deployment</span></div>
    <div class="xs fg3 mt1" style="text-align:center">one learner identifier links every step</div>
  </div>
</div>
''', sec='03 · Benchmark models', bg='d')

BM = [('London 2012', 'Training tied to an employer’s actual work: tasks, mentor, paid placement, next assignment', 'Relying on contractor encouragement; thin support after job start'),
      ('Australian AIP plans', 'Publish imported opportunities early', 'Rewarding supplier directories; data that cannot show outcomes'),
      ('Crossrail', 'Contractual outputs per tender value, quarterly review, named owners', 'Ambiguous definitions that let routine training qualify'),
      ('Aramco iktva', 'A supplier baseline and an improvement plan', 'Crediting where money is spent rather than the verified gain above baseline')]
bm_html = ''.join(f'''<div style="display:grid;grid-template-columns:34mm 1fr 1fr;gap:4mm;padding:2.6mm 0;border-top:.25mm solid rgba(255,255,255,{'.0' if i == 0 else '.09'})">
   <b class="sm">{a}</b><div class="sm"><span class="green" style="font-weight:800">✓ </span>{b}</div><div class="sm"><span class="imp" style="font-weight:800">✕ </span>{d}</div></div>''' for i, (a, b, d) in enumerate(BM))

page(f'''
<h2>Saudi comparator: Aramco’s iktva programme</h2>
<div class="g5" style="display:grid;grid-template-columns:repeat(5,1fr);gap:2.6mm;margin-bottom:4mm">
  <div class="gl tight"><div class="v m">Dec 2015</div><div class="kv">programme launched</div></div>
  <div class="gl tight green"><div class="v m green">70%</div><div class="kv">local content target reached, Feb 2026</div></div>
  <div class="gl tight"><div class="v m">47</div><div class="kv">strategic products made in the Kingdom for the first time</div></div>
  <div class="gl tight"><div class="v m">350+</div><div class="kv">investments backed by USD 9 billion</div></div>
  <div class="gl tight imp"><div class="v m" style="color:#FF8A57;white-space:nowrap;font-size:13pt">USD 280bn</div><div class="kv">reported GDP contribution, a gross figure</div></div>
</div>

<div class="g3" style="gap:4mm">
  <div><div class="k">What it tried</div>
    <p>Launched in December 2015, iktva sets a baseline score for each Aramco supplier, measured through localised goods and services and
    salaries paid to Saudis, then agrees an improvement plan and tracks progress. Contractor evaluation matrices bring the score into project awards.
    It is the closest Saudi comparator: a large buyer with a construction-heavy supply chain. {c('17–19')}</p></div>
  <div><div class="k">What worked and what proved weaker</div>
    <p>In February 2026 Aramco reported reaching its 70% local content target, with 47 strategic products made in the Kingdom for the
    first time and more than 350 investments backed by USD 9 billion. These results are reported by the programme owner, and we found no independent
    evaluation. Because the score measures where money is spent, existing local purchases can raise it without new capability. {c('17, 18')}</p></div>
  <div><div class="k">Was the activity additional</div>
    <p>Aramco’s reported USD 280 billion contribution to GDP is a gross figure, not net of spending that would have occurred anyway.
    <strong>Our adaptation is to borrow iktva’s supplier baseline and improvement plan, but credit only the verified gain above that baseline.</strong>
    {c('17')}</p></div>
</div>

<div class="gl gold mt3" style="padding:5mm 5.5mm">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2mm">
    <span class="eb">Four benchmarks, one design</span><span class="xs fg3">group synthesis of this section</span></div>
  <div style="display:grid;grid-template-columns:34mm 1fr 1fr;gap:4mm;padding:1.5mm 0 1mm">
    <span class="k m mb0">Programme</span><span class="k g mb0">What we borrow</span><span class="k o mb0">What we avoid</span></div>
  {bm_html}
</div>

<div class="gl dark mt3" style="padding:4.5mm 5mm;display:grid;grid-template-columns:auto 1fr;gap:5mm;align-items:center">
  <span class="eb g">Our design rule</span>
  <div style="font-size:10.5pt;font-weight:600;line-height:1.45;color:var(--fg)">Credit only the verified gain above a supplier’s baseline, and tie every
  learner to paid work that is agreed before the cohort begins.</div>
</div>
''', sec='03 · Benchmark models', bg='a')

# ════════════════════════════════════════════════════════════════════════════
# 4 CHALLENGES
# ════════════════════════════════════════════════════════════════════════════
SECTION_START[4] = len(PAGES) + 1
page(f'''
<div class="g2" style="gap:5mm">
  <div>
    <h2><span class="n">4.1</span>Additionality and causality</h2>
    <p>Commissioning, operating manuals and warranty training may already form part of a stadium contract. Article 8 excludes original contractual
    duties, activities included or assumed in the main price, and routine operations. Before approval, each supplier should submit its existing scope,
    planned investment and training budget. The EP proposal must identify the extra expenditure and capability attributable to the programme. Existing
    facilities can contribute where the incremental economic effect is evidenced. {c('4, Articles 5 and 8')}</p>
    <div class="gl imp tight" style="padding:3.2mm 4mm"><div class="k o">Article 8 excludes</div>
      <div class="chip-row"><span class="tag o">Original contractual duties</span><span class="tag o">Activities in the main price</span><span class="tag o">Routine operations</span></div></div>
  </div>
  <div>
    <h2><span class="n">4.2</span>Valuation factors and usable rights</h2>
    <p>The draft gives qualitative criteria within each multiplier range, while detailed calibration still requires implementing guidance. Our
    proposed factors of 3 for technology transfer and 2 for knowledge transfer and localisation are negotiating assumptions. Access to equipment,
    duration of licences, permission to train others and rights to serve future clients must justify them. WIPO identifies territory and permitted
    uses as central licensing terms. {c('4, Article 9; 16')}</p>
    <div class="gl gold tight" style="padding:3.2mm 4mm"><div class="k">What must justify the factor</div>
      <div class="chip-row"><span class="tag y">Access to equipment</span><span class="tag y">Licence duration</span><span class="tag y">Permission to train others</span><span class="tag y">Rights to serve future clients</span></div></div>
  </div>
</div>

<h2 class="mt3"><span class="n">4.3</span>Alternative track and early investment</h2>
<div class="ms" style="gap:5mm">
  <div>
    <p>Article 10 permits an outcomes-based track where imported purchases exceed SAR 500 million, or where LCGPA considers a project’s outputs
    sufficient. Our SAR 421.6 million import scenario falls below that numerical criterion. A discretionary application would need measurable
    production, employment and service outcomes. Proactive and surplus credit provisions do not apply to projects on the outcomes track.
    {c('4, Article 10')}</p>
    <p>Under the credit track, early materials trials and licence development can be proposed for proactive approval. Surplus credits may support
    future obligations, generally within five years of the final completion certificate, with extension at LCGPA’s discretion. Proactive and surplus
    credits cannot be transferred to another party. Suppliers therefore need their own credit balances even when delivery is shared.
    {c('4, Article 14')}</p>
  </div>
  <div style="display:flex;flex-direction:column;gap:3mm">
    <div class="gl" style="padding:4mm"><div class="k">Outcomes-track criterion</div>{C.gauge(56)}
      <div class="xs mt1">Below the numerical criterion: only a discretionary application remains.</div></div>
    <div class="gl green tight" style="padding:3.4mm 4mm"><div class="k g">Credit track</div>
      <div style="display:flex;gap:3mm;align-items:baseline"><div class="v m green" style="white-space:nowrap">5 years</div><div class="xs">window for surplus credits after the final completion certificate, generally</div></div>
      <div class="xs mt1" style="color:#FFB08C">Proactive and surplus credits cannot be transferred.</div></div>
  </div>
</div>
''', sec='04 · Challenges', bg='b',
     banner=('ban_4', '04', 'Challenges for stadium <em>implementation</em>', 'Six design problems the programme must solve before the first riyal is committed.'))

ISSUES = ['Whole-base or incremental tier calculation', 'Obligations cascaded to foreign subcontractors', 'Outcomes-track criteria',
          'Non-transferable proactive and surplus credits under shared delivery', 'The 2% fee with quarterly reporting', 'The transition between policy versions']
iss_html = ''.join(f'''<div class="gl tight" style="display:flex;gap:3mm;align-items:center;padding:3mm 3.6mm"><div class="num">{i + 1}</div><span class="sm fg" style="font-weight:700;line-height:1.3">{t}</span></div>''' for i, t in enumerate(ISSUES))

page(f'''
{contd('04', 'Challenges for stadium implementation')}
<div class="g2" style="gap:5mm">
  <div>
    <h2><span class="n">4.4</span>Subcontracts and competing deadlines</h2>
    <p>A local prime contractor must include applicable requirements in foreign subcontracts. Every participating party’s role and commitment should
    appear in the EP proposal. The obligor remains responsible, and an activity can earn credit for only one obligor. Allocate shared equipment,
    trainers and testing costs before work begins. Late substitutions require revised origin, specification and obligation records.
    {c('4, Articles 7, 13 and 15')}</p>
    <div class="gl tight" style="padding:3.4mm 4mm;display:flex;align-items:center;gap:3.5mm">
      <div class="v l gold">1</div><div class="xs"><b>obligor per activity.</b> An activity can earn credit for only one obligor, and the obligor remains responsible.</div></div>
  </div>
  <div>
    <h2><span class="n">4.5</span>Reporting costs and measurement</h2>
    <p>The draft requires quarterly reports within ten working days of quarter-end and remediation plans for delays. Its administration fee is 2% of
    approved EP project value. External audit costs count within that fee, subject to the policy’s controls. The separate EP guarantee is 10% of EP
    obligations. {c('4, Articles 13 and 16')}</p>
    <div class="g3" style="gap:2.4mm">
      <div class="gl tight"><div class="v m">10 days</div><div class="kv">working days after quarter-end to report</div></div>
      <div class="gl tight gold"><div class="v m gold">2%</div><div class="kv">fee on approved EP project value</div></div>
      <div class="gl tight"><div class="v m">10%</div><div class="kv">EP guarantee on obligations</div></div>
    </div>
  </div>
</div>

<h2 class="mt3"><span class="n">4.6</span>Transition and capacity constraints</h2>
<div class="ms" style="gap:5mm">
  <p>Article 19 provides for effectiveness 120 days after publication, while Article 4 preserves existing obligations under the rules applying when they
  arose. Maintain a version register for each tender and secure any transition treatment in writing. A substitution should proceed only after the
  designer accepts performance, warranty, delivery and total cost. {c('4, Articles 4 and 19')}</p>
  <div class="gl tight" style="padding:3.4mm 4mm"><div class="k">A substitution proceeds only after the designer accepts</div>
    <div class="chip-row"><span class="tag g">Performance</span><span class="tag g">Warranty</span><span class="tag g">Delivery</span><span class="tag g">Total cost</span></div></div>
</div>

<div class="gl gold mt3" style="padding:5mm 5.5mm">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3.5mm">
    <span class="eb">Open draft issues that matter most</span><span class="xs fg3">for stadiums</span></div>
  <div class="g3" style="gap:2.6mm">{iss_html}</div>
  <p class="sm mt2 mb0">For stadiums, the issues that matter most are whole-base or incremental tier calculation, obligations cascaded to foreign
  subcontractors, outcomes-track criteria, non-transferable proactive and surplus credits under shared delivery, the 2% fee with quarterly reporting,
  and the transition between policy versions.</p>
</div>
''', sec='04 · Challenges', bg='c')

# ════════════════════════════════════════════════════════════════════════════
# 5 REINVESTMENT SOLUTIONS
# ════════════════════════════════════════════════════════════════════════════
SECTION_START[5] = len(PAGES) + 1
PROJ = [('A', 'Licensed systems commissioning capability', 'Technology transfer', 3, '2–4', 'blue', 'Pilot'),
        ('B', 'Paid placements and Saudi trainer development', 'Knowledge transfer', 2, '1–3', 'green', 'Pilot'),
        ('C', 'Saudi materials qualification and repeat orders', 'Localisation', 2, '1–3', 'gold', 'Pilot'),
        ('D', 'Exportable Saudi services and training', 'Export development', None, '2–4', 'm', 'Later')]
colmap = {'blue': '#4A95F0', 'green': '#22D38B', 'gold': '#E2B357', 'm': '#7F928F'}
proj_html = ''.join(f'''<div class="gl tight" style="padding:3.6mm 3.6mm;border-top:.7mm solid {colmap[col]};{'opacity:.88;border-style:dashed;border-top-style:solid' if f is None else ''}">
   <div style="display:flex;justify-content:space-between;align-items:center"><span style="font-size:16pt;font-weight:300;color:{colmap[col]};line-height:1">{k}</span>
   <span class="tag {'g' if st == 'Pilot' else ''}">{st}</span></div>
   <div style="font-size:8pt;font-weight:800;color:var(--fg);line-height:1.25;margin:1.6mm 0 1.2mm;min-height:7.5mm">{t}</div>
   <div class="xs" style="color:{colmap[col]};font-weight:700">{cat}</div>
   <div class="xs fg3">factor {('<b class="fg">' + str(f) + '</b> in ') if f else 'within '}{rng}</div></div>''' for k, t, cat, f, rng, col, st in PROJ)


def facts(col, items):
    cells = ''.join(f'''<div style="padding:2.6mm 3mm;border-radius:2mm;background:rgba(255,255,255,.04);border:.25mm solid rgba(255,255,255,.08)">
      <div class="k" style="color:{colmap[col]};margin-bottom:1mm">{h}</div><div class="xs fg" style="font-weight:600">{t}</div></div>''' for h, t in items)
    return f'<div style="display:grid;grid-template-columns:1fr 1.25fr 1.25fr 1fr;gap:2mm;margin-bottom:3.4mm">{cells}</div>'


def proj_block(k, col, title, parts, ref='', fx=None):
    rows = ''.join(f'''<div><div class="k" style="color:{colmap[col]}">{h}</div><p class="sm mb0">{t}</p></div>''' for h, t in parts)
    return f'''<div class="gl" style="padding:4.5mm 5mm;border-left:.8mm solid {colmap[col]}">
      <div style="display:flex;align-items:baseline;gap:3mm;margin-bottom:3mm"><span style="font-size:20pt;font-weight:300;color:{colmap[col]};line-height:1">{k}</span>
      <h2 style="margin:0">{title}</h2></div>
      {facts(col, fx) if fx else ''}
      <div class="g3" style="gap:5mm">{rows}</div></div>'''


page(f'''
<p class="lead" style="font-size:10pt">We propose four projects within a shared Materials and Systems Academy programme. Participating suppliers would use an
existing training host and approved construction sites. Each project needs its own eligible activity, evidence and cost allocation. The organisations
below are candidate partners whose roles require agreement.</p>

<div class="gl dark mt2 mb2" style="padding:4mm 5mm">
  <div style="display:flex;justify-content:center;margin-bottom:3mm">
    <div class="gl green" style="padding:3mm 7mm;text-align:center;border-radius:99px">
      <div style="font-size:10.5pt;font-weight:800;color:var(--fg)">Shared Materials and Systems Academy</div>
      <div class="xs">existing training host · approved construction sites · separate obligations and ledgers per supplier</div></div></div>
  <svg width="100%" viewBox="0 0 168 6" style="margin:-1mm 0 1mm"><path d="M84 0 V2.5 M21 2.5 H147 M21 2.5 V6 M63 2.5 V6 M105 2.5 V6 M147 2.5 V6" stroke="rgba(34,211,139,.6)" stroke-width=".35" fill="none"/></svg>
  <div class="g4" style="gap:3mm">{proj_html}</div>
</div>

{proj_block('A', 'blue', 'Licensed systems commissioning capability', [
    ('Activity and category', 'Foreign HVAC and building-controls vendors would transfer diagnostic tools, technical procedures and licences to a Saudi service partner, alongside supervised commissioning practice. We propose technology transfer with an illustrative factor of 3 within the draft’s 2–4 range. ' + c('4, Article 9')),
    ('Case for additionality and value', 'The Saudi team would gain rights and practical competence to diagnose and service specified systems on subsequent projects. Approval should identify the additional tools and rights beyond the original handover requirements. A factor above the minimum would depend on demonstrated independent capability and the depth of the rights transferred.'),
    ('Partners, evidence and risk', 'Candidate partners are the relevant foreign equipment manufacturers, a qualified Saudi mechanical or controls firm, and NITI or an equivalent provider. The evidence would include licence schedules, tool delivery and practical tests performed without supplier intervention. The main risk is restricted software access that prevents independent work. Future-use and trainer rights should be agreed before expenditure. ' + c('10, 16'))], fx=[('Category', 'Technology transfer · <b class="blue">3</b> in 2–4'), ('Candidate partners', 'Foreign equipment makers, a Saudi controls firm, NITI or equivalent'), ('Evidence', 'Licence schedules, tool delivery, unassisted practical tests'), ('Main risk', 'Restricted software access')])}
''', sec='05 · Reinvestment solutions', bg='a',
     banner=('ban_5', '05', 'Reinvestment <em>solutions</em>', 'One shared academy, four projects: turning the EP obligation into Saudi capability that keeps working after the stadium opens.'))

ppl = ''.join(f'<i style="width:4.6mm;height:4.6mm;border-radius:50%;background:var(--green);box-shadow:0 0 1.6mm rgba(34,211,139,.6)"></i>' for _ in range(24))
trn = ''.join(f'<i style="width:4.6mm;height:4.6mm;border-radius:50%;background:var(--gold);box-shadow:0 0 1.6mm rgba(226,179,87,.6)"></i>' for _ in range(6))

page(f'''
{proj_block('B', 'green', 'Paid placements and Saudi trainer development', [
    ('Activity and category', 'Vendors and the host would develop new assessed modules tied to stadium tasks, provide paid placements and prepare Saudi instructors to teach later cohorts. We propose knowledge transfer at factor 2 within the 1–3 range. The starting design retains the presentation’s 24 learners and six trainer candidates across two confirmed eligible sites. ' + c('1, 4')),
    ('Case for additionality and value', 'Participants would gain competencies beyond routine induction and contractual warranty training. The provider would document baseline skills, independently assess practical tasks and observe trainer delivery. An upper-range claim would require stronger evidence, such as recognised qualifications and an auditable programme. A certificate of attendance would provide insufficient evidence of competence.'),
    ('Partners, evidence and risk', 'NITI’s industrial and customised training capabilities make it a potential host, alongside participating vendors and Saudi employers. These capabilities require adaptation to stadium work. Employers would confirm placements and expected next-site assignments before intake. The main risk is that graduates have limited paid work after commissioning. Employment verification at six and twelve months would determine whether to repeat the cohort. ' + c('10'))], fx=[('Category', 'Knowledge transfer · <b class="green">2</b> in 1–3'), ('Candidate partners', 'NITI as host, participating vendors, Saudi employers'), ('Evidence', 'Baseline skills, independent assessment, paid work at 6 and 12 months'), ('Main risk', 'Little paid work after commissioning')])}

<div class="gl mt3" style="padding:5mm">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4mm">
    <span class="eb g">Starting design · first cohort</span><span class="xs fg3">learner numbers are design targets</span></div>
  <div style="display:grid;grid-template-columns:1.6fr 1fr 1fr;gap:6mm;align-items:start">
    <div><div style="display:flex;align-items:baseline;gap:2mm"><div class="v l green">24</div><div class="sm">learners in paid placements</div></div>
      <div style="display:grid;grid-template-columns:repeat(8,4.6mm);gap:2.2mm;margin-top:3.5mm">{ppl}</div></div>
    <div><div style="display:flex;align-items:baseline;gap:2mm"><div class="v l gold">6</div><div class="sm">trainer candidates</div></div>
      <div style="display:grid;grid-template-columns:repeat(3,4.6mm);gap:2.2mm;margin-top:3.5mm">{trn}</div>
      <div class="xs mt1">prepared to teach later cohorts</div></div>
    <div><div style="display:flex;align-items:baseline;gap:2mm"><div class="v l">2</div><div class="sm">confirmed eligible sites</div></div>
      <div style="display:flex;gap:2mm;margin-top:3mm">
        <svg width="16mm" height="12mm" viewBox="0 0 12 9"><ellipse cx="6" cy="5" rx="5.4" ry="3.4" fill="none" stroke="#F2F7F6" stroke-width=".5"/><ellipse cx="6" cy="5" rx="3" ry="1.6" fill="rgba(34,211,139,.6)"/></svg>
        <svg width="16mm" height="12mm" viewBox="0 0 12 9"><ellipse cx="6" cy="5" rx="5.4" ry="3.4" fill="none" stroke="#F2F7F6" stroke-width=".5"/><ellipse cx="6" cy="5" rx="3" ry="1.6" fill="rgba(34,211,139,.6)"/></svg></div>
      <div class="xs mt1">paid work confirmed before intake</div></div>
  </div>
  <div class="hr" style="margin:4.5mm 0 3.5mm;background:linear-gradient(90deg,rgba(34,211,139,.6),transparent)"></div>
  <div class="k g">The cohort journey</div>
  <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:2mm">
    {''.join(f'''<div style="padding:2.6mm 3mm;border-radius:2mm;background:rgba(255,255,255,.04);border:.25mm solid rgba(255,255,255,.08)">
      <div style="display:flex;align-items:center;gap:1.6mm;margin-bottom:1.2mm"><span class="num g" style="width:5mm;height:5mm;font-size:6pt">{i + 1}</span><b class="sm">{a}</b></div>
      <div class="xs">{d}</div></div>''' for i, (a, d) in enumerate([('Before intake', 'Employers confirm placements and next-site assignments'), ('Baseline', 'The provider documents each learner’s skills'), ('Paid placement', 'New assessed modules tied to stadium tasks'), ('Assessment', 'Independent practical tests; trainer delivery observed'), ('6 and 12 months', 'Verify employment, then decide whether to repeat the cohort')]))}
  </div>
</div>

<div class="gl gold mt3" style="padding:4.5mm 5mm">
  <div class="k">Conditions for starting</div>
  <div class="ms" style="gap:5mm;align-items:start">
    <p class="mb0">The initial agreement should name the employers, training host and assessors, confirm site access and licences, and approve a costed
    programme. Learner numbers are design targets. The SAR 36 million-scale illustration on the following page concerns a wider portfolio of rights,
    equipment and supplier development. <strong>A pilot intake needs its own priced budget and approval before recruitment.</strong></p>
    <div>
      <div class="li"><span class="d"></span><span class="xs"><b>Named</b> employers, training host and assessors</span></div>
      <div class="li"><span class="d"></span><span class="xs"><b>Confirmed</b> site access and licences</span></div>
      <div class="li"><span class="d"></span><span class="xs"><b>Approved</b> costed programme</span></div>
      <div class="li"><span class="d"></span><span class="xs"><b>Priced</b> pilot budget before recruitment</span></div>
    </div>
  </div>
</div>
''', sec='05 · Reinvestment solutions', bg='d')

page(f'''
{contd('05', 'Reinvestment solutions')}
<div class="gl" style="padding:4.5mm 5mm;border-left:.8mm solid #E2B357">
  <div style="display:flex;align-items:baseline;gap:3mm;margin-bottom:3mm"><span style="font-size:20pt;font-weight:300;color:#E2B357;line-height:1">C</span>
  <h2 style="margin:0">Saudi materials qualification and repeat orders</h2></div>
  {facts('gold', [('Category', 'Localisation · <b class="gold">2</b> in 1–3'), ('Candidate partners', 'ALUPCO and eligible Saudi chemical manufacturers'), ('Evidence', 'A newly qualified grade, laboratory and designer approval, repeat orders'), ('Main risk', 'Missing the specification or warranty')])}
  <div class="g2" style="gap:5mm">
    <p class="sm mb0"><span class="k" style="display:block">Activity and category</span>Establish a programme of trials, testing and tooling for specific
    locally produced metal components and construction chemicals. Propose localisation at factor 2 within the 1–3 range. Additionality would come from a
    newly qualified grade or production capability and evidenced demand beyond existing contracts. ALUPCO and eligible Saudi chemical manufacturers are
    candidates. Sika’s documented admixture production supports a capability starting point, with each proposed chemical grade requiring separate
    validation. {c('4, 8, 9')}</p>
    <p class="sm mb0"><span class="k" style="display:block">Risk and safeguards</span>The principal risk is failure to meet the stadium’s technical
    specification or warranty. An independent qualified laboratory and the designer should approve tests before substitution. Buyers could coordinate
    specifications and competitive orders while preserving access for multiple qualified suppliers. Record ordinary purchasing separately from the
    additional development activity proposed for EP credit.</p>
  </div>
  <div class="gl dark mt3" style="padding:4mm 4.5mm">{C.basket(160)}</div>
  <p class="sm mt2 mb0">The modelled chemicals and metals import basket totals SAR 176.97 million. A 25% shift would imply SAR 44.24 million in
  additional domestic purchases, subject to actual items, capacity and cost. <strong>This is an opportunity scenario.</strong> Domestic value added
  depends on imported inputs within those purchases. Any change in the contractual import base must also update the EP obligation.
  {c('1, 2; 4, Article 7')}</p>
</div>

<div class="gl mt3" style="padding:4.5mm 5mm;border-left:.8mm solid #7F928F;border-top-style:dashed;border-right-style:dashed;border-bottom-style:dashed">
  <div style="display:flex;align-items:baseline;gap:3mm;margin-bottom:3mm"><span style="font-size:20pt;font-weight:300;color:#7F928F;line-height:1">D</span>
  <h2 style="margin:0">Exportable Saudi services and training</h2><span class="tag" style="margin-left:auto">Later phase · outside the initial funding</span></div>
  {facts('m', [('Category', 'Export development · within 2–4'), ('Candidate partners', 'Saudi service firms, training host and manufacturers from projects A–C'), ('Evidence', 'Export licences, independent sales and receipts'), ('Main risk', 'Thin demand or restricted territorial rights')])}
  <div class="g2" style="gap:5mm">
    <p class="sm mb0"><span class="k" style="display:block">Activity and category</span>After the pilot proves local demand, participating foreign vendors
    could introduce Saudi commissioning services, qualified products and Saudi-authored training to regional customers. Propose export development within
    the 2–4 range, with a higher factor justified by durable channels, meaningful Saudi content and repeat contracts. Additionality would require new
    customers or export activity beyond the supplier’s baseline. {c('4, Articles 8–9')}</p>
    <p class="sm mb0"><span class="k" style="display:block">Partners, evidence and risk</span>Candidate partners are the Saudi service firms, training
    host and manufacturers developed through the first three projects. The main risk is insufficient demand or restricted territorial rights. Verify
    export licences, independent sales and receipts before claiming achievement. This expansion is outside the initial funding illustration.</p>
  </div>
</div>
''', sec='05 · Reinvestment solutions', bg='b', rail_on=[3, 5])

GATES = [('Independent skills tests', 'learners perform without supplier intervention'), ('Approved product trials', 'laboratory and designer sign-off'),
         ('Paid demand', 'placements, orders and next-site work'), ('Expand', 'only after acceptable performance')]
gates_html = ''
for i, (a, b) in enumerate(GATES):
    last = i == len(GATES) - 1
    gates_html += f'''<div class="gl tight {'green' if last else ''}" style="flex:1;padding:3mm 3.4mm"><div class="k {'g' if last else ''}" style="margin-bottom:1mm">{'Then' if last else 'Gate ' + str(i + 1)}</div>
      <div class="sm fg" style="font-weight:800;line-height:1.25">{a}</div><div class="xs fg3">{b}</div></div>'''
    if not last:
        gates_html += '<div class="arrow" style="align-self:center">→</div>'

page(f'''
<h2>Illustrative funding and approval gates</h2>
<p>Higher valuation factors reduce the activity needed to discharge the same obligation. Required activity equals EP obligation × 3 ÷ sum of the three
factors, with technology, knowledge and localisation in equal values.</p>

<div class="gl dark mt1 mb3" style="padding:4.5mm 5mm 4mm">{C.funding(168)}
  <div class="src mt1">Group calculation using the unrounded SAR 421.6096m import estimate. Values are indicative and rounded.</div></div>

<div class="g2 mb3" style="gap:3mm">
  <div class="gl" style="padding:4mm 4.5mm">
    <div class="k">Portfolio assumption</div>
    <div style="display:grid;grid-template-columns:1.7fr .6fr 1fr 1fr;gap:2.4mm 3mm;align-items:baseline" class="xs">
      <span class="fg3">Mix</span><span class="fg3">Factors</span><span class="fg3">Activity</span><span class="fg3">EP credit</span>
      <b>Equal values across the three categories</b><span>3, 2, 2</span><b class="green" style="font-size:9pt;white-space:nowrap">SAR 36.14m</b><b style="font-size:9pt;white-space:nowrap">SAR 84.32m</b>
      <b>Same mix at category minima</b><span>2, 1, 1</span><b style="font-size:9pt;color:var(--fg2);white-space:nowrap">SAR 63.24m</b><b style="font-size:9pt;white-space:nowrap">SAR 84.32m</b>
    </div>
  </div>
  <div style="display:flex;flex-direction:column;gap:2.4mm">
    <div class="gl tight gold" style="display:flex;align-items:center;gap:4mm;padding:2.6mm 4mm"><div class="v m gold" style="width:30mm;flex:none;white-space:nowrap">SAR 0.72m</div><div class="xs">2% administration fee at factors 3, 2, 2</div></div>
    <div class="gl tight" style="display:flex;align-items:center;gap:4mm;padding:2.6mm 4mm"><div class="v m" style="width:30mm;flex:none;white-space:nowrap">SAR 1.26m</div><div class="xs">2% administration fee at category minima</div></div>
    <div class="gl tight" style="display:flex;align-items:center;gap:4mm;padding:2.6mm 4mm"><div class="v m" style="width:30mm;flex:none;white-space:nowrap">SAR 8.43m</div><div class="xs">10% EP guarantee on the SAR 84.32m obligation</div></div>
  </div>
</div>

<p>The 2% fee would be approximately SAR 0.72 million or SAR 1.26 million respectively, with treatment toward fulfilment subject to approved rules.
These illustrations show the full activity target before any fee credit. The 10% EP guarantee would be SAR 8.43 million. Confirm valuation and cash
commitments before funding. Expand after independent skills tests, approved product trials and paid demand demonstrate acceptable performance.
{c('4, Articles 13 and 16')}</p>

<div class="k mt2">Approval gates before expansion</div>
<div style="display:flex;gap:2mm">{gates_html}</div>
''', sec='05 · Reinvestment solutions', bg='c', rail_on=[4, 6])

# ════════════════════════════════════════════════════════════════════════════
# 6 PLAYBOOK AND RECOMMENDATIONS
# ════════════════════════════════════════════════════════════════════════════
SECTION_START[6] = len(PAGES) + 1
STEPS = [('Before bidding', 'Commercial lead', 'Record the buyer, applicable policy, supplier ownership and covered imports excluding VAT. Check tender and cumulative thresholds.', ''),
         ('Before pricing', 'Finance', 'Obtain the approved obligation calculation and model proposed and minimum valuation factors, administration fees and guarantee requirements.', ''),
         ('Before proposing projects', 'EP lead', 'Document existing duties and planned investment. Identify the extra capability, local beneficiary, partner commitments and evidence.', ''),
         ('Before execution', '', 'Secure LCGPA approval, technical rights, cost allocation and paid demand. Record one claimant for each shared activity and include duties in relevant subcontracts.', ''),
         ('After main-contract signature', '', 'Track the draft’s 90-day EP-contract deadline and the guarantee due within 30 days of EP-contract signature. Use the approved project schedule.', '90 days · 30 days'),
         ('Each quarter', '', 'Reconcile expenditure, progress and evidence. Submit the report within ten working days and a remediation plan where obligations are delayed.', '10 working days'),
         ('At completion', '', 'Submit the final statement within 60 working days of the last project. Track permitted surplus credit and verify paid work, trainer return and repeat orders at six and twelve months.', '60 working days · 6 and 12 months')]
steps_html = ''
for i, (when, who, what, dl) in enumerate(STEPS):
    last = i == len(STEPS) - 1
    steps_html += f'''<div style="display:grid;grid-template-columns:9mm 1fr;gap:3mm;position:relative">
      <div style="position:relative;display:flex;justify-content:center">
        {'' if last else '<i style="position:absolute;top:7mm;bottom:-3mm;width:.35mm;background:linear-gradient(rgba(226,179,87,.7),rgba(226,179,87,.2))"></i>'}
        <div style="width:6.4mm;height:6.4mm;border-radius:1.4mm;border:.35mm solid var(--gold);background:rgba(140,100,26,.3);display:flex;align-items:center;justify-content:center;font-size:7pt;font-weight:800;color:var(--gold);position:relative">{i + 1}</div></div>
      <div class="gl tight" style="padding:3.1mm 4.4mm;margin-bottom:2.5mm;display:grid;grid-template-columns:42mm 1fr;gap:4mm;align-items:start">
        <div><div style="font-size:8.6pt;font-weight:800;color:var(--fg);line-height:1.25">{when}</div><div class="xs fg3">{who}</div>
          {f'<span class="tag y" style="margin-top:1.4mm;white-space:normal">{dl}</span>' if dl else ''}</div>
        <div class="sm"><span style="color:var(--green);font-weight:800">☐ </span>{what}</div></div></div>'''

page(f'''
<h2>Company checklist</h2>
<div class="mt1">{steps_html}</div>
<div class="gl gold" style="padding:4.5mm 5mm">
  <div class="k">The deadline clock under the April 2026 draft</div>
  <svg width="100%" viewBox="0 0 168 22" style="margin-top:2mm">
    <line x1="4" y1="9" x2="164" y2="9" stroke="rgba(226,179,87,.55)" stroke-width=".4"/>
    {''.join(f'<circle cx="{x}" cy="9" r="1.8" fill="{c_}" stroke="#141007" stroke-width=".5"/><text x="{x}" y="4.4" font-size="2.5" font-weight="800" fill="#F2F7F6" text-anchor="middle">{t}</text><text x="{x}" y="14.6" font-size="2.05" font-weight="500" fill="#B4C5C2" text-anchor="middle">{s1}</text><text x="{x}" y="17.6" font-size="2.05" font-weight="500" fill="#B4C5C2" text-anchor="middle">{s2}</text>' for x, c_, t, s1, s2 in [(10, '#7F928F', 'Day 0', 'main contract', 'signed'), (42, '#E2B357', '90 days', 'EP contract', 'deadline'), (74, '#E2B357', '+30 days', 'guarantee after', 'EP-contract signature'), (106, '#22D38B', 'Quarterly', 'report within 10', 'working days'), (138, '#22D38B', '60 working days', 'final statement after', 'the last project'), (160, '#4A95F0', '6 · 12 mo', 'verify work and', 'repeat orders')])}
  </svg>
</div>
<div class="src">Policy deadlines above follow the April 2026 draft, Articles 13–16. Confirm the applicable terms for each contract.</div>
''', sec='06 · Playbook', bg='a',
     banner=('ban_6', '06', 'Playbook and <em>recommendations</em>', 'A seven-step checklist for obligated companies, and four requests to LCGPA that make shared delivery workable.'))

REC = [('Publish construction examples for eligibility and valuation.', 'Show treatment of joint ventures, foreign subcontracts, imported services and tier calculations, alongside evidence needed for each factor.'),
       ('Provide a shared-programme agreement.', 'Standardise supplier roles, cost allocation and evidence identifiers so an academy can serve several projects with attributable claims.'),
       ('Define the outcomes track and transition rules.', 'Publish qualifying evidence, partial-achievement treatment and handling of existing commitments, proactive activity and surplus credits.'),
       ('Connect credit to verified additional outcomes.', 'Combine quarterly milestone evidence with later checks on employment, usable rights and repeat orders, using a proportionate common reporting template.')]
rec_html = ''.join(f'''<div class="gl" style="padding:4.5mm 5mm;display:grid;grid-template-columns:auto 1fr;gap:4mm">
  <div style="font-size:26pt;font-weight:300;line-height:.9;color:var(--gold)">0{i + 1}</div>
  <div><div style="font-size:10.6pt;font-weight:800;color:var(--fg);line-height:1.28;margin-bottom:2mm">{a}</div><div style="font-size:8.8pt;line-height:1.48">{b}</div></div></div>''' for i, (a, b) in enumerate(REC))

page(f'''
{contd('06', 'Playbook and recommendations')}
<h2>Recommendations for LCGPA</h2>
<div class="g2 mb3" style="gap:3.5mm;grid-auto-rows:1fr">{rec_html}</div>

<div class="grow" style="position:relative;border-radius:4mm;overflow:hidden;min-height:110mm;border:.3mm solid rgba(226,179,87,.55);box-shadow:0 2mm 7mm rgba(0,0,0,.4)">
  <div style="position:absolute;inset:0;background:url(img/closing.jpg) 40% 30%/cover"></div>
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,9,11,.05) 0%,rgba(4,9,11,.35) 35%,rgba(4,9,11,.94) 72%),linear-gradient(90deg,rgba(4,9,11,.45),rgba(4,9,11,0) 70%)"></div>
  <div style="position:absolute;left:8mm;right:8mm;bottom:8mm">
    <span class="eb">What we would tell LCGPA</span>
    <div style="font-size:15pt;font-weight:800;line-height:1.3;color:var(--fg);letter-spacing:-.01em;margin:4.5mm 0 3.5mm">Approve a small, costed
    <span class="green">Materials and Systems Academy</span> programme around eligible stadium suppliers.</div>
    <div style="font-size:9.6pt;font-weight:500;line-height:1.55;color:var(--fg2)">Require additional capability, usable rights and paid demand before
    committing funds. Let firms share delivery through an existing host, with clear responsibility for every claim. Expansion should follow demonstrated
    technical performance, sustainable work and competitive local supply.</div>
  </div>
</div>
''', sec='06 · Recommendations', bg='d')

# ════════════════════════════════════════════════════════════════════════════
# REFERENCES
# ════════════════════════════════════════════════════════════════════════════
REFS = [
 ('Group 8. (2026). King Salman Stadium Group 8. Supplied presentation, slides 3–19 and source appendix. Group assumptions and proposed programme.', None),
 ('GASTAT. (2025). Supply and Use and Input-Output Tables by Sections 2023. Sheets 6.1–6.3, thousand SAR. Recalculated from the downloaded workbook.', 'https://www.stats.gov.sa/documents/20117/2435267/SUT_and_IO_By_Sections_-En.xlsx_fixed_3036245/91b73a34-05e8-0e49-46e8-eda783beae16?t=1746090703771'),
 ('FIFA. (2024). FIFA World Cup 2034 Bid Evaluation Report. Stadium proposals, pp. 48–50.', 'https://digitalhub.fifa.com/m/51d8a13714827f1d/original/FIFA-World-Cup-2034-Bid-Evaluation-Report.pdf'),
 ('LCGPA. (2026). Economic Participation Policy Update. Official Arabic consultation text, Articles 1–20. April consultation, accessed 15 November 2026.', 'https://istitlaa.ncc.gov.sa/ar/finance/lcgpa/economicparticipationpolicyupdate/Pages/default.aspx'),
 ('LCGPA. (n.d.). Economic Participation Policy, Unit 7. PC-GEN-TM-ECP-EN-V12. Preceding-framework training material, pp. 4–5, 11–15.', 'https://lcgpa.futurex.sa/pluginfile.php/2095/mod_folder/content/0/pdf%20E/Economic%20Participation%20Policy%20%281%29.pdf?forcedownload=1'),
 ('Umm Al-Qura. (14 April 2026). Consultation announcement covering the Economic Participation Policy Update. Consultation closed 22 April 2026.', 'https://www.uqn.gov.sa/news/reports/4000737'),
 ('DGA Group / Albright Stonebridge Group. (April 2026). Updated Version of Saudi Economic Participation Policy Issued for Public Consultation. pp. 3–6.', 'https://dgagroup.com/wp-content/uploads/2026/04/DGA-ASG-Analysis-Updated-Version-of-Saudi-Economic-Participation-Policy-Issued-for-Public-Consultation-1.pdf'),
 ('ALUPCO. (n.d.). Aluminium. Company information on extrusion, finishing, die-making and fabrication capabilities.', 'https://alupco.com/aluminium/'),
 ('Sika. (27 June 2018). Sika Commissions New Factory in Saudi Arabia. Concrete-admixture production in Dammam.', 'https://www.sika.com/dms/getdocument.get/e671630e-2b9d-4256-898e-bd30c9a627fa/glo-en-media-release-saudi-arabia-27-06-2018.pdf'),
 ('National Industrial Training Institute. (n.d.). About Training. Industrial training, customised programmes and technical disciplines.', 'https://www.niti.edu.sa/?page_id=1961'),
 ('UK Department for Culture, Media and Sport. (20 May 2012). 2012 Games construction on track thanks to 12,000-strong workforce.', 'https://www.gov.uk/government/news/2012-games-construction-on-track-thanks-to-12-000-strong-workforce'),
 ('Olympic Delivery Authority. (2012). Annual Report and Accounts 2011–12. Employment and skills, p. 46.', 'https://assets.publishing.service.gov.uk/media/5a78fe5e40f0b679c0a07b21/ODA_Annual_Report_and_Accounts_2011-1212.pdf'),
 ('Eldred, A., and Blin, A.-S. (17 August 2018). Implementing Contractual Skills and Employment Targets. Crossrail Learning Legacy, sections 1.2, 2.1 and 3.2–3.6.', 'https://learninglegacy.crossrail.co.uk/documents/implementing-contractual-skills-and-employment-targets/'),
 ('UK Department for Culture, Media and Sport. (2013). 2012 Games Meta-Evaluation, Report 5, East London Evidence Base. Employment additionality and sustained outcomes, pp. 54–55.', 'https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/224147/Report_5_East_London_Evidence_Base_FINAL.pdf'),
 ('Transport for London / Department for Transport. (May 2022). Crossrail Baseline Evaluation, Construction Impacts. Employment and skills, pp. 40–44.', 'https://content.tfl.gov.uk/construction-impacts-report-acc.pdf'),
 ('World Intellectual Property Organization. (n.d.). Technology Transfer Agreements. Licensing scope, territory and permitted uses.', 'https://www.wipo.int/en/web/technology-transfer/agreements'),
 ('Aramco. (11 February 2026). Aramco achieves 70% local content target through flagship iktva program.', 'https://www.aramco.com/en/news-media/news/2026/aramco-achieves-70-local-content-target-through-flagship-iktva-program'),
 ('Supplhi. (December 2017). The Saudi approach to local content: making In-Kingdom Total Value Add (IKTVA) real. Supplier baseline, action plan and measured parameters.', 'https://www.supplhi.com/the-saudi-approach-to-local-content-making-in-kingdom-total-value-add-iktva-real/'),
 ('Arab News. (n.d.). Aramco IKTVA contractor matrices are now well established.', 'https://www.arabnews.com/node/2011136'),
 ('Argaam. (October 2024). Qiddiya awards SAR 4B stadium project contract to Saudi-Spanish consortium.', 'https://www.argaam.com/en/article/articledetail/id/1758470'),
 ('MEED. (26 February 2024). Saudi Arabia selects Dammam stadium contractor. BESIX–Albawani, estimated SAR 3.7 billion.', 'https://www.meed.com/saudi-arabia-selects-dammam-stadium-contractor'),
 ('Estithmar Holding. (10 September 2026). Elegancia Arabia Trading awarded SAR 829 million mechanical works, Prince Mohammed bin Salman Stadium.', 'https://www.estithmarholding.com/media/read/263'),
 ('China Fangda Group. (19 October 2026). Announcement 2026-41, stadium façade package; SAR 997.3 million excluding VAT.', 'http://static.cninfo.com.cn/finalpage/2026-10-19/1225610057.PDF'),
 ('Australian Department of Industry, Science and Resources. (August 2023). Australian Industry Participation Policy Impact Evaluation Report, pp. 16, 23–25.', 'https://www.industry.gov.au/sites/default/files/2024-08/australian-industry-participation-policy-impact-evaluation-report_0.pdf'),
]
GROUPS = [('Case, sector and data', [1, 2, 3]), ('EP policy', [4, 5, 6, 7]), ('Saudi suppliers and training', [8, 9, 10]),
          ('London 2012 and Crossrail', [11, 12, 13, 14, 15]), ('Licensing', [16]), ('Aramco iktva', [17, 18, 19]),
          ('Stadium contracts', [20, 21, 22, 23]), ('Australia', [24])]
grp_of = {n: g for g, ns in GROUPS for n in ns}


def ref_html(i):
    t, u = REFS[i - 1]
    link = f' <a href="{u}" style="color:var(--green);font-weight:700">Source ↗</a>' if u else ''
    return f'''<div style="display:grid;grid-template-columns:7.5mm 1fr;gap:1.5mm;margin-bottom:2.9mm;break-inside:avoid">
      <span style="font-size:7.9pt;font-weight:800;color:var(--gold)">[{i}]</span><span style="font-size:7.9pt;line-height:1.46">{t}{link}</span></div>'''


def refs_block(nums):
    out = ''; last = None
    for n in nums:
        g = grp_of[n]
        if g != last:
            out += f'<div class="k" style="margin-top:{0 if last is None else 2.4}mm;break-after:avoid">{g}</div>'
            last = g
        out += ref_html(n)
    return out


SECTION_START['R'] = len(PAGES) + 1
page(f'''
<div class="cont-title"><b>R</b><h1>References</h1></div>
<p class="sm" style="max-width:150mm">Numbered references correspond to citations in the text. Public sources accessed on 15 November 2026. Publication
and data years are stated below.</p>
<div class="col2 mt2" style="column-gap:7mm">{refs_block(range(1, 25))}</div>
<div class="gl dark mt2" style="padding:3.4mm 4.5mm;display:grid;grid-template-columns:auto 1fr;gap:4mm;align-items:center">
  <span class="eb m">AI assistance</span>
  <p class="sm mb0">ChatGPT supported research, calculations and drafting. The submitting group is responsible for final review and approval.</p>
</div>
''', sec='References', bg='c', spread_on=False)

# ════════════════════════════════════════════════════════════════════════════
# BACK COVER
# ════════════════════════════════════════════════════════════════════════════
BACK = f'''
<section class="page" style="background:#04090B">
  <div style="position:absolute;left:0;top:0;width:210mm;height:170mm;background:url(img/back.jpg) center/cover;
       -webkit-mask-image:linear-gradient(180deg,#000 60%,transparent)"></div>
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,9,11,.45),rgba(4,9,11,0) 30%),radial-gradient(130mm 80mm at 20% 85%,rgba(20,110,75,.25),transparent 70%)"></div>
  <div style="position:absolute;left:16mm;right:16mm;top:150mm">
    <span class="eb">Group 8 · MBSC EMBA · ECN 511</span>
    <div style="font-size:40pt;font-weight:800;color:var(--fg);letter-spacing:-.03em;line-height:1;margin:5mm 0 3mm">Thank you</div>
    <div style="font-size:11pt;color:var(--fg2);max-width:130mm;line-height:1.45">Economic Participation in Saudi Stadium Construction · a practical
    playbook using the King Salman Stadium case</div>
    <div style="display:grid;grid-template-columns:repeat(7,1fr);gap:2mm;margin-top:9mm">{team_html}</div>
  </div>
  <div class="gl" style="position:absolute;left:16mm;right:16mm;bottom:16mm;padding:4.5mm 5mm;display:grid;grid-template-columns:auto 1fr auto;gap:5mm;align-items:center">
    <img src="img/qr.png" style="width:22mm;height:22mm;border-radius:1.6mm;background:#fff;padding:1.2mm">
    <div><div class="k">The main presentation</div><div style="font-size:9pt;font-weight:700;color:var(--fg)">Interactive 3D edition, live in the browser</div>
      <a href="https://mbsc-group8-ecn511.com" style="font-size:10.5pt;font-weight:800;color:var(--green)">mbsc-group8-ecn511.com</a></div>
    <img src="img/mbsc_logo_dark.svg" style="height:13mm">
  </div>
  <div class="src" style="position:absolute;left:16mm;bottom:8mm;font-size:5.4pt">Image: Group 8 3D model of King Salman Stadium</div>
</section>'''
PAGES.append(BACK)

# ════════════════════════════════════════════════════════════════════════════
# CONTENTS (now that page numbers are known)
# ════════════════════════════════════════════════════════════════════════════
TOC = [(1, 'Sector at a glance', 'The case, the SAR 4.5bn scenario and our three priorities'),
       (2, 'The current scenario', 'Procurement exposure, Saudi suppliers, and the path from imports to EP obligations'),
       (3, 'Benchmark models', 'London 2012, Australia’s AIP plans, Crossrail and Aramco’s iktva'),
       (4, 'Challenges for stadium implementation', 'Additionality, valuation, tracks, subcontracts, reporting and transition'),
       (5, 'Reinvestment solutions', 'Four projects in a shared Materials and Systems Academy, with funding gates'),
       (6, 'Playbook and recommendations', 'A seven-step company checklist and four recommendations for LCGPA')]
toc_html = ''.join(f'''<div style="display:grid;grid-template-columns:16mm 1fr auto;gap:4mm;align-items:center;padding:4.2mm 0;border-top:.25mm solid rgba(255,255,255,.1)">
  <div style="font-size:24pt;font-weight:300;color:var(--gold);line-height:1">0{n}</div>
  <div><div style="font-size:12pt;font-weight:800;color:var(--fg);line-height:1.2">{t}</div><div class="sm fg3">{d}</div></div>
  <div style="font-size:11pt;font-weight:800;color:var(--fg)">{SECTION_START[n]:02d}</div></div>''' for n, t, d in TOC)
toc_html += f'''<div style="display:grid;grid-template-columns:16mm 1fr auto;gap:4mm;align-items:center;padding:4.2mm 0;border-top:.25mm solid rgba(255,255,255,.1);border-bottom:.25mm solid rgba(255,255,255,.1)">
  <div style="font-size:24pt;font-weight:300;color:var(--fg3);line-height:1">R</div>
  <div><div style="font-size:12pt;font-weight:800;color:var(--fg);line-height:1.2">References</div><div class="sm fg3">24 numbered sources, accessed 15 November 2026</div></div>
  <div style="font-size:11pt;font-weight:800;color:var(--fg)">{SECTION_START['R']:02d}</div></div>'''

KEYS = [('SAR 338.3bn', 'construction gross value added, 2023', ''), ('7.8%', 'of Saudi gross value added', 'green'),
        ('19.67%', 'of construction’s intermediate purchases are imported', 'imp'), ('SAR 421.6m', 'estimated imports in the SAR 4.5bn scenario', 'imp'),
        ('SAR 84.32m', 'EP obligation at the 20% draft rate', 'gold'), ('4 projects', 'in one shared Materials and Systems Academy', 'green')]
key_html = ''.join(f'''<div class="gl tight {cl if cl in ('green', 'gold', 'imp') else ''}" style="padding:3.4mm 4mm"><div class="v m" style="color:{ {'green': '#22D38B', 'gold': '#E2B357', 'imp': '#FF8A57', '': '#F2F7F6'}[cl] }">{v}</div><div class="kv">{k}</div></div>''' for v, k, cl in KEYS)

saved = PAGES[:]
PAGES[:] = PAGES[:CONTENTS_IDX]
page(f'''
<div style="display:flex;justify-content:space-between;align-items:flex-end;margin:2mm 0 6mm">
  <div><span class="eb">Inside the report</span><div style="font-size:30pt;font-weight:800;color:var(--fg);letter-spacing:-.025em;line-height:1;margin-top:4mm">Contents</div></div>
  <div class="xs fg3" style="text-align:right">Group 8 · MBSC Executive MBA<br>ECN 511 Economics for Managers · 15 November 2026</div>
</div>
{toc_html}
<div class="k mt4">The case in six numbers</div>
<div class="g3" style="gap:3mm">{key_html}</div>
<div class="gl dark mt3" style="padding:4mm 4.5mm">
  <div class="k">How to read the figures</div>
  <p class="xs mb0">The SAR 4.5 billion stadium value is a teaching assumption anchored on two awarded Saudi stadiums. Import estimates apply GASTAT’s
  2023 national ratios and are screening estimates, not an EPP calculation. Policy references follow LCGPA’s April 2026 consultation draft. Charts are
  drawn from the figures in the text and the group’s presentation; bracketed numbers point to the references.</p>
</div>
''', sec='Contents', bg='d')
PAGES[:] = PAGES + saved[CONTENTS_IDX + 1:]

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Economic Participation in Saudi Stadium Construction · Group 8</title>
<meta name="author" content="Group 8 · MBSC EMBA"><meta name="description" content="A practical playbook using the King Salman Stadium case">
<link rel="stylesheet" href="style.css"></head><body>
{''.join(PAGES)}
</body></html>'''
open(os.path.join(HERE, 'report.html'), 'w').write(html)
print('pages:', len(PAGES), 'sections:', SECTION_START)
