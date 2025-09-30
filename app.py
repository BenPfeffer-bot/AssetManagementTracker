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
from core.loader import load_asset_info, load_price_data, update_price_data
from core.portfolio import Portfolio
from analytics.performance import (
    calculate_returns, calculate_volatility, calculate_sharpe_ratio,
    calculate_max_drawdown, calculate_total_return, calculate_annualized_return
)
from analytics.risk import calculate_correlation_matrix, calculate_var, calculate_cvar, calculate_sortino_ratio

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
        portfolio_value = portfolio.calculate_value(price_data)
        
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
            ["🏠 Dashboard", "📊 Analytics", "💼 Holdings", "📈 Data Explorer", "⚙️ Settings"],
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
    elif page == "📈 Data Explorer":
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