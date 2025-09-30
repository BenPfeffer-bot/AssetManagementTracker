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
    page_title="Portfolio Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .positive {
        color: #28a745;
        font-weight: bold;
    }
    .negative {
        color: #dc3545;
        font-weight: bold;
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


def main():
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150x150.png?text=Portfolio", width=150)
        st.title("📊 Portfolio Tracker")
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigation",
            ["🏠 Dashboard", "📈 Analytics", "💼 Holdings", "📊 Data Explorer", "⚙️ Settings"]
        )
        
        st.markdown("---")
        
        # Data refresh button
        if st.button("🔄 Refresh Data", use_container_width=True):
            try:
                with st.spinner("Fetching latest data..."):
                    update_price_data(settings.ASSET_TICKERS, settings.PRICES_CSV_PATH)
                    st.cache_data.clear()
                    st.success("Data refreshed!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error refreshing data: {e}")
        
        st.markdown("---")
        st.caption(f"**Project Period**\n{settings.START_DATE} to {settings.END_DATE}")
    
    # Load data
    assets_info, price_data, portfolio, portfolio_value = load_portfolio_data()
    
    if assets_info is None:
        st.error(f"Error loading data: {portfolio_value}")
        return
    
    # Route to selected page
    if page == "🏠 Dashboard":
        show_dashboard(assets_info, price_data, portfolio, portfolio_value)
    elif page == "📈 Analytics":
        show_analytics(price_data, portfolio_value)
    elif page == "💼 Holdings":
        show_holdings(assets_info, portfolio, price_data)
    elif page == "📊 Data Explorer":
        show_data_explorer(price_data, portfolio_value)
    elif page == "⚙️ Settings":
        show_settings()


