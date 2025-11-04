# Weekly Report Generator Guide 📧

## Overview

The **Weekly Report Generator** creates formatted reports in French with closing prices for all portfolio assets. This feature is specifically designed to send weekly updates to your teacher (`ckharoubi@escp.eu`) every Wednesday.

## Quick Start

### Generate Your First Report

1. **Launch the Dashboard**
   ```bash
   streamlit run app.py
   ```

2. **Navigate to Weekly Report**
   - Click **📧 Weekly Report** in the sidebar

3. **Generate Report**
   - Select report date (Most Recent Data, Specific Wednesday, or Custom Date)
   - Click **🚀 Generate Report**

4. **Review and Send**
   - Review the generated report in multiple formats
   - Copy/download the report
   - Send via email or manually

## Report Format

### Plain Text Format

The report follows this French format:

```
Bonsoir Madame,

Veuillez trouver ci-dessous les cours de clôture de ce soir pour les indices/ETF que nous avons sélectionnés dans le cadre du suivi de portefeuille :

QQQ (US Tech Stocks): 600,62 USD 

IEMG (Emerging Markets Stocks): 65,94 USD 

SHV (Short-Term US Treasury Bonds): 110,48 USD 

TLT (Long-Term US Treasury Bonds): 89,59 USD 

IAU (Gold (Precious Metals)): 72,76 USD 

Ces données reflètent les cours de clôture du 30 septembre 2025.

Bien cordialement,

le groupe 7
```

### HTML Format

The report also generates a beautiful HTML version with:
- Professional header with gradient styling
- Formatted table with all asset prices
- Price change indicators (color-coded)
- Responsive design
- Ready to send as HTML email

## Features

### 1. Date Selection

**Three Options:**

#### Most Recent Data (Default)
- Uses the last available date in your price data
- Best for real-time reporting

#### Specific Wednesday
- Select from all Wednesdays in your project period
- Formatted in French dates for easy selection
- Ideal for generating past reports

#### Custom Date
- Pick any date within your project period
- Date picker with validation
- Use for special circumstances

### 2. Report Preview

**Four Tabs:**

#### 📄 Plain Text
- View the plain text email format
- Copy to clipboard
- Download as `.txt` file
- Perfect for email clients

#### 🎨 HTML Preview
- See the formatted HTML version
- Preview exactly how it will look
- Download as `.html` file
- Ideal for rich email formats

#### 📊 Closing Prices
- Detailed table with all assets
- Shows current price, initial price
- Price changes ($and %)
- Summary statistics:
  - Average change across all assets
  - Best performer
  - Worst performer
  - Report date

#### 📤 Send/Export
- Send email directly (with SMTP configuration)
- Manual send instructions
- Save to file for records
- Export options

### 3. Historical Reports

- View all Wednesday dates in project period
- See which reports are past/future
- French date formatting
- Track your reporting progress

### 4. Quick Stats

- Total report weeks in project
- Weeks elapsed
- Weeks remaining
- Next Wednesday date

## How to Send Reports

### Option 1: Manual Send (Recommended)

1. Generate the report
2. Go to **📄 Plain Text** tab
3. Click **📥 Download TXT**
4. Open your email client
5. Compose email to: `ckharoubi@escp.eu`
6. Subject: `Suivi de portefeuille - [date]`
7. Paste the downloaded content
8. Send!

### Option 2: Copy & Paste

1. Generate the report
2. View **📄 Plain Text** tab
3. Select and copy the text
4. Paste into your email
5. Send to `ckharoubi@escp.eu`

### Option 3: Automated Email (Advanced)

**Setup Required:**

1. Edit `config/settings.py`
2. Set your email credentials:
   ```python
   SENDER_EMAIL = 'your.email@gmail.com'
   SENDER_PASSWORD = 'your-app-specific-password'
   ```

3. For Gmail users:
   - Enable 2-factor authentication
   - Generate an app-specific password
   - Use that password (not your regular password)

4. In the app:
   - Go to **📤 Send/Export** tab
   - Expand "Configure Email Settings"
   - Enter credentials
   - Click **📧 Send Email Now**

**Security Note:** Never commit your password to git. Consider using environment variables.

## Report Schedule

### Project Period
- **Start**: September 23, 2025
- **End**: November 25, 2025
- **Frequency**: Weekly (Wednesdays)

### All Wednesday Dates

The system automatically calculates all Wednesdays in the project period:
- **2025-09-25** - 25 septembre 2025
- **2025-10-02** - 2 octobre 2025
- **2025-10-09** - 9 octobre 2025
- **2025-10-16** - 16 octobre 2025
- **2025-10-23** - 23 octobre 2025
- **2025-10-30** - 30 octobre 2025
- **2025-11-06** - 6 novembre 2025
- **2025-11-13** - 13 novembre 2025
- **2025-11-20** - 20 novembre 2025

### Sending Checklist

Before Wednesday evening:
- [ ] Ensure price data is updated
- [ ] Navigate to Weekly Report page
- [ ] Select "Most Recent Data" or current Wednesday
- [ ] Generate report
- [ ] Review all prices are correct
- [ ] Copy or download the report
- [ ] Send email to `ckharoubi@escp.eu`
- [ ] Confirm email sent successfully

## Configuration

### Email Settings

Edit `config/settings.py`:

```python
# Email configuration for weekly reports
TEACHER_EMAIL = 'ckharoubi@escp.eu'
GROUP_NUMBER = 7

# SMTP configuration (optional, for automated sending)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your.email@gmail.com'
SENDER_PASSWORD = 'your-app-password'
```

### Change Group Number

If you're not Group 7, update `GROUP_NUMBER` in settings.

### Change Recipient

