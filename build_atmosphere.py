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

def create_atmosphere_pdf(filename):
    dark_pages = [1, 14, 15]
    canvas_class = type('AtmosphereCanvas', (TwoPassCanvas,), {
        '_workbook_title': 'BUILDING ATMOSPHERE WORKBOOK (V2)',
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
    story.append(Paragraph("BRAND & ENVIRONMENT FRAMEWORK", st['cover_tag']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Building Atmosphere (v2)", st['cover_title']))
    story.append(Paragraph("Crafting an engaging brand presence, tone of voice, and immersive community ecosystem.", st['cover_sub']))
    story.append(Spacer(1, 140))
    story.append(Paragraph("BY @VEEMETA", st['cover_foot']))
    story.append(PageBreak())

    # MODULE 1: THE ATMOSPHERE CORE
    story.append(Paragraph("MODULE 1", st['section_tag']))
    story.append(Paragraph("The Atmosphere Core", st['section_title']))
    story.append(Paragraph("Atmosphere is the emotional climate surrounding your presence. People join for content; they stay for atmosphere.", st['intro_italic']))

    story.extend(make_prompt_block(st, "01", "When people enter your space, what 5 emotions do you want them to feel?", "Complete the sentence 5 times. Write what you actually want.", None, 4))
    story.extend(make_prompt_block(st, "02", "What 3 words define your ideal brand atmosphere?", "Grounded, Sharp, Visionary, Calm, Resilient, Focused, Courageous...", None, 2))
    story.append(PageBreak())

    # MODULE 2: THE ATMOSPHERE AUDIT
    story.append(Paragraph("MODULE 2", st['section_tag']))
    story.append(Paragraph("The Atmosphere Audit", st['section_title']))
    story.append(Paragraph("You cannot improve what you have not honestly assessed. Rate your current reality from 1 to 10.", st['intro_italic']))

    audit_headers = [Paragraph("<b>AREA</b>", st['body_bold']), Paragraph("<b>SCORE (1–10)</b>", st['body_bold']), Paragraph("<b>CURRENT REALITY & NOTES</b>", st['body_bold'])]
    audit_rows = [audit_headers]
    areas = ["Clarity", "Energy", "Trust", "Consistency", "Leadership Presence", "Momentum", "Belonging", "Hope"]
    for a in areas:
        audit_rows.append([Paragraph(f"<b>{a}</b>", st['body']), Paragraph("[ &nbsp;&nbsp;&nbsp; / 10 ]", st['body']), Paragraph("", st['body'])])

    audit_table = Table(audit_rows, colWidths=[2.0*inch, 1.2*inch, 3.8*inch])
    audit_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(audit_table)
    story.append(Spacer(1, 14))

    story.extend(make_prompt_block(st, "03", "Which two scores surprised you most, and why?", "Look at your lowest scores. Those are your primary opportunities.", None, 3))
    story.append(PageBreak())

    # MODULE 3: THE ATMOSPHERE GAP
    story.append(Paragraph("MODULE 3", st['section_tag']))
    story.append(Paragraph("The Atmosphere Gap", st['section_title']))
    story.append(Paragraph("The gap between your current atmosphere and desired one is your strategic agenda.", st['intro_italic']))

    story.extend(make_prompt_block(st, "01", "Describe your current atmosphere honestly in one paragraph.", "What does it feel like to be in your world right now?", None, 3))
    story.extend(make_prompt_block(st, "02", "Describe your ideal atmosphere 6 months from now.", "Write in present tense as if it is already true...", None, 3))
    story.extend(make_prompt_block(st, "03", "Identify the 3 largest gaps between current and desired state.", "Name them clearly. Then close them deliberately.", None, 3))
    story.append(PageBreak())

    # MODULE 4: THE FIVE ATMOSPHERE DRIVERS
    story.append(Paragraph("MODULE 4", st['section_tag']))
    story.append(Paragraph("The Five Atmosphere Drivers", st['section_title']))
    story.append(Paragraph("Atmosphere is engineered through 5 repeatable drivers: Language, Rituals, Symbols, Standards, and Leadership Presence.", st['intro_italic']))

    story.extend(make_prompt_block(st, "01", "Driver 1: Language — 5 phrases that reinforce your mission.", "Memorable, repeatable, and authentic phrases your community shares...", None, 3))
    story.extend(make_prompt_block(st, "02", "Driver 2: Rituals — 3 new recurring rituals to introduce.", "Daily questions, weekly check-ins, opening monologues, spotlighting...", None, 3))
    story.append(PageBreak())

    # Page 6: Drivers 3, 4, 5
    story.extend(make_prompt_block(st, "03", "Driver 3: Symbols — What visual symbols represent your movement?", "Icons, colors, metaphors, emojis, visual motifs...", None, 2))
    story.extend(make_prompt_block(st, "04", "Driver 4: Standards — Your top 5 non-negotiable community standards.", "What behavior is encouraged, respected, or never tolerated?", None, 3))
    story.extend(make_prompt_block(st, "05", "Driver 5: Leadership Presence — What emotional state do you model?", "Calm, conviction, courage, curiosity, resilience...", None, 3))
    story.append(PageBreak())

    # MODULE 5: NARRATIVE AND ATMOSPHERE
    story.append(Paragraph("MODULE 5", st['section_tag']))
    story.append(Paragraph("Narrative & Atmosphere", st['section_title']))
    story.append(Paragraph("Stories create emotional weather. The story your community tells about itself becomes its atmosphere.", st['intro_italic']))

    story.extend(make_prompt_block(st, "01", "What story are people currently telling about your movement?", "Be honest. What is the word-of-mouth narrative?", None, 3))
    story.extend(make_prompt_block(st, "02", "Write your defining 3-part narrative spine:", "1. We are the people who...\n2. We believe...\n3. We are building...", None, 4))
    story.append(PageBreak())

    # MODULE 6: ATMOSPHERE THROUGH CONTENT
    story.append(Paragraph("MODULE 6", st['section_tag']))
    story.append(Paragraph("Atmosphere Through Content", st['section_title']))
    story.append(Paragraph("Every post is an atmospheric signal. Audit your last 20 posts by emotional category.", st['intro_italic']))

    c_audit_rows = [
        [Paragraph("<b>CATEGORY</b>", st['body_bold']), Paragraph("<b>DESCRIPTION</b>", st['body_bold']), Paragraph("<b>POST COUNT (OUT OF 20)</b>", st['body_bold'])],
        [Paragraph("Fear / Threat", st['body']), Paragraph("Warns, alerts, or creates urgency through threat.", st['body']), Paragraph("", st['body'])],
        [Paragraph("Hope / Possibility", st['body']), Paragraph("Inspires, uplifts, or points toward possibility.", st['body']), Paragraph("", st['body'])],
        [Paragraph("Education", st['body']), Paragraph("Teaches a skill, framework, or clear insight.", st['body']), Paragraph("", st['body'])],
        [Paragraph("Humor / Connection", st['body']), Paragraph("Creates belonging through shared laughter.", st['body']), Paragraph("", st['body'])],
        [Paragraph("Inspiration", st['body']), Paragraph("Elevates mood and activates motivation.", st['body']), Paragraph("", st['body'])],
        [Paragraph("Challenge", st['body']), Paragraph("Confronts, disrupts, or demands more.", st['body']), Paragraph("", st['body'])],
    ]
    c_table = Table(c_audit_rows, colWidths=[1.8*inch, 3.4*inch, 1.8*inch])
    c_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(c_table)
    story.append(Spacer(1, 14))

    story.extend(make_prompt_block(st, "03", "Which emotional category dominates, and is it intentional?", "What missing category does your desired atmosphere require?", None, 3))
    story.append(PageBreak())

    # MODULE 7 & 8: DAILY PRACTICE & BLUEPRINT
    story.append(Paragraph("MODULE 7 & 8", st['section_tag']))
    story.append(Paragraph("The Atmosphere Blueprint", st['section_title']))
    story.append(Paragraph("Every day ask yourself: What am I amplifying? Rewarding? Repeating? Tolerating? Embodying?", st['intro_italic']))

    story.extend(make_prompt_block(st, "01", "My Desired Atmosphere (3 Words):", "The 3 core words defining your brand climate...", None, 2))
    story.extend(make_prompt_block(st, "02", "My Leadership Commitment:", "The emotional state I commit to embodying every single day...", None, 3))
    story.extend(make_prompt_block(st, "03", "Daily Action Checklist:", "What I will do daily to reinforce this atmosphere...", None, 4))
    story.append(PageBreak())

    # CLOSING (Dark)
    story.append(Spacer(1, 120))
    story.append(Paragraph("CLOSING THOUGHT", ParagraphStyle('AskHead', parent=st['body_bold'], textColor=colors.HexColor('#f59e0b'), alignment=1)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("“Atmosphere is not created by one post.<br/>It is created by thousands of small signals repeated with intention.”", ParagraphStyle('QClose', parent=st['dark_gold'], fontSize=20, leading=28, alignment=1)))
    story.append(Spacer(1, 20))
    story.append(Paragraph("People join because of content. People stay because of atmosphere.<br/>Movements grow because atmosphere becomes culture.", ParagraphStyle('QSub2', parent=st['dark_sub'], alignment=1)))
    story.append(Spacer(1, 35))
    story.append(Paragraph("— @veemeta", ParagraphStyle('QAuth', parent=st['body_bold'], textColor=colors.HexColor('#f59e0b'), alignment=1)))

    doc.build(
        story,
        canvasmaker=canvas_class,
        onFirstPage=make_background_callback(dark_pages),
        onLaterPages=make_background_callback(dark_pages)
    )
    print("Built Building-Atmosphere-Workbook-v2.pdf successfully!")

if __name__ == '__main__':
    create_atmosphere_pdf('workbooks/Building-Atmosphere-Workbook-v2.pdf')
