# PS Tender Tracker - Setup Guide

## Prerequisites
- Python 3.14+
- Google account with access to Google Drive and Google Sheets
- Google Cloud project

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up Google Cloud OAuth

### 2a. Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project: "PS Tender Tracker"
3. Enable the following APIs:
   - Google Sheets API
   - Google Drive API

### 2b. Create OAuth 2.0 Credentials
1. Go to Credentials → Create Credentials → OAuth 2.0 Client ID
2. Choose "Desktop application"
3. Download the JSON file and save it as `credentials/credentials.json`

```
credentials/
├── credentials.json   # Your OAuth credentials
├── ps_tender_token.json  # Generated automatically on first run
└── .gitignore
```

### 2c. First Run Authentication
When you first run `main.py`, it will:
1. Open a browser window asking you to authorize access
2. Store the token in `credentials/ps_tender_token.json` for future runs
3. Token will automatically refresh when expired

## Step 3: Configuration

Edit `config.py` if you need to change:
- `TARGET_FOLDER_ID`: Your Google Drive folder ID (currently: `1sFREkEsaedTc1voiO7QYwwTJtbtd7tHc`)
- `KEYWORDS`: Keywords to filter by
- Date ranges and other filters

## Step 4: Run the Scraper

```bash
python main.py
```

### On First Run:
1. A browser will open asking for authorization
2. Grant permission to access Google Sheets and Drive
3. Token will be saved automatically
4. Scraping will begin

### Output:
- A new Google Sheet "PS Tender Tracker" will be created in your target folder
- Each run appends unique tenders (duplicates are skipped with comments)
- Detailed logs are saved in `tender_scraper.log`

## Troubleshooting

### "Credentials file not found"
- Ensure `credentials/credentials.json` exists
- Download it from Google Cloud Console

### "Token refresh failed"
- Delete `credentials/ps_tender_token.json`
- Run again to re-authenticate

### No tenders found
- Check filters in `config.py`
- Verify date ranges are correct
- Check if portal has JavaScript content (may need Selenium)

### Google Sheets API errors
- Ensure both Sheets and Drive APIs are enabled
- Check permissions on target folder

## File Structure

```
PS WebScrapper Tool/
├── main.py                  # Main entry point
├── requirements.txt         # Python dependencies
├── config.py               # Configuration and constants
├── google_sheets_auth.py   # Google OAuth handling
├── scraper.py              # Web scraper
├── tender_parser.py        # Tender data extraction
├── sheets_writer.py        # Google Sheets writer
├── SETUP.md                # This file
├── tender_scraper.log      # Generated log file
└── credentials/            # Google credentials
    ├── credentials.json    # OAuth credentials
    ├── ps_tender_token.json  # Auth token (generated)
    └── .gitignore
```

## Notes

- The scraper uses UK timezone (Europe/London) for all dates
- Publication dates are rounded to the previous Monday if mid-week
- Closing dates are rounded to Saturday if needed
- All tender data is deduplicated by Tender ID
- Duplicates get a comment with processing timestamp
