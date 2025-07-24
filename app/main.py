from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
import threading
import time
from scraper import CanadianPublicSectorScraper

app = Flask(__name__)
CORS(app)

# Global variables for caching
leads_cache = []
last_update = None
update_lock = threading.Lock()

def update_leads():
    """Update leads from scraper"""
    global leads_cache, last_update
    
    print("Updating leads...")
    scraper = CanadianPublicSectorScraper()
    new_leads = scraper.get_all_leads()
    
    with update_lock:
        leads_cache = new_leads
        last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"Updated {len(new_leads)} leads at {last_update}")

def background_update():
    """Background thread to update leads periodically"""
    while True:
        time.sleep(3600)  # Update every hour
        update_leads()

@app.route('/api/leads')
def get_leads():
    """Get all leads"""
    with update_lock:
        return jsonify({
            'leads': leads_cache,
            'last_update': last_update,
            'count': len(leads_cache)
        })

@app.route('/api/refresh')
def refresh_leads():
    """Force refresh of leads"""
    update_leads()
    return jsonify({
        'status': 'success',
        'message': 'Leads refreshed',
        'count': len(leads_cache),
        'last_update': last_update
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'leads_count': len(leads_cache),
        'last_update': last_update
    })

if __name__ == '__main__':
    # Initial load of leads when server starts
    update_leads()
    
    # Start background update thread
    update_thread = threading.Thread(target=background_update, daemon=True)
    update_thread.start()
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)