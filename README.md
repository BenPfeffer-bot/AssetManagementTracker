# Portfolio Management Tracker

A Python application to track, analyze, and report on the performance of a financial portfolio.

## Overview

This project tracks a diversified portfolio consisting of:
- **QQQ** (30%) - US Tech Stocks
- **IEMG** (15%) - Emerging Markets Stocks
- **SHV** (18%) - Short-Term US Treasury Bonds
- **TLT** (22%) - Long-Term US Treasury Bonds
- **IAU** (15%) - Gold (Precious Metals)

**Project Duration:** September 23, 2025 - November 25, 2025  
**Initial Capital:** $100,000  
**Reporting:** Weekly performance reports

## Features

- **Real-time Data Fetching:** Uses yfinance to fetch historical and current market data
- **Performance Analytics:** Calculate returns, volatility, Sharpe ratio, and maximum drawdown
- **Risk Metrics:** Correlation analysis, VaR, CVaR, and downside deviation
- **Portfolio Builder:** 🆕 Interactive tool to experiment with different assets, compare expected returns, and optimize allocations
- **Markowitz Optimization:** Efficient frontier analysis and optimal portfolio recommendations
- **Professional Visualizations:** Portfolio evolution, asset allocation, correlation heatmaps, and more
- **Automated Reports:** Generate comprehensive one-page performance reports
- **Interactive Dashboard:** Modern Streamlit web interface with real-time updates

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AssetManagementTracker
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
AssetManagementTracker/
├── config/
│   └── settings.py           # Configuration and constants
├── core/
│   ├── loader.py             # Data loading utilities
│   └── portfolio.py          # Portfolio class
├── analytics/
│   ├── performance.py        # Performance metrics
│   ├── risk.py               # Risk metrics
│   └── visualizer.py         # Chart generation
├── reports/
│   ├── onepager_generator.py # Report generator
│   ├── report_template.html  # HTML template
│   └── charts/               # Generated charts
├── utils/
│   └── helpers.py            # Helper functions
├── data/
│   ├── assets_info.json      # Asset metadata
│   └── prices.csv            # Historical price data
├── main.py                   # Main entry point
└── requirements.txt          # Python dependencies
```

## Usage

### 🌐 Interactive Web Dashboard (Recommended)

Launch the interactive Streamlit dashboard for real-time portfolio tracking:

```bash
# Option 1: Using the startup script
./run_dashboard.sh

# Option 2: Direct command
streamlit run app.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

**Dashboard Features:**
- 📊 Real-time portfolio metrics and visualizations
- 📈 Interactive charts with Plotly
- 💼 Detailed holdings analysis
- 📉 Risk analytics and correlation matrices
- 🔧 **Portfolio Builder** - NEW! Experiment with different assets and see expected returns
- 🎯 Markowitz optimization with efficient frontier visualization
- 📥 Data export capabilities
- 🔄 One-click data refresh

### 📊 Command Line Interface

#### Fetch Market Data

```bash
python main.py --fetch-data
```

This command downloads historical price data for all assets and saves it to `data/prices.csv`.

#### Generate Report

```bash
python main.py --generate-report
```

This command generates a comprehensive performance report with:
- Key performance metrics (returns, volatility, Sharpe ratio)
- Risk analytics (VaR, CVaR, correlations)
- Professional charts and visualizations

#### Fetch Data and Generate Report

```bash
python main.py --all
```

This command fetches the latest data and generates a report in one step.

## 🔧 Portfolio Builder (New Feature!)

The **Portfolio Builder** is an interactive tool that allows you to:

1. **Experiment with Different Assets**
   - Add any stock, bond, or ETF by ticker symbol
   - Try popular portfolio templates (60/40, All Weather, Three Fund, etc.)
   - Build completely custom portfolios from scratch

2. **Compare Expected Returns**
   - See expected returns, volatility, and Sharpe ratios
   - Compare your custom portfolio with the current portfolio
   - View side-by-side performance metrics

3. **Optimize Allocations**
   - Run full Markowitz optimization analysis
   - Visualize the efficient frontier
   - Get optimal weight recommendations

4. **Backtest Performance**
   - See how your portfolio would have performed historically
   - Compare multiple portfolio strategies
   - Analyze asset correlations and diversification

**Quick Start:**
1. Launch the dashboard: `streamlit run app.py`
2. Click **🔧 Portfolio Builder** in the sidebar
3. Choose a template or add assets manually
4. Click **🚀 Analyze Portfolio**
5. Review the comprehensive analysis

**Documentation:**
- `docs/PORTFOLIO_BUILDER_QUICKSTART.md` - 60-second quick start
- `docs/PORTFOLIO_BUILDER_GUIDE.md` - Comprehensive user guide
- `docs/PORTFOLIO_BUILDER_FEATURE.md` - Technical implementation details

## Performance Metrics

The system calculates and reports:

- **Returns:** Daily, weekly, and cumulative returns
- **Volatility:** Annualized volatility (standard deviation)
- **Sharpe Ratio:** Risk-adjusted return measure
- **Maximum Drawdown:** Largest peak-to-trough decline
- **Value at Risk (VaR):** Potential loss at 95% confidence
- **Conditional VaR (CVaR):** Expected loss beyond VaR
- **Correlation Matrix:** Asset correlation analysis

## Visualizations

The report includes:

1. **Portfolio Evolution:** Line chart showing portfolio value over time
2. **Asset Allocation:** Pie chart of portfolio weights
3. **Correlation Heatmap:** Asset correlation matrix
4. **Returns Distribution:** Histogram of daily returns
5. **Drawdown Chart:** Portfolio drawdown over time

## Configuration

Edit `config/settings.py` to customize:

- Start and end dates
- Initial capital
- Asset tickers
- Risk-free rate
- Report recipient email

## Weekly Reporting

To set up automated weekly reporting:

1. Configure email settings in `utils/helpers.py`
2. Set up a cron job (Linux/Mac) or Task Scheduler (Windows)

Example cron job (runs every Monday at 9 AM):
```bash
0 9 * * 1 cd /path/to/AssetManagementTracker && /path/to/venv/bin/python main.py --all
```

## Requirements

- Python 3.8+
- pandas
- numpy
- yfinance
- matplotlib
- seaborn
- Jinja2
- streamlit
- plotly

## License

This project is for educational purposes.


