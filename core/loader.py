"""
Data loading utilities for portfolio management
"""

import json
import pandas as pd
import yfinance as yf
from pathlib import Path
from typing import List, Dict
from datetime import datetime


def load_asset_info(file_path: str = 'data/assets_info.json') -> List[Dict]:
    """
    Load asset information from JSON file.
    
    Args:
        file_path: Path to the assets_info.json file
        
    Returns:
        List of dictionaries containing asset information
    """
    with open(file_path, 'r') as f:
        assets = json.load(f)
    return assets


def load_price_data(file_path: str = 'data/prices.csv') -> pd.DataFrame:
    """
    Load historical price data from CSV file.
    
    Args:
        file_path: Path to the prices.csv file
        
    Returns:
        DataFrame with Date as index and ticker symbols as columns
    """
    if not Path(file_path).exists():
        return pd.DataFrame()
    
    df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
    return df


def fetch_market_data(tickers: List[str], start_date: str, end_date: str = None) -> pd.DataFrame:
    """
    Fetch historical market data using yfinance.
    
    Args:
        tickers: List of ticker symbols
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format (defaults to today)
        
    Returns:
        DataFrame with Date as index and ticker symbols as columns
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Download data for all tickers
    data = yf.download(tickers, start=start_date, end=end_date, progress=False, auto_adjust=True)
    
    # If only one ticker, yfinance returns different structure
    if len(tickers) == 1:
        prices = data['Close'].to_frame()
        prices.columns = tickers
    else:
        # Extract closing prices
        if 'Close' in data.columns.levels[0]:
            prices = data['Close']
        else:
            # If data is already just prices (single level columns)
            prices = data
    
    # Ensure index is named properly
    if prices.index.name != 'Date':
        prices.index.name = 'Date'
    
    # Reset index to make Date a column
    prices = prices.reset_index()
    
    return prices


def save_price_data(price_data: pd.DataFrame, file_path: str = 'data/prices.csv'):
    """
    Save price data to CSV file.
    
    Args:
        price_data: DataFrame with Date column and ticker columns
        file_path: Path to save the CSV file
    """
    price_data.to_csv(file_path, index=False)
    print(f"Price data saved to {file_path}")


def update_price_data(tickers: List[str], file_path: str = 'data/prices.csv'):
    """
    Update price data with latest market data.
    
    Args:
        tickers: List of ticker symbols
        file_path: Path to the prices.csv file
    """
    # Load existing data
    existing_data = load_price_data(file_path)
    
    if existing_data.empty:
        # If no existing data, fetch from start date
        from config.settings import START_DATE
        new_data = fetch_market_data(tickers, START_DATE)
        save_price_data(new_data, file_path)
    else:
        # Fetch only new data since last date
        last_date = existing_data.index.max()
        next_date = (last_date + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        new_data = fetch_market_data(tickers, next_date)
        
        if not new_data.empty:
            # Convert new_data Date to index for concatenation
            new_data = new_data.set_index('Date')
            # Combine with existing data
            combined_data = pd.concat([existing_data, new_data])
            # Remove duplicates and sort
            combined_data = combined_data[~combined_data.index.duplicated(keep='last')]
            combined_data = combined_data.sort_index()
            # Reset index for saving
            combined_data = combined_data.reset_index()
            save_price_data(combined_data, file_path)
        else:
            print("No new data to update")
