"""
Configuration settings for the Portfolio Management Tracker
"""

# Date range for the project
START_DATE = '2025-09-23'
END_DATE = '2025-11-25'

# Initial capital for the portfolio (in USD)
INITIAL_CAPITAL = 100000

# Asset tickers to track
ASSET_TICKERS = ['QQQ', 'IEMG', 'SHV', 'TLT', 'IAU']

# Reporting configuration

REPORT_FREQUENCY = 'weekly'  # weekly reporting

# Risk-free rate for Sharpe ratio calculation (annualized)
RISK_FREE_RATE = 0.04  # 5% annualized

# File paths
ASSETS_INFO_PATH = 'data/assets_info.json'
PRICES_CSV_PATH = 'data/prices.csv'
REPORTS_DIR = 'reports'
CHARTS_DIR = 'reports/charts'
WEEKLY_REPORTS_DIR = 'reports/weekly'

# Email configuration for weekly reports
TEACHER_EMAIL = 'ckharoubi@escp.eu'
GROUP_NUMBER = 7

# # SMTP configuration (for sending emails)
# # Note: Configure these if you want to send emails automatically
# SMTP_SERVER = 'smtp.gmail.com'
# SMTP_PORT = 587
# SENDER_EMAIL = ''  # Set your email here
# SENDER_PASSWORD = ''  # Set your app-specific password here