def show_dashboard(assets_info, price_data, portfolio, portfolio_value):
    """Main dashboard page"""
    st.markdown('<p class="main-header">📈 Portfolio Dashboard</p>', unsafe_allow_html=True)
    
    # Calculate metrics
    current_value = portfolio_value.iloc[-1]
    total_return = calculate_total_return(portfolio_value)
    returns_df = calculate_returns(portfolio_value)
    daily_returns = returns_df['daily_return']
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Value",
            f"${current_value:,.2f}",
            f"${current_value - settings.INITIAL_CAPITAL:,.2f}"
        )
    
    with col2:
        st.metric(
            "Total Return",
            f"{total_return*100:.2f}%",
            delta=f"{total_return*100:.2f}%"
        )
    
    with col3:
        volatility = calculate_volatility(daily_returns)
        st.metric("Volatility (Ann.)", f"{volatility*100:.2f}%")
    
    with col4:
        sharpe = calculate_sharpe_ratio(daily_returns, settings.RISK_FREE_RATE)
        st.metric("Sharpe Ratio", f"{sharpe:.2f}")
    
    st.markdown("---")
    
    # Portfolio evolution chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Portfolio Value Evolution")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=portfolio_value.index,
            y=portfolio_value.values,
            mode='lines',
            name='Portfolio Value',
            line=dict(color='#2E86AB', width=3),
            fill='tozeroy',
            fillcolor='rgba(46, 134, 171, 0.1)'
        ))
        fig.add_hline(
            y=settings.INITIAL_CAPITAL,
            line_dash="dash",
            line_color="gray",
            annotation_text=f"Initial: ${settings.INITIAL_CAPITAL:,.0f}"
        )
        fig.update_layout(
            height=400,
            xaxis_title="Date",
            yaxis_title="Portfolio Value ($)",
            hovermode='x unified',
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Asset Allocation")
        tickers = [asset['ticker'] for asset in assets_info]
        weights = [asset['initial_weight'] for asset in assets_info]
        names = [asset['name'] for asset in assets_info]
        
        fig = go.Figure(data=[go.Pie(
            labels=tickers,
            values=weights,
            hole=0.4,
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Weight: %{percent}<extra></extra>'
        )])
        fig.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Performance metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📊 Returns")
        annualized_return = calculate_annualized_return(portfolio_value)
        st.metric("Annualized Return", f"{annualized_return*100:.2f}%")
        
        latest_weekly = returns_df['weekly_return'].iloc[-1]
        if pd.notna(latest_weekly):
            st.metric("Latest Weekly Return", f"{latest_weekly*100:.2f}%")
        
        cumulative = returns_df['cumulative_return'].iloc[-1]
        st.metric("Cumulative Return", f"{cumulative*100:.2f}%")
    
    with col2:
        st.subheader("⚠️ Risk Metrics")
        max_dd = calculate_max_drawdown(portfolio_value)
        st.metric("Max Drawdown", f"{max_dd['max_drawdown_pct']:.2f}%")
        
        var_95 = calculate_var(daily_returns, 0.95)
        st.metric("VaR (95%)", f"{var_95*100:.2f}%")
        
        cvar_95 = calculate_cvar(daily_returns, 0.95)
        st.metric("CVaR (95%)", f"{cvar_95*100:.2f}%")
    
    with col3:
        st.subheader("🎯 Risk-Adjusted")
        st.metric("Sharpe Ratio", f"{sharpe:.2f}")
        
        sortino = calculate_sortino_ratio(daily_returns, settings.RISK_FREE_RATE)
        st.metric("Sortino Ratio", f"{sortino:.2f}")
        
        info_text = "📈 **Status:** "
        if total_return > 0:
            info_text += "Outperforming"
        else:
            info_text += "Underperforming"
        st.info(info_text)


def show_analytics(price_data, portfolio_value):
    """Analytics page with detailed charts"""
    st.markdown('<p class="main-header">📈 Portfolio Analytics</p>', unsafe_allow_html=True)
    
    # Returns distribution
    returns_df = calculate_returns(portfolio_value)
    daily_returns = returns_df['daily_return'].dropna()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Returns Distribution")
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=daily_returns,
            nbinsx=30,
            name='Daily Returns',
            marker_color='#2E86AB'
        ))
        fig.add_vline(
            x=daily_returns.mean(),
            line_dash="dash",
            line_color="red",
            annotation_text=f"Mean: {daily_returns.mean():.4f}"
        )
        fig.update_layout(
            xaxis_title="Daily Returns",
            yaxis_title="Frequency",
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Drawdown Analysis")
        running_max = portfolio_value.expanding().max()
        drawdown = (portfolio_value - running_max) / running_max
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=drawdown.index,
            y=drawdown.values * 100,
            mode='lines',
            name='Drawdown',
            fill='tozeroy',
            line=dict(color='red', width=2),
            fillcolor='rgba(255, 0, 0, 0.1)'
        ))
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Drawdown (%)",
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Asset correlation
    st.subheader("Asset Correlation Matrix")
    correlation_matrix = calculate_correlation_matrix(price_data)
    
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
    fig.update_layout(height=500, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Individual asset performance
    st.subheader("Individual Asset Performance")
    asset_returns = price_data.pct_change().dropna()
    
    fig = go.Figure()
    for column in asset_returns.columns:
        cumulative_returns = (1 + asset_returns[column]).cumprod() - 1
        fig.add_trace(go.Scatter(
            x=cumulative_returns.index,
            y=cumulative_returns.values * 100,
            mode='lines',
            name=column,
            line=dict(width=2)
        ))
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Cumulative Returns (%)",
        height=400,
        template='plotly_white',
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)


