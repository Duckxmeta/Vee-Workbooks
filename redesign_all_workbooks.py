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
        dark_pages = getattr(self, '_dark_pages', [1, page_count-1, page_count])
        is_dark = self._pageNumber in dark_pages
        workbook_title = getattr(self, '_workbook_title', 'VEE\'S WORKBOOK')

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
                self.drawString(54, height - 32, workbook_title.upper())
                self.setFillColor(colors.HexColor("#e2e8f0"))
                self.drawRightString(width - 54, height - 32, "@veemeta")
                
                self.setFont("Helvetica", 8)
                self.setFillColor(colors.HexColor("#e2e8f0"))
                self.drawString(54, 26, "A Positioning & Execution Framework")
                page_str = f"Page {self._pageNumber} of {page_count}"
                self.drawRightString(width - 54, 26, page_str)
                
                self.setStrokeColor(colors.HexColor("#334155"))
                self.setLineWidth(0.5)
                self.line(54, height - 38, width - 54, height - 38)
                self.line(54, 38, width - 54, 38)

            else:
                self.setFont("Helvetica-Bold", 8)
                self.setFillColor(colors.HexColor("#b45309")) # Rich amber header
                self.drawString(54, height - 32, workbook_title.upper())
                self.setFillColor(colors.HexColor("#64748b"))
                self.drawRightString(width - 54, height - 32, "@veemeta")
                
                self.setFont("Helvetica", 8)
                self.setFillColor(colors.HexColor("#64748b"))
                self.drawString(54, 26, "Positioning & Influence Library")
                page_str = f"Page {self._pageNumber} of {page_count}"
                self.drawRightString(width - 54, 26, page_str)
                
                self.setStrokeColor(colors.HexColor("#cbd5e1"))
                self.setLineWidth(0.5)
                self.line(54, height - 38, width - 54, height - 38)
                self.line(54, 38, width - 54, 38)

        self.restoreState()


def make_background_callback(dark_pages):
    def draw_background(canvas_obj, doc):
        canvas_obj.saveState()
        width, height = letter
        is_dark = doc.page in dark_pages
        if is_dark:
            canvas_obj.setFillColor(colors.HexColor("#0f172a")) # Rich dark slate
        else:
            canvas_obj.setFillColor(colors.HexColor("#faf9f6")) # Warm crisp off-white
        canvas_obj.rect(0, 0, width, height, fill=1, stroke=0)
        canvas_obj.restoreState()
    return draw_background


def build_styles():
    styles = getSampleStyleSheet()
    
    return {
        'cover_tag': ParagraphStyle('CTag', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=colors.HexColor('#f59e0b'), spaceAfter=14),
        'cover_title': ParagraphStyle('CTitle', parent=styles['Normal'], fontName='Times-Bold', fontSize=40, leading=46, textColor=colors.HexColor('#ffffff'), spaceAfter=14),
        'cover_sub': ParagraphStyle('CSub', parent=styles['Normal'], fontName='Times-Italic', fontSize=15, leading=22, textColor=colors.HexColor('#cbd5e1'), spaceAfter=28),
        'cover_foot': ParagraphStyle('CFoot', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor('#f59e0b')),
        
        'section_tag': ParagraphStyle('STag', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=colors.HexColor('#b45309'), spaceAfter=4),
        'section_title': ParagraphStyle('STitle', parent=styles['Normal'], fontName='Times-Bold', fontSize=26, leading=30, textColor=colors.HexColor('#0f172a'), spaceAfter=8),
        'intro_italic': ParagraphStyle('IItalic', parent=styles['Normal'], fontName='Times-Italic', fontSize=12, leading=16, textColor=colors.HexColor('#334155'), spaceAfter=14),
        
        'body': ParagraphStyle('BodyTextC', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=15, textColor=colors.HexColor('#1e293b'), spaceAfter=10),
        'body_bold': ParagraphStyle('BodyBoldC', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=15, textColor=colors.HexColor('#0f172a'), spaceAfter=10),
        
        'prompt_num': ParagraphStyle('PNum', parent=styles['Normal'], fontName='Times-Italic', fontSize=24, leading=26, textColor=colors.HexColor('#b45309')),
        'prompt_label': ParagraphStyle('PLabel', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=10, textColor=colors.HexColor('#78350f')),
        'prompt_q': ParagraphStyle('PQ', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.HexColor('#0f172a'), spaceAfter=4),
        'prompt_hint': ParagraphStyle('PHint', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=9, leading=13, textColor=colors.HexColor('#475569'), spaceAfter=8),
        
        'dark_heading': ParagraphStyle('DHeading', parent=styles['Normal'], fontName='Times-Bold', fontSize=30, leading=36, textColor=colors.HexColor('#ffffff')),
        'dark_gold': ParagraphStyle('DGold', parent=styles['Normal'], fontName='Times-BoldItalic', fontSize=30, leading=36, textColor=colors.HexColor('#f59e0b')),
        'dark_sub': ParagraphStyle('DSub', parent=styles['Normal'], fontName='Times-Italic', fontSize=14, leading=20, textColor=colors.HexColor('#e2e8f0')),
    }


def make_writing_lines(num_lines=4):
    table_data = [[''] for _ in range(num_lines)]
    t = Table(table_data, colWidths=[7.0*inch], rowHeights=[20]*num_lines)
    t.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    return t


def make_prompt_block(st, num_str, question, hint, example_list=None, num_lines=4):
    header_table_data = [
        [
            Paragraph(num_str, st['prompt_num']),
            [
                Paragraph("PROMPT", st['prompt_label']),
                Spacer(1, 2),
                Paragraph(question, st['prompt_q'])
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
        ex_style = ParagraphStyle('ExStyle', parent=st['body'], fontSize=8.5, leading=12, textColor=colors.HexColor('#64748b'), spaceAfter=6)
        elements.append(Paragraph(f"<b>Examples:</b> {ex_str}", ex_style))
    
    if hint:
        elements.append(Paragraph(hint, st['prompt_hint']))
    
    elements.append(make_writing_lines(num_lines))
    elements.append(Spacer(1, 14))
    return elements

import build_signal_story
import build_narrative
import build_atmosphere
import build_authority
import build_momentum

def main():
    print("Building all 5 redesigned, high-contrast workbooks...")
    
    # 1. Signal and Story
    build_signal_story.create_signal_and_story_pdf('workbooks/Signal-and-Story-Workbook.pdf')
    print("  [1/5] Signal-and-Story-Workbook.pdf DONE")
    
    # 2. The Narrative
    build_narrative.create_narrative_pdf('workbooks/The-Narrative-Workbook-v2.pdf')
    print("  [2/5] The-Narrative-Workbook-v2.pdf DONE")

    # 3. Building Atmosphere
    build_atmosphere.create_atmosphere_pdf('workbooks/Building-Atmosphere-Workbook-v2.pdf')
    print("  [3/5] Building-Atmosphere-Workbook-v2.pdf DONE")

    # 4. Building Authority
    build_authority.create_authority_pdf('workbooks/Building-Authority-Workbook.pdf')
    print("  [4/5] Building-Authority-Workbook.pdf DONE")

    # 5. Building Momentum
    build_momentum.create_momentum_pdf('workbooks/Building-Momentum-Workbook.pdf')
    print("  [5/5] Building-Momentum-Workbook.pdf DONE")

    print("\nALL 5 WORKBOOKS REDESIGNED AND BUILT SUCCESSFULLY!")

if __name__ == '__main__':
    main()
