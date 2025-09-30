"""
Risk metrics calculations for portfolio analysis
"""

import pandas as pd
import numpy as np


def calculate_correlation_matrix(price_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate correlation matrix for asset returns.
    
    Args:
        price_data: DataFrame with Date as index and ticker symbols as columns
        
    Returns:
        Correlation matrix as DataFrame
    """
    # Calculate daily returns
    returns = price_data.pct_change().dropna()
    
    # Calculate correlation matrix
    correlation_matrix = returns.corr()
    
    return correlation_matrix


def calculate_var(returns_series: pd.Series, confidence_level: float = 0.95) -> float:
    """
    Calculate Value at Risk (VaR) using historical method.
    
    Args:
        returns_series: Series of returns
        confidence_level: Confidence level (default 95%)
        
    Returns:
        VaR as a negative number (loss)
    """
    # Remove NaN values
    returns_clean = returns_series.dropna()
    
    if len(returns_clean) == 0:
        return 0
    
    # Calculate VaR at the specified confidence level
    var = returns_clean.quantile(1 - confidence_level)
    
    return var


def calculate_cvar(returns_series: pd.Series, confidence_level: float = 0.95) -> float:
    """
    Calculate Conditional Value at Risk (CVaR/Expected Shortfall).
    
    Args:
        returns_series: Series of returns
        confidence_level: Confidence level (default 95%)
        
    Returns:
        CVaR as a negative number (expected loss beyond VaR)
    """
    # Remove NaN values
    returns_clean = returns_series.dropna()
    
    if len(returns_clean) == 0:
        return 0
    
    # Calculate VaR
    var = calculate_var(returns_clean, confidence_level)
    
    # Calculate CVaR (average of returns below VaR)
    cvar = returns_clean[returns_clean <= var].mean()
    
    return cvar


def calculate_beta(asset_returns: pd.Series, market_returns: pd.Series) -> float:
    """
    Calculate beta of an asset relative to the market.
    
    Args:
        asset_returns: Series of asset returns
        market_returns: Series of market returns
        
    Returns:
        Beta coefficient
    """
    # Align the two series
    aligned_data = pd.DataFrame({
        'asset': asset_returns,
        'market': market_returns
    }).dropna()
    
    if len(aligned_data) < 2:
        return 0
    
    # Calculate covariance and variance
    covariance = aligned_data['asset'].cov(aligned_data['market'])
    market_variance = aligned_data['market'].var()
    
    if market_variance == 0:
        return 0
    
    beta = covariance / market_variance
    
    return beta


def calculate_downside_deviation(returns_series: pd.Series, target_return: float = 0) -> float:
    """
    Calculate downside deviation (semi-deviation).
    
    Args:
        returns_series: Series of returns
        target_return: Target return threshold (default 0)
        
    Returns:
        Downside deviation
    """
    # Remove NaN values
    returns_clean = returns_series.dropna()
    
    # Calculate downside returns (returns below target)
    downside_returns = returns_clean[returns_clean < target_return]
    
    if len(downside_returns) == 0:
        return 0
    
    # Calculate downside deviation
    downside_deviation = np.sqrt(np.mean((downside_returns - target_return) ** 2))
    
    return downside_deviation


def calculate_sortino_ratio(returns_series: pd.Series, risk_free_rate: float = 0.05, 
                            target_return: float = 0) -> float:
    """
    Calculate Sortino ratio (return-to-downside-risk ratio).
    
    Args:
        returns_series: Series of daily returns
        risk_free_rate: Annual risk-free rate (default 5%)
        target_return: Target return threshold (default 0)
        
    Returns:
        Sortino ratio
    """
    # Calculate annualized return
    mean_daily_return = returns_series.mean()
    annualized_return = mean_daily_return * 252
    
    # Calculate annualized downside deviation
    downside_dev = calculate_downside_deviation(returns_series, target_return)
    annualized_downside_dev = downside_dev * np.sqrt(252)
    
    if annualized_downside_dev == 0:
        return 0
    
    # Calculate Sortino ratio
    sortino_ratio = (annualized_return - risk_free_rate) / annualized_downside_dev
    
    return sortino_ratio
