# PS Tender Tracker - Web Scraper Tool

A Python-based web scraper that automatically extracts UK government tender opportunities from the find-tender.service.gov.uk portal, applies intelligent filters, and populates a Google Sheet with detailed tender information.

## Features

✅ **Intelligent Filtering**
- Keywords: AI, GenAI, LLM, Data Integration, Cloud, DevSecOps, and 40+ more
- CPV Code: 72000000 (IT services)
- Location: United Kingdom only
- SME Suitability: Small/medium-sized enterprises
- Date Ranges: Published last 7 days, closing 2-14 days ahead

✅ **Data Extraction**
- 20 fields per tender: ID, Name, Value, Buyer, Stage, Description, etc.
- Handles missing/malformed data gracefully
- UK timezone (Europe/London) for all dates

✅ **Smart Deduplication**
- Checks entire sheet history for duplicate Tender IDs
- Marks duplicates with processing timestamp comment
- Prevents re-processing old tenders

✅ **Google Sheets Integration**
- OAuth 2.0 authentication (secure, no password storage)
- Creates "PS Tender Tracker" sheet automatically
- Batch writes for performance
- Auto-token refresh on each run

✅ **Comprehensive Logging**
- Detailed logs in `tender_scraper.log`
- Error tracking and reporting
- Processing summary after each run

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Google Cloud OAuth:**
   - See [SETUP.md](SETUP.md) for detailed instructions
   - Download credentials from Google Cloud Console
   - Save to `credentials/credentials.json`

3. **Run the scraper:**
   ```bash
   python main.py
   ```

4. **Check results:**
   - New "PS Tender Tracker" sheet appears in your Google Drive folder
   - Logs saved to `tender_scraper.log`

## Architecture

### Core Modules

| Module | Purpose |
|--------|---------|
| `main.py` | Orchestrates the entire pipeline |
| `scraper.py` | Fetches tender listings from portal with filters |
| `tender_parser.py` | Extracts all 20 fields from tender detail pages |
| `sheets_writer.py` | Writes to Google Sheets with dedup logic |
| `google_sheets_auth.py` | Handles OAuth authentication |
| `config.py` | Central configuration and constants |

### Data Flow
```
Portal Search → Scraper → Parser → Dedup Check → Sheets Write
```

## Configuration

Edit `config.py` to customize:
- **Keywords**: Add/remove tender categories
- **Filters**: CPV codes, location, SME suitability
- **Target Folder**: Google Drive folder for storing sheets
- **Date Ranges**: Publication and closing date logic

## Dataset Fields

Each tender record includes:
- Portal Name, Direct URL, Published Date, ID, Name
- Due Date, Procurement Stage, Contract Value (Total & Annual)
- Contract Duration, Description, Buyer Name
- SME Suitability, Status, Status Date
- Processed Date, Comments, Last Modified/Created Dates
- SC_Flag (default: TBD)

## Status

✅ **Completed:**
- Web scraper with filter support
- Tender detail parser (20 fields)
- Google Sheets OAuth & writer
- Deduplication logic
- Error handling & logging
- Setup documentation

📅 **Future Enhancements:**
- Automated scheduling (daily/weekly runs)
- Selenium fallback for JS-heavy pages
- Email notifications on new tenders
- Advanced filtering UI
- Historical trend analysis

## Troubleshooting

See [SETUP.md](SETUP.md) for detailed troubleshooting steps.

**Common Issues:**
- `Credentials file not found` → Download from Google Cloud Console
- `No tenders found` → Check filters and date ranges
- `Token refresh failed` → Delete `credentials/ps_tender_token.json` and re-run

## Project Status

**Version:** 1.0.0 (MVP)  
**Last Updated:** 2026-05-14  
**Lead Data Engineer:** PS Team

For questions or issues, refer to logs in `tender_scraper.log`.
