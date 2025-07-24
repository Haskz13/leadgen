# How to Save the Lead Generation System to Your Local Machine

## Option 1: Clone from GitHub (Recommended)

Open a terminal/command prompt on your local machine and run:

```bash
# Navigate to where you want to save the project
cd C:\Users\ethan.haskins\Documents

# Clone the repository
git clone https://github.com/Haskz13/leadgen.git

# Navigate into the project
cd leadgen
```

## Option 2: Download as ZIP from GitHub

1. Visit: https://github.com/Haskz13/leadgen
2. Click the green "Code" button
3. Select "Download ZIP"
4. Extract the ZIP file to your desired location

## Running the Application Locally

### 1. Install Python (if not already installed)
- Download Python 3.8+ from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### 2. Install Dependencies

Open a terminal/command prompt in the project directory:

```bash
cd app
pip install -r requirements.txt
```

### 3. Run the Comprehensive Lead Generation System

```bash
# For the comprehensive system with 200+ opportunities
python comprehensive_app.py
```

Or for the simpler version:

```bash
# For the basic system with 5 example opportunities
python app.py
```

### 4. Access the Dashboard

Open your web browser and go to: http://localhost:5001

## File Structure

```
leadgen/
├── app/
│   ├── comprehensive_app.py      # Main application with 200+ leads
│   ├── comprehensive_ai_scraper.py # AI lead generator
│   ├── app.py                    # Simple version with 5 leads
│   ├── ai_scraper.py            # Basic AI scraper
│   ├── requirements.txt         # Python dependencies
│   ├── run.sh                   # Linux/Mac startup script
│   └── README.md                # Project documentation
```

## Key Features

- **236+ Training Opportunities** across Canadian public sector
- **109 Organizations** covered
- **AI-Powered Intelligence** for each opportunity
- **Advanced Filtering** by type, category, and priority
- **Real-time Search** across all fields
- **Professional Dashboard** with dark theme

## Support

If you encounter any issues:
1. Make sure Python 3.8+ is installed
2. Ensure all dependencies are installed with `pip install -r requirements.txt`
3. Check that port 5001 is not in use by another application

## Next Steps

1. Customize the search queries in `comprehensive_ai_scraper.py` for your specific needs
2. Integrate with your CRM using the API endpoints
3. Set up automated updates to refresh opportunities periodically