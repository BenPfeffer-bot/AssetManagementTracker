"""
Helper utilities for the portfolio management system
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import logging
from pathlib import Path


def setup_logger(name: str = 'portfolio_tracker', log_file: str = 'portfolio_tracker.log'):
    """
    Set up a logger for the application.
    
    Args:
        name: Logger name
        log_file: Path to log file
        
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def format_currency(amount: float, currency: str = 'USD') -> str:
    """
    Format a number as currency.
    
    Args:
        amount: Amount to format
        currency: Currency symbol (default USD)
        
    Returns:
        Formatted currency string
    """
    if currency == 'USD':
        return f'${amount:,.2f}'
    else:
        return f'{amount:,.2f} {currency}'


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format a decimal value as percentage.
    
    Args:
        value: Value to format (e.g., 0.15 for 15%)
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    return f'{value * 100:.{decimals}f}%'


def send_email(recipient: str, subject: str, body: str, 
               html_body: str = None, attachments: list = None,
               smtp_server: str = 'smtp.gmail.com', smtp_port: int = 587,
               sender_email: str = None, sender_password: str = None):
    """
    Send an email with optional HTML body and attachments.
    
    Args:
        recipient: Email address of recipient
        subject: Email subject
        body: Plain text body
        html_body: HTML body (optional)
        attachments: List of file paths to attach (optional)
        smtp_server: SMTP server address
        smtp_port: SMTP server port
        sender_email: Sender's email address
        sender_password: Sender's email password
        
    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        # Create message
        message = MIMEMultipart('alternative')
        message['From'] = sender_email
        message['To'] = recipient
        message['Subject'] = subject
        
        # Add plain text body
        part1 = MIMEText(body, 'plain')
        message.attach(part1)
        
        # Add HTML body if provided
        if html_body:
            part2 = MIMEText(html_body, 'html')
            message.attach(part2)
        
        # Add attachments if provided
        if attachments:
            for file_path in attachments:
                if Path(file_path).exists():
                    with open(file_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename={Path(file_path).name}'
                        )
                        message.attach(part)
        
        # Connect to SMTP server and send
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        print(f"Email sent successfully to {recipient}")
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def calculate_weeks_between(start_date: str, end_date: str) -> int:
    """
    Calculate number of weeks between two dates.
    
    Args:
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format
        
    Returns:
        Number of weeks
    """
    from datetime import datetime
    
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    days_diff = (end - start).days
    weeks = days_diff // 7
    
    return weeks
