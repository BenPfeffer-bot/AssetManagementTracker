"""
Performance metrics calculations for portfolio analysis
"""

import pandas as pd
import numpy as np
from typing import Dict


def calculate_returns(portfolio_value_series: pd.Series) -> pd.DataFrame:
    """
    Calculate daily, weekly, and cumulative returns.
    
    Args:
        portfolio_value_series: Series with dates as index and portfolio values
        
    Returns:
        DataFrame with daily_return, weekly_return, and cumulative_return columns
    """
    returns_df = pd.DataFrame(index=portfolio_value_series.index)
    
    # Daily returns
    returns_df['daily_return'] = portfolio_value_series.pct_change()
    
    # Weekly returns (comparing to 7 days ago)
    returns_df['weekly_return'] = portfolio_value_series.pct_change(periods=7)
    
    # Cumulative returns (from start)
    initial_value = portfolio_value_series.iloc[0]
    returns_df['cumulative_return'] = (portfolio_value_series - initial_value) / initial_value
    
    return returns_df


def calculate_volatility(returns_series: pd.Series, annualize: bool = True) -> float:
    """
    Calculate volatility (standard deviation of returns).
    
    Args:
        returns_series: Series of returns (daily or other frequency)
        annualize: Whether to annualize the volatility (assumes daily returns)
        
    Returns:
        Volatility as a float
    """
    volatility = returns_series.std()
    
    if annualize:
        # Annualize assuming 252 trading days per year
        volatility = volatility * np.sqrt(252)
    
    return volatility


def calculate_sharpe_ratio(returns_series: pd.Series, risk_free_rate: float = 0.05) -> float:
    """
    Calculate the Sharpe ratio.
    
    Args:
        returns_series: Series of daily returns
        risk_free_rate: Annual risk-free rate (default 5%)
        
    Returns:
        Sharpe ratio as a float
    """
    # Calculate annualized return
    mean_daily_return = returns_series.mean()
    annualized_return = mean_daily_return * 252
    
    # Calculate annualized volatility
    volatility = calculate_volatility(returns_series, annualize=True)
    
    # Calculate Sharpe ratio
    if volatility == 0:
        return 0
    
    sharpe_ratio = (annualized_return - risk_free_rate) / volatility
    
    return sharpe_ratio


def calculate_max_drawdown(portfolio_value_series: pd.Series) -> Dict:
    """
    Calculate the maximum drawdown.
    
    Args:
        portfolio_value_series: Series with dates as index and portfolio values
        
    Returns:
        Dictionary with max_drawdown, peak_date, trough_date, and recovery_date
    """
    # Calculate running maximum
    running_max = portfolio_value_series.expanding().max()
    
    # Calculate drawdown
    drawdown = (portfolio_value_series - running_max) / running_max
    
    # Find maximum drawdown
    max_drawdown = drawdown.min()
    
    # Find the date of maximum drawdown
    trough_date = drawdown.idxmin()
    
    # Find the peak before the trough
    peak_date = portfolio_value_series[:trough_date].idxmax()
    
    # Find recovery date (when portfolio exceeds previous peak)
    recovery_date = None
    if trough_date < portfolio_value_series.index[-1]:
        peak_value = portfolio_value_series[peak_date]
        future_values = portfolio_value_series[trough_date:]
        recovery_mask = future_values >= peak_value
        if recovery_mask.any():
            recovery_date = future_values[recovery_mask].index[0]
    
    return {
        'max_drawdown': max_drawdown,
        'max_drawdown_pct': max_drawdown * 100,
        'peak_date': peak_date,
        'trough_date': trough_date,
        'recovery_date': recovery_date
    }


def calculate_total_return(portfolio_value_series: pd.Series) -> float:
    """
    Calculate total return over the period.
    
    Args:
        portfolio_value_series: Series with portfolio values
        
    Returns:
        Total return as a percentage
    """
    initial_value = portfolio_value_series.iloc[0]
    final_value = portfolio_value_series.iloc[-1]
    
    total_return = (final_value - initial_value) / initial_value
    
    return total_return


def calculate_annualized_return(portfolio_value_series: pd.Series) -> float:
    """
    Calculate annualized return.
    
    Args:
        portfolio_value_series: Series with dates as index and portfolio values
        
    Returns:
        Annualized return as a decimal
    """
    total_return = calculate_total_return(portfolio_value_series)
    
    # Calculate number of years
    start_date = portfolio_value_series.index[0]
    end_date = portfolio_value_series.index[-1]
    num_days = (end_date - start_date).days
    num_years = num_days / 365.25
    
    if num_years == 0:
        return 0
    
    # Calculate annualized return
    annualized_return = (1 + total_return) ** (1 / num_years) - 1
    
    return annualized_return
