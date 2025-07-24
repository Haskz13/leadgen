#!/usr/bin/env python3
"""
Simple Lead Generation Dashboard
This displays Canadian public sector training opportunities
"""

from flask import Flask, render_template_string, jsonify
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Sample leads data (realistic examples based on current Canadian government initiatives)
SAMPLE_LEADS = [
    {
        'id': 'lead_001',
        'organization': 'Government of Canada - Treasury Board Secretariat',
        'opportunity': 'Digital Transformation Training Program for Federal Employees 2025',
        'description': 'Comprehensive training program to upskill federal employees in digital technologies, data analytics, and AI adoption as part of the GC Digital Ambition 2025-2027.',
        'category': 'Digital Skills Training',
        'source': 'https://www.canada.ca/en/government/system/digital-government/digital-ambition.html',
        'date_found': datetime.now().strftime('%Y-%m-%d'),
        'deadline': '2025-03-31',
        'tier': 'Tier 1 - Urgent',
        'status': 'New Lead',
        'contact': 'digital-transformation@tbs-sct.gc.ca',
        'budget_range': '$2.5M - $5M',
        'critical_analysis': 'High-priority initiative aligned with GC Digital Ambition. Treasury Board has allocated significant budget for 2025-2026. Early engagement critical as RFP expected Q1 2025.',
        'next_steps': [
            'Contact TBS Digital Transformation Office immediately',
            'Attend upcoming industry day (February 2025)',
            'Partner with approved standing offer holders',
            'Prepare case studies of similar federal implementations',
            'Submit vendor profile to TBS procurement'
        ],
        'decision_makers': ['Chief Information Officer of Canada', 'ADM Digital Transformation', 'Director of Digital Talent'],
        'training_type': 'Digital Skills Training'
    },
    {
        'id': 'lead_002',
        'organization': 'Ontario Public Service',
        'opportunity': 'Mandatory Accessibility Training for All OPS Employees',
        'description': 'Province-wide mandatory training on AODA compliance and inclusive service delivery for 60,000+ OPS employees. Multi-year contract starting April 2025.',
        'category': 'Compliance Training',
        'source': 'https://www.ontario.ca/page/accessibility-ontario',
        'date_found': datetime.now().strftime('%Y-%m-%d'),
        'deadline': '2025-02-28',
        'tier': 'Tier 1 - Urgent',
        'status': 'New Lead',
        'contact': 'accessibility@ontario.ca',
        'budget_range': '$5M - $10M',
        'critical_analysis': 'Mandatory training driven by AODA legislation. Massive scale opportunity with recurring revenue potential. Competition will be fierce.',
        'next_steps': [
            'Register as Ontario vendor immediately',
            'Contact OPS Centre for Leadership and Learning',
            'Develop French language content capabilities',
            'Showcase accessibility credentials and certifications',
            'Propose phased rollout plan'
        ],
        'decision_makers': ['Secretary of Cabinet', 'Chief Talent Officer', 'Director of Learning and Development'],
        'training_type': 'Compliance Training'
    },
    {
        'id': 'lead_003',
        'organization': 'City of Toronto',
        'opportunity': 'Climate Action Training for Municipal Staff',
        'description': 'Training program to support TransformTO climate action strategy. Focus on sustainable practices, green procurement, and climate adaptation for 35,000 city employees.',
        'category': 'Sustainability Training',
        'source': 'https://www.toronto.ca/services-payments/water-environment/climate-action/',
        'date_found': datetime.now().strftime('%Y-%m-%d'),
        'deadline': '2025-04-15',
        'tier': 'Tier 2 - High Priority',
        'status': 'New Lead',
        'contact': 'transformto@toronto.ca',
        'budget_range': '$1M - $2.5M',
        'critical_analysis': 'Aligns with municipal climate emergency declaration. Political priority with dedicated funding.',
        'next_steps': [
            'Review TransformTO Net Zero Strategy',
            'Connect with Environment & Climate Division',
            'Highlight sustainability training credentials',
            'Propose metrics-based impact measurement',
            'Consider partnership with local environmental groups'
        ],
        'decision_makers': ['General Manager Environment & Climate', 'Director of HR', 'Chief Transformation Officer'],
        'training_type': 'Sustainability Training'
    }
]

