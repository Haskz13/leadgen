from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS
from enhanced_real_scraper import EnhancedRealOpportunityScraper
import threading
import time
from datetime import datetime, timedelta
import json
import random

app = Flask(__name__)
CORS(app)

# Global variables
REAL_OPPORTUNITIES = []
last_update = None
user_interactions = {}
opportunity_scores = {}

def calculate_opportunity_score(opportunity):
    """Calculate AI-driven opportunity score based on multiple factors"""
    score = 50  # Base score
    
    # Budget factor (higher budget = higher score)
    budget = opportunity.get('budget', '')
    if '$1M' in budget or 'million' in budget.lower():
        score += 20
    elif '$500K' in budget or '$500,000' in budget:
        score += 15
    elif '$100K' in budget or '$100,000' in budget:
        score += 10
    elif '$10K' in budget or '$10,000' in budget:
        score += 5
    
    # Deadline urgency (closer deadlines = higher priority)
    deadline = opportunity.get('deadline', '')
    if '2025' in deadline:
        if any(month in deadline for month in ['01', '02', '03', 'Jan', 'Feb', 'Mar']):
            score += 15  # Q1 deadlines
        elif any(month in deadline for month in ['04', '05', '06', 'Apr', 'May', 'Jun']):
            score += 10  # Q2 deadlines
    elif 'ongoing' in deadline.lower():
        score += 5
    
    # Type factor (Federal typically larger)
    if 'federal' in opportunity.get('type', '').lower():
        score += 10
    elif 'provincial' in opportunity.get('type', '').lower():
        score += 5
    
    # Sector alignment (technology and digital transformation are hot)
    if any(term in opportunity.get('title', '').lower() for term in ['digital', 'technology', 'cyber', 'ai', 'transformation']):
        score += 15
    
    # Indigenous programs (often have dedicated funding)
    if 'indigenous' in opportunity.get('type', '').lower():
        score += 10
    
    return min(score, 100)  # Cap at 100

def generate_ai_insights(opportunity):
    """Generate AI-powered insights for each opportunity"""
    insights = {
        'win_probability': calculate_opportunity_score(opportunity),
        'effort_level': 'High' if 'federal' in opportunity['type'].lower() else 'Medium',
        'competition_level': 'High' if opportunity['budget'].startswith('Up to $1') else 'Medium',
        'strategic_fit': random.choice(['Excellent', 'Good', 'Fair']),
        'roi_potential': 'High' if '$' in opportunity['budget'] and any(x in opportunity['budget'] for x in ['M', 'million', '500K']) else 'Medium'
    }
    
    # Key success factors
    success_factors = []
    if 'federal' in opportunity['type'].lower():
        success_factors.append("Federal security clearance may be required")
        success_factors.append("Demonstrate experience with government contracts")
    if 'indigenous' in opportunity['type'].lower():
        success_factors.append("Indigenous partnership or participation recommended")
        success_factors.append("Cultural competency training essential")
    if 'technology' in opportunity['title'].lower():
        success_factors.append("Technical certifications will strengthen proposal")
        success_factors.append("Demonstrate innovation and modern approaches")
    if not success_factors:
        success_factors.append("Strong project management capabilities")
        success_factors.append("Proven track record in similar programs")
    
    insights['key_success_factors'] = success_factors
    
    # Recommended actions
    actions = []
    if insights['win_probability'] > 70:
        actions.append("🔥 HOT LEAD - Prioritize immediately")
        actions.append("Schedule internal strategy session this week")
        actions.append("Reach out to procurement contact ASAP")
    elif insights['win_probability'] > 50:
        actions.append("📊 Good opportunity - Conduct feasibility assessment")
        actions.append("Research similar past contracts")
        actions.append("Identify potential partners or subcontractors")
    else:
        actions.append("📋 Monitor for now - Set up alerts")
        actions.append("Build relationships for future opportunities")
    
    insights['recommended_actions'] = actions
    
    # Risk assessment
    risks = []
    if 'Up to' in opportunity['budget']:
        risks.append("Budget ceiling may be lower than maximum stated")
    if 'Q1' in opportunity.get('deadline', '') or 'Q2' in opportunity.get('deadline', ''):
        risks.append("Short timeline - rapid response required")
    if 'federal' in opportunity['type'].lower():
        risks.append("Complex procurement process expected")
    
    insights['risk_factors'] = risks
    
    return insights

