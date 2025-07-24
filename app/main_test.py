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

def update_leads_async():
    """Update leads asynchronously without blocking startup"""
    global leads_cache, last_update
    
    print("Starting background lead update...")
    try:
        scraper = CanadianPublicSectorScraper()
        new_leads = scraper.get_all_leads()
        
        with update_lock:
            leads_cache = new_leads
            last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"Background update complete: {len(new_leads)} leads at {last_update}")
    except Exception as e:
        print(f"Error in background update: {e}")

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
    # Run update in background
    update_thread = threading.Thread(target=update_leads_async)
    update_thread.start()
    
    return jsonify({
        'status': 'success',
        'message': 'Lead refresh started in background',
        'current_count': len(leads_cache),
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
    # Start initial update in background (non-blocking)
    print("Starting backend without blocking on initial scraping...")
    update_thread = threading.Thread(target=update_leads_async, daemon=True)
    update_thread.start()
    
    # Run Flask app immediately
    print("Backend API starting on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)