# HTML Template with improved dark theme
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Canadian Public Sector Training Leads - Sales Intelligence Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0a;
            color: #ffffff;
            line-height: 1.6;
        }
        
        .header {
            background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
            padding: 2rem;
            border-bottom: 1px solid #333;
            box-shadow: 0 2px 10px rgba(0,0,0,0.5);
        }
        
        .header h1 {
            color: #3b82f6;
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        .header p {
            color: #999;
        }
        
        .stats {
            display: flex;
            gap: 2rem;
            padding: 2rem;
            background: #141414;
            border-bottom: 1px solid #333;
        }
        
        .stat {
            flex: 1;
            background: #1a1a1a;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #333;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: #3b82f6;
        }
        
        .stat-label {
            color: #999;
            font-size: 0.9rem;
        }
        
        .container {
            padding: 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .lead-card {
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
        }
        
        .lead-card:hover {
            border-color: #3b82f6;
            box-shadow: 0 4px 20px rgba(59, 130, 246, 0.2);
        }
        
        .lead-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 1rem;
        }
        
        .lead-org {
            color: #3b82f6;
            font-size: 1.1rem;
            font-weight: 600;
        }
        
        .lead-tier {
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }
        
        .tier-1 {
            background: #dc2626;
            color: white;
        }
        
        .tier-2 {
            background: #f59e0b;
            color: white;
        }
        
        .tier-3 {
            background: #10b981;
            color: white;
        }
        
        .lead-opportunity {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #fff;
        }
        
        .lead-description {
            color: #ccc;
            margin-bottom: 1rem;
        }
        
        .lead-meta {
            display: flex;
            gap: 2rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }
        
        .meta-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #999;
            font-size: 0.9rem;
        }
        
        .lead-analysis {
            background: #0f0f0f;
            border-left: 3px solid #3b82f6;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 4px;
        }
        
        .lead-analysis h4 {
            color: #3b82f6;
            margin-bottom: 0.5rem;
        }
        
        .lead-actions {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .btn {
            padding: 0.5rem 1rem;
            border-radius: 6px;
            border: none;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn-primary {
            background: #3b82f6;
            color: white;
        }
        
        .btn-primary:hover {
            background: #2563eb;
        }
        
        .btn-secondary {
            background: #374151;
            color: white;
        }
        
        .btn-secondary:hover {
            background: #4b5563;
        }
        
        .loading {
            text-align: center;
            padding: 4rem;
            color: #666;
        }
        
        .error {
            background: #dc2626;
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 2rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Canadian Public Sector Training Leads</h1>
        <p>Sales Intelligence Dashboard - Real-time opportunities for 2025/2026</p>
    </div>
    
    <div class="stats">
        <div class="stat">
            <div class="stat-value" id="total-leads">0</div>
            <div class="stat-label">Total Leads</div>
        </div>
        <div class="stat">
            <div class="stat-value" id="urgent-leads">0</div>
            <div class="stat-label">Urgent (Tier 1)</div>
        </div>
        <div class="stat">
            <div class="stat-value" id="total-value">$0</div>
            <div class="stat-label">Potential Value</div>
        </div>
        <div class="stat">
            <div class="stat-value" id="last-update">--</div>
            <div class="stat-label">Last Update</div>
        </div>
    </div>
    
    <div class="container">
        <div id="leads-container">
            <div class="loading">Loading leads...</div>
        </div>
    </div>
    
    <script>
        // Fetch and display leads
        async function loadLeads() {
            try {
                const response = await fetch('/api/leads');
                const data = await response.json();
                
                if (data.leads && data.leads.length > 0) {
                    displayLeads(data.leads);
                    updateStats(data);
                } else {
                    document.getElementById('leads-container').innerHTML = 
                        '<div class="error">No leads found</div>';
                }
            } catch (error) {
                console.error('Error loading leads:', error);
                document.getElementById('leads-container').innerHTML = 
                    '<div class="error">Error loading leads. Please refresh the page.</div>';
            }
        }
        
        function displayLeads(leads) {
            const container = document.getElementById('leads-container');
            container.innerHTML = leads.map(lead => `
                <div class="lead-card">
                    <div class="lead-header">
                        <div class="lead-org">${lead.organization}</div>
                        <div class="lead-tier ${lead.tier.toLowerCase().replace(/[^a-z0-9]/g, '-')}">${lead.tier}</div>
                    </div>
                    
                    <h3 class="lead-opportunity">${lead.opportunity}</h3>
                    <p class="lead-description">${lead.description}</p>
                    
                    <div class="lead-meta">
                        <div class="meta-item">
                            📅 Deadline: ${lead.deadline}
                        </div>
                        <div class="meta-item">
                            💰 Budget: ${lead.budget_range}
                        </div>
                        <div class="meta-item">
                            📧 Contact: ${lead.contact}
                        </div>
                        <div class="meta-item">
                            🏷️ Type: ${lead.training_type}
                        </div>
                    </div>
                    
                    <div class="lead-analysis">
                        <h4>Critical Analysis</h4>
                        <p>${lead.critical_analysis}</p>
                    </div>
                    
                    <div class="lead-actions">
                        <a href="${lead.source}" target="_blank" class="btn btn-primary">View Source</a>
                        <button class="btn btn-secondary" onclick="alert('Contact: ${lead.contact}')">Contact Info</button>
                    </div>
                </div>
            `).join('');
        }
        
        function updateStats(data) {
            document.getElementById('total-leads').textContent = data.count || 0;
            
            const urgentCount = data.leads.filter(l => l.tier.includes('Tier 1')).length;
            document.getElementById('urgent-leads').textContent = urgentCount;
            
            // Calculate total potential value
            let totalValue = 0;
            data.leads.forEach(lead => {
                const match = lead.budget_range.match(/\$(\d+(?:\.\d+)?)[MK]?/);
                if (match) {
                    let value = parseFloat(match[1]);
                    if (lead.budget_range.includes('M')) value *= 1000000;
                    else if (lead.budget_range.includes('K')) value *= 1000;
                    totalValue += value;
                }
            });
            
            const formattedValue = totalValue >= 1000000 
                ? `$${(totalValue / 1000000).toFixed(1)}M` 
                : `$${(totalValue / 1000).toFixed(0)}K`;
            document.getElementById('total-value').textContent = formattedValue;
            
            // Update last refresh time
            const updateTime = data.last_update || new Date().toLocaleTimeString();
            document.getElementById('last-update').textContent = updateTime;
        }
        
        // Load leads on page load
        loadLeads();
        
        // Auto-refresh every 5 minutes
        setInterval(loadLeads, 300000);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/leads')
def get_leads():
    """API endpoint to get leads"""
    return jsonify({
        'leads': SAMPLE_LEADS,
        'count': len(SAMPLE_LEADS),
        'last_update': datetime.now().strftime('%H:%M:%S')
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Canadian Public Sector Lead Generation Dashboard")
    print("="*60)
    print("✅ Starting application...")
    print("📊 Dashboard: http://localhost:5001")
    print("🔌 API: http://localhost:5001/api/leads")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=False)