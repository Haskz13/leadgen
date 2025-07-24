from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
from api_real_scraper import APIRealOpportunityScraper
import threading
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Global variable to store real opportunities
REAL_OPPORTUNITIES = []
last_update = None

def update_real_opportunities():
    """Background task to update real opportunities"""
    global REAL_OPPORTUNITIES, last_update
    while True:
        try:
            print(f"\n[{datetime.now()}] Updating real opportunities...")
            scraper = APIRealOpportunityScraper()
            REAL_OPPORTUNITIES = scraper.get_all_real_opportunities()
            last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{datetime.now()}] Successfully updated {len(REAL_OPPORTUNITIES)} real opportunities")
        except Exception as e:
            print(f"[{datetime.now()}] Error updating opportunities: {e}")
        
        # Update every 30 minutes
        time.sleep(1800)

# Start background updater
updater_thread = threading.Thread(target=update_real_opportunities, daemon=True)
updater_thread.start()

# Initial load
print("Loading initial real opportunities...")
scraper = APIRealOpportunityScraper()
REAL_OPPORTUNITIES = scraper.get_all_real_opportunities()
last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route('/')
def index():
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/api/leads')
def get_leads():
    """Return real opportunities"""
    return jsonify({
        'leads': REAL_OPPORTUNITIES,
        'total': len(REAL_OPPORTUNITIES),
        'last_update': last_update,
        'message': 'These are REAL opportunities from official Canadian government sources'
    })

@app.route('/api/stats')
def get_stats():
    """Return statistics about real opportunities"""
    stats = {
        'total_leads': len(REAL_OPPORTUNITIES),
        'federal': len([l for l in REAL_OPPORTUNITIES if 'federal' in l['type'].lower()]),
        'provincial': len([l for l in REAL_OPPORTUNITIES if 'provincial' in l['type'].lower()]),
        'indigenous': len([l for l in REAL_OPPORTUNITIES if 'indigenous' in l['type'].lower()]),
        'grants': len([l for l in REAL_OPPORTUNITIES if 'grant' in l['type'].lower()]),
        'new_leads': len([l for l in REAL_OPPORTUNITIES if l['status'] == 'Active Opportunity']),
        'last_update': last_update
    }
    return jsonify(stats)

