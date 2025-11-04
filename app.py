"""
Streamlit Dashboard for Portfolio Management Tracker
Main entry point for the interactive web application
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import sys
from pathlib import Path
import numpy as np

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from core.loader import load_asset_info, load_price_data, update_price_data, fetch_market_data
from core.portfolio import Portfolio
from analytics.performance import (
    calculate_returns, calculate_volatility, calculate_sharpe_ratio,
    calculate_max_drawdown, calculate_total_return, calculate_annualized_return
)
from analytics.risk import calculate_correlation_matrix, calculate_var, calculate_cvar, calculate_sortino_ratio
from analytics.markowitz import (
    analyze_portfolio_markowitz, plot_efficient_frontier,
    calculate_expected_returns, calculate_covariance_matrix
)
from core.optimizer import (
    PortfolioOptimizer, compare_strategies, create_optimized_portfolio_config,
    calculate_implementation_schedule
)
from reports.weekly_report import WeeklyReportGenerator, get_next_wednesday_dates

# Page configuration
st.set_page_config(
    page_title="Portfolio Tracker | Asset Management",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with modern design
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Header */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1.5rem;
        padding: 1rem 0;
    }
    
    /* Subheader styling */
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1f2937;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* Metric cards */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 600;
        color: #6b7280;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left-color: #10b981;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fed7aa 0%, #fbbf24 100%);
        border-left-color: #f59e0b;
    }
    
    .danger-box {
        background: linear-gradient(135deg, #fee2e2 0%, #fca5a5 100%);
        border-left-color: #ef4444;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f2937 0%, #111827 100%);
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* DataFrame styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Card effect for columns */
    div[data-testid="column"] {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin: 0.5rem;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    
    .badge-success {
        background-color: #d1fae5;
        color: #065f46;
    }
    
    .badge-warning {
        background-color: #fed7aa;
        color: #92400e;
    }
    
    .badge-danger {
        background-color: #fee2e2;
        color: #991b1b;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Smooth animations */
    * {
        transition: all 0.3s ease;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_portfolio_data():
    """Load and cache portfolio data"""
    try:
        assets_info = load_asset_info(settings.ASSETS_INFO_PATH)
        price_data = load_price_data(settings.PRICES_CSV_PATH)
        
        if price_data.empty:
            return None, None, None, "No price data available"
        
        portfolio = Portfolio(assets_info, settings.INITIAL_CAPITAL)
        # Calculate portfolio value starting from project start date
        portfolio_value = portfolio.calculate_value(price_data, start_date=settings.START_DATE)
        
        return assets_info, price_data, portfolio, portfolio_value
    except Exception as e:
        return None, None, None, str(e)


def create_metric_card(label, value, delta=None, delta_color="normal"):
    """Create a styled metric card"""
    delta_html = ""
    if delta is not None:
        color = "#10b981" if delta >= 0 else "#ef4444"
        arrow = "↑" if delta >= 0 else "↓"
        delta_html = f'<div style="color: {color}; font-size: 1rem; font-weight: 600;">{arrow} {abs(delta):.2f}%</div>'
    
    return f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); text-align: center;">
        <div style="color: #6b7280; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem;">{label}</div>
        <div style="color: #1f2937; font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;">{value}</div>
        {delta_html}
    </div>
    """


