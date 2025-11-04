"""
Advanced Portfolio Optimizer
Provides practical rebalancing recommendations with transaction cost analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime


class PortfolioOptimizer:
    """
    Advanced portfolio optimizer with practical rebalancing capabilities.
    """
    
    def __init__(self, assets_info: List[Dict], current_portfolio_value: float,
                 transaction_cost_pct: float = 0.001):
        """
        Initialize the optimizer.
        
        Args:
            assets_info: List of asset information dictionaries
            current_portfolio_value: Current total portfolio value
            transaction_cost_pct: Transaction cost as percentage (default 0.1%)
        """
        self.assets_info = assets_info
        self.current_value = current_portfolio_value
        self.transaction_cost = transaction_cost_pct
        self.tickers = [asset['ticker'] for asset in assets_info]
    
    def calculate_rebalancing_trades(self, current_weights: np.ndarray,
                                    target_weights: np.ndarray,
                                    current_prices: Dict[str, float],
                                    current_shares: Dict[str, float]) -> pd.DataFrame:
        """
        Calculate specific trades needed to rebalance portfolio.
        
        Args:
            current_weights: Current portfolio weights
            target_weights: Target portfolio weights
            current_prices: Current prices for each asset
            current_shares: Current shares held for each asset
            
        Returns:
            DataFrame with trade details
        """
        trades = []
        
        for i, asset in enumerate(self.assets_info):
            ticker = asset['ticker']
            current_weight = current_weights[i]
            target_weight = target_weights[i]
            price = current_prices[ticker]
            
            # Calculate values
            current_value = current_shares[ticker] * price
            target_value = self.current_value * target_weight
            value_change = target_value - current_value
            
            # Calculate shares
            current_shares_amt = current_shares[ticker]
            target_shares_amt = target_value / price
            shares_change = target_shares_amt - current_shares_amt
            
            # Determine action
            if abs(shares_change) < 0.01:  # Negligible change
                action = "HOLD"
            elif shares_change > 0:
                action = "BUY"
            else:
                action = "SELL"
            
            trades.append({
                'Ticker': ticker,
                'Name': asset['name'],
                'Current Weight': current_weight * 100,
                'Target Weight': target_weight * 100,
                'Weight Change': (target_weight - current_weight) * 100,
                'Current Shares': current_shares_amt,
                'Target Shares': target_shares_amt,
                'Shares to Trade': abs(shares_change),
                'Current Value': current_value,
                'Target Value': target_value,
                'Dollar Amount': abs(value_change),
                'Action': action,
                'Transaction Cost': abs(value_change) * self.transaction_cost
            })
        
        return pd.DataFrame(trades)
    
    def calculate_optimization_metrics(self, trades_df: pd.DataFrame) -> Dict:
        """
        Calculate metrics for the rebalancing operation.
        
        Args:
            trades_df: DataFrame with trade details
            
        Returns:
            Dictionary with optimization metrics
        """
        total_trade_value = trades_df['Dollar Amount'].sum()
        total_transaction_cost = trades_df['Transaction Cost'].sum()
        turnover_percentage = (total_trade_value / self.current_value) * 100
        
        num_buys = len(trades_df[trades_df['Action'] == 'BUY'])
        num_sells = len(trades_df[trades_df['Action'] == 'SELL'])
        num_holds = len(trades_df[trades_df['Action'] == 'HOLD'])
        
        return {
            'total_trade_value': total_trade_value,
            'total_transaction_cost': total_transaction_cost,
            'net_cost': total_transaction_cost,
            'turnover_percentage': turnover_percentage,
            'num_buys': num_buys,
            'num_sells': num_sells,
            'num_holds': num_holds,
            'efficiency_score': 100 - turnover_percentage  # Lower turnover = higher efficiency
        }
    
    def generate_optimization_report(self, strategy_name: str,
                                    optimal_weights: np.ndarray,
                                    current_weights: np.ndarray,
                                    current_prices: Dict[str, float],
                                    current_shares: Dict[str, float],
                                    expected_improvement: Dict) -> Dict:
        """
        Generate a comprehensive optimization report.
        
        Args:
            strategy_name: Name of the strategy
            optimal_weights: Target optimal weights
            current_weights: Current weights
            current_prices: Current prices
            current_shares: Current shares
            expected_improvement: Expected improvements (return, risk, sharpe)
            
        Returns:
            Dictionary with complete report
        """
        # Calculate trades
        trades_df = self.calculate_rebalancing_trades(
            current_weights, optimal_weights, current_prices, current_shares
        )
        
        # Calculate metrics
        metrics = self.calculate_optimization_metrics(trades_df)
        
        # Net expected return after costs
        expected_return_improvement = expected_improvement['return']
        annual_cost_impact = (metrics['total_transaction_cost'] / self.current_value) * 100
        net_improvement = expected_return_improvement - annual_cost_impact
        
        return {
            'strategy_name': strategy_name,
            'trades': trades_df,
            'metrics': metrics,
            'expected_improvement': expected_improvement,
            'net_improvement_after_costs': net_improvement,
            'total_trade_value': metrics['total_trade_value'],
            'total_transaction_cost': metrics['total_transaction_cost'],
            'turnover_percentage': metrics['turnover_percentage'],
            'recommendation': self._generate_recommendation(metrics, net_improvement)
        }
    
    def _generate_recommendation(self, metrics: Dict, net_improvement: float) -> str:
        """
        Generate a text recommendation based on metrics.
        
        Args:
            metrics: Optimization metrics
            net_improvement: Net improvement after costs
            
        Returns:
            Recommendation text
        """
        if net_improvement < 0.5:
            return "⚠️ HOLD: Transaction costs may outweigh benefits. Consider waiting for larger improvements."
        elif metrics['turnover_percentage'] > 50:
            return "⚠️ HIGH TURNOVER: Significant rebalancing required. Consider implementing gradually."
        elif net_improvement > 2.0:
            return "✅ STRONGLY RECOMMENDED: Significant improvement potential after costs."
        else:
            return "✅ RECOMMENDED: Moderate improvement with reasonable transaction costs."
    
    def apply_constraints(self, weights: np.ndarray,
                         min_weight: float = 0.05,
                         max_weight: float = 0.40) -> np.ndarray:
        """
        Apply position size constraints to weights.
        
        Args:
            weights: Unconstrained weights
            min_weight: Minimum position size (default 5%)
            max_weight: Maximum position size (default 40%)
            
        Returns:
            Constrained weights
        """
        constrained = weights.copy()
        
        # Apply min/max constraints
        constrained = np.maximum(constrained, min_weight)
        constrained = np.minimum(constrained, max_weight)
        
        # Renormalize to sum to 1
        constrained = constrained / constrained.sum()
        
        return constrained


def compare_strategies(current_portfolio: Dict,
                      optimal_portfolios: Dict[str, Dict]) -> pd.DataFrame:
    """
    Compare different portfolio strategies.
    
    Args:
        current_portfolio: Current portfolio metrics
        optimal_portfolios: Dictionary of optimal portfolio strategies
        
    Returns:
        Comparison DataFrame
    """
    comparisons = []
    
    # Add current portfolio
    comparisons.append({
        'Strategy': 'Current',
        'Expected Return': current_portfolio['return'] * 100,
        'Volatility': current_portfolio['volatility'] * 100,
        'Sharpe Ratio': current_portfolio['sharpe_ratio'],
        'Return Improvement': 0.0,
        'Risk Change': 0.0,
        'Sharpe Improvement': 0.0
    })
    
    # Add optimal strategies
    for name, portfolio in optimal_portfolios.items():
        comparisons.append({
            'Strategy': name,
            'Expected Return': portfolio['return'] * 100,
            'Volatility': portfolio['volatility'] * 100,
            'Sharpe Ratio': portfolio['sharpe_ratio'],
            'Return Improvement': (portfolio['return'] - current_portfolio['return']) * 100,
            'Risk Change': (portfolio['volatility'] - current_portfolio['volatility']) * 100,
            'Sharpe Improvement': portfolio['sharpe_ratio'] - current_portfolio['sharpe_ratio']
        })
    
    return pd.DataFrame(comparisons)


def create_optimized_portfolio_config(optimal_weights: np.ndarray,
                                     assets_info: List[Dict],
                                     current_prices: Dict[str, float],
                                     strategy_name: str) -> Dict:
    """
    Create a configuration file for the optimized portfolio.
    
    Args:
        optimal_weights: Optimal portfolio weights
        assets_info: Asset information
        current_prices: Current prices
        strategy_name: Name of the strategy
        
    Returns:
        Configuration dictionary
    """
    optimized_assets = []
    
    for i, asset in enumerate(assets_info):
        ticker = asset['ticker']
        optimized_assets.append({
            'name': asset['name'],
            'ticker': ticker,
            'asset_class': asset['asset_class'],
            'initial_weight': float(optimal_weights[i]),
            'initial_price': current_prices[ticker],
            'optimization_date': datetime.now().strftime('%Y-%m-%d')
        })
    
    return {
        'strategy': strategy_name,
        'creation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'assets': optimized_assets,
        'note': f'Optimized portfolio using {strategy_name} strategy'
    }


def calculate_implementation_schedule(trades_df: pd.DataFrame,
                                     num_periods: int = 4) -> List[pd.DataFrame]:
    """
    Create a gradual implementation schedule for large rebalancing.
    
    Args:
        trades_df: Trade details DataFrame
        num_periods: Number of periods to split trades over
        
    Returns:
        List of DataFrames, one per period
    """
    schedules = []
    
    for period in range(num_periods):
        period_trades = trades_df.copy()
        period_trades['Shares to Trade'] = period_trades['Shares to Trade'] / num_periods
        period_trades['Dollar Amount'] = period_trades['Dollar Amount'] / num_periods
        period_trades['Transaction Cost'] = period_trades['Transaction Cost'] / num_periods
        period_trades['Period'] = period + 1
        schedules.append(period_trades)
    
    return schedules


def analyze_tax_impact(trades_df: pd.DataFrame,
                      purchase_prices: Dict[str, float],
                      current_prices: Dict[str, float],
                      short_term_rate: float = 0.24,
                      long_term_rate: float = 0.15) -> pd.DataFrame:
    """
    Analyze potential tax impact of trades (US tax rates example).
    
    Args:
        trades_df: Trade details
        purchase_prices: Original purchase prices
        current_prices: Current prices
        short_term_rate: Short-term capital gains rate
        long_term_rate: Long-term capital gains rate
        
    Returns:
        DataFrame with tax analysis
    """
    tax_analysis = trades_df.copy()
    
    tax_impacts = []
    for _, row in trades_df.iterrows():
        if row['Action'] == 'SELL':
            ticker = row['Ticker']
            shares_sold = row['Shares to Trade']
            
            # Calculate gains
            cost_basis = purchase_prices.get(ticker, current_prices[ticker])
            proceeds = shares_sold * current_prices[ticker]
            capital_gain = proceeds - (shares_sold * cost_basis)
            
            # Assume long-term for this example
            tax_owed = capital_gain * long_term_rate if capital_gain > 0 else 0
            
            tax_impacts.append(tax_owed)
        else:
            tax_impacts.append(0)
    
    tax_analysis['Estimated Tax Impact'] = tax_impacts
    
    return tax_analysis
