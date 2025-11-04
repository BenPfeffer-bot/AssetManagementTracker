"""
Weekly Report Generator for Portfolio Tracker
Generates French-language weekly reports with closing prices
"""

from datetime import datetime
from typing import Dict, List
import pandas as pd
from pathlib import Path

# PDF generation imports
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.pdfgen import canvas
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


class WeeklyReportGenerator:
    """
    Generates weekly reports in French for the teacher.
    """
    
    def __init__(self, assets_info: List[Dict], group_number: int = 7):
        """
        Initialize the report generator.
        
        Args:
            assets_info: List of asset information dictionaries
            group_number: Group number for signature (default 7)
        """
        self.assets_info = assets_info
        self.group_number = group_number
        self.recipient_email = "ckharoubi@escp.eu"
        self.recipient_name = "Madame"
    
    def get_wednesday_date(self, date_str: str = None) -> str:
        """
        Get the most recent Wednesday date or the provided date.
        
        Args:
            date_str: Optional date string in 'YYYY-MM-DD' format
            
        Returns:
            Date string in 'YYYY-MM-DD' format
        """
        if date_str:
            return date_str
        
        # Get today's date
        today = datetime.now()
        
        # Find the most recent Wednesday (0=Monday, 2=Wednesday)
        days_since_wednesday = (today.weekday() - 2) % 7
        wednesday = today - pd.Timedelta(days=days_since_wednesday)
        
        return wednesday.strftime('%Y-%m-%d')
    
    def format_french_date(self, date_str: str) -> str:
        """
        Format date in French style: "30 septembre 2025"
        
        Args:
            date_str: Date string in 'YYYY-MM-DD' format
            
        Returns:
            French formatted date string
        """
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        
        months_fr = {
            1: 'janvier', 2: 'février', 3: 'mars', 4: 'avril',
            5: 'mai', 6: 'juin', 7: 'juillet', 8: 'août',
            9: 'septembre', 10: 'octobre', 11: 'novembre', 12: 'décembre'
        }
        
        day = date_obj.day
        month = months_fr[date_obj.month]
        year = date_obj.year
        
        return f"{day} {month} {year}"
    
    def format_price(self, price: float) -> str:
        """
        Format price in French style with comma as decimal separator.
        
        Args:
            price: Price value
            
        Returns:
            Formatted price string
        """
        # Convert to French format: 600.62 -> 600,62
        return f"{price:.2f}".replace('.', ',')
    
    def generate_email_body(self, closing_prices: Dict[str, float], 
                           report_date: str = None) -> str:
        """
        Generate the email body in French.
        
        Args:
            closing_prices: Dictionary with ticker symbols as keys and prices as values
            report_date: Date for the report (defaults to most recent Wednesday)
            
        Returns:
            Formatted email body
        """
        if report_date is None:
            report_date = self.get_wednesday_date()
        
        french_date = self.format_french_date(report_date)
        
        # Build the asset lines
        asset_lines = []
        for asset in self.assets_info:
            ticker = asset['ticker']
            name = asset['name']
            price = closing_prices.get(ticker, 0.0)
            formatted_price = self.format_price(price)
            
            asset_lines.append(f"{ticker} ({name}): {formatted_price} USD")
        
        # Combine into full email
        email_body = f"""Bonsoir {self.recipient_name},

Veuillez trouver ci-dessous les cours de clôture de ce soir pour les indices/ETF que nous avons sélectionnés dans le cadre du suivi de portefeuille :

{chr(10).join(asset_lines)}

Ces données reflètent les cours de clôture du {french_date}.

Bien cordialement,

le groupe {self.group_number}"""
        
        return email_body
    
    def generate_email_subject(self, report_date: str = None) -> str:
        """
        Generate email subject line.
        
        Args:
            report_date: Date for the report
            
        Returns:
            Email subject string
        """
        if report_date is None:
            report_date = self.get_wednesday_date()
        
        french_date = self.format_french_date(report_date)
        
        return f"Suivi de portefeuille - {french_date}"
    
    def generate_html_body(self, closing_prices: Dict[str, float], 
                          report_date: str = None) -> str:
        """
        Generate HTML version of the email body.
        
        Args:
            closing_prices: Dictionary with ticker symbols as keys and prices as values
            report_date: Date for the report
            
        Returns:
            HTML formatted email body
        """
        if report_date is None:
            report_date = self.get_wednesday_date()
        
        french_date = self.format_french_date(report_date)
        
        # Build the asset table
        asset_rows = []
        for asset in self.assets_info:
            ticker = asset['ticker']
            name = asset['name']
            price = closing_prices.get(ticker, 0.0)
            formatted_price = self.format_price(price)
            
            # Calculate price change if available
            initial_price = asset.get('initial_price', 0)
            if initial_price > 0:
                change_pct = ((price - initial_price) / initial_price) * 100
                change_color = '#10b981' if change_pct >= 0 else '#ef4444'
                change_text = f"{change_pct:+.2f}%".replace('.', ',')
            else:
                change_color = '#6b7280'
                change_text = '-'
            
            asset_rows.append(f"""
                <tr>
                    <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; font-weight: 600;">{ticker}</td>
                    <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; color: #6b7280;">{name}</td>
                    <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; font-weight: 600;">{formatted_price} USD</td>
                    <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; font-weight: 600; color: {change_color};">{change_text}</td>
                </tr>
            """)
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #1f2937;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                }}
                .content {{
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th {{
                    background: #f3f4f6;
                    padding: 12px;
                    text-align: left;
                    font-weight: 600;
                    color: #374151;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 2px solid #e5e7eb;
                    color: #6b7280;
                }}
                .signature {{
                    margin-top: 20px;
                    font-style: italic;
                    color: #374151;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1 style="margin: 0; font-size: 24px;">📊 Suivi de Portefeuille</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">Groupe {self.group_number}</p>
            </div>
            
            <div class="content">
                <p>Bonsoir {self.recipient_name},</p>
                
                <p>Veuillez trouver ci-dessous les cours de clôture de ce soir pour les indices/ETF que nous avons sélectionnés dans le cadre du suivi de portefeuille :</p>
                
                <table>
                    <thead>
                        <tr>
                            <th>Ticker</th>
                            <th>Nom</th>
                            <th>Cours de clôture</th>
                            <th>Variation</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(asset_rows)}
                    </tbody>
                </table>
                
                <p style="color: #6b7280; font-size: 14px; margin-top: 20px;">
                    <strong>Date de référence :</strong> {french_date}
                </p>
                
                <div class="footer">
                    <p>Bien cordialement,</p>
                    <p class="signature">Le groupe {self.group_number}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_body
    
    def get_closing_prices_from_data(self, price_data: pd.DataFrame, 
                                     date_str: str = None) -> Dict[str, float]:
        """
        Extract closing prices from price data for a specific date.
        
        Args:
            price_data: DataFrame with price data
            date_str: Date string (defaults to last available date)
            
        Returns:
            Dictionary of ticker: price
        """
        if date_str:
            # Try to find exact date
            try:
                prices_row = price_data.loc[date_str]
                return prices_row.to_dict()
            except KeyError:
                # Date not found, use last available
                pass
        
        # Use last available date
        last_row = price_data.iloc[-1]
        return last_row.to_dict()
    
    def generate_pdf(self, closing_prices: Dict[str, float], 
                    report_date: str = None,
                    output_dir: str = 'reports/weekly') -> str:
        """
        Generate a PDF report.
        
        Args:
            closing_prices: Dictionary with ticker symbols as keys and prices as values
            report_date: Date for the report
            output_dir: Directory to save PDF
            
        Returns:
            Path to saved PDF file
        """
        if not PDF_AVAILABLE:
            raise ImportError("reportlab library not available. Install with: pip install reportlab")
        
        if report_date is None:
            report_date = self.get_wednesday_date()
        
        french_date = self.format_french_date(report_date)
        
        # Create output directory if needed
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create filename
        filename = f"weekly_report_{report_date}.pdf"
        file_path = output_path / filename
        
        # Create PDF
        doc = SimpleDocTemplate(str(file_path), pagesize=A4,
                               topMargin=0.75*inch, bottomMargin=0.75*inch,
                               leftMargin=0.75*inch, rightMargin=0.75*inch)
        
        # Container for PDF elements
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#374151'),
            spaceAfter=12,
            leading=16,
            fontName='Helvetica'
        )
        
        signature_style = ParagraphStyle(
            'Signature',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#374151'),
            spaceAfter=6,
            leading=16,
            fontName='Helvetica-Oblique',
            alignment=TA_RIGHT
        )
        
        # Add title
        title = Paragraph("📊 Suivi de Portefeuille", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.3*inch))
        
        # Add date
        date_para = Paragraph(f"<b>Date:</b> {french_date}", heading_style)
        elements.append(date_para)
        elements.append(Spacer(1, 0.2*inch))
        
        # Add greeting
        greeting = Paragraph(f"Bonsoir {self.recipient_name},", body_style)
        elements.append(greeting)
        elements.append(Spacer(1, 0.1*inch))
        
        # Add intro text
        intro = Paragraph(
            "Veuillez trouver ci-dessous les cours de clôture de ce soir pour les indices/ETF "
            "que nous avons sélectionnés dans le cadre du suivi de portefeuille :",
            body_style
        )
        elements.append(intro)
        elements.append(Spacer(1, 0.3*inch))
        
        # Create table data
        table_data = [['Ticker', 'Nom', 'Cours de clôture', 'Variation']]
        
        for asset in self.assets_info:
            ticker = asset['ticker']
            name = asset['name']
            price = closing_prices.get(ticker, 0.0)
            formatted_price = self.format_price(price) + " USD"
            
            # Calculate variation
            initial_price = asset.get('initial_price', 0)
            if initial_price > 0:
                variation = ((price - initial_price) / initial_price) * 100
                var_text = f"{variation:+.2f}%".replace('.', ',')
            else:
                var_text = "-"
            
            table_data.append([ticker, name, formatted_price, var_text])
        
        # Create table
        table = Table(table_data, colWidths=[1*inch, 2.5*inch, 1.5*inch, 1*inch])
        
        # Style the table
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Body
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1f2937')),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Ticker
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),     # Name
            ('ALIGN', (2, 1), (2, -1), 'RIGHT'),    # Price
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),   # Variation
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Add footer text
        footer_text = Paragraph(
            f"Ces données reflètent les cours de clôture du {french_date}.",
            body_style
        )
        elements.append(footer_text)
        elements.append(Spacer(1, 0.4*inch))
        
        # Add closing
        closing = Paragraph("Bien cordialement,", signature_style)
        elements.append(closing)
        
        signature = Paragraph(f"Le groupe {self.group_number}", signature_style)
        elements.append(signature)
        
        # Build PDF
        doc.build(elements)
        
        return str(file_path)
    
    def save_report_to_file(self, email_body: str, report_date: str = None,
                           output_dir: str = 'reports/weekly') -> str:
        """
        Save report to a text file.
        
        Args:
            email_body: The formatted email body
            report_date: Date for the report
            output_dir: Directory to save reports
            
        Returns:
            Path to saved file
        """
        if report_date is None:
            report_date = self.get_wednesday_date()
        
        # Create output directory if needed
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create filename
        filename = f"weekly_report_{report_date}.txt"
        file_path = output_path / filename
        
        # Save file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(email_body)
        
        return str(file_path)


def get_next_wednesday_dates(start_date: str, end_date: str) -> List[str]:
    """
    Get all Wednesday dates between start and end dates.
    
    Args:
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format
        
    Returns:
        List of Wednesday dates in 'YYYY-MM-DD' format
    """
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    
    # Generate all dates in range
    all_dates = pd.date_range(start=start, end=end, freq='D')
    
    # Filter for Wednesdays (weekday 2)
    wednesdays = [date.strftime('%Y-%m-%d') for date in all_dates if date.weekday() == 2]
    
    return wednesdays

