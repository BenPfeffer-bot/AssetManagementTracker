"""
Portfolio class for tracking and calculating portfolio value
"""

import pandas as pd
import numpy as np
from typing import List, Dict


class Portfolio:
    """
    Represents a portfolio of assets with tracking and valuation capabilities.
    """
    
    def __init__(self, assets_info: List[Dict], initial_capital: float):
        """
        Initialize the portfolio with asset information and starting capital.
        
        Args:
            assets_info: List of dictionaries containing asset details
            initial_capital: Starting capital amount in USD
        """
        self.assets_info = assets_info
        self.initial_capital = initial_capital
        self.shares = {}
        
        # Calculate number of shares for each asset based on initial weights
        for asset in assets_info:
            ticker = asset['ticker']
            weight = asset['initial_weight']
            price = asset['initial_price']
            
            # Calculate dollar amount allocated to this asset
            allocation = initial_capital * weight
            
            # Calculate number of shares (rounded to 2 decimals)
            num_shares = round(allocation / price, 2)
            
            self.shares[ticker] = num_shares
    
    def calculate_value(self, price_data: pd.DataFrame) -> pd.Series:
        """
        Calculate total portfolio value over time.
        
        Args:
            price_data: DataFrame with Date as index and ticker symbols as columns
            
        Returns:
            Series with dates as index and portfolio value as values
        """
        portfolio_value = pd.Series(index=price_data.index, dtype=float)
        
        for date in price_data.index:
            total_value = 0
            for ticker, shares in self.shares.items():
                if ticker in price_data.columns:
                    price = price_data.loc[date, ticker]
                    total_value += shares * price
            
            portfolio_value[date] = total_value
        
        return portfolio_value
    
    def get_current_allocation(self, current_prices: Dict[str, float]) -> pd.DataFrame:
        """
        Get current portfolio allocation.
        
        Args:
            current_prices: Dictionary of ticker -> current price
            
        Returns:
            DataFrame with asset allocation details
        """
        allocation_data = []
        total_value = 0
        
        # Calculate total value first
        for ticker, shares in self.shares.items():
            if ticker in current_prices:
                value = shares * current_prices[ticker]
                total_value += value
        
        # Calculate weights
        for asset in self.assets_info:
            ticker = asset['ticker']
            shares = self.shares[ticker]
            
            if ticker in current_prices:
                price = current_prices[ticker]
                value = shares * price
                weight = value / total_value if total_value > 0 else 0
                
                allocation_data.append({
                    'ticker': ticker,
                    'name': asset['name'],
                    'asset_class': asset['asset_class'],
                    'shares': shares,
                    'price': price,
                    'value': value,
                    'weight': weight,
                    'initial_weight': asset['initial_weight']
                })
        
        return pd.DataFrame(allocation_data)
    
    def get_summary(self) -> Dict:
        """
        Get a summary of the portfolio holdings.
        
        Returns:
            Dictionary with portfolio summary information
        """
        return {
            'initial_capital': self.initial_capital,
            'num_assets': len(self.shares),
            'holdings': self.shares,
            'assets_info': self.assets_info
        }
