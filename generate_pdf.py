#!/usr/bin/env python3
"""Generate Screaming Architecture PDF Guide"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white, gray
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Preformatted
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os, re, sys

PRIMARY = HexColor("#1a1a2e")
ACCENT = HexColor("#e94560")
SECONDARY = HexColor("#16213e")
CODE_BG = HexColor("#f8f9fa")

try:
    pdfmetrics.registerFont(TTFont('Menlo', '/System/Library/Fonts/Menlo.ttc'))
    MONO = 'Menlo'
except:
    MONO = 'Courier'

s = getSampleStyleSheet()

sty_cover_title = ParagraphStyle('CovTitle', fontName='Helvetica-Bold', fontSize=36,
    textColor=PRIMARY, alignment=TA_CENTER, leading=42, spaceAfter=10)
sty_cover_sub = ParagraphStyle('CovSub', fontName='Helvetica-Bold', fontSize=20,
    textColor=ACCENT, alignment=TA_CENTER, leading=28, spaceAfter=8)
sty_cover_body = ParagraphStyle('CovBody', fontName='Helvetica', fontSize=13,
    textColor=SECONDARY, alignment=TA_CENTER, leading=18, spaceAfter=6)
sty_h1 = ParagraphStyle('MyH1', fontName='Helvetica-Bold', fontSize=20,
    textColor=PRIMARY, spaceBefore=18, spaceAfter=8)
sty_h2 = ParagraphStyle('MyH2', fontName='Helvetica-Bold', fontSize=14,
    textColor=ACCENT, spaceBefore=14, spaceAfter=6)
sty_h3 = ParagraphStyle('MyH3', fontName='Helvetica-Bold', fontSize=12,
    textColor=SECONDARY, spaceBefore=10, spaceAfter=4)
sty_body = ParagraphStyle('MyBody', fontName='Helvetica', fontSize=10,
    textColor=black, alignment=TA_JUSTIFY, leading=14.5, spaceAfter=5)
sty_code = ParagraphStyle('MyCode', fontName=MONO, fontSize=8,
    textColor=HexColor("#333"), leftIndent=10, leading=11, spaceAfter=2, backColor=CODE_BG)
sty_bullet = ParagraphStyle('MyBullet', fontName='Helvetica', fontSize=10,
    textColor=black, leading=14, spaceAfter=2, leftIndent=18, bulletIndent=6)
sty_quote = ParagraphStyle('MyQuote', fontName='Helvetica-Oblique', fontSize=10.5,
    textColor=SECONDARY, leading=15, spaceAfter=8, leftIndent=22, rightIndent=22, alignment=TA_CENTER)
sty_footer = ParagraphStyle('MyFooter', fontName='Helvetica', fontSize=7.5, textColor=gray, alignment=TA_CENTER)

def inline_fmt(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'`([^`]+)`', rf'<font face="{MONO}" size=8>\1</font>', text)
    text = text.replace('---', '—')
    return text

def build_elements(filepath):
    elems = []
    # Cover
    elems.append(Spacer(1, 5*cm))
    elems.append(Paragraph("SCREAMING<br/>ARCHITECTURE", sty_cover_title))
    elems.append(Spacer(1, 0.5*cm))
    elems.append(Paragraph("The 30-Minute Field Guide", sty_cover_sub))
    elems.append(Spacer(1, 0.3*cm))
    elems.append(Paragraph("From Zero to Clean Architecture in One Sitting", sty_cover_body))
    elems.append(Spacer(1, 1*cm))
    div = Table([["━" * 50]], colWidths=[12*cm])
    div.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('TEXTCOLOR',(0,0),(-1,-1),ACCENT),('FONTSIZE',(0,0),(-1,-1),8)]))
    elems.append(div)
    elems.append(Spacer(1, 0.8*cm))
    elems.append(Paragraph(
        "Everything you need to stop writing spaghetti code<br/>"
        "and start designing systems that <b>scream</b> their intent.", sty_cover_body))
    elems.append(Spacer(1, 3*cm))
    elems.append(Paragraph("PromptPolish AI — 2026", sty_footer))
    elems.append(PageBreak())

    # Content
    with open(filepath) as f:
        content = f.read()

    # Strip frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2]

    in_code = False
    code_acc = []

    def flush_code():
        nonlocal code_acc, in_code
        if code_acc:
            txt = ''.join(code_acc)
            elems.append(Preformatted(txt, sty_code))
            elems.append(Spacer(1, 3))
            code_acc = []
            in_code = False

    for line in content.split('\n'):
        if line.strip().startswith('```'):
            if in_code:
                flush_code()
            else:
                in_code = True
                code_acc = []
            continue

        if in_code:
            code_acc.append(line + '\n')
            continue

        if not line.strip():
            elems.append(Spacer(1, 3))
            continue

        if line.startswith('## ') and not line.startswith('### '):
            elems.append(Paragraph(line[3:].strip(), sty_h1))
            continue
        if line.startswith('### '):
            elems.append(Paragraph(line[4:].strip(), sty_h2))
            continue
        if line.startswith('#### '):
            elems.append(Paragraph(line[5:].strip(), sty_h3))
            continue
        if line.startswith('> '):
            elems.append(Paragraph(line[2:].strip(), sty_quote))
            continue
        if line.strip() in ['---', '___']:
            elems.append(Spacer(1, 4))
            d2 = Table([["━" * 60]], colWidths=[14*cm])
            d2.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('TEXTCOLOR',(0,0),(-1,-1),HexColor("#ccc")),('FONTSIZE',(0,0),(-1,-1),5)]))
            elems.append(d2)
            elems.append(Spacer(1, 4))
            continue
        if line.strip().startswith('- '):
            txt = inline_fmt(line.strip()[2:])
            elems.append(Paragraph(f"• {txt}", sty_bullet))
            continue
        if re.match(r'^\d+\.', line.strip()):
            txt = inline_fmt(re.sub(r'^\d+\.\s*', '', line.strip()))
            elems.append(Paragraph(txt, sty_bullet))
            continue

        txt = inline_fmt(line.strip())
        if txt:
            elems.append(Paragraph(txt, sty_body))

    flush_code()
    return elems

def page_cb(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(gray)
    canvas.drawCentredString(A4[0]/2, 1.3*cm, f"PromptPolish AI  —  Screaming Architecture Field Guide  —  Page {doc.page}")
    canvas.restoreState()

outpath = '/tmp/screaming-architecture-guide/screaming-architecture-guide.pdf'
doc = SimpleDocTemplate(outpath, pagesize=A4,
    leftMargin=2.2*cm, rightMargin=2.2*cm, topMargin=2.2*cm, bottomMargin=2.5*cm)

doc.build(build_elements('/tmp/screaming-architecture-guide/guide.md'),
          onFirstPage=page_cb, onLaterPages=page_cb)
print(f"OK: {outpath} ({os.path.getsize(outpath)} bytes)")
