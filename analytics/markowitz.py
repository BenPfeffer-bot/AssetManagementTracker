"""
Markowitz Modern Portfolio Theory Analysis
Efficient frontier calculation and portfolio optimization
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, List
import plotly.graph_objects as go
from scipy.optimize import minimize


def calculate_portfolio_performance(weights: np.ndarray, mean_returns: np.ndarray, 
                                   cov_matrix: np.ndarray) -> Tuple[float, float]:
    """
    Calculate portfolio return and risk (volatility).
    
    Args:
        weights: Asset weights array
        mean_returns: Expected returns for each asset
        cov_matrix: Covariance matrix of returns
        
    Returns:
        Tuple of (return, volatility)
    """
    portfolio_return = np.sum(mean_returns * weights)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    return portfolio_return, portfolio_volatility


def negative_sharpe_ratio(weights: np.ndarray, mean_returns: np.ndarray, 
                          cov_matrix: np.ndarray, risk_free_rate: float = 0.05) -> float:
    """
    Calculate negative Sharpe ratio (for minimization).
    
    Args:
        weights: Asset weights
        mean_returns: Expected returns
        cov_matrix: Covariance matrix
        risk_free_rate: Risk-free rate (default 5%)
        
    Returns:
        Negative Sharpe ratio
    """
    p_return, p_volatility = calculate_portfolio_performance(weights, mean_returns, cov_matrix)
    
    if p_volatility == 0:
        return 0
    
    sharpe_ratio = (p_return - risk_free_rate) / p_volatility
    return -sharpe_ratio  # Negative because we minimize


def portfolio_volatility(weights: np.ndarray, mean_returns: np.ndarray, 
                        cov_matrix: np.ndarray) -> float:
    """
    Calculate portfolio volatility (for minimization).
    
    Args:
        weights: Asset weights
        mean_returns: Expected returns
        cov_matrix: Covariance matrix
        
    Returns:
        Portfolio volatility
    """
    return calculate_portfolio_performance(weights, mean_returns, cov_matrix)[1]


def optimize_portfolio(mean_returns: np.ndarray, cov_matrix: np.ndarray, 
                      objective: str = 'sharpe', risk_free_rate: float = 0.05) -> Dict:
    """
    Optimize portfolio using mean-variance optimization.
    
    Args:
        mean_returns: Expected returns for each asset
        cov_matrix: Covariance matrix
        objective: 'sharpe' for max Sharpe or 'min_vol' for minimum volatility
        risk_free_rate: Risk-free rate
        
    Returns:
        Dictionary with optimal weights and performance metrics
    """
    num_assets = len(mean_returns)
    
    # Constraints: weights sum to 1
    constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    
    # Bounds: weights between 0 and 1 (no short selling)
    bounds = tuple((0, 1) for _ in range(num_assets))
    
    # Initial guess: equal weights
    initial_weights = np.array([1/num_assets] * num_assets)
    
    # Choose objective function
    if objective == 'sharpe':
        obj_func = lambda w: negative_sharpe_ratio(w, mean_returns, cov_matrix, risk_free_rate)
    else:  # min_vol
        obj_func = lambda w: portfolio_volatility(w, mean_returns, cov_matrix)
    
    # Optimize
    result = minimize(obj_func, initial_weights, method='SLSQP', 
                     bounds=bounds, constraints=constraints)
    
    if not result.success:
        raise ValueError("Optimization failed")
    
    optimal_weights = result.x
    opt_return, opt_volatility = calculate_portfolio_performance(
        optimal_weights, mean_returns, cov_matrix
    )
    opt_sharpe = (opt_return - risk_free_rate) / opt_volatility if opt_volatility > 0 else 0
    
    return {
        'weights': optimal_weights,
        'return': opt_return,
        'volatility': opt_volatility,
        'sharpe_ratio': opt_sharpe
    }


def generate_efficient_frontier(mean_returns: np.ndarray, cov_matrix: np.ndarray, 
                               num_portfolios: int = 100, 
                               risk_free_rate: float = 0.05) -> pd.DataFrame:
    """
    Generate efficient frontier by optimizing portfolios at different target returns.
    
    Args:
        mean_returns: Expected returns for each asset
        cov_matrix: Covariance matrix
        num_portfolios: Number of portfolios to generate
        risk_free_rate: Risk-free rate
        
    Returns:
        DataFrame with returns, volatilities, and Sharpe ratios
    """
    num_assets = len(mean_returns)
    
    # Generate target returns
    min_return = np.min(mean_returns)
    max_return = np.max(mean_returns)
    target_returns = np.linspace(min_return, max_return, num_portfolios)
    
    results = []
    
    for target_return in target_returns:
        try:
            # Constraints: weights sum to 1 and target return achieved
            constraints = [
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                {'type': 'eq', 'fun': lambda x: np.sum(x * mean_returns) - target_return}
            ]
            
            bounds = tuple((0, 1) for _ in range(num_assets))
            initial_weights = np.array([1/num_assets] * num_assets)
            
            # Minimize volatility for this target return
            result = minimize(
                lambda w: portfolio_volatility(w, mean_returns, cov_matrix),
                initial_weights,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints,
                options={'maxiter': 500}
            )
            
            if result.success:
                weights = result.x
                ret, vol = calculate_portfolio_performance(weights, mean_returns, cov_matrix)
                sharpe = (ret - risk_free_rate) / vol if vol > 0 else 0
                
                results.append({
                    'return': ret,
                    'volatility': vol,
                    'sharpe_ratio': sharpe
                })
        except:
            continue
    
    return pd.DataFrame(results)


def generate_random_portfolios(mean_returns: np.ndarray, cov_matrix: np.ndarray, 
                               num_portfolios: int = 5000,
                               risk_free_rate: float = 0.05) -> pd.DataFrame:
    """
    Generate random portfolio allocations for Monte Carlo simulation.
    
    Args:
        mean_returns: Expected returns
        cov_matrix: Covariance matrix
        num_portfolios: Number of random portfolios
        risk_free_rate: Risk-free rate
        
    Returns:
        DataFrame with portfolio metrics
    """
    num_assets = len(mean_returns)
    results = []
    
    for _ in range(num_portfolios):
        # Generate random weights
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)  # Normalize to sum to 1
        
        ret, vol = calculate_portfolio_performance(weights, mean_returns, cov_matrix)
        sharpe = (ret - risk_free_rate) / vol if vol > 0 else 0
        
        results.append({
            'return': ret,
            'volatility': vol,
            'sharpe_ratio': sharpe
        })
    
    return pd.DataFrame(results)


def calculate_expected_returns(price_data: pd.DataFrame, method: str = 'mean') -> pd.Series:
    """
    Calculate expected returns for each asset.
    
    Args:
        price_data: DataFrame with asset prices
        method: 'mean' for historical mean or 'capm' for CAPM
        
    Returns:
        Series of expected annualized returns
    """
    # Calculate daily returns
    returns = price_data.pct_change().dropna()
    
    if method == 'mean':
        # Use historical mean and annualize
        expected_returns = returns.mean() * 252  # 252 trading days
    else:
        # For now, default to mean
        expected_returns = returns.mean() * 252
    
    return expected_returns


def calculate_covariance_matrix(price_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate annualized covariance matrix of returns.
    
    Args:
        price_data: DataFrame with asset prices
        
    Returns:
        Covariance matrix
    """
    returns = price_data.pct_change().dropna()
    # Annualize covariance matrix
    cov_matrix = returns.cov() * 252
    return cov_matrix