To send to a different email, update `TEACHER_EMAIL` in settings.

## Features Details

### French Date Formatting

The system automatically converts dates to French format:
- `2025-09-30` → `30 septembre 2025`
- `2025-10-15` → `15 octobre 2025`

All French months are correctly formatted:
- janvier, février, mars, avril, mai, juin
- juillet, août, septembre, octobre, novembre, décembre

### Price Formatting

Prices are formatted in French style:
- Decimal separator: comma (`,`) instead of period (`.`)
- `600.62` → `600,62 USD`
- `65.94` → `65,94 USD`

### Asset Information

Each asset includes:
- Ticker symbol (e.g., QQQ)
- Full name (e.g., US Tech Stocks)
- Closing price in USD
- French date reference

## Saving Reports

### Automatic File Saving

Click **💾 Save Report to File** to save the report to:
```
reports/weekly/weekly_report_YYYY-MM-DD.txt
```

This creates a permanent record of all sent reports.

### File Naming Convention

Reports are saved with the format:
- `weekly_report_2025-09-30.txt`
- `weekly_report_2025-10-07.txt`
- etc.

### File Storage

All saved reports are stored in:
```
AssetManagementTracker/
└── reports/
    └── weekly/
        ├── weekly_report_2025-09-25.txt
        ├── weekly_report_2025-10-02.txt
        ├── weekly_report_2025-10-09.txt
        └── ...
```

## Tips & Best Practices

### 1. Weekly Workflow

**Every Wednesday:**
1. Update price data (click 🔄 Refresh in sidebar)
2. Navigate to Weekly Report
3. Generate report with "Most Recent Data"
4. Review prices
5. Send to teacher
6. Save report to file

### 2. Quality Checks

Before sending:
- ✅ All prices are reasonable (no obvious errors)
- ✅ Date is correct (current Wednesday)
- ✅ French formatting is correct
- ✅ Group number is correct
- ✅ Recipient email is correct

### 3. Backup Strategy

- Always save reports to file
- Keep a copy of sent emails
- Export HTML version for records
- Create a sent emails folder

### 4. Early Preparation

Generate reports on Tuesday evening if:
- Wednesday morning is busy
- You want to review before sending
- Markets close early

## Troubleshooting

### "No data available for date"

**Solution:**
- Ensure price data is updated
- Click 🔄 Refresh in sidebar
- Use "Most Recent Data" option
- Check that date is not in the future

### "Email failed to send"

**Solution:**
1. Check SMTP settings in `config/settings.py`
2. Verify email credentials
3. For Gmail: use app-specific password
4. Check internet connection
5. Use manual send method instead

### "Wrong date format"

**Issue:** Date not in French format

**Solution:**
- The system automatically formats dates
- If issues persist, regenerate the report
- Check language settings

### "Prices look wrong"

**Solution:**
- Refresh price data
- Check the selected date
- Verify data source (yfinance)
- Compare with previous reports

### "Cannot find Wednesday dates"

**Solution:**
- Check START_DATE and END_DATE in settings
- Ensure dates are in YYYY-MM-DD format
- Verify project period is correctly configured

## Advanced Usage

### Batch Generate Reports

To generate reports for multiple past Wednesdays:

1. Select "Specific Wednesday"
2. Choose the first date
3. Generate and save
4. Repeat for each Wednesday

### Custom Report Modifications

The report generator is in:
```
reports/weekly_report.py
```

You can customize:
- Email greeting
- Report format
- Asset display order
- Additional statistics
- Signature format

### Automated Scheduling

To automatically send reports every Wednesday:

**Option 1: Cron Job (Linux/Mac)**
```bash
0 18 * * 3 cd /path/to/AssetManagementTracker && python weekly_send_script.py
```

**Option 2: Task Scheduler (Windows)**
- Create a task that runs every Wednesday at 6 PM
- Runs the report generation and sending script

**Note:** Requires SMTP configuration and a custom script.

## Security Considerations

### Email Credentials

- **Never** commit passwords to git
- Use app-specific passwords, not account passwords
- Consider environment variables:
  ```python
  import os
  SENDER_PASSWORD = os.getenv('EMAIL_APP_PASSWORD')
  ```

### File Permissions

- Saved reports may contain sensitive data
- Ensure proper file permissions
- Don't share reports directory publicly

### SMTP Security

- Always use TLS/SSL (port 587 or 465)
- Don't send passwords over plain text
- Use secure, encrypted connections

## Support

### Common Questions

**Q: Can I change the email language?**  
A: Yes, edit the `generate_email_body()` function in `reports/weekly_report.py`

**Q: Can I add more assets to the report?**  
A: Yes, they'll automatically appear if they're in `assets_info.json`

**Q: Can I change the report template?**  
A: Yes, edit the template strings in `weekly_report.py`

**Q: Can I send to multiple recipients?**  
A: Modify the `send_email()` function to accept multiple recipients

### Getting Help

If you encounter issues:
1. Check this guide first
2. Review error messages carefully
3. Verify all configuration settings
4. Check data is updated
5. Try manual send as fallback

## Quick Reference

### Keyboard Shortcuts

- **Ctrl+C / Cmd+C**: Copy selected text
- **Ctrl+S / Cmd+S**: Save (when in browser)

### File Locations

- Reports: `reports/weekly/`
- Config: `config/settings.py`
- Generator: `reports/weekly_report.py`

### Important Emails

- Teacher: `ckharoubi@escp.eu`
- Subject format: `Suivi de portefeuille - [date in French]`

### Key Dates

- Project Start: September 23, 2025
- Project End: November 25, 2025
- Report Day: Wednesday
- Total Weeks: 9

---

**Ready to send your first report? Launch the app and navigate to 📧 Weekly Report!**

