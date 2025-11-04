# PDF Report Setup Guide

## Installation

To enable PDF generation for weekly reports, you need to install the `reportlab` library.

### Method 1: Using pip (Recommended)

```bash
cd /Users/benpfeffer/AssetManagementTracker
source venv/bin/activate
pip install reportlab
```

### Method 2: If SSL Issues Occur

If you encounter SSL certificate errors, try:

```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org reportlab
```

### Method 3: Install from requirements.txt

The reportlab dependency is already in requirements.txt:

```bash
pip install -r requirements.txt
```

### Verify Installation

Test that reportlab is installed:

```bash
python -c "from reportlab.lib.pagesizes import letter; print('✅ reportlab installed successfully')"
```

## Using the PDF Generator

### Quick Start

1. **Launch the Dashboard**
   ```bash
   streamlit run app.py
   ```

2. **Navigate to Weekly Report**
   - Click **📧 Weekly Report** in the sidebar

3. **Generate Report**
   - Select report date
   - Click **🚀 Generate Report**

4. **Create PDF**
   - Go to **📕 PDF Export** tab
   - Click **📕 Generate PDF Document**
   - Click **📥 Download PDF**

5. **Send to Teacher**
   - Attach PDF to email
   - Send to `ckharoubi@escp.eu`

## PDF Features

### Professional Layout

The generated PDF includes:

- **Header**: Colored gradient title "📊 Suivi de Portefeuille"
- **Date**: French-formatted date (e.g., "30 septembre 2025")
- **Greeting**: "Bonsoir Madame,"
- **Asset Table**: 
  - Ticker symbols
  - Full asset names
  - Closing prices (French format: 600,62 USD)
  - Price variations from initial prices
- **Footer**: "Ces données reflètent les cours de clôture du [date]"
- **Signature**: "Bien cordialement, Le groupe 7"

### Table Styling

- Colored header (purple gradient)
- Alternating row colors for readability
- Right-aligned numbers
- Grid lines for clarity
- Professional fonts (Helvetica)

### Format

- **Page Size**: A4
- **Margins**: 0.75 inches all around
- **Font**: Helvetica family
- **Colors**: Professional color scheme matching dashboard

## Workflow

### Every Wednesday

1. ✅ Update price data (🔄 Refresh button in sidebar)
2. ✅ Navigate to **📧 Weekly Report**
3. ✅ Select "Most Recent Data"
4. ✅ Click **🚀 Generate Report**
5. ✅ Review prices in **📊 Closing Prices** tab
6. ✅ Go to **📕 PDF Export** tab
7. ✅ Click **📕 Generate PDF Document**
8. ✅ Click **📥 Download PDF**
9. ✅ Attach to email and send to teacher

### File Storage

PDFs are automatically saved to:
```
reports/weekly/weekly_report_YYYY-MM-DD.pdf
```

Example:
- `weekly_report_2025-09-30.pdf`
- `weekly_report_2025-10-07.pdf`

## Troubleshooting

### "PDF library not installed"

**Error:** `❌ PDF library not installed. Run: pip install reportlab`

**Solution:**
```bash
source venv/bin/activate
pip install reportlab
```

If that fails due to SSL:
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org reportlab
```

### "Error generating PDF"

**Common causes:**
1. reportlab not installed → Install it
2. No write permissions → Check `reports/weekly/` directory
3. Invalid data → Verify price data is loaded

**Solutions:**
- Verify installation: `python -c "import reportlab; print('OK')"`
- Check directory exists: `mkdir -p reports/weekly`
- Ensure data is updated: Click 🔄 Refresh

### "Cannot find PDF file"

**Cause:** PDF generation failed silently

**Solution:**
- Check `reports/weekly/` directory
- Verify no error messages
- Try generating again
- Check console for errors

### SSL Certificate Errors (During Installation)

**Error:** `SSLError(SSLCertVerificationError...)`

**Solution 1:** Use trusted hosts
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org reportlab
```

**Solution 2:** Update certificates
```bash
/Applications/Python\ 3.13/Install\ Certificates.command
```

**Solution 3:** Manual download
1. Download reportlab from https://pypi.org/project/reportlab/#files
2. Install manually: `pip install reportlab-*.whl`

## Alternative: Use Plain Text