def main():
    # Sidebar with enhanced design
    with st.sidebar:
        # Logo/Header
        st.markdown("""
            <div style="text-align: center; padding: 2rem 0 1rem 0;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">💼</div>
                <h1 style="font-size: 1.5rem; font-weight: 700; margin: 0; color: white !important;">Portfolio Tracker</h1>
                <p style="color: #9ca3af !important; font-size: 0.875rem; margin-top: 0.5rem;">Asset Management System</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation with icons
        st.markdown("### 📍 Navigation")
        page = st.radio(
            "Select Page",
            ["🏠 Dashboard", "📊 Analytics", "💼 Holdings", "📈 Markowitz", "🔧 Portfolio Builder", "📧 Weekly Report", "📊 Data Explorer", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Data management section
        st.markdown("### 🔄 Data Management")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh", use_container_width=True):
                try:
                    with st.spinner("Updating..."):
                        update_price_data(settings.ASSET_TICKERS, settings.PRICES_CSV_PATH)
                        st.cache_data.clear()
                        st.success("✓ Updated!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        
        with col2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.cache_data.clear()
                st.success("✓ Cleared!")
        

        st.markdown("---")
        st.caption("© 2025 Portfolio Management System")
    
    # Load data
    assets_info, price_data, portfolio, portfolio_value = load_portfolio_data()
    
    if assets_info is None:
        st.error(f"❌ Error loading data: {portfolio_value}")
        st.info("💡 Try running: `python main.py --fetch-data`")
        return
    
    # Route to selected page
    if page == "🏠 Dashboard":
        show_dashboard(assets_info, price_data, portfolio, portfolio_value)
    elif page == "📊 Analytics":
        show_analytics(price_data, portfolio_value)
    elif page == "💼 Holdings":
        show_holdings(assets_info, portfolio, price_data)
    elif page == "📈 Markowitz":
        show_markowitz(assets_info, price_data, portfolio)
    elif page == "🔧 Portfolio Builder":
        show_portfolio_builder(assets_info, price_data, portfolio)
    elif page == "📧 Weekly Report":
        show_weekly_report(assets_info, price_data)
    elif page == "📊 Data Explorer":
        show_data_explorer(price_data, portfolio_value)
    elif page == "⚙️ Settings":
        show_settings()


def show_dashboard(assets_info, price_data, portfolio, portfolio_value):
    """Enhanced main dashboard page"""
    
    # Header
    st.markdown('<p class="main-header">📈 Portfolio Dashboard</p>', unsafe_allow_html=True)
    
    # Calculate metrics
    current_value = portfolio_value.iloc[-1]
    total_return = calculate_total_return(portfolio_value)
    returns_df = calculate_returns(portfolio_value)
    daily_returns = returns_df['daily_return']
    
    # Top-level metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "💰 Current Value",
            f"${current_value:,.0f}",
            f"{(current_value - settings.INITIAL_CAPITAL):+,.0f}"
        )
    
    with col2:
        st.metric(
            "📈 Total Return",
            f"{total_return*100:.2f}%",
            delta=f"{total_return*100:.2f}%"
        )
    
    with col3:
        volatility = calculate_volatility(daily_returns)
        st.metric("📊 Volatility", f"{volatility*100:.1f}%")
    
    with col4:
        sharpe = calculate_sharpe_ratio(daily_returns, settings.RISK_FREE_RATE)
        st.metric("⭐ Sharpe Ratio", f"{sharpe:.2f}")
    
    with col5:
        max_dd = calculate_max_drawdown(portfolio_value)
        st.metric("⚠️ Max Drawdown", f"{max_dd['max_drawdown_pct']:.2f}%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📊 Performance", "🎯 Allocation", "📉 Risk Analysis"])
    
    with tab1:
        # Portfolio evolution chart
        st.markdown('<h3 class="sub-header">Portfolio Value Evolution</h3>', unsafe_allow_html=True)
        
        fig = go.Figure()
        
        # Main line
        fig.add_trace(go.Scatter(
            x=portfolio_value.index,
            y=portfolio_value.values,
            mode='lines',
            name='Portfolio Value',
            line=dict(color='#667eea', width=3),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.1)',
            hovertemplate='<b>Date:</b> %{x}<br><b>Value:</b> $%{y:,.2f}<extra></extra>'
        ))
        
        # Baseline
        fig.add_hline(
            y=settings.INITIAL_CAPITAL,
            line_dash="dash",
            line_color="#94a3b8",
            annotation_text=f"Initial Capital: ${settings.INITIAL_CAPITAL:,.0f}",
            annotation_position="right"
        )
        
        fig.update_layout(
            height=450,
            xaxis_title="Date",
            yaxis_title="Portfolio Value ($)",
            hovermode='x unified',
            template='plotly_white',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=12),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            annualized_return = calculate_annualized_return(portfolio_value)
            st.metric("📅 Annualized Return", f"{annualized_return*100:.2f}%")
        
        with col2:
            cumulative = returns_df['cumulative_return'].iloc[-1]
            st.metric("📈 Cumulative Return", f"{cumulative*100:.2f}%")
        
        with col3:
            sortino = calculate_sortino_ratio(daily_returns, settings.RISK_FREE_RATE)
            st.metric("🎯 Sortino Ratio", f"{sortino:.2f}")
        
        with col4:
            var_95 = calculate_var(daily_returns, 0.95)
            st.metric("⚠️ VaR (95%)", f"{var_95*100:.2f}%")
    
    with tab2:
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            st.markdown('<h3 class="sub-header">Current Asset Allocation</h3>', unsafe_allow_html=True)
            
            # Get current allocation
            current_prices = {col: price_data[col].iloc[-1] for col in price_data.columns}
            allocation_df = portfolio.get_current_allocation(current_prices)
            
            # Create enhanced allocation chart
            fig = go.Figure(data=[go.Pie(
                labels=[f"{row['ticker']}<br>{row['name']}" for _, row in allocation_df.iterrows()],
                values=allocation_df['weight'],
                hole=0.5,
                textinfo='label+percent',
                textposition='outside',
                marker=dict(
                    colors=px.colors.qualitative.Set3,
                    line=dict(color='white', width=2)
                ),
                hovertemplate='<b>%{label}</b><br>Value: $%{value:,.0f}<br>Weight: %{percent}<extra></extra>'
            )])
            
            # Add center text
            fig.add_annotation(
                text=f"<b>${current_value:,.0f}</b><br>Total Value",
                x=0.5, y=0.5,
                font_size=16,
                showarrow=False
            )
            
            fig.update_layout(
                height=400,
                template='plotly_white',
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                margin=dict(l=20, r=20, t=20, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown('<h3 class="sub-header">Asset Details</h3>', unsafe_allow_html=True)
            
            for _, asset in allocation_df.iterrows():
                with st.container():
                    weight_change = (asset['weight'] - asset['initial_weight']) * 100
                    st.markdown(f"""
                    <div style="background: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #667eea;">
                        <h4 style="margin: 0; color: #1f2937;">{asset['ticker']}</h4>
                        <p style="color: #6b7280; font-size: 0.875rem; margin: 0.25rem 0;">{asset['asset_class']}</p>
                        <div style="margin-top: 0.5rem;">
                            <span style="font-size: 1.25rem; font-weight: 700; color: #667eea;">${asset['value']:,.0f}</span>
                            <span style="color: #6b7280; font-size: 0.875rem; margin-left: 0.5rem;">({asset['weight']*100:.1f}%)</span>
                        </div>
                        <div style="margin-top: 0.5rem; font-size: 0.875rem; color: {'#10b981' if weight_change >= 0 else '#ef4444'};">
                            Weight drift: {weight_change:+.2f}%
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h3 class="sub-header">Risk Metrics</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Drawdown chart
            running_max = portfolio_value.expanding().max()
            drawdown = (portfolio_value - running_max) / running_max
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=drawdown.index,
                y=drawdown.values * 100,
                mode='lines',
                name='Drawdown',
                fill='tozeroy',
                line=dict(color='#ef4444', width=2),
                fillcolor='rgba(239, 68, 68, 0.1)',
                hovertemplate='<b>Date:</b> %{x}<br><b>Drawdown:</b> %{y:.2f}%<extra></extra>'
            ))
            
            fig.update_layout(
                title="Drawdown Over Time",
                xaxis_title="Date",
                yaxis_title="Drawdown (%)",
                height=350,
                template='plotly_white',
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Returns distribution
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=daily_returns.dropna() * 100,
                nbinsx=30,
                name='Daily Returns',
                marker_color='#667eea',
                opacity=0.7
            ))
            
            # Add mean line
            mean_return = daily_returns.mean() * 100
            fig.add_vline(
                x=mean_return,
                line_dash="dash",
                line_color="#10b981",
                annotation_text=f"Mean: {mean_return:.3f}%",
                annotation_position="top"
            )
            
            fig.update_layout(
                title="Returns Distribution",
                xaxis_title="Daily Returns (%)",
                yaxis_title="Frequency",
                height=350,
                template='plotly_white',
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Risk metrics summary
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            cvar_95 = calculate_cvar(daily_returns, 0.95)
            st.metric("📉 CVaR (95%)", f"{cvar_95*100:.2f}%")
        
        with col2:
            downside_days = (daily_returns < 0).sum()
            total_days = len(daily_returns.dropna())
            st.metric("📊 Down Days", f"{downside_days}/{total_days}")
        
        with col3:
            best_day = daily_returns.max() * 100
            st.metric("🎯 Best Day", f"+{best_day:.2f}%")
        
        with col4:
            worst_day = daily_returns.min() * 100
            st.metric("⚠️ Worst Day", f"{worst_day:.2f}%")


def show_analytics(price_data, portfolio_value):
    """Enhanced analytics page"""
    st.markdown('<p class="main-header">📊 Portfolio Analytics</p>', unsafe_allow_html=True)
    
    # Correlation matrix
    st.markdown('<h3 class="sub-header">Asset Correlation Analysis</h3>', unsafe_allow_html=True)
    
    correlation_matrix = calculate_correlation_matrix(price_data)
    
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        colorscale='RdBu',
        zmid=0,
        text=correlation_matrix.values,
        texttemplate='%{text:.2f}',
        textfont={"size": 14, "color": "white"},
        colorbar=dict(title="Correlation", thickness=15)
    ))
    
    fig.update_layout(
        height=500,
        template='plotly_white',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Individual asset performance
    st.markdown('<h3 class="sub-header">Individual Asset Performance</h3>', unsafe_allow_html=True)
    
    asset_returns = price_data.pct_change().dropna()
    
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set2
    for idx, column in enumerate(asset_returns.columns):
        cumulative_returns = (1 + asset_returns[column]).cumprod() - 1
        fig.add_trace(go.Scatter(
            x=cumulative_returns.index,
            y=cumulative_returns.values * 100,
            mode='lines',
            name=column,
            line=dict(width=3, color=colors[idx % len(colors)]),
            hovertemplate=f'<b>{column}</b><br>Date: %{{x}}<br>Return: %{{y:.2f}}%<extra></extra>'
        ))
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Cumulative Returns (%)",
        height=450,
        template='plotly_white',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Asset statistics
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h3 class="sub-header">Asset Statistics</h3>', unsafe_allow_html=True)
    
    stats_data = []
    for column in asset_returns.columns:
        returns = asset_returns[column]
        stats_data.append({
            'Asset': column,
            'Mean Daily Return': f"{returns.mean()*100:.3f}%",
            'Volatility (Ann.)': f"{returns.std() * np.sqrt(252) * 100:.2f}%",
            'Best Day': f"{returns.max()*100:.2f}%",
            'Worst Day': f"{returns.min()*100:.2f}%",
            'Total Return': f"{((1 + returns).prod() - 1)*100:.2f}%"
        })
    
    stats_df = pd.DataFrame(stats_data)
    st.dataframe(stats_df, use_container_width=True, hide_index=True)


def show_holdings(assets_info, portfolio, price_data):
    """Enhanced holdings page"""
    st.markdown('<p class="main-header">💼 Portfolio Holdings</p>', unsafe_allow_html=True)
    
    # Get current prices and allocation
    current_prices = {col: price_data[col].iloc[-1] for col in price_data.columns}
    allocation_df = portfolio.get_current_allocation(current_prices)
    
    # Holdings overview
    st.markdown('<h3 class="sub-header">Holdings Overview</h3>', unsafe_allow_html=True)
    
    # Create formatted display
    display_data = []
    for _, row in allocation_df.iterrows():
        asset_info = next(a for a in assets_info if a['ticker'] == row['ticker'])
        initial_price = asset_info['initial_price']
        price_change = (row['price'] - initial_price) / initial_price * 100
        
        display_data.append({
            'Ticker': row['ticker'],
            'Name': row['name'],
            'Class': row['asset_class'],
            'Shares': f"{row['shares']:.2f}",
            'Price': f"${row['price']:.2f}",
            'Price Change': f"{price_change:+.2f}%",
            'Value': f"${row['value']:,.2f}",
            'Weight': f"{row['weight']*100:.2f}%",
            'Target': f"{row['initial_weight']*100:.2f}%",
            'Drift': f"{(row['weight']-row['initial_weight'])*100:+.2f}%"
        })
    
    holdings_df = pd.DataFrame(display_data)
    
    # Style the dataframe
    st.dataframe(
        holdings_df,
        use_container_width=True,
        hide_index=True,
        height=300
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Weight comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="sub-header">Weight Comparison</h3>', unsafe_allow_html=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=allocation_df['ticker'],
            y=allocation_df['initial_weight'] * 100,
            name='Target Weight',
            marker_color='#94a3b8',
            text=allocation_df['initial_weight'] * 100,
            texttemplate='%{text:.1f}%',
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            x=allocation_df['ticker'],
            y=allocation_df['weight'] * 100,
            name='Current Weight',
            marker_color='#667eea',
            text=allocation_df['weight'] * 100,
            texttemplate='%{text:.1f}%',
            textposition='outside'
        ))
        
        fig.update_layout(
            xaxis_title="Asset",
            yaxis_title="Weight (%)",
            height=400,
            barmode='group',
            template='plotly_white',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<h3 class="sub-header">Value Distribution</h3>', unsafe_allow_html=True)
        
        fig = go.Figure(data=[go.Pie(
            labels=allocation_df['ticker'],
            values=allocation_df['value'],
            hole=0.4,
            marker=dict(colors=px.colors.qualitative.Set3),
            textinfo='label+value',
            texttemplate='<b>%{label}</b><br>$%{value:,.0f}',
            hovertemplate='<b>%{label}</b><br>Value: $%{value:,.2f}<br>Weight: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            height=400,
            template='plotly_white',
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)


def show_data_explorer(price_data, portfolio_value):
    """Enhanced data explorer page"""
    st.markdown('<p class="main-header">📈 Data Explorer</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["💲 Price Data", "📊 Portfolio Value", "📈 Statistics"])
    
    with tab1:
        st.markdown('<h3 class="sub-header">Historical Price Data</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"📅 Data Range: {price_data.index[0].strftime('%Y-%m-%d')} to {price_data.index[-1].strftime('%Y-%m-%d')} ({len(price_data)} days)")
        with col2:
            csv = price_data.to_csv()
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"price_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        st.dataframe(price_data.style.format("${:.2f}"), use_container_width=True, height=400)
    
    with tab2:
        st.markdown('<h3 class="sub-header">Portfolio Value History</h3>', unsafe_allow_html=True)
        
        portfolio_df = portfolio_value.to_frame(name='Portfolio Value')
        portfolio_df['Daily Change'] = portfolio_df['Portfolio Value'].diff()
        portfolio_df['Daily Change %'] = portfolio_df['Portfolio Value'].pct_change() * 100
        
        col1, col2 = st.columns([3, 1])
        with col1:
            total_change = portfolio_value.iloc[-1] - portfolio_value.iloc[0]
            st.info(f"💰 Total Change: ${total_change:+,.2f} ({total_change/portfolio_value.iloc[0]*100:+.2f}%)")
        with col2:
            csv = portfolio_df.to_csv()
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"portfolio_value_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        st.dataframe(
            portfolio_df.style.format({
                'Portfolio Value': '${:,.2f}',
                'Daily Change': '${:+,.2f}',
                'Daily Change %': '{:+.2f}%'
            }),
            use_container_width=True,
            height=400
        )
    
    with tab3:
        st.markdown('<h3 class="sub-header">Summary Statistics</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Price Data Statistics**")
            st.dataframe(
                price_data.describe().style.format("${:.2f}"),
                use_container_width=True
            )
        
        with col2:
            st.markdown("**Returns Statistics**")
            returns_df = calculate_returns(portfolio_value)
            st.dataframe(
                returns_df.describe().style.format("{:.4f}"),
                use_container_width=True
            )


def show_markowitz(assets_info, price_data, portfolio):
    """Markowitz Modern Portfolio Theory analysis page"""
    st.markdown('<p class="main-header">📈 Markowitz Portfolio Analysis</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>Modern Portfolio Theory (MPT)</strong> by Harry Markowitz shows the relationship between risk and return.
        The <strong>Efficient Frontier</strong> represents optimal portfolios offering the highest expected return for a given level of risk.
    </div>
    """, unsafe_allow_html=True)
    
    try:
        # Get current weights
        current_prices = {col: price_data[col].iloc[-1] for col in price_data.columns}
        allocation_df = portfolio.get_current_allocation(current_prices)
        current_weights = allocation_df['weight'].values
        
        # Perform Markowitz analysis
        with st.spinner("Analyzing portfolio using Markowitz theory..."):
            analysis_results = analyze_portfolio_markowitz(
                price_data,
                current_weights,
                settings.RISK_FREE_RATE
            )
        
        # Display key metrics
        st.markdown('<h3 class="sub-header">Portfolio Comparison</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 📊 Current Portfolio")
            current = analysis_results['current_portfolio']
            st.metric("Expected Return", f"{current['return']*100:.2f}%")
            st.metric("Volatility (Risk)", f"{current['volatility']*100:.2f}%")
            st.metric("Sharpe Ratio", f"{current['sharpe_ratio']:.2f}")
        
        with col2:
            st.markdown("#### ⭐ Max Sharpe Portfolio")
            max_sharpe = analysis_results['optimal_portfolios']['max_sharpe']
            st.metric(
                "Expected Return", 
                f"{max_sharpe['return']*100:.2f}%",
                delta=f"{(max_sharpe['return']-current['return'])*100:.2f}%"
            )
            st.metric(
                "Volatility (Risk)", 
                f"{max_sharpe['volatility']*100:.2f}%",
                delta=f"{(max_sharpe['volatility']-current['volatility'])*100:.2f}%",
                delta_color="inverse"
            )
            st.metric(
                "Sharpe Ratio", 
                f"{max_sharpe['sharpe_ratio']:.2f}",
                delta=f"{(max_sharpe['sharpe_ratio']-current['sharpe_ratio']):.2f}"
            )
        
        with col3:
            st.markdown("#### 🛡️ Min Volatility Portfolio")
            min_vol = analysis_results['optimal_portfolios']['min_vol']
            st.metric(
                "Expected Return", 
                f"{min_vol['return']*100:.2f}%",
                delta=f"{(min_vol['return']-current['return'])*100:.2f}%"
            )
            st.metric(
                "Volatility (Risk)", 
                f"{min_vol['volatility']*100:.2f}%",
                delta=f"{(min_vol['volatility']-current['volatility'])*100:.2f}%",
                delta_color="inverse"
            )
            st.metric(
                "Sharpe Ratio", 
                f"{min_vol['sharpe_ratio']:.2f}",
                delta=f"{(min_vol['sharpe_ratio']-current['sharpe_ratio']):.2f}"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Efficient Frontier Chart
        st.markdown('<h3 class="sub-header">Efficient Frontier Visualization</h3>', unsafe_allow_html=True)
        
        fig = plot_efficient_frontier(
            analysis_results['efficient_frontier'],
            analysis_results['random_portfolios'],
            analysis_results['current_portfolio'],
            analysis_results['optimal_portfolios'],
            analysis_results['asset_metrics']
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="info-box">
            <strong>📊 Chart Legend:</strong><br>
            • <strong>Random Portfolios</strong> (colored points): 5,000 simulated portfolio combinations<br>
            • <strong>Efficient Frontier</strong> (red line): Optimal risk-return combinations<br>
            • <strong>Current Portfolio</strong> (cyan star): Your current allocation<br>
            • <strong>Max Sharpe</strong> (yellow diamond): Optimal risk-adjusted returns<br>
            • <strong>Min Volatility</strong> (green square): Lowest risk portfolio<br>
            • <strong>Individual Assets</strong> (purple circles): Single asset positions
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Optimal Portfolio Weights
        tab1, tab2, tab3 = st.tabs(["⭐ Max Sharpe Weights", "🛡️ Min Vol Weights", "📊 Current Weights"])
        
        with tab1:
            st.markdown("### Optimal Weights for Maximum Sharpe Ratio")
            weights_df = pd.DataFrame({
                'Asset': [asset['ticker'] for asset in assets_info],
                'Name': [asset['name'] for asset in assets_info],
                'Optimal Weight': max_sharpe['weights'] * 100,
                'Current Weight': current_weights * 100,
                'Difference': (max_sharpe['weights'] - current_weights) * 100
            })
            
            st.dataframe(
                weights_df.style.format({
                    'Optimal Weight': '{:.2f}%',
                    'Current Weight': '{:.2f}%',
                    'Difference': '{:+.2f}%'
                }),
                use_container_width=True,
                hide_index=True
            )
            
            # Bar chart comparison
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Current',
                x=weights_df['Asset'],
                y=weights_df['Current Weight'],
                marker_color='#94a3b8'
            ))
            fig.add_trace(go.Bar(
                name='Optimal (Max Sharpe)',
                x=weights_df['Asset'],
                y=weights_df['Optimal Weight'],
                marker_color='#FFD93D'
            ))
            fig.update_layout(
                title='Weight Comparison: Current vs Max Sharpe',
                yaxis_title='Weight (%)',
                barmode='group',
                height=400,
                template='plotly_white'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.markdown("### Optimal Weights for Minimum Volatility")
            weights_df = pd.DataFrame({
                'Asset': [asset['ticker'] for asset in assets_info],
                'Name': [asset['name'] for asset in assets_info],
                'Optimal Weight': min_vol['weights'] * 100,
                'Current Weight': current_weights * 100,
                'Difference': (min_vol['weights'] - current_weights) * 100
            })
            
            st.dataframe(
                weights_df.style.format({
                    'Optimal Weight': '{:.2f}%',
                    'Current Weight': '{:.2f}%',
                    'Difference': '{:+.2f}%'
                }),
                use_container_width=True,
                hide_index=True
            )
            
            # Bar chart comparison
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Current',
                x=weights_df['Asset'],
                y=weights_df['Current Weight'],
                marker_color='#94a3b8'
            ))
            fig.add_trace(go.Bar(
                name='Optimal (Min Vol)',
                x=weights_df['Asset'],
                y=weights_df['Optimal Weight'],
                marker_color='#95E1D3'
            ))
            fig.update_layout(
                title='Weight Comparison: Current vs Min Volatility',
                yaxis_title='Weight (%)',
                barmode='group',
                height=400,
                template='plotly_white'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.markdown("### Current Portfolio Weights")
            current_df = pd.DataFrame({
                'Asset': [asset['ticker'] for asset in assets_info],
                'Name': [asset['name'] for asset in assets_info],
                'Weight': current_weights * 100,
                'Initial Weight': [asset['initial_weight'] * 100 for asset in assets_info],
                'Drift': (current_weights * 100) - np.array([asset['initial_weight'] * 100 for asset in assets_info])
            })
            
            st.dataframe(
                current_df.style.format({
                    'Weight': '{:.2f}%',
                    'Initial Weight': '{:.2f}%',
                    'Drift': '{:+.2f}%'
                }),
                use_container_width=True,
                hide_index=True
            )
        
        # Expected Returns and Risk by Asset
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<h3 class="sub-header">Individual Asset Risk-Return Profile</h3>', unsafe_allow_html=True)
        
        asset_metrics_display = analysis_results['asset_metrics'].copy()
        asset_metrics_display['return'] = asset_metrics_display['return'] * 100
        asset_metrics_display['volatility'] = asset_metrics_display['volatility'] * 100
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.dataframe(
                asset_metrics_display.style.format({
                    'return': '{:.2f}%',
                    'volatility': '{:.2f}%'
                }).background_gradient(subset=['return'], cmap='RdYlGn'),
                use_container_width=True
            )
        
        with col2:
            st.markdown("""
            **Expected Returns** are calculated from historical data and annualized.
            
            **Volatility** measures the standard deviation of returns (risk).
            
            Higher return often comes with higher volatility.
            """)
        
        # Portfolio Optimization & Rebalancing Section
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<h3 class="sub-header">🎯 Portfolio Optimization & Rebalancing</h3>', unsafe_allow_html=True)
        
        # Create optimizer
        current_value = portfolio.calculate_value(price_data, start_date=settings.START_DATE).iloc[-1]
        optimizer = PortfolioOptimizer(assets_info, current_value, transaction_cost_pct=0.001)
        
        # Strategy comparison
        st.markdown("#### Strategy Comparison")
        
        strategies_comparison = compare_strategies(
            analysis_results['current_portfolio'],
            {
                'Max Sharpe': analysis_results['optimal_portfolios']['max_sharpe'],
                'Min Volatility': analysis_results['optimal_portfolios']['min_vol']
            }
        )
        
        st.dataframe(
            strategies_comparison.style.format({
                'Expected Return': '{:.2f}%',
                'Volatility': '{:.2f}%',
                'Sharpe Ratio': '{:.2f}',
                'Return Improvement': '{:+.2f}%',
                'Risk Change': '{:+.2f}%',
                'Sharpe Improvement': '{:+.2f}'
            }).background_gradient(subset=['Sharpe Ratio'], cmap='RdYlGn'),
            width='stretch',
            hide_index=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Choose optimization strategy
        col1, col2 = st.columns([2, 1])
        
        with col1:
            optimization_strategy = st.radio(
                "Select Optimization Strategy:",
                ["Max Sharpe Ratio (Recommended)", "Min Volatility (Conservative)", "Keep Current"],
                help="Choose which strategy to implement"
            )
        
        with col2:
            st.markdown("""
            **Max Sharpe:** Best risk-adjusted returns  
            **Min Volatility:** Lowest risk  
            **Keep Current:** No changes  
            """)
        
        if optimization_strategy != "Keep Current":
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 📋 Rebalancing Instructions")
            
            # Get optimal weights and expected improvements
            if "Max Sharpe" in optimization_strategy:
                optimal_weights = max_sharpe['weights']
                strategy_name = "Max Sharpe"
                improvement = {
                    'return': (max_sharpe['return'] - current['return']) * 100,
                    'risk': (max_sharpe['volatility'] - current['volatility']) * 100,
                    'sharpe': max_sharpe['sharpe_ratio'] - current['sharpe_ratio']
                }
            else:
                optimal_weights = min_vol['weights']
                strategy_name = "Min Volatility"
                improvement = {
                    'return': (min_vol['return'] - current['return']) * 100,
                    'risk': (min_vol['volatility'] - current['volatility']) * 100,
                    'sharpe': min_vol['sharpe_ratio'] - current['sharpe_ratio']
                }
            
            # Generate rebalancing report
            rebalancing_report = optimizer.generate_optimization_report(
                strategy_name,
                optimal_weights,
                current_weights,
                current_prices,
                portfolio.shares,
                improvement
            )
            
            # Display expected improvements
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(
                    "Return Improvement",
                    f"{improvement['return']:+.2f}%",
                    delta=f"{improvement['return']:+.2f}%"
                )
            with col2:
                st.metric(
                    "Risk Change",
                    f"{improvement['risk']:+.2f}%",
                    delta=f"{improvement['risk']:+.2f}%",
                    delta_color="inverse"
                )
            with col3:
                st.metric(
                    "Sharpe Improvement",
                    f"{improvement['sharpe']:+.2f}",
                    delta=f"{improvement['sharpe']:+.2f}"
                )
            with col4:
                st.metric(
                    "Net Benefit After Costs",
                    f"{rebalancing_report['net_improvement_after_costs']:+.2f}%"
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Recommendation
            recommendation = rebalancing_report['recommendation']
            if "STRONGLY RECOMMENDED" in recommendation:
                st.success(recommendation)
            elif "RECOMMENDED" in recommendation:
                st.info(recommendation)
            else:
                st.warning(recommendation)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Trades table
            st.markdown("##### 📊 Trade Instructions")
            trades_df = rebalancing_report['trades']
            
            # Color code actions
            def color_actions(row):
                if row['Action'] == 'BUY':
                    return ['background-color: #d1fae5'] * len(row)
                elif row['Action'] == 'SELL':
                    return ['background-color: #fee2e2'] * len(row)
                else:
                    return ['background-color: #f3f4f6'] * len(row)
            
            styled_trades = trades_df.style.format({
                'Current Weight': '{:.2f}%',
                'Target Weight': '{:.2f}%',
                'Weight Change': '{:+.2f}%',
                'Current Shares': '{:.2f}',
                'Target Shares': '{:.2f}',
                'Shares to Trade': '{:.2f}',
                'Dollar Amount': '${:,.2f}',
                'Current Value': '${:,.2f}',
                'Target Value': '${:,.2f}',
                'Transaction Cost': '${:,.2f}'
            }).apply(color_actions, axis=1)
            
            st.dataframe(styled_trades, width='stretch', hide_index=True, height=400)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Trade Value", f"${rebalancing_report['total_trade_value']:,.2f}")
            with col2:
                st.metric("Transaction Costs", f"${rebalancing_report['total_transaction_cost']:,.2f}")
            with col3:
                st.metric("Portfolio Turnover", f"{rebalancing_report['turnover_percentage']:.1f}%")
            with col4:
                assets_to_trade = len(trades_df[trades_df['Action'] != 'HOLD'])
                st.metric("Assets to Rebalance", f"{assets_to_trade}/{len(trades_df)}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Implementation options
            tab1, tab2 = st.tabs(["📥 Download Config", "📅 Gradual Implementation"])
            
            with tab1:
                st.markdown("##### Download Optimized Portfolio Configuration")
                
                import json
                optimized_config = create_optimized_portfolio_config(
                    optimal_weights,
                    assets_info,
                    current_prices,
                    strategy_name
                )
                
                config_json = json.dumps(optimized_config, indent=2)
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown("""
                    Download the optimized configuration file for your records.
                    This file contains the target weights and can be used to update your portfolio.
                    """)
                with col2:
                    st.download_button(
                        label="📥 Download JSON Config",
                        data=config_json,
                        file_name=f"optimized_portfolio_{strategy_name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                # Also provide CSV export
                csv = trades_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Trade Instructions (CSV)",
                    data=csv,
                    file_name=f"trade_instructions_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with tab2:
                st.markdown("##### Gradual Implementation Schedule")
                st.markdown("""
                For large rebalancing operations, consider implementing gradually to reduce market impact.
                Below is a suggested 4-period implementation schedule.
                """)
                
                num_periods = st.slider("Number of periods:", 2, 8, 4)
                schedules = calculate_implementation_schedule(trades_df, num_periods)
                
                for i, schedule in enumerate(schedules):
                    with st.expander(f"Period {i+1} - Trade {100/num_periods:.0f}% of total"):
                        st.dataframe(
                            schedule[['Ticker', 'Action', 'Shares to Trade', 'Dollar Amount']].style.format({
                                'Shares to Trade': '{:.2f}',
                                'Dollar Amount': '${:,.2f}'
                            }),
                            width='stretch',
                            hide_index=True
                        )
        else:
            st.markdown("""
            <div class="info-box" style="background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);">
                <strong>💡 Current Portfolio Status</strong><br>
                Your current portfolio is already performing well with a Sharpe ratio of {:.2f}!<br><br>
                While optimization opportunities exist, they may not justify the transaction costs at this time.
                Consider reviewing optimization options:
                <ul>
                    <li>When market conditions change significantly</li>
                    <li>When your portfolio drifts more than 5% from targets</li>
                    <li>During your scheduled rebalancing periods (quarterly/annually)</li>
                </ul>
            </div>
            """.format(current['sharpe_ratio']), unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error performing Markowitz analysis: {e}")
        import traceback
        st.code(traceback.format_exc())


def show_portfolio_builder(assets_info, price_data, portfolio):
    """Interactive Portfolio Builder - experiment with different assets"""
    st.markdown('<p class="main-header">🔧 Portfolio Builder</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>🎯 Build Your Custom Portfolio</strong><br>
        Experiment with different stocks, bonds, and ETFs to see how they would perform.
        Add assets, adjust weights, and compare the expected returns with your current portfolio.
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for custom portfolio
    if 'custom_assets' not in st.session_state:
        st.session_state.custom_assets = []
    
    # Two column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<h3 class="sub-header">🎨 Design Your Portfolio</h3>', unsafe_allow_html=True)
        
        # Add asset section
        with st.expander("➕ Add New Asset", expanded=True):
            st.markdown("##### Search and Add Assets")
            
            # Ticker input
            new_ticker = st.text_input(
                "Enter Ticker Symbol",
                placeholder="e.g., AAPL, MSFT, SPY, AGG",
                help="Enter any stock, ETF, or bond ticker symbol"
            ).upper()
            
            # Weight input
            new_weight = st.number_input(
                "Allocation (%)",
                min_value=0.0,
                max_value=100.0,
                value=10.0,
                step=1.0,
                help="Percentage allocation for this asset"
            )
            
            # Asset name and class
            col_a, col_b = st.columns(2)
            with col_a:
                new_name = st.text_input("Asset Name (optional)", placeholder="e.g., Apple Inc.")
            with col_b:
                new_class = st.selectbox("Asset Class", 
                    ["Equities", "Fixed Income", "Commodities", "Real Estate", "Cash", "Alternatives"])
            
            # Add button
            if st.button("➕ Add Asset", use_container_width=True):
                if new_ticker:
                    # Check if ticker already exists
                    if any(asset['ticker'] == new_ticker for asset in st.session_state.custom_assets):
                        st.warning(f"⚠️ {new_ticker} is already in your portfolio!")
                    else:
                        st.session_state.custom_assets.append({
                            'ticker': new_ticker,
                            'name': new_name if new_name else new_ticker,
                            'asset_class': new_class,
                            'weight': new_weight / 100
                        })
                        st.success(f"✅ Added {new_ticker}")
                        st.rerun()
                else:
                    st.error("Please enter a ticker symbol")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Quick add current portfolio
        if st.button("📋 Load Current Portfolio", use_container_width=True):
            st.session_state.custom_assets = [
                {
                    'ticker': asset['ticker'],
                    'name': asset['name'],
                    'asset_class': asset['asset_class'],
                    'weight': asset['initial_weight']
                }
                for asset in assets_info
            ]
            st.success("✅ Loaded current portfolio")
            st.rerun()
        
        # Quick add popular portfolios
        with st.expander("🌟 Popular Portfolio Templates"):
            template = st.selectbox(
                "Choose a template:",
                ["Select...", "60/40 Stock/Bond", "All Weather", "Three Fund", "Aggressive Growth"]
            )
            
            if st.button("Load Template") and template != "Select...":
                if template == "60/40 Stock/Bond":
                    st.session_state.custom_assets = [
                        {'ticker': 'VTI', 'name': 'Total Stock Market', 'asset_class': 'Equities', 'weight': 0.60},
                        {'ticker': 'BND', 'name': 'Total Bond Market', 'asset_class': 'Fixed Income', 'weight': 0.40}
                    ]
                elif template == "All Weather":
                    st.session_state.custom_assets = [
                        {'ticker': 'VTI', 'name': 'Stocks', 'asset_class': 'Equities', 'weight': 0.30},
                        {'ticker': 'TLT', 'name': 'Long-Term Bonds', 'asset_class': 'Fixed Income', 'weight': 0.40},
                        {'ticker': 'IEF', 'name': 'Intermediate Bonds', 'asset_class': 'Fixed Income', 'weight': 0.15},
                        {'ticker': 'GLD', 'name': 'Gold', 'asset_class': 'Commodities', 'weight': 0.075},
                        {'ticker': 'DBC', 'name': 'Commodities', 'asset_class': 'Commodities', 'weight': 0.075}
                    ]
                elif template == "Three Fund":
                    st.session_state.custom_assets = [
                        {'ticker': 'VTI', 'name': 'US Stocks', 'asset_class': 'Equities', 'weight': 0.40},
                        {'ticker': 'VXUS', 'name': 'International Stocks', 'asset_class': 'Equities', 'weight': 0.30},
                        {'ticker': 'BND', 'name': 'Bonds', 'asset_class': 'Fixed Income', 'weight': 0.30}
                    ]
                elif template == "Aggressive Growth":
                    st.session_state.custom_assets = [
                        {'ticker': 'QQQ', 'name': 'Tech Growth', 'asset_class': 'Equities', 'weight': 0.40},
                        {'ticker': 'VUG', 'name': 'Growth Stocks', 'asset_class': 'Equities', 'weight': 0.30},
                        {'ticker': 'VXUS', 'name': 'International', 'asset_class': 'Equities', 'weight': 0.20},
                        {'ticker': 'ARKK', 'name': 'Innovation', 'asset_class': 'Equities', 'weight': 0.10}
                    ]
                st.success(f"✅ Loaded {template} template")
                st.rerun()
    
    with col2:
        st.markdown('<h3 class="sub-header">📊 Your Custom Portfolio</h3>', unsafe_allow_html=True)
        
        if not st.session_state.custom_assets:
            st.info("👈 Add assets to start building your portfolio")
        else:
            # Display current assets
            total_weight = sum(asset['weight'] for asset in st.session_state.custom_assets)
            
            # Weight status indicator
            if abs(total_weight - 1.0) < 0.001:
                st.success(f"✅ Total Allocation: {total_weight*100:.1f}%")
            else:
                st.warning(f"⚠️ Total Allocation: {total_weight*100:.1f}% (should be 100%)")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Editable assets list
            for idx, asset in enumerate(st.session_state.custom_assets):
                with st.container():
                    col_a, col_b, col_c = st.columns([3, 2, 1])
                    
                    with col_a:
                        st.markdown(f"""
                        <div style="padding: 0.5rem; background: white; border-radius: 8px; border-left: 4px solid #667eea;">
                            <strong>{asset['ticker']}</strong> - {asset['name']}<br>
                            <span style="color: #6b7280; font-size: 0.875rem;">{asset['asset_class']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_b:
                        # Update weight
                        new_weight = st.number_input(
                            f"Weight_{idx}",
                            min_value=0.0,
                            max_value=100.0,
                            value=asset['weight'] * 100,
                            step=1.0,
                            key=f"weight_{idx}",
                            label_visibility="collapsed"
                        )
                        st.session_state.custom_assets[idx]['weight'] = new_weight / 100
                    
                    with col_c:
                        if st.button("🗑️", key=f"delete_{idx}", use_container_width=True):
                            st.session_state.custom_assets.pop(idx)
                            st.rerun()
                    
                    st.markdown("<br>", unsafe_allow_html=True)
            
            # Normalize weights button
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("⚖️ Normalize Weights", use_container_width=True):
                    if total_weight > 0:
                        for asset in st.session_state.custom_assets:
                            asset['weight'] = asset['weight'] / total_weight
                        st.success("✅ Weights normalized to 100%")
                        st.rerun()
            
            with col_b:
                if st.button("🗑️ Clear All", use_container_width=True):
                    st.session_state.custom_assets = []
                    st.rerun()
    
    # Analysis section
    if st.session_state.custom_assets and abs(total_weight - 1.0) < 0.05:  # Allow 5% tolerance
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<h3 class="sub-header">📈 Portfolio Analysis</h3>', unsafe_allow_html=True)
        
        if st.button("🚀 Analyze Portfolio", type="primary", use_container_width=True):
            with st.spinner("Fetching market data and analyzing..."):
                try:
                    # Fetch data for custom tickers
                    custom_tickers = [asset['ticker'] for asset in st.session_state.custom_assets]
                    
                    # Try to fetch data
                    from config.settings import START_DATE
                    custom_price_data = fetch_market_data(custom_tickers, START_DATE)
                    
                    if custom_price_data.empty:
                        st.error("❌ No data available for these tickers")
                        return
                    
                    # Set Date as index
                    custom_price_data = custom_price_data.set_index('Date')
                    
                    # Normalize weights
                    weights = np.array([asset['weight'] for asset in st.session_state.custom_assets])
                    weights = weights / weights.sum()
                    
                    # Store in session state
                    st.session_state.custom_price_data = custom_price_data
                    st.session_state.custom_weights = weights
                    st.session_state.analysis_ready = True
                    
                    st.success("✅ Analysis complete!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error fetching data: {str(e)}")
                    st.info("💡 Make sure all ticker symbols are valid")
        
        # Display analysis if ready
        if hasattr(st.session_state, 'analysis_ready') and st.session_state.analysis_ready:
            st.markdown("<br>", unsafe_allow_html=True)
            
            custom_price_data = st.session_state.custom_price_data
            custom_weights = st.session_state.custom_weights
            
            # Calculate custom portfolio metrics
            try:
                # Calculate expected returns and covariance
                custom_expected_returns = calculate_expected_returns(custom_price_data)
                custom_cov_matrix = calculate_covariance_matrix(custom_price_data)
                
                # Calculate portfolio metrics
                custom_portfolio_return = np.dot(custom_weights, custom_expected_returns)
                custom_portfolio_volatility = np.sqrt(np.dot(custom_weights, np.dot(custom_cov_matrix, custom_weights)))
                custom_sharpe = (custom_portfolio_return - settings.RISK_FREE_RATE) / custom_portfolio_volatility
                
                # Calculate current portfolio metrics for comparison
                current_expected_returns = calculate_expected_returns(price_data)
                current_cov_matrix = calculate_covariance_matrix(price_data)
                
                current_prices = {col: price_data[col].iloc[-1] for col in price_data.columns}
                allocation_df = portfolio.get_current_allocation(current_prices)
                current_weights_array = allocation_df['weight'].values
                
                current_portfolio_return = np.dot(current_weights_array, current_expected_returns)
                current_portfolio_volatility = np.sqrt(np.dot(current_weights_array, np.dot(current_cov_matrix, current_weights_array)))
                current_sharpe = (current_portfolio_return - settings.RISK_FREE_RATE) / current_portfolio_volatility
                
                # Display comparison
                st.markdown("#### 📊 Portfolio Comparison")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("##### Your Custom Portfolio")
                    st.metric("Expected Return", f"{custom_portfolio_return*100:.2f}%")
                    st.metric("Volatility (Risk)", f"{custom_portfolio_volatility*100:.2f}%")
                    st.metric("Sharpe Ratio", f"{custom_sharpe:.3f}")
                
                with col2:
                    st.markdown("##### Current Portfolio")
                    st.metric("Expected Return", f"{current_portfolio_return*100:.2f}%")
                    st.metric("Volatility (Risk)", f"{current_portfolio_volatility*100:.2f}%")
                    st.metric("Sharpe Ratio", f"{current_sharpe:.3f}")
                
                with col3:
                    st.markdown("##### Difference")
                    return_diff = (custom_portfolio_return - current_portfolio_return) * 100
                    vol_diff = (custom_portfolio_volatility - current_portfolio_volatility) * 100
                    sharpe_diff = custom_sharpe - current_sharpe
                    
                    st.metric("Return Difference", f"{return_diff:+.2f}%", delta=f"{return_diff:+.2f}%")
                    st.metric("Risk Difference", f"{vol_diff:+.2f}%", delta=f"{vol_diff:+.2f}%", delta_color="inverse")
                    st.metric("Sharpe Difference", f"{sharpe_diff:+.3f}", delta=f"{sharpe_diff:+.3f}")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Tabs for detailed analysis
                tab1, tab2, tab3, tab4 = st.tabs(["📊 Allocation", "📈 Efficient Frontier", "📉 Historical Performance", "📋 Asset Details"])
                
                with tab1:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("##### Custom Portfolio Allocation")
                        fig = go.Figure(data=[go.Pie(
                            labels=[asset['ticker'] for asset in st.session_state.custom_assets],
                            values=[asset['weight'] for asset in st.session_state.custom_assets],
                            hole=0.4,
                            marker=dict(colors=px.colors.qualitative.Set3)
                        )])
                        fig.update_layout(height=400, template='plotly_white', showlegend=True)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.markdown("##### Current Portfolio Allocation")
                        fig = go.Figure(data=[go.Pie(
                            labels=[asset['ticker'] for asset in assets_info],
                            values=[asset['initial_weight'] for asset in assets_info],
                            hole=0.4,
                            marker=dict(colors=px.colors.qualitative.Set2)
                        )])
                        fig.update_layout(height=400, template='plotly_white', showlegend=True)
                        st.plotly_chart(fig, use_container_width=True)
                
                with tab2:
                    st.markdown("##### Custom Portfolio Efficient Frontier")
                    
                    # Run Markowitz analysis for custom portfolio
                    custom_analysis = analyze_portfolio_markowitz(
                        custom_price_data,
                        custom_weights,
                        settings.RISK_FREE_RATE
                    )
                    
                    fig = plot_efficient_frontier(
                        custom_analysis['efficient_frontier'],
                        custom_analysis['random_portfolios'],
                        custom_analysis['current_portfolio'],
                        custom_analysis['optimal_portfolios'],
                        custom_analysis['asset_metrics']
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show optimal weights
                    st.markdown("##### 🎯 Optimized Weights (Max Sharpe)")
                    max_sharpe = custom_analysis['optimal_portfolios']['max_sharpe']
                    
                    weights_comparison = pd.DataFrame({
                        'Asset': [asset['ticker'] for asset in st.session_state.custom_assets],
                        'Current Weight': [asset['weight'] * 100 for asset in st.session_state.custom_assets],
                        'Optimal Weight': max_sharpe['weights'] * 100,
                        'Difference': max_sharpe['weights'] * 100 - np.array([asset['weight'] * 100 for asset in st.session_state.custom_assets])
                    })
                    
                    st.dataframe(
                        weights_comparison.style.format({
                            'Current Weight': '{:.2f}%',
                            'Optimal Weight': '{:.2f}%',
                            'Difference': '{:+.2f}%'
                        }),
                        use_container_width=True,
                        hide_index=True
                    )
                
                with tab3:
                    st.markdown("##### Simulated Historical Performance")
                    
                    # Calculate hypothetical portfolio values
                    custom_returns = custom_price_data.pct_change().dropna()
                    custom_portfolio_returns = (custom_returns * custom_weights).sum(axis=1)
                    custom_portfolio_value = settings.INITIAL_CAPITAL * (1 + custom_portfolio_returns).cumprod()
                    
                    current_returns = price_data.pct_change().dropna()
                    current_portfolio_returns = (current_returns * current_weights_array).sum(axis=1)
                    current_portfolio_value = settings.INITIAL_CAPITAL * (1 + current_portfolio_returns).cumprod()
                    
                    # Plot comparison
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatter(
                        x=custom_portfolio_value.index,
                        y=custom_portfolio_value.values,
                        mode='lines',
                        name='Custom Portfolio',
                        line=dict(color='#667eea', width=3)
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=current_portfolio_value.index,
                        y=current_portfolio_value.values,
                        mode='lines',
                        name='Current Portfolio',
                        line=dict(color='#f59e0b', width=3, dash='dash')
                    ))
                    
                    fig.add_hline(
                        y=settings.INITIAL_CAPITAL,
                        line_dash="dot",
                        line_color="#94a3b8",
                        annotation_text=f"Initial: ${settings.INITIAL_CAPITAL:,.0f}"
                    )
                    
                    fig.update_layout(
                        title="Hypothetical Performance Comparison",
                        xaxis_title="Date",
                        yaxis_title="Portfolio Value ($)",
                        height=500,
                        template='plotly_white',
                        hovermode='x unified',
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Performance metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        custom_final = custom_portfolio_value.iloc[-1]
                        st.metric("Custom Final Value", f"${custom_final:,.0f}", 
                                 f"{(custom_final - settings.INITIAL_CAPITAL)/settings.INITIAL_CAPITAL*100:.2f}%")
                    
                    with col2:
                        current_final = current_portfolio_value.iloc[-1]
                        st.metric("Current Final Value", f"${current_final:,.0f}",
                                 f"{(current_final - settings.INITIAL_CAPITAL)/settings.INITIAL_CAPITAL*100:.2f}%")
                    
                    with col3:
                        custom_vol = custom_portfolio_returns.std() * np.sqrt(252) * 100
                        st.metric("Custom Volatility", f"{custom_vol:.2f}%")
                    
                    with col4:
                        current_vol = current_portfolio_returns.std() * np.sqrt(252) * 100
                        st.metric("Current Volatility", f"{current_vol:.2f}%")
                
                with tab4:
                    st.markdown("##### Individual Asset Metrics")
                    
                    asset_details = []
                    for i, asset in enumerate(st.session_state.custom_assets):
                        ticker = asset['ticker']
                        returns = custom_price_data[ticker].pct_change().dropna()
                        
                        asset_details.append({
                            'Ticker': ticker,
                            'Name': asset['name'],
                            'Class': asset['asset_class'],
                            'Weight': f"{asset['weight']*100:.2f}%",
                            'Expected Return': f"{custom_expected_returns.iloc[i]*100:.2f}%",
                            'Volatility': f"{returns.std() * np.sqrt(252) * 100:.2f}%",
                            'Total Return': f"{((custom_price_data[ticker].iloc[-1] / custom_price_data[ticker].iloc[0]) - 1) * 100:.2f}%"
                        })
                    
                    details_df = pd.DataFrame(asset_details)
                    st.dataframe(details_df, use_container_width=True, hide_index=True)
                    
                    # Correlation heatmap
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("##### Asset Correlation Matrix")
                    
                    correlation_matrix = custom_price_data.corr()
                    
                    fig = go.Figure(data=go.Heatmap(
                        z=correlation_matrix.values,
                        x=correlation_matrix.columns,
                        y=correlation_matrix.index,
                        colorscale='RdBu',
                        zmid=0,
                        text=correlation_matrix.values,
                        texttemplate='%{text:.2f}',
                        textfont={"size": 12},
                        colorbar=dict(title="Correlation")
                    ))
                    
                    fig.update_layout(
                        height=400,
                        template='plotly_white'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error in analysis: {str(e)}")
                import traceback
                st.code(traceback.format_exc())


def show_weekly_report(assets_info, price_data):
    """Weekly report generation page"""
    st.markdown('<p class="main-header">📧 Weekly Report Generator</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>📨 Rapport Hebdomadaire</strong><br>
        Generate weekly PDF reports in French with closing prices to send to your teacher every Wednesday.
        The PDF contains professional formatting with asset prices, variations, and French date formatting.
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize report generator
    report_gen = WeeklyReportGenerator(assets_info, settings.GROUP_NUMBER)
    
    # Get all Wednesday dates in project range
    all_wednesdays = get_next_wednesday_dates(settings.START_DATE, settings.END_DATE)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h3 class="sub-header">📅 Report Configuration</h3>', unsafe_allow_html=True)
        
        # Date selection
        report_date_option = st.radio(
            "Select report date:",
            ["Most Recent Data", "Specific Wednesday", "Custom Date"],
            help="Choose which date to use for the report"
        )
        
        if report_date_option == "Most Recent Data":
            # Use last available date from data
            report_date = price_data.index[-1].strftime('%Y-%m-%d')
            st.info(f"📅 Using last available date: {report_date}")
        
        elif report_date_option == "Specific Wednesday":
            # Select from available Wednesdays
            selected_wednesday = st.selectbox(
                "Choose Wednesday:",
                all_wednesdays,
                index=len(all_wednesdays)-1 if all_wednesdays else 0,
                format_func=lambda x: report_gen.format_french_date(x)
            )
            report_date = selected_wednesday
        
        else:  # Custom Date
            # Use date picker
            min_date = datetime.strptime(settings.START_DATE, '%Y-%m-%d').date()
            max_date = price_data.index[-1].date()
            
            selected_date = st.date_input(
                "Select date:",
                value=max_date,
                min_value=min_date,
                max_value=max_date
            )
            report_date = selected_date.strftime('%Y-%m-%d')
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Recipient information
        with st.expander("✉️ Email Configuration", expanded=False):
            recipient_email = st.text_input(
                "Recipient Email",
                value=settings.TEACHER_EMAIL,
                help="Email address of the teacher"
            )
            
            group_number = st.number_input(
                "Group Number",
                value=settings.GROUP_NUMBER,
                min_value=1,
                max_value=20,
                help="Your group number"
            )
            
            report_gen.recipient_email = recipient_email
            report_gen.group_number = int(group_number)
    
    with col2:
        st.markdown('<h3 class="sub-header">📊 Quick Stats</h3>', unsafe_allow_html=True)
        
        # Show statistics about reports
        total_wednesdays = len(all_wednesdays)
        weeks_elapsed = sum(1 for w in all_wednesdays if w <= report_date)
        
        st.metric("Total Report Weeks", total_wednesdays)
        st.metric("Weeks Elapsed", weeks_elapsed)
        st.metric("Weeks Remaining", total_wednesdays - weeks_elapsed)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Quick info
        st.markdown("""
        **Report Schedule:**
        - Frequency: Weekly
        - Day: Wednesday
        - Recipient: ckharoubi@escp.eu
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Generate report button
    if st.button("🚀 Generate Report", type="primary", use_container_width=True):
        try:
            # Get closing prices for selected date
            closing_prices = report_gen.get_closing_prices_from_data(price_data, report_date)
            
            # Generate report bodies
            plain_body = report_gen.generate_email_body(closing_prices, report_date)
            html_body = report_gen.generate_html_body(closing_prices, report_date)
            subject = report_gen.generate_email_subject(report_date)
            
            # Store in session state
            st.session_state.report_plain = plain_body
            st.session_state.report_html = html_body
            st.session_state.report_subject = subject
            st.session_state.report_date = report_date
            st.session_state.closing_prices = closing_prices
            st.session_state.report_generated = True
            
            st.success("✅ Report generated successfully!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error generating report: {str(e)}")
    
    # Display generated report
    if hasattr(st.session_state, 'report_generated') and st.session_state.report_generated:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<h3 class="sub-header">📝 Generated Report</h3>', unsafe_allow_html=True)
        
        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📄 Plain Text", "📊 Closing Prices", "📕 PDF Export", "📤 Download Options"])
        
        with tab1:
            st.markdown("##### Plain Text Email")
            st.code(st.session_state.report_plain, language=None)
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "📥 Download TXT",
                    st.session_state.report_plain,
                    file_name=f"weekly_report_{st.session_state.report_date}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with col2:
                if st.button("📋 Copy to Clipboard", use_container_width=True):
                    st.code(st.session_state.report_plain, language=None)
                    st.info("💡 Select the text above and copy it (Ctrl+C or Cmd+C)")
        
        with tab2:
            st.markdown("##### Closing Prices Table")
            
            # Create detailed table
            prices_data = []
            for asset in assets_info:
                ticker = asset['ticker']
                price = st.session_state.closing_prices.get(ticker, 0.0)
                initial_price = asset.get('initial_price', 0.0)
                
                if initial_price > 0:
                    change = price - initial_price
                    change_pct = (change / initial_price) * 100
                else:
                    change = 0
                    change_pct = 0
                
                prices_data.append({
                    'Ticker': ticker,
                    'Name': asset['name'],
                    'Asset Class': asset['asset_class'],
                    'Closing Price': f"${price:.2f}",
                    'Initial Price': f"${initial_price:.2f}",
                    'Change': f"${change:+.2f}",
                    'Change %': f"{change_pct:+.2f}%"
                })
            
            prices_df = pd.DataFrame(prices_data)
            st.dataframe(prices_df, use_container_width=True, hide_index=True)
            
            # Summary statistics
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_change = sum((st.session_state.closing_prices.get(a['ticker'], a.get('initial_price', 0)) - a.get('initial_price', 0)) / a.get('initial_price', 1) * 100 for a in assets_info) / len(assets_info)
                st.metric("Average Change", f"{avg_change:.2f}%")
            
            with col2:
                best_performer = max(assets_info, key=lambda a: (st.session_state.closing_prices.get(a['ticker'], a.get('initial_price', 0)) - a.get('initial_price', 0)) / a.get('initial_price', 1))
                st.metric("Best Performer", best_performer['ticker'])
            
            with col3:
                worst_performer = min(assets_info, key=lambda a: (st.session_state.closing_prices.get(a['ticker'], a.get('initial_price', 0)) - a.get('initial_price', 0)) / a.get('initial_price', 1))
                st.metric("Worst Performer", worst_performer['ticker'])
            
            with col4:
                report_date_obj = datetime.strptime(st.session_state.report_date, '%Y-%m-%d')
                st.metric("Report Date", report_date_obj.strftime('%d/%m/%Y'))
        
        with tab3:
            st.markdown("##### 📕 Generate PDF Report")
            
            st.markdown("""
            Generate a professional PDF document ready to send to your teacher.
            
            **Features:**
            - ✅ Professional formatting with colored header
            - ✅ Formatted table with all asset prices
            - ✅ Price variations shown
            - ✅ French date and number formatting
            - ✅ Ready to email as attachment
            """)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if st.button("📕 Generate PDF Document", type="primary", use_container_width=True):
                    try:
                        with st.spinner("Generating PDF..."):
                            pdf_path = report_gen.generate_pdf(
                                st.session_state.closing_prices,
                                st.session_state.report_date,
                                settings.WEEKLY_REPORTS_DIR
                            )
                            st.session_state.pdf_path = pdf_path
                            st.success(f"✅ PDF generated successfully!")
                            st.info(f"📁 Saved to: `{pdf_path}`")
                    except ImportError:
                        st.error("❌ PDF library not installed. Run: `pip install reportlab`")
                    except Exception as e:
                        st.error(f"❌ Error generating PDF: {str(e)}")
            
            with col2:
                st.markdown("""
                **PDF Contents:**
                - Title page
                - Date
                - Greeting
                - Asset table
                - Signature
                """)
            
            # Show download button if PDF exists
            if hasattr(st.session_state, 'pdf_path'):
                st.markdown("<br>", unsafe_allow_html=True)
                
                try:
                    with open(st.session_state.pdf_path, 'rb') as pdf_file:
                        pdf_bytes = pdf_file.read()
                        
                        st.download_button(
                            label="📥 Download PDF",
                            data=pdf_bytes,
                            file_name=f"weekly_report_{st.session_state.report_date}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            type="primary"
                        )
                        
                        st.success("✅ PDF ready to download! Click the button above.")
                except Exception as e:
                    st.error(f"❌ Error loading PDF: {str(e)}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("---")
            
            # Instructions
            st.markdown("##### 📧 How to Send the PDF")
            st.markdown("""
            1. Click **"Generate PDF Document"** above
            2. Click **"Download PDF"** to save to your computer
            3. Open your email client (Gmail, Outlook, etc.)
            4. Compose new email to: **`ckharoubi@escp.eu`**
            5. Subject: **`Suivi de portefeuille - {}`**
            6. Attach the downloaded PDF file
            7. Add a brief message (optional)
            8. Send!
            
            **The PDF contains all the information in a professional format.**
            """.format(report_gen.format_french_date(st.session_state.report_date)))
        
        with tab4:
            st.markdown("##### 📤 Additional Download Options")
            
            st.markdown("**💾 Save Text Report**")
            if st.button("💾 Save Plain Text to File", use_container_width=True):
                try:
                    file_path = report_gen.save_report_to_file(
                        st.session_state.report_plain,
                        st.session_state.report_date,
                        settings.WEEKLY_REPORTS_DIR
                    )
                    st.success(f"✅ Text report saved to: `{file_path}`")
                except Exception as e:
                    st.error(f"❌ Error saving file: {str(e)}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("**📥 Download HTML Version**")
            st.download_button(
                "📥 Download HTML",
                st.session_state.report_html,
                file_name=f"weekly_report_{st.session_state.report_date}.html",
                mime="text/html",
                use_container_width=True
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("---")
            
            st.markdown("**📋 Copy for Email Body**")
            st.markdown("""
            If you prefer to paste the report directly into an email body:
            1. Go to the **📄 Plain Text** tab
            2. Copy the text
            3. Paste into your email
            4. Send to `ckharoubi@escp.eu`
            """)
    
    # Historical reports section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<h3 class="sub-header">📚 Historical Reports</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("##### All Wednesday Dates in Project Period")
        
        if all_wednesdays:
            wednesdays_data = []
            for wednesday in all_wednesdays:
                french_date = report_gen.format_french_date(wednesday)
                is_past = wednesday <= datetime.now().strftime('%Y-%m-%d')
                status = "✅ Past" if is_past else "📅 Future"
                
                wednesdays_data.append({
                    'Date': wednesday,
                    'French Date': french_date,
                    'Status': status
                })
            
            wednesdays_df = pd.DataFrame(wednesdays_data)
            st.dataframe(wednesdays_df, use_container_width=True, hide_index=True, height=300)
        else:
            st.info("No Wednesday dates found in the project period")
    
    with col2:
        st.markdown("##### Quick Actions")
        
        if all_wednesdays:
            st.markdown(f"""
            **Project Period:**
            - Start: {report_gen.format_french_date(settings.START_DATE)}
            - End: {report_gen.format_french_date(settings.END_DATE)}
            
            **Total Reports:** {len(all_wednesdays)}
            
            **Next Wednesday:**
            """)
            
            # Find next Wednesday
            today = datetime.now().strftime('%Y-%m-%d')
            future_wednesdays = [w for w in all_wednesdays if w > today]
            
            if future_wednesdays:
                next_wed = future_wednesdays[0]
                st.info(f"📅 {report_gen.format_french_date(next_wed)}")
            else:
                st.info("No future Wednesdays in project period")


def show_settings():
    """Enhanced settings page"""
    st.markdown('<p class="main-header">⚙️ Settings & Configuration</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="sub-header">Project Configuration</h3>', unsafe_allow_html=True)
        
        config_data = {
            'Parameter': ['Start Date', 'End Date', 'Initial Capital', 'Risk-Free Rate', 'Report Frequency'],
            'Value': [
                settings.START_DATE,
                settings.END_DATE,
                f"${settings.INITIAL_CAPITAL:,.0f}",
                f"{settings.RISK_FREE_RATE*100:.1f}%",
                'Weekly'
            ]
        }
        
        config_df = pd.DataFrame(config_data)
        st.dataframe(config_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown('<h3 class="sub-header">Tracked Assets</h3>', unsafe_allow_html=True)
        
        assets_info = load_asset_info(settings.ASSETS_INFO_PATH)
        assets_display = []
        for asset in assets_info:
            assets_display.append({
                'Ticker': asset['ticker'],
                'Name': asset['name'],
                'Class': asset['asset_class'],
                'Weight': f"{asset['initial_weight']*100:.0f}%"
            })
        
        assets_df = pd.DataFrame(assets_display)
        st.dataframe(assets_df, use_container_width=True, hide_index=True)
    

    


if __name__ == "__main__":
    main()