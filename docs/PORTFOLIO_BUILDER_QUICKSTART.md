# Portfolio Builder - Quick Start Guide 🚀

## In 60 Seconds

### 1️⃣ Launch the App
```bash
cd /Users/benpfeffer/AssetManagementTracker
source venv/bin/activate
streamlit run app.py
```

### 2️⃣ Navigate
Click **🔧 Portfolio Builder** in the sidebar

### 3️⃣ Choose Your Path

**Path A: Use a Template** (Fastest)
1. Expand "🌟 Popular Portfolio Templates"
2. Select a template (e.g., "60/40 Stock/Bond")
3. Click "Load Template"
4. Click "🚀 Analyze Portfolio"
5. ✅ Done! Review the results

**Path B: Build Custom** (More Control)
1. Expand "➕ Add New Asset"
2. Enter ticker (e.g., "AAPL")
3. Set allocation (e.g., 25%)
4. Click "➕ Add Asset"
5. Repeat for 3-5 assets
6. Click "⚖️ Normalize Weights"
7. Click "🚀 Analyze Portfolio"
8. ✅ Done! Review the results

**Path C: Start from Current**
1. Click "📋 Load Current Portfolio"
2. Adjust weights as desired
3. Add/remove assets
4. Click "🚀 Analyze Portfolio"
5. ✅ Done! Review the results

## What You'll See

### Comparison Metrics
- ✅ Expected Return
- ✅ Volatility (Risk)
- ✅ Sharpe Ratio
- ✅ Performance vs. Current Portfolio

### Four Analysis Tabs

1. **📊 Allocation**: Visual comparison charts
2. **📈 Efficient Frontier**: Optimization recommendations
3. **📉 Historical Performance**: Backtest results
4. **📋 Asset Details**: Individual asset statistics

## Quick Tips

### ✅ Do This
- Start with 3-5 assets
- Use well-known ETFs first (VTI, BND, GLD)
- Click "Normalize Weights" before analyzing
- Review all 4 analysis tabs
- Try multiple scenarios

### ❌ Avoid This
- Don't use invalid ticker symbols
- Don't forget to normalize weights to 100%
- Don't add too many assets at once (10+ is slow)
- Don't rely solely on past performance
- Don't skip the efficient frontier analysis

## Popular Starting Points

### Conservative (Lower Risk)
```
BND (Bonds)         60%
VTI (US Stocks)     30%
GLD (Gold)          10%
```

### Balanced (Moderate Risk)
```
VTI (US Stocks)     50%
BND (Bonds)         40%
VXUS (Intl Stocks)  10%
```

### Growth (Higher Risk)
```
QQQ (Tech)          40%
VTI (US Stocks)     35%
VXUS (Intl Stocks)  25%
```

### Aggressive (High Risk)
```
QQQ (Tech)          50%
VUG (Growth)        30%
IEMG (Emerging)     20%
```

## Common Tickers

### 📈 Stocks
- **VTI**: Total US Market
- **SPY**: S&P 500
- **QQQ**: Tech/Nasdaq
- **VXUS**: International

### 📉 Bonds
- **BND**: Total Bond Market
- **TLT**: Long-Term Treasury
- **AGG**: Aggregate Bonds

### 🏆 Alternatives
- **GLD**: Gold
- **VNQ**: Real Estate

## Troubleshooting

### "No data available"
➡️ Check ticker symbols are correct

### "Total allocation should be 100%"
➡️ Click "⚖️ Normalize Weights"

### Analysis is slow
➡️ Normal for 5+ assets, wait 30-60 seconds

### Can't add asset
➡️ Make sure ticker isn't already added

## Understanding Results

### Sharpe Ratio
- **< 1.0**: Poor
- **1.0 - 2.0**: Good
- **> 2.0**: Excellent

### Expected Return
- Higher = Better potential returns
- But usually means higher risk too

### Volatility
- Lower = More stable
- Higher = More price swings

### Return Difference (vs Current)
- **Positive (+)**: Custom portfolio expected to do better
- **Negative (-)**: Current portfolio expected to do better

## Next Steps

1. ✅ Try the templates first
2. ✅ Build 2-3 custom portfolios
3. ✅ Compare them all
4. ✅ Review the efficient frontier recommendations
5. ✅ Document your findings

## Full Documentation

For complete details, see:
- **PORTFOLIO_BUILDER_GUIDE.md** - Comprehensive user guide
- **PORTFOLIO_BUILDER_FEATURE.md** - Technical implementation details

---

**Ready? Launch the app and click 🔧 Portfolio Builder!**

