# 🚀 Quick Start Guide

## First Time Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Fetch Historical Data

```bash
# Option A: Fetch extended historical data (recommended for richer analysis)
python scripts/fetch_extended_data.py

# Option B: Fetch only project period data
python main.py --fetch-data
```

### 3. Launch Dashboard

```bash
# Easy way
./run_dashboard.sh

# Or directly
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501` 🎉

## Daily Workflow

### Update Data & View Dashboard

```bash
# 1. Open the dashboard
./run_dashboard.sh

# 2. Click "🔄 Refresh" in the sidebar to get latest data
```

## Dashboard Overview

### 🏠 Dashboard Tab
- **Quick Metrics**: Value, returns, volatility, Sharpe ratio
- **Performance Tab**: Portfolio evolution chart, annualized metrics
- **Allocation Tab**: Current allocation with pie chart and drift analysis
- **Risk Analysis Tab**: Drawdown and returns distribution

### 📊 Analytics
- Asset correlation heatmap
- Individual asset performance comparison
- Detailed statistics for each asset

### 💼 Holdings
- Complete holdings table
- Weight comparison (target vs actual)
- Value distribution visualization

### 📈 Data Explorer
- Browse all historical data
- Export to CSV for external analysis
- View summary statistics

### ⚙️ Settings
- Project configuration
- Asset information
- System details

## Tips for Best Results

### 📊 Better Visualizations
- More data = Better charts! Use `fetch_extended_data.py` for 6 months of history
- Hover over charts for detailed information
- Click legend items to show/hide specific assets

### 🔄 Keeping Data Fresh
- Click "Refresh" button daily for latest market data
- Data is cached for 1 hour for performance

### 📤 Sharing Your Research
1. **Screenshots**: Use the Plotly camera icon on charts
2. **Export Data**: Download CSVs from Data Explorer
3. **Deploy Online**: Use Streamlit Cloud (see STREAMLIT_GUIDE.md)

## Troubleshooting

### Dashboard Won't Load
```bash
# Check if data exists
ls -la data/prices.csv

# If not, fetch data
python scripts/fetch_extended_data.py
```

### Charts Look Empty
- You need more data points! Run `fetch_extended_data.py`
- Currently you have 128 days of data (from March to September 2025)

### Port Already in Use
```bash
# Use a different port
streamlit run app.py --server.port 8503
```

## Command Reference

```bash
# Data Management
python scripts/fetch_extended_data.py  # Get 6 months of data
python main.py --fetch-data            # Get project period data
python main.py --generate-report       # Generate static report
python main.py --all                   # Fetch + report

# Dashboard
./run_dashboard.sh                     # Launch dashboard
streamlit run app.py                   # Launch directly
streamlit run app.py --server.port 8503  # Custom port
```

## What's Next?

1. ✅ **Explore the dashboard** - Check all tabs and features
2. ✅ **Review your holdings** - See asset allocation and weights
3. ✅ **Analyze performance** - Study returns and risk metrics
4. ✅ **Export data** - Download CSVs for presentations
5. ✅ **Share results** - Deploy to Streamlit Cloud or export reports

## Need Help?

- 📖 **Full Documentation**: See `README.md`
- 🎨 **Dashboard Guide**: See `STREAMLIT_GUIDE.md`

---

