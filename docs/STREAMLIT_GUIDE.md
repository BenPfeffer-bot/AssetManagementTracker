# 🚀 Streamlit Dashboard Guide

## Quick Start

Launch your interactive portfolio dashboard in seconds:

```bash
./run_dashboard.sh
```

Or directly:

```bash
streamlit run app.py
```

The dashboard will automatically open at `http://localhost:8501`

## Dashboard Overview

### 📊 Main Pages

#### 1. **Dashboard** (Home)
The main overview page featuring:
- **Current Portfolio Value** with gain/loss indicators
- **Total Return** percentage
- **Risk Metrics** (Volatility, Sharpe Ratio)
- **Interactive Portfolio Evolution Chart** - Track your portfolio value over time
- **Asset Allocation Pie Chart** - Visualize your diversification
- **Performance Summary** - Returns, risk metrics, and risk-adjusted returns

#### 2. **Analytics** 
Deep dive into portfolio analytics:
- **Returns Distribution** - Histogram showing daily return patterns
- **Drawdown Analysis** - Visualize portfolio drawdowns over time
- **Correlation Matrix** - Interactive heatmap of asset correlations
- **Individual Asset Performance** - Compare each asset's cumulative returns

#### 3. **Holdings** 
Detailed view of your portfolio composition:
- **Current Holdings Table** - All positions with current values and weights
- **Weight Drift Analysis** - Compare current vs. initial allocations
- **Asset Details Cards** - Individual asset performance and metrics

#### 4. **Data Explorer**
Access and export your data:
- **Price Data Table** - Historical prices for all assets
- **Portfolio Value Table** - Time series of portfolio values
- **Summary Statistics** - Descriptive statistics for all metrics
- **CSV Export** - Download data for external analysis

#### 5. **Settings**
Project configuration and information:
- Project timeline and parameters
- Tracked assets list
- About section with feature overview

## Key Features

### 🔄 Live Data Refresh
Click the **"🔄 Refresh Data"** button in the sidebar to fetch the latest market data without restarting the app.

### 📊 Interactive Charts
All charts are built with Plotly, offering:
- **Zoom and Pan** - Explore data in detail
- **Hover Information** - See exact values on hover
- **Legend Toggle** - Click legend items to show/hide series
- **Export** - Download charts as PNG images

### 📥 Data Export
Export any table or dataset as CSV:
- Price data with all tickers
- Portfolio value time series
- Holdings information
- Returns and statistics

### 💡 Real-Time Metrics
All metrics update automatically when data is refreshed:
- Portfolio value and returns
- Sharpe and Sortino ratios
- Volatility and drawdowns
- Value at Risk (VaR) and CVaR
- Correlation matrices

## Tips for Best Experience

### 1. **Regular Updates**
- Use the refresh button daily to get latest market data
- The app caches data for 1 hour for optimal performance

### 2. **Sharing Your Research**
To share your dashboard:

```bash
# Run on a specific port
streamlit run app.py --server.port 8501

# Share via network (be careful with security)
streamlit run app.py --server.address 0.0.0.0
```

### 3. **Deployment Options**

#### Option A: Streamlit Cloud (Free)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy! Your dashboard will be live on the web

#### Option B: Local Network
1. Find your local IP address:
   ```bash
   ipconfig getifaddr en0  # macOS
   hostname -I             # Linux
   ipconfig               # Windows
   ```
2. Run: `streamlit run app.py --server.address 0.0.0.0`
3. Share the URL: `http://YOUR_IP:8501`

### 4. **Performance Optimization**
- The app uses caching to minimize recomputations
- Data refreshes are on-demand to save API calls
- Charts render efficiently with Plotly

## Customization

### Modify Colors and Themes

Edit `app.py` to change the color scheme in the CSS section:

```python
st.markdown("""
    <style>
    .main-header {
        color: #YOUR_COLOR;  # Change this
    }
    </style>
""", unsafe_allow_html=True)
```

### Add Custom Metrics

To add new metrics to the dashboard:

1. Create calculation function in `analytics/`
2. Import in `app.py`
3. Add to the relevant page function
4. Display with `st.metric()` or charts

### Modify Layout

Streamlit uses a simple layout system:
- `st.columns()` - Create side-by-side layouts
- `st.tabs()` - Create tabbed interfaces
- `st.expander()` - Create collapsible sections

## Troubleshooting

### Port Already in Use
```bash
# Use a different port
streamlit run app.py --server.port 8503
```

### Data Not Loading
1. Check that `data/prices.csv` exists
2. Run `python main.py --fetch-data` first
3. Click "Refresh Data" in the sidebar

### Charts Not Displaying
1. Ensure plotly is installed: `pip install plotly`
2. Clear cache: Click "Clear Cache" in settings menu (⋮)
3. Refresh browser (Cmd/Ctrl + R)

## Advanced Usage

### Automated Reports
Combine CLI and dashboard:

```bash
# Update data via CLI
python main.py --fetch-data

# Dashboard will automatically pick up changes
# (or click refresh button)
```

### API Integration
The dashboard can be extended to:
- Send email reports
- Post to Slack/Teams
- Update databases
- Generate PDF reports

## Support

For issues or questions:
- Check the main README.md
- Review the code comments in `app.py`

---

