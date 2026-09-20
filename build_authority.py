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

def create_authority_pdf(filename):
    dark_pages = [1, 14, 15]
    canvas_class = type('AuthorityCanvas', (TwoPassCanvas,), {
        '_workbook_title': 'BUILDING AUTHORITY WORKBOOK',
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
    story.append(Paragraph("BRAND POSITIONING & INFLUENCE WORKBOOK", st['cover_tag']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Building Authority", st['cover_title']))
    story.append(Paragraph("Practical frameworks for establishing industry expertise, trust, and premium market positioning.", st['cover_sub']))
    story.append(Spacer(1, 140))
    story.append(Paragraph("BY @VEEMETA", st['cover_foot']))
    story.append(PageBreak())

    # MODULE 1: THE 3 PILLARS OF AUTHORITY
    story.append(Paragraph("MODULE 1", st['section_tag']))
    story.append(Paragraph("The Three Pillars of Authority", st['section_title']))
    story.append(Paragraph("Authority is built on Competence, Consistency, and Character. Without all three, influence is fragile.", st['intro_italic']))

    p_data = [
        [Paragraph("<b>I. Competence</b>", st['body_bold']), Paragraph("<b>II. Consistency</b>", st['body_bold']), Paragraph("<b>III. Character</b>", st['body_bold'])],
        [Paragraph("Proof of knowledge & results.", st['body']), Paragraph("Reliable presence & message.", st['body']), Paragraph("Integrity, ethics & trust.", st['body'])]
    ]
    p_t = Table(p_data, colWidths=[2.25*inch]*3)
    p_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(p_t)
    story.append(Spacer(1, 14))

    story.extend(make_prompt_block(st, "01", "What is your core domain of unquestioned competence?", "Where do your results, knowledge, or experience stand out?", None, 3))
    story.extend(make_prompt_block(st, "02", "What proof points currently validate your authority?", "Case studies, testimonials, metrics, public track record...", None, 3))
    story.append(PageBreak())

    # MODULE 2: THE AUTHORITY AUDIT
    story.append(Paragraph("MODULE 2", st['section_tag']))
    story.append(Paragraph("The Authority Audit", st['section_title']))
    story.append(Paragraph("Honest evaluation across 5 critical dimensions of market authority.", st['intro_italic']))

    a_rows = [
        [Paragraph("<b>DIMENSION</b>", st['body_bold']), Paragraph("<b>SCORE (1–10)</b>", st['body_bold']), Paragraph("<b>STRATEGIC ACTION</b>", st['body_bold'])],
        [Paragraph("Domain Proof", st['body']), Paragraph("[ &nbsp;&nbsp;&nbsp; / 10 ]", st['body']), Paragraph("", st['body'])],
        [Paragraph("Clarity of Stance", st['body']), Paragraph("[ &nbsp;&nbsp;&nbsp; / 10 ]", st['body']), Paragraph("", st['body'])],
        [Paragraph("Content Depth", st['body']), Paragraph("[ &nbsp;&nbsp;&nbsp; / 10 ]", st['body']), Paragraph("", st['body'])],
        [Paragraph("Network Gravity", st['body']), Paragraph("[ &nbsp;&nbsp;&nbsp; / 10 ]", st['body']), Paragraph("", st['body'])],
        [Paragraph("Emotional Composure", st['body']), Paragraph("[ &nbsp;&nbsp;&nbsp; / 10 ]", st['body']), Paragraph("", st['body'])],
    ]
    a_t = Table(a_rows, colWidths=[2.0*inch, 1.2*inch, 3.8*inch])
    a_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(a_t)
    story.append(Spacer(1, 14))

    story.extend(make_prompt_block(st, "03", "What single action would double your proof in 90 days?", "Focus on your single highest-leverage asset...", None, 3))
    story.append(PageBreak())

    # MODULE 3: THE CONVICTION ENGINE
    story.append(Paragraph("MODULE 3", st['section_tag']))
    story.append(Paragraph("The Conviction Engine", st['section_title']))
    story.append(Paragraph("Authority requires opinions. Neutrality creates zero gravity.", st['intro_italic']))

    story.extend(make_prompt_block(st, "01", "What opinion in your industry are you willing to defend publicly?", "What do you believe that most people in your field get wrong?", None, 3))
    story.extend(make_prompt_block(st, "02", "What is your non-negotiable professional code?", "What will you never compromise on, even for money or attention?", None, 3))
    story.extend(make_prompt_block(st, "03", "What is your 'Borrowed vs Owned' Authority balance?", "How much of your authority comes from your own original work vs affiliations?", None, 3))
    story.append(PageBreak())

    # MODULE 4: THE 90-DAY AUTHORITY BUILD
    story.append(Paragraph("MODULE 4", st['section_tag']))
    story.append(Paragraph("The 90-Day Authority Build", st['section_title']))
    story.append(Paragraph("Three phases to systematically build authority and industry positioning.", st['intro_italic']))

    story.extend(make_prompt_block(st, "01", "Phase 1 (Days 1–30): Foundation & Proof Assets", "What foundational breakdown or flagship guide will you publish?", None, 3))
    story.extend(make_prompt_block(st, "02", "Phase 2 (Days 31–60): Deep Signal Content", "How will you elevate your weekly content depth?", None, 3))
    story.extend(make_prompt_block(st, "03", "Phase 3 (Days 61–90): Distribution & Alliances", "Who are the key peers and platforms you will collaborate with?", None, 3))
    story.append(PageBreak())

    # MODULE 5: THE BUILDER'S OATH (Dark)
    story.append(Spacer(1, 120))
    story.append(Paragraph("THE BUILDER'S OATH", ParagraphStyle('AskHead', parent=st['body_bold'], textColor=colors.HexColor('#f59e0b'), alignment=1)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("“I will not confuse attention with authority.<br/>I will build real competence, publish honest proof, and stand on conviction.”", ParagraphStyle('QClose', parent=st['dark_gold'], fontSize=20, leading=28, alignment=1)))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Consistency becomes credibility. Credibility becomes gravity.", ParagraphStyle('QSub2', parent=st['dark_sub'], alignment=1)))
    story.append(Spacer(1, 35))
    story.append(Paragraph("— @veemeta", ParagraphStyle('QAuth', parent=st['body_bold'], textColor=colors.HexColor('#f59e0b'), alignment=1)))

    doc.build(
        story,
        canvasmaker=canvas_class,
        onFirstPage=make_background_callback(dark_pages),
        onLaterPages=make_background_callback(dark_pages)
    )
    print("Built Building-Authority-Workbook.pdf successfully!")

if __name__ == '__main__':
    create_authority_pdf('workbooks/Building-Authority-Workbook.pdf')
