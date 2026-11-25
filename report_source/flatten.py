"""Put each baked page image underneath the live text layer: python3 flatten.py out.pdf"""
import io, os, sys
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))
FLAT = os.path.join(HERE, 'flat')
out = sys.argv[1] if len(sys.argv) > 1 else 'report.pdf'

writer = PdfWriter(clone_from=os.path.join(FLAT, 'text.pdf'))
for i, pg in enumerate(writer.pages):
    w, h = float(pg.mediabox.width), float(pg.mediabox.height)
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(w, h))
    c.drawImage(os.path.join(FLAT, f'bg_{i + 1:02d}.jpg'), 0, 0, width=w, height=h)
    c.save()
    img_page = PdfReader(buf).pages[0]
    pg.merge_page(img_page, over=False)        # artwork underneath, text on top
writer.add_metadata({'/Title': 'Economic Participation in Saudi Stadium Construction', '/Author': 'Group 8 · MBSC EMBA',
                     '/Subject': 'A practical playbook using the King Salman Stadium case'})
writer.compress_identical_objects()
with open(out, 'wb') as f:
    writer.write(f)
print(out, len(writer.pages), 'pages', os.path.getsize(out) // 1024, 'KB')
