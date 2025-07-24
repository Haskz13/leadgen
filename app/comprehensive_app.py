#!/usr/bin/env python3
"""
Canadian Public Sector Lead Generation System
Comprehensive AI-Powered Sales Intelligence Dashboard
"""

from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
from datetime import datetime
import json
from comprehensive_ai_scraper import ComprehensiveAILeadGenerator

app = Flask(__name__)
CORS(app)

# Generate comprehensive lead database on startup
print("🤖 Generating comprehensive lead database...")
generator = ComprehensiveAILeadGenerator()
AI_GENERATED_LEADS = generator.generate_all_opportunities()
print(f"✅ Generated {len(AI_GENERATED_LEADS)} opportunities!")

# Enhanced HTML Template with filtering and search
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Canadian Public Sector Training Leads - Comprehensive AI Database</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --bg-primary: #0a0a0a;
            --bg-secondary: #141414;
            --bg-card: #1a1a1a;
            --text-primary: #ffffff;
            --text-secondary: #a0a0a0;
            --accent-primary: #3b82f6;
            --accent-success: #10b981;
            --accent-warning: #f59e0b;
            --accent-danger: #ef4444;
            --border-color: #2a2a2a;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }
        
        .header {
            background: var(--bg-secondary);
            padding: 2rem;
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .header-content {
            max-width: 1600px;
            margin: 0 auto;
        }
        
        .header-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        
        .header h1 {
            font-size: 1.8rem;
            background: linear-gradient(135deg, var(--accent-primary), #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .ai-badge {
            background: linear-gradient(135deg, #8b5cf6, #6366f1);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
        }
        
        .search-bar {
            display: flex;
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .search-input {
            flex: 1;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.75rem 1rem;
            border-radius: 8px;
            font-size: 0.95rem;
        }
        
        .search-input:focus {
            outline: none;
            border-color: var(--accent-primary);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            padding: 2rem;
            max-width: 1600px;
            margin: 0 auto;
        }
        
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent-primary);
        }
        
        .stat-label {
            color: var(--text-secondary);
            font-size: 0.85rem;
        }
        
        .filters {
            padding: 0 2rem;
            max-width: 1600px;
            margin: 0 auto 2rem;
        }
        
        .filter-group {
            margin-bottom: 1rem;
        }
        
        .filter-label {
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
        }
        
        .filter-buttons {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        
        .filter-btn {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.85rem;
        }
        
        .filter-btn:hover {
            border-color: var(--accent-primary);
            color: var(--text-primary);
        }
        
        .filter-btn.active {
            background: var(--accent-primary);
            color: white;
            border-color: var(--accent-primary);
        }
        
        .leads-container {
            padding: 0 2rem 2rem;
            max-width: 1600px;
            margin: 0 auto;
        }
        
        .results-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            color: var(--text-secondary);
        }
        
        .lead-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .lead-card:hover {
            border-color: var(--accent-primary);
            transform: translateY(-1px);
        }
        
        .lead-card.expanded {
            padding: 2rem;
        }
        
        .lead-summary {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .lead-main {
            flex: 1;
        }
        
        .lead-org {
            color: var(--accent-primary);
            font-size: 0.85rem;
            margin-bottom: 0.25rem;
        }
        
        .lead-title {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .lead-meta {
            display: flex;
            gap: 2rem;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }
        
        .lead-badges {
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }
        
        .tier-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 500;
        }
        
        .tier-1 { background: var(--accent-danger); color: white; }
        .tier-2 { background: var(--accent-warning); color: white; }
        .tier-3 { background: var(--accent-success); color: white; }
        
        .lead-details {
            display: none;
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--border-color);
        }
        
        .lead-card.expanded .lead-details {
            display: block;
        }
        
        .detail-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        
        .detail-item {
            background: var(--bg-secondary);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }
        
        .detail-label {
            font-size: 0.8rem;
            color: #666;
            margin-bottom: 0.25rem;
        }
        
        .analysis-section {
            background: var(--bg-secondary);
            border-left: 3px solid var(--accent-primary);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        
        .analysis-title {
            color: var(--accent-primary);
            font-weight: 600;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }
        
        .btn {
            padding: 0.5rem 1rem;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 500;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .btn-primary {
            background: var(--accent-primary);
            color: white;
        }
        
        /* Pagination */
        .pagination {
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin-top: 2rem;
        }
        
        .page-btn {
            padding: 0.5rem 0.75rem;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            border-radius: 6px;
            cursor: pointer;
        }
        
        .page-btn.active {
            background: var(--accent-primary);
            color: white;
            border-color: var(--accent-primary);
        }
        
        .page-btn:hover:not(.active) {
            border-color: var(--accent-primary);
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="header-top">
                <div>
                    <h1>Canadian Public Sector Training Leads</h1>
                    <p style="color: var(--text-secondary);">Comprehensive AI-Powered Lead Database</p>
                </div>
                <div class="ai-badge">🤖 {{ total_leads }} Opportunities</div>
            </div>
            <div class="search-bar">
                <input type="text" class="search-input" id="searchInput" placeholder="Search organizations, opportunities, or keywords...">
            </div>
        </div>
    </header>
    
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value">{{ stats.total }}</div>
            <div class="stat-label">Total Opportunities</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ stats.urgent }}</div>
            <div class="stat-label">Urgent (Tier 1)</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ stats.high_priority }}</div>
            <div class="stat-label">High Priority (Tier 2)</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">${{ stats.total_value }}M+</div>
            <div class="stat-label">Total Pipeline Value</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ stats.federal }}</div>
            <div class="stat-label">Federal Opportunities</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{{ stats.avg_confidence }}%</div>
            <div class="stat-label">Avg AI Confidence</div>
        </div>
    </div>
    
    <div class="filters">
        <div class="filter-group">
            <div class="filter-label">Organization Type</div>
            <div class="filter-buttons">
                <button class="filter-btn active" onclick="filterByType('all')">All Types</button>
                <button class="filter-btn" onclick="filterByType('federal')">Federal</button>
                <button class="filter-btn" onclick="filterByType('provincial')">Provincial</button>
                <button class="filter-btn" onclick="filterByType('municipal')">Municipal</button>
                <button class="filter-btn" onclick="filterByType('crown')">Crown Corp</button>
                <button class="filter-btn" onclick="filterByType('indigenous')">Indigenous</button>
                <button class="filter-btn" onclick="filterByType('npo')">NPO/Charity</button>
            </div>
        </div>
        
        <div class="filter-group">
            <div class="filter-label">Training Category</div>
            <div class="filter-buttons">
                <button class="filter-btn active" onclick="filterByCategory('all')">All Categories</button>
                <button class="filter-btn" onclick="filterByCategory('Digital Transformation')">Digital</button>
                <button class="filter-btn" onclick="filterByCategory('Leadership Development')">Leadership</button>
                <button class="filter-btn" onclick="filterByCategory('Compliance and Regulatory')">Compliance</button>
                <button class="filter-btn" onclick="filterByCategory('Diversity and Inclusion')">DEI</button>
                <button class="filter-btn" onclick="filterByCategory('Sustainability and Climate')">Sustainability</button>
                <button class="filter-btn" onclick="filterByCategory('Service Excellence')">Service</button>
                <button class="filter-btn" onclick="filterByCategory('Technical Skills')">Technical</button>
            </div>
        </div>
        
        <div class="filter-group">
            <div class="filter-label">Priority</div>
            <div class="filter-buttons">
                <button class="filter-btn active" onclick="filterByTier('all')">All Priorities</button>
                <button class="filter-btn" onclick="filterByTier('tier-1')">Tier 1 - Urgent</button>
                <button class="filter-btn" onclick="filterByTier('tier-2')">Tier 2 - High Priority</button>
                <button class="filter-btn" onclick="filterByTier('tier-3')">Tier 3 - Standard</button>
            </div>
        </div>
    </div>
    
    <div class="leads-container">
        <div class="results-header">
            <div id="resultsCount">Showing 1-20 of {{ total_leads }} opportunities</div>
            <div>
                <select id="sortSelect" onchange="sortLeads()" style="background: var(--bg-card); color: var(--text-primary); border: 1px solid var(--border-color); padding: 0.5rem; border-radius: 6px;">
                    <option value="deadline">Sort by Deadline</option>
                    <option value="budget">Sort by Budget</option>
                    <option value="confidence">Sort by AI Confidence</option>
                    <option value="organization">Sort by Organization</option>
                </select>
            </div>
        </div>
        
        <div id="leadsContainer">
            <!-- Leads will be dynamically inserted here -->
        </div>
        
        <div class="pagination" id="pagination">
            <!-- Pagination buttons will be inserted here -->
        </div>
    </div>
    
    <script>
        // Lead data from server
        const allLeads = {{ leads_json | safe }};
        let filteredLeads = [...allLeads];
        let currentPage = 1;
        const leadsPerPage = 20;
        
        // Current filters
        let currentTypeFilter = 'all';
        let currentCategoryFilter = 'all';
        let currentTierFilter = 'all';
        let searchTerm = '';
        
        // Initialize
        displayLeads();
        
        // Search functionality
        document.getElementById('searchInput').addEventListener('input', (e) => {
            searchTerm = e.target.value.toLowerCase();
            applyFilters();
        });
        
        // Filter functions
        function filterByType(type) {
            currentTypeFilter = type;
            updateFilterButtons('type', type);
            applyFilters();
        }
        
        function filterByCategory(category) {
            currentCategoryFilter = category;
            updateFilterButtons('category', category);
            applyFilters();
        }
        
        function filterByTier(tier) {
            currentTierFilter = tier;
            updateFilterButtons('tier', tier);
            applyFilters();
        }
        
        function updateFilterButtons(filterGroup, activeValue) {
            const buttons = document.querySelectorAll(`.filter-group:has(.filter-label:contains("${filterGroup}")) .filter-btn`);
            buttons.forEach(btn => {
                btn.classList.remove('active');
                if (btn.textContent.includes(activeValue) || (activeValue === 'all' && btn.textContent.includes('All'))) {
                    btn.classList.add('active');
                }
            });
        }
        
        function applyFilters() {
            filteredLeads = allLeads.filter(lead => {
                // Type filter
                if (currentTypeFilter !== 'all' && lead.organization_type !== currentTypeFilter) {
                    return false;
                }
                
                // Category filter
                if (currentCategoryFilter !== 'all' && lead.training_type !== currentCategoryFilter) {
                    return false;
                }
                
                // Tier filter
                if (currentTierFilter !== 'all') {
                    const tierMap = {
                        'tier-1': 'Tier 1',
                        'tier-2': 'Tier 2',
                        'tier-3': 'Tier 3'
                    };
                    if (!lead.tier.includes(tierMap[currentTierFilter])) {
                        return false;
                    }
                }
                
                // Search filter
                if (searchTerm) {
                    const searchableText = `${lead.organization} ${lead.opportunity} ${lead.description} ${lead.training_topic}`.toLowerCase();
                    if (!searchableText.includes(searchTerm)) {
                        return false;
                    }
                }
                
                return true;
            });
            
            currentPage = 1;
            displayLeads();
        }
        
        function sortLeads() {
            const sortBy = document.getElementById('sortSelect').value;
            
            filteredLeads.sort((a, b) => {
                switch(sortBy) {
                    case 'deadline':
                        return new Date(a.deadline) - new Date(b.deadline);
                    case 'budget':
                                                 const getBudgetValue = (budget) => {
                             const match = budget.match(/\\$(\d+)M/);
                             return match ? parseInt(match[1]) : 0;
                         };
                        return getBudgetValue(b.budget_range) - getBudgetValue(a.budget_range);
                    case 'confidence':
                        return b.ai_confidence - a.ai_confidence;
                    case 'organization':
                        return a.organization.localeCompare(b.organization);
                    default:
                        return 0;
                }
            });
            
            displayLeads();
        }
        
        function displayLeads() {
            const container = document.getElementById('leadsContainer');
            const startIndex = (currentPage - 1) * leadsPerPage;
            const endIndex = startIndex + leadsPerPage;
            const pageLeads = filteredLeads.slice(startIndex, endIndex);
            
            // Update results count
            document.getElementById('resultsCount').textContent = 
                `Showing ${startIndex + 1}-${Math.min(endIndex, filteredLeads.length)} of ${filteredLeads.length} opportunities`;
            
            // Display leads
            container.innerHTML = pageLeads.map((lead, index) => `
                <div class="lead-card" onclick="toggleLead(${startIndex + index})">
                    <div class="lead-summary">
                        <div class="lead-main">
                            <div class="lead-org">${lead.organization}</div>
                            <div class="lead-title">${lead.opportunity}</div>
                            <div class="lead-meta">
                                <span>📅 ${lead.deadline}</span>
                                <span>💰 ${lead.budget_range}</span>
                                <span>📊 ${lead.win_probability}</span>
                                <span>🤖 ${(lead.ai_confidence * 100).toFixed(0)}% confidence</span>
                            </div>
                        </div>
                        <div class="lead-badges">
                            <span class="tier-badge ${lead.tier.toLowerCase().replace(/[^a-z0-9]/g, '-')}">${lead.tier}</span>
                        </div>
                    </div>
                    
                    <div class="lead-details" id="details-${startIndex + index}">
                        <p style="color: var(--text-secondary); margin-bottom: 1rem;">${lead.description}</p>
                        
                        <div class="detail-grid">
                            <div class="detail-item">
                                <div class="detail-label">Contact</div>
                                <div>📧 ${lead.contact}</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Category</div>
                                <div>🏷️ ${lead.training_type}</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Topic</div>
                                <div>📚 ${lead.training_topic}</div>
                            </div>
                            <div class="detail-item">
                                <div class="detail-label">Organization Type</div>
                                <div>🏛️ ${lead.organization_type.charAt(0).toUpperCase() + lead.organization_type.slice(1)}</div>
                            </div>
                        </div>
                        
                        <div class="analysis-section">
                            <div class="analysis-title">Critical Analysis</div>
                            <div>${lead.critical_analysis}</div>
                        </div>
                        
                        <div class="analysis-section">
                            <div class="analysis-title">Competitive Landscape</div>
                            <div>${lead.competitive_landscape}</div>
                        </div>
                        
                        <div style="margin-top: 1rem;">
                            <a href="${lead.source}" target="_blank" class="btn btn-primary">View Details</a>
                        </div>
                    </div>
                </div>
            `).join('');
            
            // Update pagination
            updatePagination();
        }
        
        function toggleLead(index) {
            const card = event.currentTarget;
            card.classList.toggle('expanded');
        }
        
        function updatePagination() {
            const totalPages = Math.ceil(filteredLeads.length / leadsPerPage);
            const pagination = document.getElementById('pagination');
            
            let html = '';
            
            // Previous button
            if (currentPage > 1) {
                html += `<button class="page-btn" onclick="goToPage(${currentPage - 1})">Previous</button>`;
            }
            
            // Page numbers
            for (let i = 1; i <= Math.min(totalPages, 10); i++) {
                html += `<button class="page-btn ${i === currentPage ? 'active' : ''}" onclick="goToPage(${i})">${i}</button>`;
            }
            
            if (totalPages > 10) {
                html += `<span style="color: var(--text-secondary); padding: 0.5rem;">...</span>`;
                html += `<button class="page-btn ${totalPages === currentPage ? 'active' : ''}" onclick="goToPage(${totalPages})">${totalPages}</button>`;
            }
            
            // Next button
            if (currentPage < totalPages) {
                html += `<button class="page-btn" onclick="goToPage(${currentPage + 1})">Next</button>`;
            }
            
            pagination.innerHTML = html;
        }
        
        function goToPage(page) {
            currentPage = page;
            displayLeads();
            window.scrollTo(0, 0);
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    # Calculate comprehensive statistics
    stats = {
        'total': len(AI_GENERATED_LEADS),
        'urgent': len([l for l in AI_GENERATED_LEADS if 'Tier 1' in l['tier']]),
        'high_priority': len([l for l in AI_GENERATED_LEADS if 'Tier 2' in l['tier']]),
        'federal': len([l for l in AI_GENERATED_LEADS if l['organization_type'] == 'federal']),
        'total_value': sum(
            float(l['budget_range'].split('$')[1].split('M')[0].split('-')[1].strip()) 
            for l in AI_GENERATED_LEADS
        ),
        'avg_confidence': int(
            sum(l['ai_confidence'] * 100 for l in AI_GENERATED_LEADS) / len(AI_GENERATED_LEADS)
        )
    }
    
    return render_template_string(
        HTML_TEMPLATE, 
        leads_json=json.dumps(AI_GENERATED_LEADS),
        total_leads=len(AI_GENERATED_LEADS),
        stats=stats
    )

@app.route('/api/leads')
def api_leads():
    # Support filtering via query params
    org_type = request.args.get('type')
    category = request.args.get('category')
    tier = request.args.get('tier')
    search = request.args.get('search', '').lower()
    
    filtered = AI_GENERATED_LEADS
    
    if org_type and org_type != 'all':
        filtered = [l for l in filtered if l['organization_type'] == org_type]
    
    if category and category != 'all':
        filtered = [l for l in filtered if l['training_type'] == category]
    
    if tier and tier != 'all':
        filtered = [l for l in filtered if tier in l['tier'].lower()]
    
    if search:
        filtered = [l for l in filtered if search in f"{l['organization']} {l['opportunity']} {l['description']}".lower()]
    
    return jsonify({
        'leads': filtered,
        'count': len(filtered),
        'total': len(AI_GENERATED_LEADS),
        'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/stats')
def api_stats():
    # Detailed statistics
    stats = {
        'total_opportunities': len(AI_GENERATED_LEADS),
        'by_tier': {
            'tier_1': len([l for l in AI_GENERATED_LEADS if 'Tier 1' in l['tier']]),
            'tier_2': len([l for l in AI_GENERATED_LEADS if 'Tier 2' in l['tier']]),
            'tier_3': len([l for l in AI_GENERATED_LEADS if 'Tier 3' in l['tier']])
        },
        'by_type': {},
        'by_category': {},
        'total_pipeline_value': sum(
            float(l['budget_range'].split('$')[1].split('M')[0].split('-')[1].strip()) 
            for l in AI_GENERATED_LEADS
        ),
        'average_confidence': sum(l['ai_confidence'] for l in AI_GENERATED_LEADS) / len(AI_GENERATED_LEADS)
    }
    
    # Count by organization type
    for lead in AI_GENERATED_LEADS:
        org_type = lead['organization_type']
        stats['by_type'][org_type] = stats['by_type'].get(org_type, 0) + 1
        
        category = lead['training_type']
        stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
    
    return jsonify(stats)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Canadian Public Sector Lead Generation System")
    print("🤖 Comprehensive AI-Powered Lead Database")
    print("="*60)
    print(f"✅ Loaded {len(AI_GENERATED_LEADS)} opportunities!")
    print("🌐 Dashboard: http://localhost:5001")
    print("🔌 API: http://localhost:5001/api/leads")
    print("\n💡 Features:")
    print("   - Comprehensive database with 200+ opportunities")
    print("   - Advanced filtering by type, category, and tier")
    print("   - Real-time search across all fields")
    print("   - Detailed AI analysis for each opportunity")
    print("   - Sortable and paginated results")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=False)