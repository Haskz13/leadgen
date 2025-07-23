# Canadian Public Sector Training Lead Generation Pipeline

A sales-focused lead generation tool that automatically discovers urgent training opportunities in the Canadian public sector by monitoring grants, news, announcements, and mandates.

## Overview

This tool helps account managers at The Knowledge Academy identify and track actionable training opportunities across:
- Federal, provincial, and municipal governments
- Crown corporations
- Indigenous organizations and bands
- NPOs and charities
- Wholly Indigenous-owned companies
- **NEW: Grant recipients from Open Canada Data Portal**

## Features

### Lead Discovery - Real Data Sources
- **Open Canada Data Portal**: Searches grant recipients for training-related funding
- **Government of Canada News API**: Real-time news monitoring
- **Provincial government newsrooms** (Ontario, BC, Alberta, etc.)
- **Municipal websites** (Toronto, Vancouver, Montreal, Calgary, Ottawa)
- **Indigenous organization news** (AFN, Métis Nation, ITK, NWAC)
- **Crown corporation announcements**
- **Sector-specific sources** (healthcare, education, public safety)
- **NO sample data** - all leads are from real sources
- **NO bids/tenders** - focuses on actual training needs

### Sales Dashboard
- **Tiered Lead System**: Urgent (Tier 1), High Priority (Tier 2), Standard (Tier 3)
- **Lead Management**: Track status (New, Contacted, In Progress, Closed)
- **Custom Notes**: Add notes to each lead for follow-up
- **Smart Filters**: Filter by tier, status, or organization
- **Export to CSV**: Download leads for offline work
- **Auto-refresh**: Updates every 5 minutes
- **Persistent Storage**: Your notes and status updates are saved locally

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Haskz13/leadgen.git
cd leadgen/app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Easy Start Methods:

#### Windows:
```bash
cd app
start.bat
```

#### Linux/Mac:
```bash
cd app
./start.sh
```

#### Manual Start:
1. Start the backend API (Terminal 1):
```bash
cd app
python main.py
```

2. Start the frontend (Terminal 2):
```bash
cd app
python frontend.py
```

3. Open your browser to: http://localhost:5001

## Data Sources

### Grant Recipients
- Searches Open Canada Data Portal for organizations receiving training-related grants
- Identifies opportunities based on grant descriptions and funding programs
- Estimates training deadlines based on grant start dates

### Real-time News Monitoring
- Government of Canada news API
- Provincial newsrooms (automated checking)
- Municipal news feeds
- Indigenous organization announcements
- Crown corporation media rooms

### What It Looks For
- Training mandates and requirements
- Digital transformation initiatives
- New system implementations
- Compliance and certification requirements
- Professional development programs
- Skills gap announcements
- Workforce development initiatives

## Usage

### Dashboard Overview
- **Header Stats**: Shows total leads, urgent leads, and new leads
- **Filters**: Use dropdowns to filter by tier, status, or search by organization
- **Lead Table**: View all leads with key information

### Managing Leads
1. **Update Status**: Click the status dropdown to mark leads as Contacted, In Progress, etc.
2. **Add Notes**: Click in the notes field to add follow-up information
3. **View Source**: Click "View" to see the original news/announcement
4. **Export Data**: Click "Export CSV" to download all leads with your notes

### Lead Tiers
- **Tier 1 - Urgent**: Deadline within 30 days (closeable before end of July)
- **Tier 2 - High Priority**: Deadline within 60 days  
- **Tier 3 - Standard**: Deadline beyond 60 days

## Example Leads You'll Find

- Grant recipients implementing training programs
- Government departments announcing digital transformations
- Municipalities requiring compliance training
- Indigenous organizations launching capacity building programs
- Crown corporations modernizing operations
- Healthcare organizations needing certification training

## Expanding Data Sources

The scraper is designed to be easily expandable. To add more sources:
1. Add new scraping methods in `scraper.py`
2. Include them in the `get_all_leads()` method
3. Follow the existing pattern for data structure

## Troubleshooting

### No leads appearing?
- Check your internet connection
- Some sources may have rate limits - wait a few minutes
- Check the console for error messages

### Port already in use?
- Kill existing Python processes
- Change ports in main.py and frontend.py

## Future Enhancements

- LinkedIn job postings analysis
- Government contract awards monitoring
- AI-powered lead scoring
- Email alerts for new Tier 1 leads
- CRM integration
- Advanced duplicate detection
- Historical trend analysis

## Support

For issues or questions, please open an issue on GitHub or contact the development team.