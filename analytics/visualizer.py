"""
Visualization utilities for portfolio analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List


# Set style for all plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def plot_portfolio_evolution(portfolio_value_series: pd.Series, 
                            save_path: str = 'reports/charts/portfolio_evolution.png'):
    """
    Create a line chart of portfolio value over time.
    
    Args:
        portfolio_value_series: Series with dates as index and portfolio values
        save_path: Path to save the chart
    """
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot portfolio value
    ax.plot(portfolio_value_series.index, portfolio_value_series.values, 
            linewidth=2, color='#2E86AB', label='Portfolio Value')
    
    # Add initial value line
    initial_value = portfolio_value_series.iloc[0]
    ax.axhline(y=initial_value, color='gray', linestyle='--', 
               linewidth=1, alpha=0.7, label=f'Initial Value: ${initial_value:,.0f}')
    
    # Formatting
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Portfolio Value ($)', fontsize=12, fontweight='bold')
    ax.set_title('Portfolio Value Evolution', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Format y-axis as currency
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Rotate x-axis labels
    plt.xticks(rotation=45)
    
    # Tight layout
    plt.tight_layout()
    
    # Save figure
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Portfolio evolution chart saved to {save_path}")


def plot_asset_allocation(assets_info: List[Dict], 
                         save_path: str = 'reports/charts/asset_allocation.png'):
    """
    Create a pie chart of the initial asset allocation.
    
    Args:
        assets_info: List of dictionaries with asset information
        save_path: Path to save the chart
    """
    # Extract data
    labels = [asset['ticker'] + '\n' + asset['name'] for asset in assets_info]
    weights = [asset['initial_weight'] for asset in assets_info]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create pie chart
    colors = sns.color_palette("husl", len(labels))
    wedges, texts, autotexts = ax.pie(weights, labels=labels, autopct='%1.1f%%',
                                        startangle=90, colors=colors,
                                        textprops={'fontsize': 10})
    
    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    ax.set_title('Initial Asset Allocation', fontsize=14, fontweight='bold', pad=20)
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')
    
    # Tight layout
    plt.tight_layout()
    
    # Save figure
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Asset allocation chart saved to {save_path}")


def plot_correlation_heatmap(correlation_matrix: pd.DataFrame,
                             save_path: str = 'reports/charts/correlation_heatmap.png'):
    """
    Create a heatmap of the asset correlation matrix.
    
    Args:
        correlation_matrix: Correlation matrix as DataFrame
        save_path: Path to save the chart
    """
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create heatmap
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                vmin=-1, vmax=1, ax=ax)
    
    ax.set_title('Asset Correlation Matrix', fontsize=14, fontweight='bold', pad=20)
    
    # Tight layout
    plt.tight_layout()
    
    # Save figure
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Correlation heatmap saved to {save_path}")


def plot_returns_distribution(returns_series: pd.Series,
                              save_path: str = 'reports/charts/returns_distribution.png'):
    """
    Create a histogram of returns distribution.
    
    Args:
        returns_series: Series of returns
        save_path: Path to save the chart
    """
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create histogram
    returns_clean = returns_series.dropna()
    ax.hist(returns_clean, bins=50, color='#2E86AB', alpha=0.7, edgecolor='black')
    
    # Add mean line
    mean_return = returns_clean.mean()
    ax.axvline(x=mean_return, color='red', linestyle='--', 
               linewidth=2, label=f'Mean: {mean_return:.4f}')
    
    # Formatting
    ax.set_xlabel('Daily Returns', fontsize=12, fontweight='bold')
    ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax.set_title('Distribution of Daily Returns', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Tight layout
    plt.tight_layout()
    
    # Save figure
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Returns distribution chart saved to {save_path}")


def plot_drawdown(portfolio_value_series: pd.Series,
                 save_path: str = 'reports/charts/drawdown.png'):
    """
    Create a chart showing drawdown over time.
    
    Args:
        portfolio_value_series: Series with portfolio values
        save_path: Path to save the chart
    """
    # Calculate running maximum
    running_max = portfolio_value_series.expanding().max()
    
    # Calculate drawdown
    drawdown = (portfolio_value_series - running_max) / running_max
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot drawdown
    ax.fill_between(drawdown.index, drawdown.values, 0, 
                     color='red', alpha=0.3, label='Drawdown')
    ax.plot(drawdown.index, drawdown.values, color='darkred', linewidth=1.5)
    
    # Formatting
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Drawdown', fontsize=12, fontweight='bold')
    ax.set_title('Portfolio Drawdown Over Time', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Format y-axis as percentage
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x*100:.1f}%'))
    
    # Rotate x-axis labels
    plt.xticks(rotation=45)
    
    # Tight layout
    plt.tight_layout()
    
    # Save figure
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Drawdown chart saved to {save_path}")
