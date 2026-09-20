import os
import fitz
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas

class TwoPassCanvas(canvas.Canvas):
    """Two-pass canvas for correct total page counts and background rendering."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        width, height = letter
        is_dark = self._pageNumber in [1, 11, 12]
        
        # Save state to draw decorations on top of page
        self.saveState()
        
        # Subtle top accent bar on light pages
        if not is_dark:
            self.setFillColor(colors.HexColor("#d97706")) # Warm gold top bar
            self.rect(0, height - 6, width, 6, fill=1, stroke=0)

        # Header and Footer (Pages 2+)
        if self._pageNumber > 1:
            if is_dark:
                self.setFont("Helvetica-Bold", 8)
                self.setFillColor(colors.HexColor("#f59e0b"))
                self.drawString(54, height - 32, "SIGNAL & STORY WORKBOOK")
                self.setFillColor(colors.HexColor("#94a3b8"))
                self.drawRightString(width - 54, height - 32, "@veemeta")
                
                self.setFont("Helvetica", 8)
                self.drawString(54, 26, "A Narrative Positioning Framework")
                page_str = f"Page {self._pageNumber} of {page_count}"
                self.drawRightString(width - 54, 26, page_str)
                
                self.setStrokeColor(colors.HexColor("#334155"))
                self.setLineWidth(0.5)
                self.line(54, height - 38, width - 54, height - 38)
                self.line(54, 38, width - 54, 38)
            else:
                self.setFont("Helvetica-Bold", 8)
                self.setFillColor(colors.HexColor("#b45309")) # Rich amber header
                self.drawString(54, height - 32, "SIGNAL & STORY WORKBOOK")
                self.setFillColor(colors.HexColor("#64748b"))
                self.drawRightString(width - 54, height - 32, "@veemeta")
                
                self.setFont("Helvetica", 8)
                self.setFillColor(colors.HexColor("#64748b"))
                self.drawString(54, 26, "Emotional Continuity & Narrative Gravity")
                page_str = f"Page {self._pageNumber} of {page_count}"
                self.drawRightString(width - 54, 26, page_str)
                
                self.setStrokeColor(colors.HexColor("#cbd5e1"))
                self.setLineWidth(0.5)
                self.line(54, height - 38, width - 54, height - 38)
                self.line(54, 38, width - 54, 38)

        self.restoreState()


def draw_background(canvas_obj, doc):
    """Draw background color BEFORE flowables are rendered."""
    canvas_obj.saveState()
    width, height = letter
    is_dark = doc.page in [1, 11, 12]
    
    if is_dark:
        canvas_obj.setFillColor(colors.HexColor("#0f172a")) # Dark slate/navy
    else:
        canvas_obj.setFillColor(colors.HexColor("#faf9f6")) # Warm crisp off-white
    
    canvas_obj.rect(0, 0, width, height, fill=1, stroke=0)
    canvas_obj.restoreState()


def create_signal_and_story_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Dark Theme Styles
    cover_tag_style = ParagraphStyle(
        'CoverTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#f59e0b'),
        spaceAfter=15
    )

    cover_title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=44,
        leading=48,
        textColor=colors.HexColor('#ffffff'),
        spaceAfter=15
    )

    cover_sub_style = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=16,
        leading=22,
        textColor=colors.HexColor('#cbd5e1'),
        spaceAfter=30
    )

    # Light Theme Styles
    section_tag_style = ParagraphStyle(
        'SectionTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#b45309'),
        spaceAfter=4
    )

    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=26,
        leading=30,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=8
    )

    intro_italic_style = ParagraphStyle(
        'IntroItalic',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#475569'),
        spaceAfter=14
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=10
    )

    body_bold_style = ParagraphStyle(
        'BodyBoldCustom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=10
    )

    prompt_num_style = ParagraphStyle(
        'PromptNum',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=24,
        leading=26,
        textColor=colors.HexColor('#b45309')
    )

    prompt_label_style = ParagraphStyle(
        'PromptLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10,
        textColor=colors.HexColor('#78350f')
    )

    prompt_q_style = ParagraphStyle(
        'PromptQuestion',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=4
    )

    prompt_hint_style = ParagraphStyle(
        'PromptHint',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=8
    )

    story = []

    def make_writing_lines(num_lines=4):
        table_data = [[''] for _ in range(num_lines)]
        t = Table(table_data, colWidths=[7.0*inch], rowHeights=[20]*num_lines)
        t.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        return t

    def make_prompt_block(num_str, question, hint, example_list=None, num_lines=4):
        header_table_data = [
            [
                Paragraph(num_str, prompt_num_style),
                [
                    Paragraph("PROMPT", prompt_label_style),
                    Spacer(1, 2),
                    Paragraph(question, prompt_q_style)
                ]
            ]
        ]
        h_table = Table(header_table_data, colWidths=[0.5*inch, 6.5*inch])
        h_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))

        elements = [h_table, Spacer(1, 4)]
        
        if example_list:
            ex_items = [f"• {ex}" for ex in example_list]
            ex_str = " &nbsp;&nbsp;&nbsp;&nbsp; ".join(ex_items)
            ex_style = ParagraphStyle('ExStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor('#64748b'), spaceAfter=6)
            elements.append(Paragraph(f"<b>Examples:</b> {ex_str}", ex_style))
        
        if hint:
            elements.append(Paragraph(hint, prompt_hint_style))
        
        elements.append(make_writing_lines(num_lines))
        elements.append(Spacer(1, 14))
        return elements

    # ----------------------------------------------------
    # PAGE 1: COVER PAGE (Dark)
    # ----------------------------------------------------
    story.append(Spacer(1, 120))
    story.append(Paragraph("A NARRATIVE POSITIONING WORKBOOK FOR X", cover_tag_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Signal & Story", cover_title_style))
    story.append(Paragraph("The art of building influence through emotional continuity — not just content.", cover_sub_style))
    story.append(Spacer(1, 140))
    
    brand_foot = ParagraphStyle('BrandFoot', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor('#f59e0b'))
    story.append(Paragraph("BY @VEEMETA", brand_foot))
    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 2: INTRODUCTION (Light)
    # ----------------------------------------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("THE FOUNDATION", section_tag_style))
    story.append(Paragraph("Influence Over Attention", section_title_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Most people think personal branding is posting consistently, getting engagement, and building followers.", body_style))
    story.append(Paragraph("<b>But attention alone does not create influence.</b>", body_bold_style))
    story.append(Spacer(1, 10))

    # Highlight box
    box_data = [[
        Paragraph("<b>PEOPLE REMEMBER</b><br/>"
                  "• The feeling your content leaves them with<br/>"
                  "• The identity you embody consistently<br/>"
                  "• The atmosphere of your presence<br/>"
                  "• The unfolding story they're witnessing",
                  ParagraphStyle('BoxText', parent=styles['Normal'], fontName='Helvetica', fontSize=10.5, leading=17, textColor=colors.HexColor('#0f172a')))
    ]]
    box_table = Table(box_data, colWidths=[7.0*inch])
    box_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 18),
    ]))
    story.append(box_table)
    story.append(Spacer(1, 20))

    story.append(Paragraph("The strongest creators understand this instinctively.", body_style))
    story.append(Paragraph("They are not simply posting content.<br/><b>They are building narrative gravity.</b>", ParagraphStyle('Gravity', parent=styles['Normal'], fontName='Times-Italic', fontSize=15, leading=20, textColor=colors.HexColor('#b45309'))))
    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 3 & 4: SECTION ONE - LORE (Light)
    # ----------------------------------------------------
    story.append(Paragraph("SECTION ONE", section_tag_style))
    story.append(Paragraph("Lore", section_title_style))
    story.append(Paragraph("The internet rewards ongoing stories — not isolated posts. Your lore transforms an audience into participants.", intro_italic_style))
    story.append(Spacer(1, 4))

    # 3 Cards table
    card_style_head = ParagraphStyle('CHead', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#0f172a'), alignment=1)
    card_style_sub = ParagraphStyle('CSub', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor('#64748b'), alignment=1)

    card_data = [
        [
            Paragraph("<b>Inside Jokes</b>", card_style_head),
            Paragraph("<b>Memorable Moments</b>", card_style_head),
            Paragraph("<b>Symbolic Milestones</b>", card_style_head)
        ],
        [
            Paragraph("Recurring references only your community understands. Creates belonging.", card_style_sub),
            Paragraph("The posts and threads where people say \"I was there for that.\"", card_style_sub),
            Paragraph("Recognizable patterns that mark your evolution over time.", card_style_sub)
        ]
    ]
    card_table = Table(card_data, colWidths=[2.25*inch, 2.25*inch, 2.25*inch])
    card_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(card_table)
    story.append(Spacer(1, 14))

    # Prompt 01
    story.extend(make_prompt_block(
        "01",
        "What moments from your journey feel symbolic or memorable?",
        "Write freely. The best lore comes from moments that felt unremarkable at the time...",
        ["surviving a difficult period", "building during a bear market", "starting your show", "a breakthrough conversation", "rebuilding after failure"],
        num_lines=4
    ))
    story.append(PageBreak())

    # Page 4: Prompts 02 & 03
    story.extend(make_prompt_block(
        "02",
        "What phrases, jokes, or recurring ideas already exist inside your community?",
        "What language are people already borrowing from you?",
        ["\"Do Only Good Everyday\"", "\"believe in something\"", "\"consistency compounds\""],
        num_lines=3
    ))

    story.extend(make_prompt_block(
        "03",
        "What stories are people already associating with you?",
        "Not what you WANT. What already exists naturally? Ask your audience if you're unsure...",
        None,
        num_lines=3
    ))

    # Callout banner
    callout_data = [[
        Paragraph("<b>Lore transforms audiences into participants.</b><br/>"
                  "People begin to feel: <i>\"I was there for that.\"</i> That feeling creates deep attachment.",
                  ParagraphStyle('Callout', parent=styles['Normal'], fontName='Times-Italic', fontSize=11.5, leading=16, textColor=colors.HexColor('#78350f'), alignment=1))
    ]]
    callout_t = Table(callout_data, colWidths=[7.0*inch])
    callout_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fef3c7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#fde68a')),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(callout_t)
    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 5 & 6: SECTION TWO - THE MOVEMENT TEST (Light)
    # ----------------------------------------------------
    story.append(Paragraph("SECTION TWO", section_tag_style))
    story.append(Paragraph("The Movement Test", section_title_style))
    story.append(Paragraph("The highest level of personal branding is movement creation — giving other people language to express themselves.", intro_italic_style))
    
    # Question highlight
    q_box_data = [[
        Paragraph("<b>ASK YOURSELF:</b><br/>"
                  "<i>\"Does my content only express me… or does it give other people language to express themselves too?\"</i>",
                  ParagraphStyle('QText', parent=styles['Normal'], fontName='Times-BoldItalic', fontSize=12, leading=17, textColor=colors.HexColor('#b45309'), alignment=1))
    ]]
    q_table = Table(q_box_data, colWidths=[7.0*inch])
    q_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fffbeb')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#fef3c7')),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(q_table)
    story.append(Spacer(1, 14))

    story.extend(make_prompt_block(
        "01",
        "What larger emotional idea does your content represent?",
        "Go deeper than your niche. What feeling are you really selling?",
        ["freedom", "resilience", "sovereignty", "courage", "reinvention"],
        num_lines=3
    ))

    story.extend(make_prompt_block(
        "02",
        "What kind of people naturally resonate with your energy?",
        "Paint a portrait — not a demographic. Who is this person at 2am when no one's watching?",
        None,
        num_lines=3
    ))
    story.append(PageBreak())

    # Page 6: Prompt 03
    story.extend(make_prompt_block(
        "03",
        "What emotional shift should people feel after interacting with your content?",
        "This is the emotional promise of your brand. Be specific.",
        ["more focused", "calmer", "more ambitious", "inspired to act"],
        num_lines=6
    ))
    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 7: SECTION THREE - SYMBOLS (Light)
    # ----------------------------------------------------
    story.append(Paragraph("SECTION THREE", section_tag_style))
    story.append(Paragraph("Symbols", section_title_style))
    story.append(Paragraph("People begin recognizing your energy before they even read your posts. That's symbolic language working.", intro_italic_style))

    story.extend(make_prompt_block(
        "01",
        "List recurring words or phrases that feel naturally connected to your identity.",
        "These are your brand's core vocabulary...",
        None,
        num_lines=3
    ))

    story.extend(make_prompt_block(
        "02",
        "What visual energy fits your personal brand?",
        "How does your presence look and feel visually?",
        ["minimalist black/gold", "futuristic", "elegant", "tactical"],
        num_lines=2
    ))

    story.extend(make_prompt_block(
        "03",
        "What symbols or metaphors represent your worldview?",
        "What image captures how you move through the world?",
        ["storms", "wolves", "signal towers", "arenas", "tides", "architects"],
        num_lines=2
    ))
    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 8 & 9: SECTION FOUR - CONTINUITY (HIGH CONTRAST REDESIGN!)
    # ----------------------------------------------------
    story.append(Paragraph("SECTION FOUR", section_tag_style))
    story.append(Paragraph("Continuity", section_title_style))
    story.append(Paragraph("Audiences connect to unfolding stories. People should feel: <i>\"Something is happening here.\"</i>", intro_italic_style))
    story.append(Spacer(1, 4))

    # 3 Pillar Cards for Continuity
    cont_card_data = [
        [
            Paragraph("<b>I. Growth</b>", card_style_head),
            Paragraph("<b>II. Tension</b>", card_style_head),
            Paragraph("<b>III. Direction</b>", card_style_head)
        ],
        [
            Paragraph("Let people witness your evolution in real time.", card_style_sub),
            Paragraph("Tension creates emotional momentum. Don't hide the friction.", card_style_sub),
            Paragraph("People follow direction — not stagnation.", card_style_sub)
        ]
    ]
    cont_card_t = Table(cont_card_data, colWidths=[2.25*inch, 2.25*inch, 2.25*inch])
    cont_card_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(cont_card_t)
    story.append(Spacer(1, 14))

    # Prompt 01 (Crystal Clear!)
    story.extend(make_prompt_block(
        "01",
        "What journey are people witnessing through your content right now?",
        "Describe the arc as if you were pitching a documentary about your life...",
        None,
        num_lines=3
    ))

    # Prompt 02 (Crystal Clear!)
    story.extend(make_prompt_block(
        "02",
        "What tension currently exists in your story?",
        "The gap between where you are and where you're going is your most compelling story...",
        None,
        num_lines=3
    ))
    story.append(PageBreak())

    # Page 9: Prompt 03 (Crystal Clear!)
    story.extend(make_prompt_block(
        "03",
        "What future vision are you moving toward publicly?",
        "Where is this story heading? What's the destination your audience is rooting for?",
        None,
        num_lines=8
    ))
    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 10: SECTION FIVE - ATMOSPHERE (Light)
    # ----------------------------------------------------
    story.append(Paragraph("SECTION FIVE", section_tag_style))
    story.append(Paragraph("Atmosphere", section_title_style))
    story.append(Paragraph("People remember atmosphere more than information. Your atmosphere is the emotional weather surrounding your presence.", intro_italic_style))

    story.append(Paragraph("<b>SELECT 3 THAT REPRESENT YOUR IDEAL PRESENCE:</b>", ParagraphStyle('SelHead', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor('#b45309'), spaceAfter=6)))
    
    # 8 Archetype Grid Cards
    atmo_grid = [
        [
            Paragraph("<b>Grounded</b><br/><font color='#475569'>Calm authority. Unshakeable.</font>", body_style),
            Paragraph("<b>Visionary</b><br/><font color='#475569'>Sees what others miss.</font>", body_style),
            Paragraph("<b>Sharp</b><br/><font color='#475569'>Precise. No wasted words.</font>", body_style),
            Paragraph("<b>Resilient</b><br/><font color='#475569'>Built for the long game.</font>", body_style),
        ],
        [
            Paragraph("<b>Focused</b><br/><font color='#475569'>Deep work. Intentional.</font>", body_style),
            Paragraph("<b>Momentum</b><br/><font color='#475569'>Always in motion.</font>", body_style),
            Paragraph("<b>Courage</b><br/><font color='#475569'>Honest. Unafraid.</font>", body_style),
            Paragraph("<b>Elevated</b><br/><font color='#475569'>Aspirational. Pulls up.</font>", body_style),
        ]
    ]
    atmo_table = Table(atmo_grid, colWidths=[1.68*inch]*4)
    atmo_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(atmo_table)
    story.append(Spacer(1, 12))

    story.extend(make_prompt_block(
        "02",
        "What emotional atmosphere currently dominates your content?",
        "Be honest. What do your last 30 posts actually feel like? Is it aligned with who you want to become?",
        None,
        num_lines=2
    ))

    story.extend(make_prompt_block(
        "03",
        "What atmosphere do you want your audience to experience consistently?",
        "If your content were a room, what would it feel like to walk into it?",
        ["focus", "momentum", "courage", "resilience"],
        num_lines=2
    ))
    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 11: THE FINAL PRINCIPLE (Dark Theme with HIGH CONTRAST)
    # ----------------------------------------------------
    story.append(Spacer(1, 60))
    story.append(Paragraph("THE FINAL PRINCIPLE", cover_tag_style))
    story.append(Spacer(1, 10))
    
    p_title = ParagraphStyle('PTitle', parent=styles['Normal'], fontName='Times-Bold', fontSize=32, leading=38, textColor=colors.HexColor('#ffffff'))
    p_title_gold = ParagraphStyle('PTitleGold', parent=styles['Normal'], fontName='Times-BoldItalic', fontSize=32, leading=38, textColor=colors.HexColor('#f59e0b'))
    
    story.append(Paragraph("You do not post because something", p_title))
    story.append(Paragraph("happened.", p_title_gold))
    story.append(Spacer(1, 16))

    p_sub = ParagraphStyle('PSub', parent=styles['Normal'], fontName='Times-Italic', fontSize=15, leading=22, textColor=colors.HexColor('#e2e8f0'))
    story.append(Paragraph("You post because you are shaping narrative, identity, and emotional continuity in public.", p_sub))
    story.append(Paragraph("Over time, consistency becomes credibility. Credibility becomes gravity. And gravity changes opportunity.", p_sub))
    story.append(Spacer(1, 30))

    # Progression Box
    prog_data = [
        [Paragraph("<b>CONSISTENCY</b>", ParagraphStyle('Pr1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#f59e0b'))),
         Paragraph("becomes credibility", ParagraphStyle('Pr2', parent=styles['Normal'], fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#cbd5e1')))],
        [Paragraph("<b>CREDIBILITY</b>", ParagraphStyle('Pr1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#f59e0b'))),
         Paragraph("becomes gravity", ParagraphStyle('Pr2', parent=styles['Normal'], fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#cbd5e1')))],
        [Paragraph("<b>GRAVITY</b>", ParagraphStyle('Pr1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#f59e0b'))),
         Paragraph("changes opportunity", ParagraphStyle('Pr2', parent=styles['Normal'], fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#cbd5e1')))],
    ]
    prog_t = Table(prog_data, colWidths=[1.8*inch, 3.2*inch])
    prog_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1e293b')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#334155')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#334155')),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(prog_t)
    story.append(PageBreak())

    # ----------------------------------------------------
    # PAGE 12: CLOSING QUESTION (Dark Theme with HIGH CONTRAST)
    # ----------------------------------------------------
    story.append(Spacer(1, 120))
    
    q_closing = ParagraphStyle('QClosing', parent=styles['Normal'], fontName='Times-BoldItalic', fontSize=22, leading=30, textColor=colors.HexColor('#ffffff'), alignment=1)
    q_sub_c = ParagraphStyle('QSubC', parent=styles['Normal'], fontName='Times-Italic', fontSize=15, leading=22, textColor=colors.HexColor('#cbd5e1'), alignment=1)
    q_author = ParagraphStyle('QAuthor', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#f59e0b'), alignment=1)

    story.append(Paragraph("ASK YOURSELF:", ParagraphStyle('AskHead', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#f59e0b'), alignment=1)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("“Does my content only express me…<br/>or does it give other people language to express themselves too?”", q_closing))
    story.append(Spacer(1, 20))
    story.append(Paragraph("This is the difference of a brand identity that creates a movement.", q_sub_c))
    story.append(Spacer(1, 35))
    story.append(Paragraph("— @veemeta", q_author))

    doc.build(
        story,
        canvasmaker=TwoPassCanvas,
        onFirstPage=draw_background,
        onLaterPages=draw_background
    )

if __name__ == '__main__':
    create_signal_and_story_pdf('workbooks/Signal-and-Story-Workbook.pdf')
    print("PDF build complete!")
