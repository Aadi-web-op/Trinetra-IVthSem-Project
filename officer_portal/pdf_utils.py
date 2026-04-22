from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
import os
from django.conf import settings
from datetime import datetime

def generate_professional_pdf(json_data, output_buffer):
    """
    Generates a professional legal PDF based on the JSON data.
    """
    # header_y = 750
    # c = canvas.Canvas(output_buffer, pagesize=letter)
    
    # Define Layout
    doc = SimpleDocTemplate(output_buffer, pagesize=letter,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)
    
    Story = []
    styles = getSampleStyleSheet()
    
    # ------------------------------------------------------------------
    # STYLES
    # ------------------------------------------------------------------
    # Title (Center, Bold, Large)
    style_title = ParagraphStyle(
        name='OfficialTitle',
        parent=styles['Heading1'],
        fontName='Times-Bold',
        fontSize=16,
        leading=20,
        alignment=1, # Center
        spaceAfter=6,
        textColor=colors.black
    )
    
    # Subtitle (Center, Normal, Medium)
    style_subtitle = ParagraphStyle(
        name='OfficialSubtitle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=14,
        alignment=1, # Center
        spaceAfter=20,
        textColor=colors.black
    )
    
    # Section Header (Left, Bold, Caps)
    style_heading = ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading3'],
        fontName='Times-Bold',
        fontSize=12,
        leading=14,
        alignment=0, # Left
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.darkblue,
        textTransform='uppercase' 
    )
    
    # Body Text (Justified, Normal)
    style_body = ParagraphStyle(
        name='LegalBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=14,
        alignment=4, # Justify
        spaceAfter=10
    )
    
    # Metadata Label (Bold)
    style_label = ParagraphStyle(
        name='MetaLabel',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=10,
        alignment=0
    )

    # ------------------------------------------------------------------
    # HEADER SECTION
    # ------------------------------------------------------------------
    # Top Logos Placeholder (Text based if image missing)
    banner_path = os.path.join(settings.STATIC_ROOT or '', 'assets', 'header_banner.png')
    
    if os.path.exists(banner_path):
        try:
            im = Image(banner_path, width=480, height=80) 
            im.hAlign = 'CENTER'
            Story.append(im)
            Story.append(Spacer(1, 10))
        except:
            pass # Fallback

    # Official Text Header
    Story.append(Paragraph("CENTRE FOR CYBERCRIME INVESTIGATION TRAINING & RESEARCH", style_title))
    Story.append(Paragraph("Criminal Investigation Department", style_subtitle))
    
    # Separator Line
    Story.append(Paragraph("_" * 85, style_subtitle))
    Story.append(Spacer(1, 15))
    
    # ------------------------------------------------------------------
    # METADATA BLOCK
    # ------------------------------------------------------------------
    case_id = json_data.get('case_id', 'N/A')
    date_str = json_data.get('date', datetime.now().strftime("%d-%b-%Y"))
    subject = json_data.get('title', 'LEGAL OPINION / ANALYSIS REPORT')
    
    # We use a simple table for metadata to align it nicely
    from reportlab.platypus import Table, TableStyle
    
    meta_data = [
        [Paragraph(f"<b>CASE REFERENCE:</b> {case_id}", style_body), Paragraph(f"<b>DATE:</b> {date_str}", style_body)],
        [Paragraph(f"<b>SUBJECT:</b> {subject}", style_body), ""]
    ]
    
    t = Table(meta_data, colWidths=[300, 200])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    Story.append(t)
    Story.append(Spacer(1, 20))

    # ------------------------------------------------------------------
    # CONTENT SECTIONS
    # ------------------------------------------------------------------
    
    # 1. Facts
    if json_data.get('facts'):
        Story.append(Paragraph("1. FACTUAL BACKGROUND", style_heading))
        Story.append(Paragraph(json_data['facts'], style_body))
        
    # 2. Analysis
    if json_data.get('analysis'):
        Story.append(Paragraph("2. LEGAL ANALYSIS & OBSERVATIONS", style_heading))
        Story.append(Paragraph(json_data['analysis'], style_body))

    # 3. Conclusion/Opinion
    if json_data.get('conclusion'):
        Story.append(Paragraph("3. FINAL OPINION / RECOMMENDATION", style_heading))
        Story.append(Paragraph(json_data['conclusion'], style_body))
        
    Story.append(Spacer(1, 40))
    
    # ------------------------------------------------------------------
    # FOOTER / SIGNATURE
    # ------------------------------------------------------------------
    Story.append(Paragraph("_" * 35, style_body))
    Story.append(Paragraph("<b>AUTHORIZED SIGNATORY</b>", style_label))
    Story.append(Paragraph("Cybercrime Division | CCITR", style_label))
    
    doc.build(Story)