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

def create_narrative_pdf(filename):
    dark_pages = [1, 18, 19]
    canvas_class = type('NarrativeCanvas', (TwoPassCanvas,), {
        '_workbook_title': 'THE NARRATIVE WORKBOOK (V2)',
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

    # ----------------------------------------------------
    # PAGE 1: COVER PAGE (Dark)
    # ----------------------------------------------------
    story.append(Spacer(1, 120))
    story.append(Paragraph("SIGNAL & STORY — VOLUME TWO", st['cover_tag']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("The Narrative (v2)", st['cover_title']))
    story.append(Paragraph("The architecture of creator storytelling, tension, character arcs, and serialized lore.", st['cover_sub']))
    story.append(Spacer(1, 140))
    story.append(Paragraph("BY @VEEMETA", st['cover_foot']))
    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 2 & 3: SECTION ONE - THE STORY SPINE (Light)
    # ----------------------------------------------------
    story.append(Paragraph("SECTION ONE", st['section_tag']))
    story.append(Paragraph("The Story Spine", st['section_title']))
    story.append(Paragraph("Every compelling creator narrative has a spine — a structural framework that gives coherence to individual posts.", st['intro_italic']))

    story.extend(make_prompt_block(st, "01", "What was your Inciting Incident?", "The moment or event that set your creator journey in motion...", None, 3))
    story.extend(make_prompt_block(st, "02", "What was the Disruption?", "The shift or realization that meant you could never go back to the old way...", None, 3))
    story.append(PageBreak())

    # Page 3
    story.extend(make_prompt_block(st, "03", "What is the Ongoing Struggle?", "The active friction or challenge you are currently navigating in public...", None, 3))
    story.extend(make_prompt_block(st, "04", "What is the Transformation in Progress?", "How are your beliefs, habits, or standards visibly evolving right now?", None, 3))
    story.extend(make_prompt_block(st, "05", "Describe your New World vision.", "Who are you becoming, and what direction is your story heading?", None, 3))
    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 4 & 5: SECTION TWO - TENSION & RELEASE (Light)
    # ----------------------------------------------------
    story.append(Paragraph("SECTION TWO", st['section_tag']))
    story.append(Paragraph("Tension & Release", st['section_title']))
    story.append(Paragraph("Tension is the engine of attention. Without it, content is information. With it, content becomes an experience.", st['intro_italic']))

    # Tension Callout Box
    t_box = [[
        Paragraph("<b>THE TENSION ARC:</b> Hook &rarr; Reveal &rarr; Release<br/>"
                  "<i>Premature resolution is why most content gets scrolled past. Open the gap early. Widen it in the middle. Close it only when the reader has felt its weight.</i>",
                  ParagraphStyle('TBoxText', parent=st['body'], fontName='Helvetica', fontSize=10, leading=15, textColor=colors.HexColor('#0f172a')))
    ]]
    t_table = Table(t_box, colWidths=[7.0*inch])
    t_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_table)
    story.append(Spacer(1, 14))

    story.extend(make_prompt_block(st, "01", "What is the core tension in your story right now?", "The more honestly you name it, the more your audience will feel it.", ["building vs. doubting", "conviction vs. market reality", "vision vs. execution"], 3))
    story.extend(make_prompt_block(st, "02", "Are you closing tension too fast in your content?", "Review your last 10 posts. Where did you rush to the lesson before earning it?", None, 3))
    story.append(PageBreak())

    # Page 5: Prompts 03 & 04
    story.extend(make_prompt_block(st, "03", "Write a post opening that creates tension without resolving it.", "Hook only. Start with a contradiction, a confession, a number, or a weighted question.", None, 3))
    story.extend(make_prompt_block(st, "04", "What larger tension does your entire account represent?", "This is your macro-tension. It gives every post a place inside a bigger story.", None, 4))
    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 6 & 7: SECTION THREE - THE CHARACTER ARC (Light)
    # ----------------------------------------------------
    story.append(Paragraph("SECTION THREE", st['section_tag']))
    story.append(Paragraph("The Character Arc", st['section_title']))
    story.append(Paragraph("Audiences do not follow brands. They follow people becoming something.", st['intro_italic']))

    # 3 Pillar Cards
    arc_data = [
        [Paragraph("<b>Who I Was</b>", st['body_bold']), Paragraph("<b>The Moment</b>", st['body_bold']), Paragraph("<b>Who I'm Becoming</b>", st['body_bold'])],
        [Paragraph("The old identity & limits.", st['body']), Paragraph("The disruption that changed everything.", st['body']), Paragraph("The new identity taking shape.", st['body'])]
    ]
    arc_t = Table(arc_data, colWidths=[2.25*inch]*3)
    arc_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(arc_t)
    story.append(Spacer(1, 14))

    story.extend(make_prompt_block(st, "01", "Describe who you were in one sharp paragraph.", "The old beliefs, old limits, old ceiling. Write it in past tense.", None, 3))
    story.extend(make_prompt_block(st, "02", "What is visibly changing about you right now?", "Transformation in progress is magnetic. What is still uncertain?", None, 3))
    story.append(PageBreak())

    # Page 7: Prompts 03 & 04
    story.extend(make_prompt_block(st, "03", "What is at stake in your arc?", "What do you stand to lose if the transformation fails? Stakes create investment.", None, 3))
    story.extend(make_prompt_block(st, "04", "How can you make your arc more visible starting this week?", "Arc visibility is a content strategy. How will you show the change?", ["share a before/after moment", "post a living contradiction", "name what is ending"], 4))
    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 8 & 9: SECTION FOUR - SCENE VS SUMMARY (Light)
    # ----------------------------------------------------
    story.append(Paragraph("SECTION FOUR", st['section_tag']))
    story.append(Paragraph("Scene vs. Summary", st['section_title']))
    story.append(Paragraph("Summary keeps the reader outside. Scene pulls them inside. Specificity produces feeling.", st['intro_italic']))

    # Contrast Table
    scene_data = [
        [Paragraph("<b>&cross; SUMMARY (Tells)</b>", ParagraphStyle('SumH', parent=st['body_bold'], textColor=colors.HexColor('#991b1b'))),
         Paragraph("<b>&check; SCENE (Shows)</b>", ParagraphStyle('ScnH', parent=st['body_bold'], textColor=colors.HexColor('#166534')))],
        [Paragraph("\"I learned a lot from that bear market. It was hard but I grew as a builder. Grateful for the lessons.\"", st['body']),
         Paragraph("\"Feb 2023. Floor: 0.8 DOGE. I refreshed the chart every 4 minutes. Hands shaking. I posted anyway.\"", st['body'])]
    ]
    scene_t = Table(scene_data, colWidths=[3.4*inch, 3.4*inch])
    scene_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(scene_t)
    story.append(Spacer(1, 14))

    story.extend(make_prompt_block(st, "01", "Take a recent summary post. Rewrite it as a scene.", "Use specific numbers, named times, physical details, or exact quotes.", None, 3))
    story.extend(make_prompt_block(st, "02", "What moment from your story have you never written as a scene?", "The memory you keep referencing but haven't fully shown...", None, 3))
    story.append(PageBreak())

    # Page 9: Prompt 03
    story.extend(make_prompt_block(st, "03", "What is your signature detail?", "The specific image, number, or detail that makes your content unmistakably yours...", ["a recurring number", "a time of day", "a physical sensation", "a specific object"], 6))
    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 10 & 11: SECTION FIVE - THE RECURRING STORY (Light)
    # ----------------------------------------------------
    story.append(Paragraph("SECTION FIVE", st['section_tag']))
    story.append(Paragraph("The Recurring Story", st['section_title']))
    story.append(Paragraph("Lore is built through repetition with variation. Serialized narrative arcs compound attention over time.", st['intro_italic']))

    story.extend(make_prompt_block(st, "01", "What story thread have you started but never closed?", "Your audience remembers more than you think. What did you leave unresolved?", None, 3))
    story.extend(make_prompt_block(st, "02", "Design a 4-week serial narrative arc.", "Week 1: Plant seed &rarr; Week 2: Deepen &rarr; Week 3: Callback &rarr; Week 4: Payoff.", None, 4))
    story.append(PageBreak())

    # Page 11: Prompts 03 & 04
    story.extend(make_prompt_block(st, "03", "What recurring phrases or images could you seed this month?", "These become your community lore. They reward attentive readers.", None, 3))
    story.extend(make_prompt_block(st, "04", "Write the 1-sentence logline of your creator journey.", "\"A [who] tries to [what] despite [obstacle] — and discovers [truth].\"", None, 4))
    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 12: THE THROUGH-LINE (Dark)
    # ----------------------------------------------------
    story.append(Spacer(1, 60))
    story.append(Paragraph("THE THROUGH-LINE", st['cover_tag']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Structure is not a cage.", st['dark_heading']))
    story.append(Paragraph("It is the thing that sets the story free.", st['dark_gold']))
    story.append(Spacer(1, 16))
    story.append(Paragraph("The creators who build lasting audiences are not more creative than you. They are more intentional.", st['dark_sub']))
    story.append(Spacer(1, 30))

    # Dark Table
    d_data = [
        [Paragraph("<b>STRUCTURE</b>", ParagraphStyle('D1', parent=st['body'], fontName='Helvetica-Bold', textColor=colors.HexColor('#f59e0b'))), Paragraph("gives story form", ParagraphStyle('D2', parent=st['body'], textColor=colors.HexColor('#cbd5e1')))],
        [Paragraph("<b>TENSION</b>", ParagraphStyle('D1', parent=st['body'], fontName='Helvetica-Bold', textColor=colors.HexColor('#f59e0b'))), Paragraph("gives story pull", ParagraphStyle('D2', parent=st['body'], textColor=colors.HexColor('#cbd5e1')))],
        [Paragraph("<b>ARC</b>", ParagraphStyle('D1', parent=st['body'], fontName='Helvetica-Bold', textColor=colors.HexColor('#f59e0b'))), Paragraph("gives story meaning", ParagraphStyle('D2', parent=st['body'], textColor=colors.HexColor('#cbd5e1')))],
    ]
    d_table = Table(d_data, colWidths=[1.8*inch, 3.2*inch])
    d_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1e293b')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#334155')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#334155')),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(d_table)
    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 13: CLOSING (Dark)
    # ----------------------------------------------------
    story.append(Spacer(1, 120))
    story.append(Paragraph("THE QUESTION THAT CHANGES EVERYTHING", ParagraphStyle('AskHead', parent=st['body_bold'], textColor=colors.HexColor('#f59e0b'), alignment=1)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("“Your audience does not need you to have the answers.<br/>They need to feel the weight of the questions you are brave enough to carry in public.”", ParagraphStyle('QClose', parent=st['dark_gold'], fontSize=20, leading=28, alignment=1)))
    story.append(Spacer(1, 20))
    story.append(Paragraph("That is not content. That is story.", ParagraphStyle('QSub2', parent=st['dark_sub'], alignment=1)))
    story.append(Spacer(1, 35))
    story.append(Paragraph("— @veemeta", ParagraphStyle('QAuth', parent=st['body_bold'], textColor=colors.HexColor('#f59e0b'), alignment=1)))

    doc.build(
        story,
        canvasmaker=canvas_class,
        onFirstPage=make_background_callback(dark_pages),
        onLaterPages=make_background_callback(dark_pages)
    )
    print("Built The-Narrative-Workbook-v2.pdf successfully!")

if __name__ == '__main__':
    create_narrative_pdf('workbooks/The-Narrative-Workbook-v2.pdf')