def plot_efficient_frontier(efficient_frontier: pd.DataFrame, 
                           random_portfolios: pd.DataFrame,
                           current_portfolio: Dict,
                           optimal_portfolios: Dict,
                           asset_data: pd.DataFrame = None) -> go.Figure:
    """
    Create an interactive efficient frontier plot.
    
    Args:
        efficient_frontier: DataFrame with efficient frontier data
        random_portfolios: DataFrame with random portfolios
        current_portfolio: Dict with current portfolio metrics
        optimal_portfolios: Dict with max Sharpe and min volatility portfolios
        asset_data: Optional DataFrame with individual asset metrics
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    # Plot random portfolios (Monte Carlo simulation)
    fig.add_trace(go.Scatter(
        x=random_portfolios['volatility'] * 100,
        y=random_portfolios['return'] * 100,
        mode='markers',
        name='Random Portfolios',
        marker=dict(
            size=4,
            color=random_portfolios['sharpe_ratio'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Sharpe<br>Ratio"),
            opacity=0.3
        ),
        hovertemplate='<b>Random Portfolio</b><br>' +
                     'Return: %{y:.2f}%<br>' +
                     'Volatility: %{x:.2f}%<br>' +
                     '<extra></extra>'
    ))
    
    # Plot efficient frontier
    fig.add_trace(go.Scatter(
        x=efficient_frontier['volatility'] * 100,
        y=efficient_frontier['return'] * 100,
        mode='lines',
        name='Efficient Frontier',
        line=dict(color='#FF6B6B', width=4),
        hovertemplate='<b>Efficient Frontier</b><br>' +
                     'Return: %{y:.2f}%<br>' +
                     'Volatility: %{x:.2f}%<br>' +
                     '<extra></extra>'
    ))
    
    # Plot current portfolio
    fig.add_trace(go.Scatter(
        x=[current_portfolio['volatility'] * 100],
        y=[current_portfolio['return'] * 100],
        mode='markers',
        name='Current Portfolio',
        marker=dict(
            size=15,
            color='#4ECDC4',
            symbol='star',
            line=dict(color='white', width=2)
        ),
        hovertemplate='<b>Current Portfolio</b><br>' +
                     'Return: %{y:.2f}%<br>' +
                     'Volatility: %{x:.2f}%<br>' +
                     f'Sharpe: {current_portfolio["sharpe_ratio"]:.2f}<br>' +
                     '<extra></extra>'
    ))
    
    # Plot max Sharpe portfolio
    fig.add_trace(go.Scatter(
        x=[optimal_portfolios['max_sharpe']['volatility'] * 100],
        y=[optimal_portfolios['max_sharpe']['return'] * 100],
        mode='markers',
        name='Max Sharpe Ratio',
        marker=dict(
            size=15,
            color='#FFD93D',
            symbol='diamond',
            line=dict(color='white', width=2)
        ),
        hovertemplate='<b>Max Sharpe Portfolio</b><br>' +
                     'Return: %{y:.2f}%<br>' +
                     'Volatility: %{x:.2f}%<br>' +
                     f'Sharpe: {optimal_portfolios["max_sharpe"]["sharpe_ratio"]:.2f}<br>' +
                     '<extra></extra>'
    ))
    
    # Plot min volatility portfolio
    fig.add_trace(go.Scatter(
        x=[optimal_portfolios['min_vol']['volatility'] * 100],
        y=[optimal_portfolios['min_vol']['return'] * 100],
        mode='markers',
        name='Min Volatility',
        marker=dict(
            size=15,
            color='#95E1D3',
            symbol='square',
            line=dict(color='white', width=2)
        ),
        hovertemplate='<b>Min Volatility Portfolio</b><br>' +
                     'Return: %{y:.2f}%<br>' +
                     'Volatility: %{x:.2f}%<br>' +
                     f'Sharpe: {optimal_portfolios["min_vol"]["sharpe_ratio"]:.2f}<br>' +
                     '<extra></extra>'
    ))
    
    # Plot individual assets if provided
    if asset_data is not None:
        fig.add_trace(go.Scatter(
            x=asset_data['volatility'] * 100,
            y=asset_data['return'] * 100,
            mode='markers+text',
            name='Individual Assets',
            marker=dict(
                size=12,
                color='#667eea',
                symbol='circle',
                line=dict(color='white', width=2)
            ),
            text=asset_data.index,
            textposition='top center',
            textfont=dict(size=10, color='#667eea'),
            hovertemplate='<b>%{text}</b><br>' +
                         'Return: %{y:.2f}%<br>' +
                         'Volatility: %{x:.2f}%<br>' +
                         '<extra></extra>'
        ))
    
    # Update layout
    fig.update_layout(
        title='Markowitz Efficient Frontier',
        xaxis_title='Volatility (Risk) %',
        yaxis_title='Expected Return %',
        height=600,
        template='plotly_white',
        hovermode='closest',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(255,255,255,0.8)'
        ),
        font=dict(family='Inter', size=12)
    )
    
    return fig


def analyze_portfolio_markowitz(price_data: pd.DataFrame, current_weights: np.ndarray,
                                risk_free_rate: float = 0.05) -> Dict:
    """
    Complete Markowitz analysis of portfolio.
    
    Args:
        price_data: DataFrame with asset prices
        current_weights: Current portfolio weights
        risk_free_rate: Risk-free rate
        
    Returns:
        Dictionary with all analysis results
    """
    # Calculate expected returns and covariance
    expected_returns = calculate_expected_returns(price_data)
    cov_matrix = calculate_covariance_matrix(price_data)
    
    # Current portfolio performance
    current_return, current_vol = calculate_portfolio_performance(
        current_weights, expected_returns.values, cov_matrix.values
    )
    current_sharpe = (current_return - risk_free_rate) / current_vol if current_vol > 0 else 0
    
    # Optimal portfolios
    max_sharpe_portfolio = optimize_portfolio(
        expected_returns.values, cov_matrix.values, 'sharpe', risk_free_rate
    )
    min_vol_portfolio = optimize_portfolio(
        expected_returns.values, cov_matrix.values, 'min_vol', risk_free_rate
    )
    
    # Generate efficient frontier
    efficient_frontier = generate_efficient_frontier(
        expected_returns.values, cov_matrix.values, 100, risk_free_rate
    )
    
    # Generate random portfolios
    random_portfolios = generate_random_portfolios(
        expected_returns.values, cov_matrix.values, 5000, risk_free_rate
    )
    
    # Individual asset performance
    asset_returns = price_data.pct_change().dropna()
    asset_metrics = pd.DataFrame({
        'return': expected_returns,
        'volatility': asset_returns.std() * np.sqrt(252)
    })
    
    return {
        'expected_returns': expected_returns,
        'cov_matrix': cov_matrix,
        'current_portfolio': {
            'return': current_return,
            'volatility': current_vol,
            'sharpe_ratio': current_sharpe
        },
        'optimal_portfolios': {
            'max_sharpe': max_sharpe_portfolio,
            'min_vol': min_vol_portfolio
        },
        'efficient_frontier': efficient_frontier,
        'random_portfolios': random_portfolios,
        'asset_metrics': asset_metrics
    }