def show_holdings(assets_info, portfolio, price_data):
    """Holdings page"""
    st.markdown('<p class="main-header">💼 Portfolio Holdings</p>', unsafe_allow_html=True)
    
    # Get current prices
    current_prices = {col: price_data[col].iloc[-1] for col in price_data.columns}
    
    # Calculate current allocation
    allocation_df = portfolio.get_current_allocation(current_prices)
    
    st.subheader("Current Holdings")
    
    # Format the dataframe for display
    display_df = allocation_df.copy()
    display_df['price'] = display_df['price'].apply(lambda x: f"${x:.2f}")
    display_df['value'] = display_df['value'].apply(lambda x: f"${x:,.2f}")
    display_df['weight'] = display_df['weight'].apply(lambda x: f"{x*100:.2f}%")
    display_df['initial_weight'] = display_df['initial_weight'].apply(lambda x: f"{x*100:.2f}%")
    display_df['shares'] = display_df['shares'].apply(lambda x: f"{x:.2f}")
    
    st.dataframe(
        display_df[['ticker', 'name', 'asset_class', 'shares', 'price', 'value', 'weight', 'initial_weight']],
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    # Weight drift analysis
    st.subheader("Weight Drift Analysis")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=allocation_df['ticker'],
        y=allocation_df['initial_weight'] * 100,
        name='Initial Weight',
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Bar(
        x=allocation_df['ticker'],
        y=allocation_df['weight'] * 100,
        name='Current Weight',
        marker_color='#2E86AB'
    ))
    
    fig.update_layout(
        xaxis_title="Asset",
        yaxis_title="Weight (%)",
        height=400,
        barmode='group',
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Asset details
    st.markdown("---")
    st.subheader("Asset Details")
    
    cols = st.columns(len(assets_info))
    for idx, (col, asset) in enumerate(zip(cols, assets_info)):
        with col:
            ticker = asset['ticker']
            current_price = current_prices[ticker]
            initial_price = asset['initial_price']
            price_change = (current_price - initial_price) / initial_price
            
            st.markdown(f"### {ticker}")
            st.write(f"**{asset['name']}**")
            st.write(f"Class: {asset['asset_class']}")
            st.metric(
                "Current Price",
                f"${current_price:.2f}",
                f"{price_change*100:.2f}%"
            )


def show_data_explorer(price_data, portfolio_value):
    """Data explorer page"""
    st.markdown('<p class="main-header">📊 Data Explorer</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Price Data", "Portfolio Value", "Statistics"])
    
    with tab1:
        st.subheader("Historical Price Data")
        st.dataframe(price_data, use_container_width=True)
        
        # Download button
        csv = price_data.to_csv()
        st.download_button(
            label="📥 Download Price Data (CSV)",
            data=csv,
            file_name=f"price_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with tab2:
        st.subheader("Portfolio Value Over Time")
        portfolio_df = portfolio_value.to_frame(name='Portfolio Value')
        st.dataframe(portfolio_df, use_container_width=True)
        
        # Download button
        csv = portfolio_df.to_csv()
        st.download_button(
            label="📥 Download Portfolio Data (CSV)",
            data=csv,
            file_name=f"portfolio_value_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with tab3:
        st.subheader("Summary Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Price Data Statistics**")
            st.dataframe(price_data.describe(), use_container_width=True)
        
        with col2:
            st.write("**Returns Statistics**")
            returns_df = calculate_returns(portfolio_value)
            st.dataframe(returns_df.describe(), use_container_width=True)


def show_settings():
    """Settings page"""
    st.markdown('<p class="main-header">⚙️ Settings</p>', unsafe_allow_html=True)
    
    st.subheader("Project Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Project Details**")
        st.info(f"""
        - **Start Date:** {settings.START_DATE}
        - **End Date:** {settings.END_DATE}
        - **Initial Capital:** ${settings.INITIAL_CAPITAL:,.2f}
        - **Risk-Free Rate:** {settings.RISK_FREE_RATE*100:.1f}%
        """)
    
    with col2:
        st.write("**Tracked Assets**")
        for ticker in settings.ASSET_TICKERS:
            st.write(f"- {ticker}")
    
    st.markdown("---")
    
    st.subheader("About")
    st.markdown("""
    This portfolio tracker is designed to monitor and analyze the performance of a diversified portfolio
    from September 23, 2025 to November 25, 2025.
    
    **Features:**
    - Real-time data updates using yfinance
    - Comprehensive performance analytics
    - Risk metrics and correlation analysis
    - Interactive visualizations
    - Data export capabilities
    
    **Report Recipient:** `ckharoubi@escp.eu`
    """)


if __name__ == "__main__":
    main()
