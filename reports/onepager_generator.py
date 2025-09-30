"""
One-page report generator for portfolio performance
"""

import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings
from core.loader import load_asset_info, load_price_data, update_price_data
from core.portfolio import Portfolio
from analytics.performance import (
    calculate_returns, calculate_volatility, calculate_sharpe_ratio,
    calculate_max_drawdown, calculate_total_return, calculate_annualized_return
)
from analytics.risk import calculate_correlation_matrix, calculate_var, calculate_cvar
from analytics.visualizer import (
    plot_portfolio_evolution, plot_asset_allocation, plot_correlation_heatmap,
    plot_returns_distribution, plot_drawdown
)
from datetime import datetime


def generate_report():
    """
    Generate the weekly one-page portfolio report.
    """
    print("=" * 60)
    print("PORTFOLIO PERFORMANCE REPORT GENERATOR")
    print("=" * 60)
    print()
    
    # 1. Load asset information
    print("1. Loading asset information...")
    assets_info = load_asset_info(settings.ASSETS_INFO_PATH)
    print(f"   Loaded {len(assets_info)} assets")
    
    # 2. Update price data
    print("\n2. Updating price data...")
    try:
        update_price_data(settings.ASSET_TICKERS, settings.PRICES_CSV_PATH)
    except Exception as e:
        print(f"   Warning: Could not update price data: {e}")
    
    # 3. Load price data
    print("\n3. Loading price data...")
    price_data = load_price_data(settings.PRICES_CSV_PATH)
    
    if price_data.empty:
        print("   ERROR: No price data available!")
        return
    
    print(f"   Loaded price data from {price_data.index[0]} to {price_data.index[-1]}")
    
    # 4. Create portfolio
    print("\n4. Initializing portfolio...")
    portfolio = Portfolio(assets_info, settings.INITIAL_CAPITAL)
    print(f"   Initial capital: ${settings.INITIAL_CAPITAL:,.2f}")
    print(f"   Portfolio holdings:")
    for ticker, shares in portfolio.shares.items():
        print(f"      {ticker}: {shares} shares")
    
    # 5. Calculate portfolio value over time
    print("\n5. Calculating portfolio value...")
    # Calculate from project start date to ensure accurate initial value
    portfolio_value = portfolio.calculate_value(price_data, start_date=settings.START_DATE)
    current_value = portfolio_value.iloc[-1]
    print(f"   Current portfolio value: ${current_value:,.2f}")
    
    # 6. Calculate performance metrics
    print("\n6. Calculating performance metrics...")
    returns_df = calculate_returns(portfolio_value)
    daily_returns = returns_df['daily_return']
    
    total_return = calculate_total_return(portfolio_value)
    annualized_return = calculate_annualized_return(portfolio_value)
    volatility = calculate_volatility(daily_returns)
    sharpe_ratio = calculate_sharpe_ratio(daily_returns, settings.RISK_FREE_RATE)
    max_dd = calculate_max_drawdown(portfolio_value)
    
    print(f"   Total Return: {total_return*100:.2f}%")
    print(f"   Annualized Return: {annualized_return*100:.2f}%")
    print(f"   Annualized Volatility: {volatility*100:.2f}%")
    print(f"   Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"   Max Drawdown: {max_dd['max_drawdown_pct']:.2f}%")
    
    # 7. Calculate risk metrics
    print("\n7. Calculating risk metrics...")
    correlation_matrix = calculate_correlation_matrix(price_data)
    var_95 = calculate_var(daily_returns, 0.95)
    cvar_95 = calculate_cvar(daily_returns, 0.95)
    
    print(f"   VaR (95%): {var_95*100:.2f}%")
    print(f"   CVaR (95%): {cvar_95*100:.2f}%")
    
    # 8. Generate visualizations
    print("\n8. Generating visualizations...")
    plot_portfolio_evolution(portfolio_value)
    plot_asset_allocation(assets_info)
    plot_correlation_heatmap(correlation_matrix)
    plot_returns_distribution(daily_returns)
    plot_drawdown(portfolio_value)
    print("   All charts generated successfully")
    
    # 9. Prepare report data
    print("\n9. Preparing report summary...")
    report_data = {
        'report_date': datetime.now().strftime('%Y-%m-%d'),
        'start_date': settings.START_DATE,
        'end_date': settings.END_DATE,
        'initial_capital': settings.INITIAL_CAPITAL,
        'current_value': current_value,
        'total_return': total_return,
        'annualized_return': annualized_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_dd['max_drawdown'],
        'max_drawdown_pct': max_dd['max_drawdown_pct'],
        'var_95': var_95,
        'cvar_95': cvar_95,
        'assets_info': assets_info,
        'portfolio_holdings': portfolio.shares
    }
    
    print("\n" + "=" * 60)
    print("REPORT GENERATION COMPLETE")
    print("=" * 60)
    print()
    print("Summary:")
    print(f"  Initial Capital:     ${report_data['initial_capital']:,.2f}")
    print(f"  Current Value:       ${report_data['current_value']:,.2f}")
    print(f"  Total Return:        {report_data['total_return']*100:,.2f}%")
    print(f"  Sharpe Ratio:        {report_data['sharpe_ratio']:.2f}")
    print()
    print(f"Charts saved in: {settings.CHARTS_DIR}/")
    print()
    
    return report_data


if __name__ == "__main__":
    generate_report()