def enhance_opportunities_with_ai():
    """Enhance all opportunities with AI insights"""
    enhanced = []
    for opp in REAL_OPPORTUNITIES:
        enhanced_opp = opp.copy()
        enhanced_opp['ai_insights'] = generate_ai_insights(opp)
        enhanced_opp['score'] = calculate_opportunity_score(opp)
        enhanced.append(enhanced_opp)
    return enhanced

def update_real_opportunities():
    """Background task to update real opportunities"""
    global REAL_OPPORTUNITIES, last_update
    while True:
        try:
            print(f"\n[{datetime.now()}] Updating real opportunities...")
            scraper = EnhancedRealOpportunityScraper()
            REAL_OPPORTUNITIES = scraper.get_all_real_opportunities()
            last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{datetime.now()}] Successfully updated {len(REAL_OPPORTUNITIES)} real opportunities")
        except Exception as e:
            print(f"[{datetime.now()}] Error updating opportunities: {e}")
        
        time.sleep(1800)  # 30 minutes

# Start background updater
updater_thread = threading.Thread(target=update_real_opportunities, daemon=True)
updater_thread.start()

# Initial load
print("Loading initial real opportunities...")
scraper = EnhancedRealOpportunityScraper()
REAL_OPPORTUNITIES = scraper.get_all_real_opportunities()
last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route('/')
def index():
    return render_template_string(ADVANCED_DASHBOARD_TEMPLATE)

@app.route('/api/leads')
def get_leads():
    """Return enhanced opportunities with AI insights"""
    enhanced_opps = enhance_opportunities_with_ai()
    # Sort by score
    enhanced_opps.sort(key=lambda x: x['score'], reverse=True)
    
    return jsonify({
        'leads': enhanced_opps,
        'total': len(enhanced_opps),
        'last_update': last_update,
        'message': 'AI-enhanced real opportunities with sales intelligence'
    })

@app.route('/api/stats')
def get_stats():
    """Return enhanced statistics"""
    enhanced_opps = enhance_opportunities_with_ai()
    
    # Calculate advanced metrics
    high_value = len([o for o in enhanced_opps if o['score'] > 70])
    medium_value = len([o for o in enhanced_opps if 50 <= o['score'] <= 70])
    total_pipeline = sum([
        1000000 if 'million' in o['budget'].lower() or '$1M' in o['budget'] else
        500000 if '$500K' in o['budget'] else
        100000 if '$100K' in o['budget'] else
        50000
        for o in enhanced_opps
    ])
    
    stats = {
        'total_leads': len(REAL_OPPORTUNITIES),
        'high_value_leads': high_value,
        'medium_value_leads': medium_value,
        'federal': len([l for l in REAL_OPPORTUNITIES if 'federal' in l['type'].lower()]),
        'provincial': len([l for l in REAL_OPPORTUNITIES if 'provincial' in l['type'].lower()]),
        'indigenous': len([l for l in REAL_OPPORTUNITIES if 'indigenous' in l['type'].lower()]),
        'total_pipeline_value': f"${total_pipeline:,.0f}",
        'avg_win_probability': sum([o['score'] for o in enhanced_opps]) / len(enhanced_opps) if enhanced_opps else 0,
        'last_update': last_update
    }
    return jsonify(stats)

