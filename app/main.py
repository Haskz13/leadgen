from flask import Flask, jsonify
from scraper import CanadianPublicSectorScraper
import threading
import time

app = Flask(__name__)

# Global variable to store leads
leads_cache = []
last_update = None

def update_leads():
    """Background function to update leads periodically"""
    global leads_cache, last_update
    scraper = CanadianPublicSectorScraper()
    
    while True:
        try:
            print("Updating leads...")
            leads_cache = scraper.get_all_leads()
            last_update = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"Updated {len(leads_cache)} leads at {last_update}")
        except Exception as e:
            print(f"Error updating leads: {e}")
        
        # Wait 1 hour before next update
        time.sleep(3600)

# Start background thread for lead updates
update_thread = threading.Thread(target=update_leads, daemon=True)
update_thread.start()

@app.route('/api/leads')
def get_leads():
    """Return all cached leads"""
    return jsonify({
        'leads': leads_cache,
        'last_update': last_update,
        'total': len(leads_cache)
    })

@app.route('/api/refresh')
def refresh_leads():
    """Manually trigger lead refresh"""
    global leads_cache, last_update
    try:
        scraper = CanadianPublicSectorScraper()
        leads_cache = scraper.get_all_leads()
        last_update = time.strftime('%Y-%m-%d %H:%M:%S')
        return jsonify({
            'status': 'success',
            'message': f'Refreshed {len(leads_cache)} leads',
            'last_update': last_update
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    # Do initial load
    scraper = CanadianPublicSectorScraper()
    leads_cache = scraper.get_all_leads()
    last_update = time.strftime('%Y-%m-%d %H:%M:%S')
    
    app.run(debug=True)