# Professional Dashboard Template
DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Canadian Training Opportunities - REAL LEADS</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0a;
            color: #e0e0e0;
            line-height: 1.6;
        }
        
        .header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 2rem;
            box-shadow: 0 2px 20px rgba(0,0,0,0.5);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .header h1 {
            font-size: 2.5rem;
            background: linear-gradient(45deg, #00ff88, #00aaff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        
        .subtitle {
            color: #888;
            font-size: 1.1rem;
        }
        
        .real-badge {
            display: inline-block;
            background: #00ff88;
            color: #000;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9rem;
            margin-left: 1rem;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            padding: 2rem;
            background: #0f0f0f;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            border: 1px solid #333;
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(45deg, #00ff88, #00aaff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-label {
            color: #888;
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }
        
        .controls {
            padding: 2rem;
            background: #111;
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
        }
        
        .search-box {
            flex: 1;
            min-width: 300px;
            position: relative;
        }
        
        .search-box input {
            width: 100%;
            padding: 1rem 3rem 1rem 1rem;
            background: #1a1a2e;
            border: 2px solid #333;
            border-radius: 8px;
            color: #fff;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }
        
        .search-box input:focus {
            outline: none;
            border-color: #00aaff;
        }
        
        .filters {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }
        
        select, button {
            padding: 0.8rem 1.5rem;
            background: #1a1a2e;
            border: 2px solid #333;
            border-radius: 8px;
            color: #fff;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        select:hover, button:hover {
            border-color: #00aaff;
            background: #16213e;
        }
        
        button.primary {
            background: linear-gradient(135deg, #00ff88 0%, #00aaff 100%);
            border: none;
            color: #000;
            font-weight: bold;
        }
        
        .leads-container {
            padding: 2rem;
        }
        
        .lead-card {
            background: #1a1a2e;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
        }
        
        .lead-card:hover {
            border-color: #00aaff;
            box-shadow: 0 5px 20px rgba(0, 170, 255, 0.2);
        }
        
        .lead-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 1rem;
        }
        
        .lead-title {
            font-size: 1.3rem;
            color: #00ff88;
            margin-bottom: 0.5rem;
        }
        
        .lead-org {
            color: #888;
            font-size: 1.1rem;
        }
        
        .lead-badges {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        
        .badge {
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        
        .badge.tier-1 {
            background: #ff6b6b;
            color: #fff;
        }
        
        .badge.tier-2 {
            background: #4ecdc4;
            color: #000;
        }
        
        .badge.real {
            background: #00ff88;
            color: #000;
        }
        
        .lead-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;
        }
        
        .detail-item {
            padding: 1rem;
            background: #0f0f0f;
            border-radius: 8px;
        }
        
        .detail-label {
            color: #666;
            font-size: 0.8rem;
            margin-bottom: 0.3rem;
        }
        
        .detail-value {
            color: #fff;
            font-weight: 500;
        }
        
        .lead-actions {
            display: flex;
            gap: 1rem;
            margin-top: 1.5rem;
        }
        
        .lead-actions a {
            padding: 0.8rem 1.5rem;
            background: linear-gradient(135deg, #00ff88 0%, #00aaff 100%);
            color: #000;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            transition: transform 0.3s ease;
        }
        
        .lead-actions a:hover {
            transform: translateY(-2px);
        }
        
        .update-notice {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: #1a1a2e;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            border: 1px solid #00ff88;
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .update-notice .dot {
            width: 10px;
            height: 10px;
            background: #00ff88;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        .loading {
            text-align: center;
            padding: 4rem;
            font-size: 1.2rem;
            color: #666;
        }
        
        .no-results {
            text-align: center;
            padding: 4rem;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Canadian Training Opportunities Dashboard <span class="real-badge">REAL LEADS</span></h1>
        <p class="subtitle">Live data from official Canadian government procurement sources</p>
    </div>
    
    <div class="stats-grid" id="statsGrid">
        <div class="stat-card">
            <div class="stat-value">-</div>
            <div class="stat-label">Total Real Opportunities</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">-</div>
            <div class="stat-label">Federal Opportunities</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">-</div>
            <div class="stat-label">Provincial Opportunities</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">-</div>
            <div class="stat-label">Indigenous Programs</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">-</div>
            <div class="stat-label">Grant Opportunities</div>
        </div>
    </div>
    
    <div class="controls">
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Search real opportunities...">
        </div>
        <div class="filters">
            <select id="typeFilter">
                <option value="">All Types</option>
                <option value="federal">Federal</option>
                <option value="provincial">Provincial</option>
                <option value="indigenous">Indigenous</option>
                <option value="grant">Grants</option>
                <option value="sector">Sector-Specific</option>
                <option value="rfp">RFPs</option>
            </select>
            <select id="sourceFilter">
                <option value="">All Sources</option>
                <option value="government programs">Government Programs</option>
                <option value="provincial programs">Provincial Programs</option>
                <option value="indigenous programs">Indigenous Programs</option>
                <option value="sector programs">Sector Programs</option>
                <option value="current rfps">Current RFPs</option>
            </select>
            <button onclick="refreshData()" class="primary">Refresh Data</button>
        </div>
    </div>
    
    <div class="leads-container" id="leadsContainer">
        <div class="loading">Loading real opportunities...</div>
    </div>
    
    <div class="update-notice">
        <div class="dot"></div>
        <span id="updateTime">Checking for updates...</span>
    </div>
    
    <script>
        let allLeads = [];
        let filteredLeads = [];
        
        async function loadData() {
            try {
                const response = await fetch('/api/leads');
                const data = await response.json();
                allLeads = data.leads;
                filteredLeads = allLeads;
                
                updateStats();
                displayLeads();
                
                document.getElementById('updateTime').textContent = `Last update: ${data.last_update}`;
            } catch (error) {
                console.error('Error loading data:', error);
                document.getElementById('leadsContainer').innerHTML = 
                    '<div class="no-results">Error loading data. Please refresh.</div>';
            }
        }
        
        async function updateStats() {
            try {
                const response = await fetch('/api/stats');
                const stats = await response.json();
                
                const statCards = document.querySelectorAll('.stat-value');
                statCards[0].textContent = stats.total_leads;
                statCards[1].textContent = stats.federal;
                statCards[2].textContent = stats.provincial;
                statCards[3].textContent = stats.indigenous;
                statCards[4].textContent = stats.grants;
            } catch (error) {
                console.error('Error updating stats:', error);
            }
        }
        
        function displayLeads() {
            const container = document.getElementById('leadsContainer');
            
            if (filteredLeads.length === 0) {
                container.innerHTML = '<div class="no-results">No opportunities found matching your criteria.</div>';
                return;
            }
            
            container.innerHTML = filteredLeads.map(lead => `
                <div class="lead-card">
                    <div class="lead-header">
                        <div>
                            <h3 class="lead-title">${lead.title}</h3>
                            <p class="lead-org">${lead.organization}</p>
                        </div>
                        <div class="lead-badges">
                            <span class="badge real">REAL</span>
                            <span class="badge tier-${lead.tier.toLowerCase().replace(' ', '-')}">${lead.tier}</span>
                        </div>
                    </div>
                    
                    <div class="lead-details">
                        <div class="detail-item">
                            <div class="detail-label">Type</div>
                            <div class="detail-value">${lead.type}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Deadline</div>
                            <div class="detail-value">${lead.deadline}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Budget</div>
                            <div class="detail-value">${lead.budget}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Source</div>
                            <div class="detail-value">${lead.source}</div>
                        </div>
                    </div>
                    
                    <p style="margin: 1rem 0; color: #ccc;">${lead.description}</p>
                    
                    <div class="lead-actions">
                        <a href="${lead.url}" target="_blank">View Official Details</a>
                    </div>
                </div>
            `).join('');
        }
        
        function filterLeads() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const typeFilter = document.getElementById('typeFilter').value.toLowerCase();
            const sourceFilter = document.getElementById('sourceFilter').value.toLowerCase();
            
            filteredLeads = allLeads.filter(lead => {
                const matchesSearch = !searchTerm || 
                    lead.title.toLowerCase().includes(searchTerm) ||
                    lead.organization.toLowerCase().includes(searchTerm) ||
                    lead.description.toLowerCase().includes(searchTerm);
                
                const matchesType = !typeFilter || lead.type.toLowerCase().includes(typeFilter);
                const matchesSource = !sourceFilter || lead.source.toLowerCase().includes(sourceFilter);
                
                return matchesSearch && matchesType && matchesSource;
            });
            
            displayLeads();
        }
        
        function refreshData() {
            document.getElementById('leadsContainer').innerHTML = '<div class="loading">Refreshing real opportunities...</div>';
            loadData();
        }
        
        // Event listeners
        document.getElementById('searchInput').addEventListener('input', filterLeads);
        document.getElementById('typeFilter').addEventListener('change', filterLeads);
        document.getElementById('sourceFilter').addEventListener('change', filterLeads);
        
        // Initial load
        loadData();
        
        // Auto-refresh every 5 minutes
        setInterval(loadData, 300000);
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 CANADIAN TRAINING OPPORTUNITIES - REAL LEADS SYSTEM")
    print("="*60)
    print(f"✅ Loaded {len(REAL_OPPORTUNITIES)} real opportunities")
    print("🌐 Starting web server on http://localhost:5000")
    print("📊 Dashboard will auto-refresh every 5 minutes")
    print("🔄 Background updater runs every 30 minutes")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)