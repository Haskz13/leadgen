# Canadian Public Sector Training Lead Generation Pipeline

A sales-focused lead generation tool that automatically discovers urgent training opportunities in the Canadian public sector by monitoring news, announcements, and mandates.

## Overview

This tool helps account managers at The Knowledge Academy identify and track actionable training opportunities across:
- Federal, provincial, and municipal governments
- Crown corporations
- Indigenous organizations and bands
- NPOs and charities
- Wholly Indigenous-owned companies

## Features

### Lead Discovery
- Monitors government news releases and announcements
- Identifies training mandates, digital transformations, and new initiatives
- Focuses on urgent opportunities (closeable before end of July)
- NO bids/tenders - only actual training needs

### Sales Dashboard
- **Tiered Lead System**: Urgent (Tier 1), High Priority (Tier 2), Standard (Tier 3)
- **Lead Management**: Track status (New, Contacted, In Progress, Closed)
- **Custom Notes**: Add notes to each lead for follow-up
- **Smart Filters**: Filter by tier, status, or organization
- **Export to CSV**: Download leads for offline work
- **Auto-refresh**: Updates every 5 minutes

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Haskz13/leadgen.git
cd leadgen
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the backend API (runs on port 5000):
```bash
cd app
python main.py
```

2. In a new terminal, start the frontend (runs on port 5001):
```bash
cd app
python frontend.py
```

3. Open your browser to: http://localhost:5001

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
- **Tier 1 - Urgent**: Deadline within 30 days
- **Tier 2 - High Priority**: Deadline within 60 days  
- **Tier 3 - Standard**: Deadline beyond 60 days

## Example Leads

The system identifies opportunities like:
- "CRA announces digital transformation requiring extensive staff training"
- "Toronto announces accessibility training requirement for all city staff"
- "Indigenous Services Canada launches reconciliation training program"

## Data Sources

Currently monitors:
- Government of Canada news releases
- Provincial government announcements
- Municipal news and mandates
- Indigenous organization announcements
- Crown corporation transformations

## Future Enhancements

- Real-time web scraping of actual news sources
- Email alerts for new Tier 1 leads
- Integration with CRM systems
- AI-powered lead scoring
- Automated contact information extraction

## Support

For issues or questions, please contact the development team.