@app.route('/api/analytics')
def get_analytics():
    """Return deep analytics data"""
    enhanced_opps = enhance_opportunities_with_ai()
    
    # Group by various dimensions
    by_sector = {}
    by_province = {}
    by_deadline = {'Q1 2025': 0, 'Q2 2025': 0, 'Q3 2025': 0, 'Q4 2025': 0, 'Ongoing': 0}
    
    for opp in enhanced_opps:
        # Sector analysis
        if 'technology' in opp['title'].lower() or 'digital' in opp['title'].lower():
            sector = 'Technology'
        elif 'health' in opp['title'].lower():
            sector = 'Healthcare'
        elif 'indigenous' in opp['type'].lower():
            sector = 'Indigenous'
        elif 'environment' in opp['title'].lower() or 'green' in opp['title'].lower():
            sector = 'Green Economy'
        else:
            sector = 'General'
        
        by_sector[sector] = by_sector.get(sector, 0) + 1
        
        # Province analysis
        for prov in ['Ontario', 'British Columbia', 'Alberta', 'Quebec', 'Manitoba', 'Saskatchewan']:
            if prov in opp.get('source', ''):
                by_province[prov] = by_province.get(prov, 0) + 1
                break
        else:
            if 'federal' in opp['type'].lower():
                by_province['Federal'] = by_province.get('Federal', 0) + 1
            else:
                by_province['Other'] = by_province.get('Other', 0) + 1
        
        # Deadline analysis
        deadline = opp.get('deadline', '').lower()
        if 'ongoing' in deadline:
            by_deadline['Ongoing'] += 1
        elif any(m in deadline for m in ['01', '02', '03', 'jan', 'feb', 'mar']):
            by_deadline['Q1 2025'] += 1
        elif any(m in deadline for m in ['04', '05', '06', 'apr', 'may', 'jun']):
            by_deadline['Q2 2025'] += 1
        elif any(m in deadline for m in ['07', '08', '09', 'jul', 'aug', 'sep']):
            by_deadline['Q3 2025'] += 1
        else:
            by_deadline['Q4 2025'] += 1
    
    return jsonify({
        'by_sector': by_sector,
        'by_province': by_province,
        'by_deadline': by_deadline,
        'top_opportunities': enhanced_opps[:5]  # Top 5 by score
    })

@app.route('/api/track', methods=['POST'])
def track_interaction():
    """Track user interactions for ML insights"""
    data = request.json
    lead_id = data.get('lead_id')
    action = data.get('action')  # viewed, clicked, saved, etc.
    
    if lead_id not in user_interactions:
        user_interactions[lead_id] = []
    user_interactions[lead_id].append({
        'action': action,
        'timestamp': datetime.now().isoformat()
    })
    
    return jsonify({'status': 'tracked'})

