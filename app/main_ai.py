from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
import threading
import time
from ai_scraper import AITrainingOpportunityFinder

app = Flask(__name__)
CORS(app)

# Global variables for caching
leads_cache = []
last_update = None
update_lock = threading.Lock()
ai_finder = AITrainingOpportunityFinder()

def update_leads():
    """Update leads using AI-powered search"""
    global leads_cache, last_update
    
    print("🔄 Updating leads with AI search...")
    try:
        new_leads = ai_finder.find_all_opportunities()
        
        with update_lock:
            leads_cache = new_leads
            last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"✅ Updated {len(new_leads)} leads at {last_update}")
    except Exception as e:
        print(f"❌ Error updating leads: {e}")

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
    # Run update in background to avoid blocking
    refresh_thread = threading.Thread(target=update_leads)
    refresh_thread.start()
    
    return jsonify({
        'status': 'success',
        'message': 'AI search initiated',
        'current_count': len(leads_cache),
        'last_update': last_update
    })

@app.route('/api/stats')
def get_stats():
    """Get dashboard statistics"""
    with update_lock:
        stats = {
            'total_leads': len(leads_cache),
            'urgent_leads': len([l for l in leads_cache if 'Tier 1' in l.get('tier', '')]),
            'high_priority_leads': len([l for l in leads_cache if 'Tier 2' in l.get('tier', '')]),
            'total_value': 0,
            'by_type': {},
            'by_organization': {}
        }
        
        # Calculate total potential value
        for lead in leads_cache:
            budget = lead.get('budget_range', '')
            if '$' in budget and 'M' in budget:
                try:
                    # Extract max value from range
                    parts = budget.split('-')
                    if len(parts) > 1:
                        max_val = parts[1].strip()
                        value = float(max_val.replace('$', '').replace('M', '').strip())
                        stats['total_value'] += value
                except:
                    pass
        
        # Count by type
        for lead in leads_cache:
            training_type = lead.get('training_type', 'Other')
            stats['by_type'][training_type] = stats['by_type'].get(training_type, 0) + 1
        
        # Count by organization type
        for lead in leads_cache:
            org = lead.get('organization', '')
            if 'Government of Canada' in org:
                org_type = 'Federal'
            elif any(prov in org for prov in ['Ontario', 'British Columbia', 'Alberta', 'Quebec']):
                org_type = 'Provincial'
            elif 'City' in org or 'Municipal' in org:
                org_type = 'Municipal'
            else:
                org_type = 'Other'
            
            stats['by_organization'][org_type] = stats['by_organization'].get(org_type, 0) + 1
        
        return jsonify(stats)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'leads_count': len(leads_cache),
        'last_update': last_update,
        'ai_status': 'active'
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Canadian Public Sector Lead Generation System")
    print("🤖 Powered by AI Search Technology")
    print("="*60)
    
    # Initial load of leads
    print("\n📊 Performing initial AI search...")
    update_leads()
    
    # Start background update thread
    update_thread = threading.Thread(target=background_update, daemon=True)
    update_thread.start()
    
    print("\n✅ Backend API ready")
    print("🔌 API endpoints:")
    print("   - http://localhost:5000/api/leads")
    print("   - http://localhost:5000/api/refresh")
    print("   - http://localhost:5000/api/stats")
    print("   - http://localhost:5000/health")
    print("="*60 + "\n")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)