If PDF generation doesn't work, you can still use plain text:

1. Go to **📄 Plain Text** tab
2. Copy the text
3. Paste into email body
4. Send to teacher

The plain text format is also professional and includes all necessary information.

## Example PDF Output

When you generate a PDF, it will look like:

```
                    📊 Suivi de Portefeuille

Date: 30 septembre 2025

Bonsoir Madame,

Veuillez trouver ci-dessous les cours de clôture de ce soir pour les 
indices/ETF que nous avons sélectionnés dans le cadre du suivi de portefeuille :

┌─────────┬──────────────────────────────┬─────────────────┬───────────┐
│ Ticker  │ Nom                          │ Cours de clôture│ Variation │
├─────────┼──────────────────────────────┼─────────────────┼───────────┤
│  QQQ    │ US Tech Stocks               │     600,62 USD  │  +0,47%   │
│  IEMG   │ Emerging Markets Stocks      │      65,94 USD  │  -0,36%   │
│  SHV    │ Short-Term US Treasury Bonds │     110,48 USD  │  +0,06%   │
│  TLT    │ Long-Term US Treasury Bonds  │      89,59 USD  │  +0,78%   │
│  IAU    │ Gold (Precious Metals)       │      72,76 USD  │  +2,33%   │
└─────────┴──────────────────────────────┴─────────────────┴───────────┘

Ces données reflètent les cours de clôture du 30 septembre 2025.

                                              Bien cordialement,
                                              Le groupe 7
```

## Tips

### 1. Test Before Wednesday

Generate a test PDF on Tuesday to ensure everything works:
- Check formatting
- Verify all prices load
- Confirm PDF downloads
- Test email attachment

### 2. Keep PDFs Organized

PDFs are saved with dates in filename:
- Easy to find previous reports
- Good for record keeping
- Can compare week-to-week

### 3. Quality Check

Before sending:
- ✅ All 5 assets present
- ✅ Prices look reasonable
- ✅ Date is correct Wednesday
- ✅ French formatting correct
- ✅ No errors or warnings
- ✅ PDF opens properly

### 4. Backup Strategy

- Save PDFs to reports/weekly/
- Keep email confirmations
- Archive sent reports
- Create backup folder

## Advanced

### Custom Styling

To modify PDF appearance, edit `reports/weekly_report.py`:

**Change colors:**
```python
# Line ~368
colors.HexColor('#667eea')  # Header color
```

**Change fonts:**
```python
# Line ~371
fontName='Helvetica-Bold'  # Title font
```

**Change layout:**
```python
# Line ~353-355
topMargin=0.75*inch,  # Top margin
leftMargin=0.75*inch,  # Left margin
```

### Batch Generation

To generate PDFs for multiple dates:

```python
from reports.weekly_report import WeeklyReportGenerator
import pandas as pd

# Load data
assets_info = [...]  # Your assets
price_data = pd.read_csv('data/prices.csv')

# Create generator
gen = WeeklyReportGenerator(assets_info, 7)

# Generate for each Wednesday
for date in ['2025-09-30', '2025-10-07', '2025-10-14']:
    prices = {...}  # Extract prices for date
    pdf_path = gen.generate_pdf(prices, date)
    print(f"Generated: {pdf_path}")
```

## Support

### Getting Help

1. Check this guide first
2. Verify reportlab is installed
3. Check error messages
4. Review console output
5. Try plain text as fallback

### Common Questions

**Q: Why PDF instead of email text?**  
A: PDF is more professional, easier to attach, and preserves formatting

**Q: Can I customize the PDF?**  
A: Yes, edit `reports/weekly_report.py`

**Q: What if reportlab won't install?**  
A: Use plain text format instead - it works great too!

**Q: Can I add charts to the PDF?**  
A: Yes, but requires additional code. Current version focuses on simplicity.

## Summary

The PDF generator creates professional weekly reports in French with:
- ✅ Clean, professional layout
- ✅ All asset prices and variations
- ✅ French date and number formatting
- ✅ Ready to attach to email
- ✅ Automatic file naming
- ✅ Saved for records

**Installation:**
```bash
pip install reportlab
```

**Usage:**
1. Generate Report
2. Create PDF
3. Download
4. Attach to email
5. Send to teacher

---

**Ready to create your first PDF report? Try it now!**