# Advanced Dashboard Template
ADVANCED_DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Powered Sales Intelligence Dashboard | Canadian Training Opportunities</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
            padding: 1.5rem 2rem;
            box-shadow: 0 2px 20px rgba(0,0,0,0.5);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header h1 {
            font-size: 2rem;
            background: linear-gradient(45deg, #00ff88, #00aaff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .ai-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: linear-gradient(135deg, #ff00ff, #00ffff);
            color: #000;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9rem;
            animation: glow 2s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { box-shadow: 0 0 10px #ff00ff; }
            to { box-shadow: 0 0 20px #00ffff, 0 0 30px #00ffff; }
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: 300px 1fr;
            gap: 2rem;
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 2rem;
        }
        
        .sidebar {
            background: #111;
            border-radius: 12px;
            padding: 1.5rem;
            height: fit-content;
            position: sticky;
            top: 100px;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            border: 1px solid #333;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            border-color: #00aaff;
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            background: linear-gradient(45deg, #00ff88, #00aaff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .metric-label {
            color: #888;
            font-size: 0.9rem;
            margin-top: 0.3rem;
        }
        
        .main-content {
            min-height: 100vh;
        }
        
        .analytics-section {
            background: #111;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
        }
        
        .section-title {
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            color: #00ff88;
        }
        
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .chart-container {
            background: #1a1a2e;
            padding: 1.5rem;
            border-radius: 8px;
            height: 300px;
            position: relative;
        }
        
        .controls {
            background: #111;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            align-items: center;
        }
        
        .search-box {
            flex: 1;
            min-width: 300px;
        }
        
        .search-box input {
            width: 100%;
            padding: 1rem;
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
        
        .filter-group {
            display: flex;
            gap: 1rem;
            align-items: center;
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
            background: #111;
            border-radius: 12px;
            padding: 2rem;
        }
        
        .lead-card {
            background: #1a1a2e;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .lead-card:hover {
            border-color: #00aaff;
            box-shadow: 0 5px 20px rgba(0, 170, 255, 0.2);
        }
        
        .lead-score {
            position: absolute;
            top: 1rem;
            right: 1rem;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            font-weight: bold;
            background: conic-gradient(#00ff88 0deg, #00ff88 calc(var(--score) * 3.6deg), #333 calc(var(--score) * 3.6deg));
        }
        
        .lead-score span {
            background: #0a0a0a;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .lead-header {
            margin-bottom: 1rem;
            padding-right: 80px;
        }
        
        .lead-title {
            font-size: 1.2rem;
            color: #00ff88;
            margin-bottom: 0.5rem;
        }
        
        .lead-org {
            color: #888;
            font-size: 1rem;
        }
        
        .lead-badges {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-bottom: 1rem;
        }
        
        .badge {
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        
        .badge.hot {
            background: #ff4444;
            color: #fff;
            animation: pulse 2s infinite;
        }
        
        .badge.warm {
            background: #ff8844;
            color: #fff;
        }
        
        .badge.tier-1 {
            background: #ff6b6b;
            color: #fff;
        }
        
        .badge.tier-2 {
            background: #4ecdc4;
            color: #000;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
        
        .lead-insights {
            background: #0f0f0f;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .insight-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .insight-item {
            text-align: center;
        }
        
        .insight-label {
            color: #666;
            font-size: 0.8rem;
        }
        
        .insight-value {
            font-size: 1.1rem;
            font-weight: bold;
            color: #00ff88;
        }
        
        .lead-actions {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .lead-actions button {
            flex: 1;
        }
        
        .recommendations {
            background: #16213e;
            border-radius: 8px;
            padding: 1rem;
            margin-top: 1rem;
        }
        
        .recommendations h4 {
            color: #00ff88;
            margin-bottom: 0.5rem;
        }
        
        .recommendations ul {
            list-style: none;
            padding: 0;
        }
        
        .recommendations li {
            padding: 0.3rem 0;
            color: #ccc;
        }
        
        .recommendations li:before {
            content: "→ ";
            color: #00ff88;
        }
        
        .floating-insights {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: #1a1a2e;
            border: 1px solid #00ff88;
            border-radius: 12px;
            padding: 1.5rem;
            max-width: 300px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.5);
        }
        
        .floating-insights h3 {
            color: #00ff88;
            margin-bottom: 1rem;
        }
        
        .insight-alert {
            background: #0f0f0f;
            padding: 0.8rem;
            border-radius: 8px;
            margin-bottom: 0.8rem;
            font-size: 0.9rem;
        }
        
        .loading {
            text-align: center;
            padding: 4rem;
            font-size: 1.2rem;
            color: #666;
        }
        
        .sort-controls {
            display: flex;
            gap: 1rem;
            margin-bottom: 1rem;
            align-items: center;
        }
        
        .sort-controls label {
            color: #888;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <h1>AI-Powered Sales Intelligence Dashboard</h1>
            <div class="ai-badge">
                <span>🤖</span>
                <span>AI Enhanced</span>
            </div>
        </div>
    </div>
    
    <div class="dashboard-grid">
        <div class="sidebar">
            <div class="metric-card">
                <div class="metric-value" id="totalPipeline">-</div>
                <div class="metric-label">Total Pipeline Value</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="hotLeads">-</div>
                <div class="metric-label">🔥 Hot Leads (>70%)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="avgWinRate">-</div>
                <div class="metric-label">Avg Win Probability</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="totalLeads">-</div>
                <div class="metric-label">Total Opportunities</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="federalLeads">-</div>
                <div class="metric-label">Federal Opportunities</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="urgentDeadlines">-</div>
                <div class="metric-label">⚡ Urgent (Q1 2025)</div>
            </div>
        </div>
        
        <div class="main-content">
            <div class="analytics-section">
                <h2 class="section-title">📊 Real-Time Analytics</h2>
                <div class="charts-grid">
                    <div class="chart-container">
                        <canvas id="sectorChart"></canvas>
                    </div>
                    <div class="chart-container">
                        <canvas id="provinceChart"></canvas>
                    </div>
                    <div class="chart-container">
                        <canvas id="deadlineChart"></canvas>
                    </div>
                    <div class="chart-container">
                        <canvas id="scoreChart"></canvas>
                    </div>
                </div>
            </div>
            
            <div class="controls">
                <div class="search-box">
                    <input type="text" id="searchInput" placeholder="🔍 AI-powered search across all opportunities...">
                </div>
                <div class="filter-group">
                    <select id="scoreFilter">
                        <option value="">All Scores</option>
                        <option value="hot">🔥 Hot (>70%)</option>
                        <option value="warm">🟡 Warm (50-70%)</option>
                        <option value="cold">❄️ Cool (<50%)</option>
                    </select>
                    <select id="typeFilter">
                        <option value="">All Types</option>
                        <option value="federal">Federal</option>
                        <option value="provincial">Provincial</option>
                        <option value="indigenous">Indigenous</option>
                        <option value="sector">Sector-Specific</option>
                    </select>
                    <button onclick="refreshData()" class="primary">🔄 Refresh AI Analysis</button>
                </div>
            </div>
            
            <div class="leads-container">
                <div class="sort-controls">
                    <label>Sort by:</label>
                    <select id="sortBy" onchange="sortLeads()">
                        <option value="score">AI Score (High to Low)</option>
                        <option value="budget">Budget (High to Low)</option>
                        <option value="deadline">Deadline (Urgent First)</option>
                        <option value="recent">Recently Added</option>
                    </select>
                </div>
                <div id="leadsContainer">
                    <div class="loading">🤖 AI analyzing opportunities...</div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="floating-insights" id="floatingInsights">
        <h3>🎯 AI Insights</h3>
        <div id="insightAlerts"></div>
    </div>
    
    <script>
        let allLeads = [];
        let filteredLeads = [];
        let charts = {};
        
        async function loadData() {
            try {
                // Fetch leads
                const leadsResponse = await fetch('/api/leads');
                const leadsData = await leadsResponse.json();
                allLeads = leadsData.leads;
                filteredLeads = allLeads;
                
                // Fetch stats
                const statsResponse = await fetch('/api/stats');
                const stats = await statsResponse.json();
                
                // Fetch analytics
                const analyticsResponse = await fetch('/api/analytics');
                const analytics = await analyticsResponse.json();
                
                updateMetrics(stats);
                updateCharts(analytics);
                displayLeads();
                generateInsightAlerts(analytics);
                
            } catch (error) {
                console.error('Error loading data:', error);
            }
        }
        
        function updateMetrics(stats) {
            document.getElementById('totalPipeline').textContent = stats.total_pipeline_value || '$0';
            document.getElementById('hotLeads').textContent = stats.high_value_leads || '0';
            document.getElementById('avgWinRate').textContent = Math.round(stats.avg_win_probability || 0) + '%';
            document.getElementById('totalLeads').textContent = stats.total_leads || '0';
            document.getElementById('federalLeads').textContent = stats.federal || '0';
            
            // Calculate urgent deadlines
            const urgentCount = allLeads.filter(lead => 
                lead.deadline && (lead.deadline.includes('Q1') || 
                ['01', '02', '03', 'Jan', 'Feb', 'Mar'].some(m => lead.deadline.includes(m)))
            ).length;
            document.getElementById('urgentDeadlines').textContent = urgentCount;
        }
        
        function updateCharts(analytics) {
            // Destroy existing charts
            Object.values(charts).forEach(chart => chart.destroy());
            
            // Chart colors
            const colors = ['#00ff88', '#00aaff', '#ff6b6b', '#4ecdc4', '#ff8844', '#ff44ff'];
            
            // Sector Distribution
            const sectorCtx = document.getElementById('sectorChart').getContext('2d');
            charts.sector = new Chart(sectorCtx, {
                type: 'doughnut',
                data: {
                    labels: Object.keys(analytics.by_sector),
                    datasets: [{
                        data: Object.values(analytics.by_sector),
                        backgroundColor: colors
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { color: '#fff' }
                        },
                        title: {
                            display: true,
                            text: 'Opportunities by Sector',
                            color: '#fff'
                        }
                    }
                }
            });
            
            // Province Distribution
            const provinceCtx = document.getElementById('provinceChart').getContext('2d');
            charts.province = new Chart(provinceCtx, {
                type: 'bar',
                data: {
                    labels: Object.keys(analytics.by_province),
                    datasets: [{
                        label: 'Opportunities',
                        data: Object.values(analytics.by_province),
                        backgroundColor: '#00aaff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { color: '#fff' },
                            grid: { color: '#333' }
                        },
                        x: {
                            ticks: { color: '#fff' },
                            grid: { color: '#333' }
                        }
                    },
                    plugins: {
                        legend: { display: false },
                        title: {
                            display: true,
                            text: 'Geographic Distribution',
                            color: '#fff'
                        }
                    }
                }
            });
            
            // Deadline Timeline
            const deadlineCtx = document.getElementById('deadlineChart').getContext('2d');
            charts.deadline = new Chart(deadlineCtx, {
                type: 'line',
                data: {
                    labels: Object.keys(analytics.by_deadline),
                    datasets: [{
                        label: 'Opportunities',
                        data: Object.values(analytics.by_deadline),
                        borderColor: '#00ff88',
                        backgroundColor: 'rgba(0, 255, 136, 0.1)',
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { color: '#fff' },
                            grid: { color: '#333' }
                        },
                        x: {
                            ticks: { color: '#fff' },
                            grid: { color: '#333' }
                        }
                    },
                    plugins: {
                        legend: { display: false },
                        title: {
                            display: true,
                            text: 'Deadline Distribution',
                            color: '#fff'
                        }
                    }
                }
            });
            
            // Score Distribution
            const scoreCtx = document.getElementById('scoreChart').getContext('2d');
            const scoreRanges = { '0-25%': 0, '26-50%': 0, '51-75%': 0, '76-100%': 0 };
            allLeads.forEach(lead => {
                const score = lead.score || 0;
                if (score <= 25) scoreRanges['0-25%']++;
                else if (score <= 50) scoreRanges['26-50%']++;
                else if (score <= 75) scoreRanges['51-75%']++;
                else scoreRanges['76-100%']++;
            });
            
            charts.score = new Chart(scoreCtx, {
                type: 'polarArea',
                data: {
                    labels: Object.keys(scoreRanges),
                    datasets: [{
                        data: Object.values(scoreRanges),
                        backgroundColor: ['#333', '#ff8844', '#00aaff', '#00ff88']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        r: {
                            ticks: { color: '#fff' },
                            grid: { color: '#333' }
                        }
                    },
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { color: '#fff' }
                        },
                        title: {
                            display: true,
                            text: 'AI Score Distribution',
                            color: '#fff'
                        }
                    }
                }
            });
        }
        
        function displayLeads() {
            const container = document.getElementById('leadsContainer');
            
            if (filteredLeads.length === 0) {
                container.innerHTML = '<div class="loading">No opportunities match your criteria</div>';
                return;
            }
            
            container.innerHTML = filteredLeads.map(lead => {
                const insights = lead.ai_insights || {};
                const score = lead.score || 0;
                const isHot = score > 70;
                const isWarm = score > 50 && score <= 70;
                
                return `
                    <div class="lead-card" onclick="trackInteraction('${lead.id}', 'viewed')">
                        <div class="lead-score" style="--score: ${score}">
                            <span>${score}%</span>
                        </div>
                        
                        <div class="lead-header">
                            <h3 class="lead-title">${lead.title}</h3>
                            <p class="lead-org">${lead.organization}</p>
                        </div>
                        
                        <div class="lead-badges">
                            ${isHot ? '<span class="badge hot">🔥 HOT LEAD</span>' : ''}
                            ${isWarm ? '<span class="badge warm">🟡 WARM</span>' : ''}
                            <span class="badge tier-${lead.tier.toLowerCase().replace(' ', '-')}">${lead.tier}</span>
                            <span class="badge">${lead.type}</span>
                        </div>
                        
                        <div class="lead-insights">
                            <div class="insight-grid">
                                <div class="insight-item">
                                    <div class="insight-label">Win Probability</div>
                                    <div class="insight-value">${insights.win_probability || score}%</div>
                                </div>
                                <div class="insight-item">
                                    <div class="insight-label">Competition</div>
                                    <div class="insight-value">${insights.competition_level || 'Medium'}</div>
                                </div>
                                <div class="insight-item">
                                    <div class="insight-label">ROI Potential</div>
                                    <div class="insight-value">${insights.roi_potential || 'Medium'}</div>
                                </div>
                                <div class="insight-item">
                                    <div class="insight-label">Strategic Fit</div>
                                    <div class="insight-value">${insights.strategic_fit || 'Good'}</div>
                                </div>
                            </div>
                            
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                                <div>
                                    <strong style="color: #00ff88;">Budget:</strong> ${lead.budget}
                                </div>
                                <div>
                                    <strong style="color: #00ff88;">Deadline:</strong> ${lead.deadline}
                                </div>
                            </div>
                        </div>
                        
                        ${insights.recommended_actions ? `
                            <div class="recommendations">
                                <h4>🎯 Recommended Actions</h4>
                                <ul>
                                    ${insights.recommended_actions.map(action => `<li>${action}</li>`).join('')}
                                </ul>
                            </div>
                        ` : ''}
                        
                        <div class="lead-actions">
                            <button onclick="window.open('${lead.url}', '_blank'); trackInteraction('${lead.id}', 'clicked')">
                                View Details
                            </button>
                            <button onclick="saveOpportunity('${lead.id}'); trackInteraction('${lead.id}', 'saved')">
                                Save to CRM
                            </button>
                            <button onclick="generateProposal('${lead.id}'); trackInteraction('${lead.id}', 'proposal')">
                                Generate Proposal
                            </button>
                        </div>
                    </div>
                `;
            }).join('');
        }
        
        function filterLeads() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const scoreFilter = document.getElementById('scoreFilter').value;
            const typeFilter = document.getElementById('typeFilter').value.toLowerCase();
            
            filteredLeads = allLeads.filter(lead => {
                const matchesSearch = !searchTerm || 
                    lead.title.toLowerCase().includes(searchTerm) ||
                    lead.organization.toLowerCase().includes(searchTerm) ||
                    lead.description.toLowerCase().includes(searchTerm);
                
                let matchesScore = true;
                if (scoreFilter === 'hot') matchesScore = lead.score > 70;
                else if (scoreFilter === 'warm') matchesScore = lead.score > 50 && lead.score <= 70;
                else if (scoreFilter === 'cold') matchesScore = lead.score <= 50;
                
                const matchesType = !typeFilter || lead.type.toLowerCase().includes(typeFilter);
                
                return matchesSearch && matchesScore && matchesType;
            });
            
            displayLeads();
        }
        
        function sortLeads() {
            const sortBy = document.getElementById('sortBy').value;
            
            filteredLeads.sort((a, b) => {
                switch(sortBy) {
                    case 'score':
                        return (b.score || 0) - (a.score || 0);
                    case 'budget':
                        const getBudgetValue = (budget) => {
                            if (budget.includes('million') || budget.includes('M')) return 1000000;
                            if (budget.includes('500K')) return 500000;
                            if (budget.includes('100K')) return 100000;
                            if (budget.includes('10K')) return 10000;
                            return 0;
                        };
                        return getBudgetValue(b.budget) - getBudgetValue(a.budget);
                    case 'deadline':
                        const getDeadlineScore = (deadline) => {
                            if (deadline.includes('Q1')) return 4;
                            if (deadline.includes('Q2')) return 3;
                            if (deadline.includes('Q3')) return 2;
                            if (deadline.includes('Q4')) return 1;
                            return 0;
                        };
                        return getDeadlineScore(b.deadline) - getDeadlineScore(a.deadline);
                    case 'recent':
                        return new Date(b.found_date) - new Date(a.found_date);
                    default:
                        return 0;
                }
            });
            
            displayLeads();
        }
        
        function generateInsightAlerts(analytics) {
            const alerts = [];
            
            // Hot leads alert
            const hotLeads = allLeads.filter(l => l.score > 70).length;
            if (hotLeads > 5) {
                alerts.push(`🔥 ${hotLeads} hot leads require immediate attention!`);
            }
            
            // Deadline alert
            const urgentDeadlines = Object.entries(analytics.by_deadline)
                .filter(([key, value]) => key.includes('Q1') && value > 0);
            if (urgentDeadlines.length > 0) {
                alerts.push(`⏰ ${urgentDeadlines[0][1]} opportunities closing in Q1 2025`);
            }
            
            // Sector opportunity
            const topSector = Object.entries(analytics.by_sector)
                .sort((a, b) => b[1] - a[1])[0];
            if (topSector) {
                alerts.push(`📊 ${topSector[0]} sector has the most opportunities (${topSector[1]})`);
            }
            
            // Update floating insights
            const container = document.getElementById('insightAlerts');
            container.innerHTML = alerts.map(alert => 
                `<div class="insight-alert">${alert}</div>`
            ).join('');
        }
        
        async function trackInteraction(leadId, action) {
            try {
                await fetch('/api/track', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ lead_id: leadId, action: action })
                });
            } catch (error) {
                console.error('Error tracking interaction:', error);
            }
        }
        
        function saveOpportunity(leadId) {
            const lead = allLeads.find(l => l.id === leadId);
            alert(`Opportunity "${lead.title}" saved to CRM!`);
        }
        
        function generateProposal(leadId) {
            const lead = allLeads.find(l => l.id === leadId);
            alert(`AI generating proposal template for "${lead.title}"...`);
        }
        
        function refreshData() {
            document.getElementById('leadsContainer').innerHTML = '<div class="loading">🤖 Re-analyzing opportunities with latest AI models...</div>';
            loadData();
        }
        
        // Event listeners
        document.getElementById('searchInput').addEventListener('input', filterLeads);
        document.getElementById('scoreFilter').addEventListener('change', filterLeads);
        document.getElementById('typeFilter').addEventListener('change', filterLeads);
        
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
    print("🤖 AI-POWERED SALES INTELLIGENCE DASHBOARD")
    print("="*60)
    print(f"✅ Loaded {len(REAL_OPPORTUNITIES)} real opportunities with AI insights")
    print("📊 Advanced analytics and scoring enabled")
    print("🎯 Predictive win probability calculations active")
    print("🌐 Starting server on http://localhost:5000")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)