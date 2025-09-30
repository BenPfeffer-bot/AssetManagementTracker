"""
Main entry point for the Portfolio Management Tracker
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from core.loader import fetch_market_data, save_price_data, load_price_data
from reports.onepager_generator import generate_report


def fetch_data():
    """Fetch and save market data for all assets."""
    print("Fetching market data...")
    price_data = fetch_market_data(
        settings.ASSET_TICKERS,
        settings.START_DATE,
        settings.END_DATE
    )
    save_price_data(price_data, settings.PRICES_CSV_PATH)
    print("Market data fetched and saved successfully!")


def generate_weekly_report():
    """Generate the weekly portfolio report."""
    print("Generating weekly report...")
    generate_report()
    print("Report generated successfully!")


def main():
    """Main function to run the portfolio tracker."""
    parser = argparse.ArgumentParser(
        description='Portfolio Management Tracker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --fetch-data          Fetch latest market data
  python main.py --generate-report     Generate weekly report
  python main.py --all                 Fetch data and generate report
        """
    )
    
    parser.add_argument(
        '--fetch-data',
        action='store_true',
        help='Fetch and save market data'
    )
    
    parser.add_argument(
        '--generate-report',
        action='store_true',
        help='Generate weekly portfolio report'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Fetch data and generate report'
    )
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    # Execute requested actions
    if args.all or args.fetch_data:
        fetch_data()
    
    if args.all or args.generate_report:
        generate_weekly_report()


if __name__ == "__main__":
    main()
