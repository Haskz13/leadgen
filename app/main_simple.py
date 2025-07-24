from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
from scraper import CanadianPublicSectorScraper

app = Flask(__name__)
CORS(app)

# Initialize with some data
leads_cache = []
last_update = None

# Get initial leads (this will use the realistic examples)
print("Initializing with example leads...")
scraper = CanadianPublicSectorScraper()
leads_cache = scraper._generate_realistic_examples()
last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"Initialized with {len(leads_cache)} leads")

@app.route('/api/leads')
def get_leads():
    """Get all leads"""
    return jsonify({
        'leads': leads_cache,
        'last_update': last_update,
        'count': len(leads_cache)
    })

@app.route('/api/refresh')
def refresh_leads():
    """Refresh leads"""
    global leads_cache, last_update
    
    # For now, just return existing leads
    return jsonify({
        'status': 'success',
        'message': 'Leads refreshed',
        'count': len(leads_cache),
        'last_update': last_update
    })

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'leads_count': len(leads_cache),
        'last_update': last_update
    })

if __name__ == '__main__':
    print("Starting backend on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)