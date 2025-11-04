# Portfolio Builder Guide 🔧

## Overview

The **Portfolio Builder** is a powerful new feature in the Asset Management Tracker that allows you to experiment with different stocks, bonds, and ETFs to see how they would perform. This interactive tool lets you:

- Build custom portfolios with any ticker symbols
- Compare expected returns with your current portfolio
- Analyze risk-adjusted performance metrics
- Visualize efficient frontiers and optimal allocations
- Backtest hypothetical portfolio performance

## How to Use

### 1. Access the Portfolio Builder

Navigate to the **🔧 Portfolio Builder** page from the sidebar menu.

### 2. Add Assets to Your Portfolio

**Option A: Add Individual Assets**

1. Click on the "➕ Add New Asset" expander
2. Enter a ticker symbol (e.g., AAPL, MSFT, SPY, AGG)
3. Set the allocation percentage (0-100%)
4. Optionally add a descriptive name and select the asset class
5. Click "➕ Add Asset"

**Option B: Load Current Portfolio**

Click the "📋 Load Current Portfolio" button to start with your existing portfolio configuration.

**Option C: Use Portfolio Templates**

Choose from popular portfolio templates:
- **60/40 Stock/Bond**: Classic balanced portfolio
- **All Weather**: Ray Dalio's diversified approach
- **Three Fund**: Simple, effective diversification
- **Aggressive Growth**: High-growth equity focus

### 3. Adjust Weights

Once you've added assets:
- Use the number inputs next to each asset to adjust allocations
- Click "⚖️ Normalize Weights" to automatically adjust all weights to sum to 100%
- Remove assets using the 🗑️ button

### 4. Analyze Your Portfolio

When your total allocation is close to 100% (within 5% tolerance):

1. Click the **🚀 Analyze Portfolio** button
2. The system will:
   - Fetch historical market data for your selected tickers
   - Calculate expected returns and risk metrics
   - Run Markowitz optimization analysis
   - Compare with your current portfolio

### 5. Review Results

The analysis provides four detailed tabs:

#### 📊 Allocation Tab
- Visual comparison of custom vs. current portfolio allocations
- Side-by-side pie charts

#### 📈 Efficient Frontier Tab
- Interactive efficient frontier plot
- Optimal portfolio weights for maximum Sharpe ratio
- Weight comparison table showing recommended adjustments

#### 📉 Historical Performance Tab
- Simulated historical performance comparison
- Hypothetical portfolio value over time
- Performance metrics (final value, volatility)

#### 📋 Asset Details Tab
- Individual asset metrics and statistics
- Expected returns and volatility for each asset
- Asset correlation matrix heatmap

## Key Metrics Explained

### Expected Return
Annualized expected return based on historical data. This represents the average return you might expect over time.

### Volatility (Risk)
Standard deviation of returns, annualized. Higher volatility means more price fluctuations.

### Sharpe Ratio
Risk-adjusted return metric: `(Return - Risk-Free Rate) / Volatility`
- Higher is better
- Above 1.0 is good
- Above 2.0 is excellent

### Return Difference
Shows how much better (or worse) your custom portfolio's expected return is compared to the current portfolio.

### Risk Difference
Shows how much more (or less) volatile your custom portfolio is. Lower is generally better if you maintain similar returns.

## Tips for Building Better Portfolios

### 1. Diversification is Key
- Include assets from different classes (stocks, bonds, commodities)
- Mix domestic and international exposure
- Consider both growth and value assets

### 2. Watch Correlations
- Look for assets with low or negative correlations
- This reduces overall portfolio volatility
- Gold and bonds often have low correlation with stocks

### 3. Consider the Efficient Frontier
- The optimal weights tab shows mathematically optimized allocations
- "Max Sharpe" portfolio offers the best risk-adjusted returns
- You don't have to follow it exactly, but it's a good guide

### 4. Balance Risk and Return
- Higher expected returns usually mean higher volatility
- Consider your risk tolerance and investment timeline
- More conservative investors should favor lower volatility

### 5. Test Multiple Scenarios
- Try different combinations of assets
- Compare aggressive vs. conservative allocations
- See how adding alternative assets (gold, real estate) affects performance

## Popular Asset Tickers

### US Equity ETFs
- **VTI**: Total US Stock Market
- **SPY**: S&P 500
- **QQQ**: Tech-focused Nasdaq-100
- **VUG**: US Large Cap Growth
- **VTV**: US Large Cap Value
- **IJH**: Mid Cap
- **VB**: Small Cap

### International Equity ETFs
- **VXUS**: Total International Stock
- **EFA**: Developed Markets
- **IEMG**: Emerging Markets
- **VWO**: Emerging Markets

### Bond ETFs
- **BND**: Total Bond Market
- **AGG**: US Aggregate Bonds
- **TLT**: 20+ Year Treasury Bonds
- **IEF**: 7-10 Year Treasury Bonds
- **SHV**: Short-Term Treasury Bonds
- **LQD**: Investment Grade Corporate Bonds
- **HYG**: High Yield Corporate Bonds

### Alternative Assets
- **GLD**: Gold
- **IAU**: Gold (lower expense ratio)
- **SLV**: Silver
- **DBC**: Commodities
- **VNQ**: Real Estate (REITs)

### Individual Stocks
You can also add individual company stocks:
- **AAPL**: Apple
- **MSFT**: Microsoft
- **GOOGL**: Google
- **AMZN**: Amazon
- **NVDA**: Nvidia
- etc.

## Important Notes

### Historical Data
- Analysis is based on historical data since September 23, 2025
- Past performance does not guarantee future results
- Expected returns are estimates, not predictions

### Data Availability
- Not all tickers may have data for the full date range
- Invalid tickers will cause errors
- Make sure to use correct ticker symbols

### Transaction Costs
- The analysis doesn't account for:
  - Trading commissions
  - Bid-ask spreads
  - Tax implications
  - Minimum investment amounts

### Rebalancing
- The system shows expected returns but doesn't execute trades
- You would need to manually rebalance in your actual brokerage account
- Consider transaction costs before making changes

## Troubleshooting

### "No data available for these tickers"
- Check that all ticker symbols are valid
- Some tickers may not have data for the full date range
- Try removing recently added tickers one by one to identify the issue

### "Total Allocation: XX% (should be 100%)"
- Click "⚖️ Normalize Weights" to automatically fix
- Or manually adjust weights to sum to 100%
- A 5% tolerance is allowed for analysis

### Analysis Takes Too Long
- More assets = longer processing time
- Fetching data for 10+ assets may take 30-60 seconds
- Be patient, the system will complete the analysis

## Best Practices

1. **Start Simple**: Begin with 3-5 assets to understand the tool
2. **Compare Incrementally**: Make small changes and observe the impact
3. **Review All Tabs**: Each tab provides valuable insights
4. **Document Your Findings**: Download results for your records
5. **Regular Reviews**: Revisit your portfolio design quarterly or when market conditions change significantly

## Questions or Issues?

If you encounter any problems or have suggestions for improvements, please:
- Check this guide first
- Review error messages carefully
- Verify all ticker symbols are correct
- Ensure data is available for your selected date range

---

**Happy Portfolio Building! 🚀**

