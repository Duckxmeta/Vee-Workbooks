import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas
from redesign_all_workbooks import TwoPassCanvas, make_background_callback, build_styles, make_prompt_block, make_writing_lines

def create_momentum_pdf(filename):
    dark_pages = [1, 12, 13]
    canvas_class = type('MomentumCanvas', (TwoPassCanvas,), {
        '_workbook_title': 'BUILDING MOMENTUM WORKBOOK',
        '_dark_pages': dark_pages
    })
    
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=50
    )

    st = build_styles()
    story = []

    # COVER (Dark)
    story.append(Spacer(1, 120))
    story.append(Paragraph("EXECUTION & GROWTH FRAMEWORK", st['cover_tag']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Building Momentum", st['cover_title']))
    story.append(Paragraph("A practical guide to becoming someone who cannot be stopped.", st['cover_sub']))
    story.append(Spacer(1, 140))
    story.append(Paragraph("BY @VEEMETA", st['cover_foot']))
    story.append(PageBreak())

    # MODULE 1: THE MOMENTUM MYTH
    story.append(Paragraph("MODULE 1", st['section_tag']))
    story.append(Paragraph("The Momentum Myth", st['section_title']))
    story.append(Paragraph("Momentum begins long before anyone notices. The first 30 days are usually silent.", st['intro_italic']))

    story.extend(make_prompt_block(st, "01", "What project or habit have you started and stopped repeatedly?", "Name the cycle. What friction causes you to stall?", None, 3))
    story.extend(make_prompt_block(st, "02", "What would happen if you stayed consistent for 90 uninterrupted days?", "Write down the exact outcome & identity shift...", None, 3))
    story.append(PageBreak())

    # MODULE 2: UNEXAMINED FRICTION
    story.append(Paragraph("MODULE 2", st['section_tag']))
    story.append(Paragraph("Unexamined Friction", st['section_title']))
    story.append(Paragraph("Friction is not the enemy of momentum. Unexamined friction is.", st['intro_italic']))

    f_rows = [
        [Paragraph("<b>TASK YOU AVOID</b>", st['body_bold']), Paragraph("<b>HIDDEN FEAR OR FRICTION</b>", st['body_bold']), Paragraph("<b>WAY TO REDUCE FRICTION</b>", st['body_bold'])],
        [Paragraph("Writing daily posts", st['body']), Paragraph("Fear of being judged / low quality", st['body']), Paragraph("Use template & 15-min timer", st['body'])],
        [Paragraph("", st['body']), Paragraph("", st['body']), Paragraph("", st['body'])],
        [Paragraph("", st['body']), Paragraph("", st['body']), Paragraph("", st['body'])],
        [Paragraph("", st['body']), Paragraph("", st['body']), Paragraph("", st['body'])],
    ]
    f_t = Table(f_rows, colWidths=[2.2*inch, 2.4*inch, 2.4*inch])
    f_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(f_t)
    story.append(Spacer(1, 14))

    story.extend(make_prompt_block(st, "03", "What single rule will eliminate 80% of your daily friction?", "e.g., Never miss twice, write at 8am before checking email...", None, 3))
    story.append(PageBreak())

    # MODULE 3: DAILY PROOF & RHYTHMS
    story.append(Paragraph("MODULE 3", st['section_tag']))
    story.append(Paragraph("Daily Proof & Rhythms", st['section_title']))
    story.append(Paragraph("Goals inspire. Rhythms sustain. Confidence is created by kept promises.", st['intro_italic']))

    story.extend(make_prompt_block(st, "01", "List 5 daily non-negotiable promises to yourself.", "Small, achievable promises that build unshakeable self-trust...", None, 3))
    story.extend(make_prompt_block(st, "02", "What is your recovery plan when you miss a day?", "Rule: Never miss twice. One missed day is an anomaly; two is a new habit.", None, 3))
    story.append(PageBreak())

    # MODULE 4: THE 90-DAY MOMENTUM SYSTEM
    story.append(Paragraph("MODULE 4", st['section_tag']))
    story.append(Paragraph("The 90-Day Momentum System", st['section_title']))
    story.append(Paragraph("Four rules. Three phases. One direction.", st['intro_italic']))

    story.extend(make_prompt_block(st, "01", "Phase 1 (Days 1–30): Foundation & Concentration", "Single task focus. Eliminate distraction...", None, 3))
    story.extend(make_prompt_block(st, "02", "Phase 2 (Days 31–60): Speed & Compounding", "Increase velocity and output rhythm...", None, 3))
    story.extend(make_prompt_block(st, "03", "Phase 3 (Days 61–90): Expansion & Leverage", "Scale what works and share your system...", None, 3))
    story.append(PageBreak())

    # CLOSING (Dark)
    story.append(Spacer(1, 120))
    story.append(Paragraph("THE MOMENTUM PRINCIPLE", ParagraphStyle('AskHead', parent=st['body_bold'], textColor=colors.HexColor('#f59e0b'), alignment=1)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("“Momentum is not built by perfect days.<br/>It is built by refusing to quit on hard days.”", ParagraphStyle('QClose', parent=st['dark_gold'], fontSize=20, leading=28, alignment=1)))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Speed of recovery is more important than perfection.", ParagraphStyle('QSub2', parent=st['dark_sub'], alignment=1)))
    story.append(Spacer(1, 35))
    story.append(Paragraph("— @veemeta", ParagraphStyle('QAuth', parent=st['body_bold'], textColor=colors.HexColor('#f59e0b'), alignment=1)))

    doc.build(
        story,
        canvasmaker=canvas_class,
        onFirstPage=make_background_callback(dark_pages),
        onLaterPages=make_background_callback(dark_pages)
    )
    print("Built Building-Momentum-Workbook.pdf successfully!")

if __name__ == '__main__':
    create_momentum_pdf('workbooks/Building-Momentum-Workbook.pdf')
