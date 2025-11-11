from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from datetime import datetime
import os
import json
from typing import Dict, Any
import markdown
from io import BytesIO

class ReportGenerator:
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        
        # Custom styles
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=1  # Center
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
            spaceBefore=12
        ))
    
    async def generate_report(
        self,
        query: str,
        synthesis: str,
        agent_results: Dict[str, Any],
        plan: Dict[str, Any]
    ) -> str:
        """Generate comprehensive PDF report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pharma_research_report_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        
        # Title
        title = Paragraph(
            "Pharmaceutical Research Report",
            self.styles['CustomTitle']
        )
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Metadata
        metadata_data = [
            ['Query:', query],
            ['Generated:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ['Research Intent:', plan.get('intent', 'N/A')]
        ]
        metadata_table = Table(metadata_data, colWidths=[2*inch, 4.5*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8eaf6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(metadata_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", self.styles['CustomHeading']))
        
        # Convert markdown to paragraphs
        summary_paragraphs = synthesis.split('\n\n')
        for para in summary_paragraphs:
            if para.strip():
                # Clean markdown formatting for ReportLab
                clean_para = para.replace('#', '').replace('**', '').replace('*', '')
                story.append(Paragraph(clean_para, self.styles['BodyText']))
                story.append(Spacer(1, 0.1*inch))
        
        story.append(PageBreak())
        
        # Agent Results
        story.append(Paragraph("Detailed Agent Findings", self.styles['CustomHeading']))
        
        for agent_name, result in agent_results.items():
            story.append(Paragraph(f"{agent_name.replace('_', ' ').title()}", self.styles['Heading3']))
            
            # Add agent data
            if isinstance(result, dict):
                data = result.get('data', {})
                if isinstance(data, dict):
                    for key, value in data.items():
                        if key != 'analysis':
                            story.append(Paragraph(f"<b>{key}:</b> {str(value)[:200]}", self.styles['BodyText']))
            
            story.append(Spacer(1, 0.2*inch))
        
        # Build PDF
        doc.build(story)
        
        return filepath