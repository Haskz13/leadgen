# Canadian Public Sector Lead Generation System
## AI-Powered Sales Intelligence Dashboard

A sophisticated lead generation tool that uses AI-powered search to identify actionable, urgent training opportunities in the Canadian public sector. The system focuses on opportunities for 2025/2026 across all levels of government, NPOs, charities, crown corporations, and indigenous organizations.

## 🚀 Features

### AI-Powered Intelligence
- **AI Search Technology**: Simulates Claude's deep search capabilities to find relevant opportunities
- **Critical Analysis**: AI-generated insights on each opportunity
- **Win Probability Calculation**: Data-driven assessment of success likelihood
- **Competitive Landscape Analysis**: Understanding of competition for each opportunity
- **Decision Maker Identification**: Key contacts for each organization

### Sales-Focused Dashboard
- **Professional Dark Theme**: Modern, easy-on-the-eyes interface
- **Tier-Based Prioritization**: Urgent (Tier 1) and High Priority (Tier 2) opportunities
- **Comprehensive Lead Information**:
  - Organization and opportunity details
  - Budget ranges and deadlines
  - Contact information
  - AI confidence scores
  - Critical analysis and insights
  - Competitive landscape
  - Key requirements
  - Recommended next steps
  - Decision maker profiles

### Data Coverage
- **Federal Government**: Treasury Board, Service Canada, ESDC, Indigenous Services
- **Provincial**: Ontario, British Columbia, Alberta, Quebec
- **Municipal**: Major cities like Toronto, Vancouver, Calgary
- **Focus Areas**:
  - Digital transformation and AI
  - AODA compliance training
  - Indigenous capacity building
  - Climate action and sustainability
  - Leadership development
  - DEI initiatives

## 📋 Requirements

- Python 3.8+
- Flask
- Flask-CORS

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/Haskz13/leadgen.git
cd leadgen/app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🏃 Running the Application

### Option 1: Direct Python
```bash
python3 app.py
```

### Option 2: Using the run script
```bash
chmod +x run.sh
./run.sh
```

The dashboard will be available at: **http://localhost:5001**

## 🎯 Current Opportunities

The system currently tracks **5 high-value opportunities** totaling **$49M** in pipeline value:

1. **Digital Transformation Excellence Program** (Federal) - $15-20M
2. **AODA Compliance Training** (Ontario) - $8-12M  
3. **Indigenous Leadership Program** (Federal) - $5-8M
4. **AI Ethics Training** (Federal) - $3-5M
5. **Climate Action Training** (Toronto) - $2-4M

## 🔍 How It Works

1. **AI Search**: The system uses AI-powered search logic to identify training opportunities
2. **Intelligent Analysis**: Each opportunity is analyzed for:
   - Urgency and tier classification
   - Budget and timeline
   - Competition assessment
   - Win probability
   - Key requirements
3. **Sales Intelligence**: Provides actionable insights including:
   - Critical analysis
   - Next steps recommendations
   - Decision maker identification
   - Competitive positioning

## 🛠️ Architecture

- **Backend**: Flask API serving lead data and statistics
- **Frontend**: Single-page application with real-time updates
- **AI Engine**: Simulated AI search that would connect to Claude's API in production
- **Data Model**: Comprehensive lead objects with 15+ fields of intelligence

## 📊 API Endpoints

- `GET /` - Main dashboard interface
- `GET /api/leads` - JSON API for all leads
- `GET /api/stats` - Statistics endpoint (if using advanced version)

## 🔮 Future Enhancements

- Integration with real Claude API for live search
- Automated email alerts for new opportunities
- CRM integration
- Advanced filtering and search
- Lead scoring algorithms
- Historical trend analysis

## 📝 Notes

- This version demonstrates the concept with AI-generated sample data
- In production, the AI search would connect to real-time data sources
- All opportunities are based on realistic Canadian government initiatives for 2025/2026

## 🤝 Contributing

To contribute to this project:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📧 Contact

For questions about opportunities, contact the respective government departments listed in each lead.