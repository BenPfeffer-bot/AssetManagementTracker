"""
Script to fetch extended historical data for better analysis
This will fetch data from several months before the project start date
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings
from core.loader import fetch_market_data, save_price_data

"""
This script fetches extended historical price data for all portfolio assets.
It is intended to be run before launching the dashboard to provide at least 6 months
of price history prior to the project start date, enabling richer analytics and
visualizations. The script will download data for all tickers defined in the project
settings, starting from 6 months before the official project start date up to today,
and save the results to the project's prices CSV file.
"""

def fetch_extended_historical_data():
    """
    Fetch extended historical data for portfolio analysis.
    Goes back 6 months before the project start date for better context.
    """
    print("=" * 60)
    print("FETCHING EXTENDED HISTORICAL DATA")
    print("=" * 60)
    print()
    # Calculate extended start date (6 months before project start)
    project_start = datetime.strptime(settings.START_DATE, '%Y-%m-%d')
    extended_start = project_start - timedelta(days=180)  # ~6 months
    extended_start_str = extended_start.strftime('%Y-%m-%d')
    
    print(f"Extended data range:")
    print(f"  Start: {extended_start_str} (6 months before project)")
    print(f"  End:   {datetime.now().strftime('%Y-%m-%d')} (today)")
    print()
    print(f"Assets to fetch: {', '.join(settings.ASSET_TICKERS)}")
    print()
    
    try:
        # Fetch extended data
        print("Fetching data from yfinance...")
        price_data = fetch_market_data(
            settings.ASSET_TICKERS,
            extended_start_str,
            datetime.now().strftime('%Y-%m-%d')
        )
        
        if price_data.empty:
            print("❌ No data received!")
            return False
        
        print(f"✅ Fetched {len(price_data)} days of data")
        print()
        
        # Display sample
        print("Sample data (first 5 rows):")
        print(price_data.head().to_string())
        print()
        print("Sample data (last 5 rows):")
        print(price_data.tail().to_string())
        print()
        
        # Save data
        print(f"Saving to {settings.PRICES_CSV_PATH}...")
        save_price_data(price_data, settings.PRICES_CSV_PATH)
        
        print()
        print("=" * 60)
        print("✅ EXTENDED DATA FETCH COMPLETE")
        print("=" * 60)
        print()
        print(f"Total days: {len(price_data)}")
        print(f"Date range: {price_data['Date'].min()} to {price_data['Date'].max()}")
        print()
        print("You now have richer historical data for better analysis!")
        print("Run the Streamlit dashboard to see improved visualizations.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    fetch_extended_historical_data()
