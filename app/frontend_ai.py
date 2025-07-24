from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Canadian Public Sector Training Leads - AI-Powered Sales Intelligence</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --bg-primary: #0a0a0a;
            --bg-secondary: #141414;
            --bg-card: #1a1a1a;
            --bg-hover: #242424;
            --text-primary: #ffffff;
            --text-secondary: #a0a0a0;
            --text-dim: #666666;
            --accent-primary: #3b82f6;
            --accent-success: #10b981;
            --accent-warning: #f59e0b;
            --accent-danger: #ef4444;
            --border-color: #2a2a2a;
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
        }
        
        body { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }
        
        /* Header */
        .header {
            background: linear-gradient(180deg, var(--bg-secondary) 0%, rgba(20, 20, 20, 0.8) 100%);
            padding: 2rem;
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(10px);
        }
        
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header h1 {
            font-size: 1.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-primary) 0%, #60a5fa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .header-subtitle {
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-top: 0.25rem;
        }
        
        .ai-badge {
            background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            padding: 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            border-color: var(--accent-primary);
            transform: translateY(-2px);
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-primary) 0%, #60a5fa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-label {
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-top: 0.25rem;
        }
        
        /* Filters */
        .filters {
            padding: 0 2rem;
            max-width: 1400px;
            margin: 0 auto 2rem;
            display: flex;
            gap: 1rem;
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
            font-size: 0.9rem;
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
        
        /* Leads Container */
        .leads-container {
            padding: 0 2rem 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .lead-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
        }
        
        .lead-card:hover {
            border-color: var(--accent-primary);
            box-shadow: var(--shadow-lg);
        }
        
        .lead-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }
        
        .lead-org {
            font-size: 0.9rem;
            color: var(--accent-primary);
            margin-bottom: 0.25rem;
        }
        
        .lead-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }
        
        .lead-badges {
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }
        
        .tier-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .tier-1 { background: var(--accent-danger); color: white; }
        .tier-2 { background: var(--accent-warning); color: white; }
        .tier-3 { background: var(--accent-success); color: white; }
        
        .confidence-badge {
            background: var(--bg-secondary);
            color: var(--text-secondary);
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            border: 1px solid var(--border-color);
        }
        
        .lead-description {
            color: var(--text-secondary);
            margin-bottom: 1.5rem;
            line-height: 1.6;
        }
        
        .lead-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        
        .lead-info {
            background: var(--bg-secondary);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }
        
        .lead-info-label {
            font-size: 0.8rem;
            color: var(--text-dim);
            margin-bottom: 0.25rem;
        }
        
        .lead-info-value {
            font-size: 0.95rem;
            color: var(--text-primary);
            font-weight: 500;
        }
        
        .analysis-section {
            background: var(--bg-secondary);
            border-left: 3px solid var(--accent-primary);
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
        }
        
        .analysis-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--accent-primary);
            margin-bottom: 0.75rem;
        }
        
        .analysis-content {
            color: var(--text-secondary);
            line-height: 1.6;
        }
        
        .requirements-list {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }
        
        .requirement-tag {
            background: var(--bg-card);
            color: var(--text-secondary);
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            border: 1px solid var(--border-color);
        }
        
        .lead-actions {
            display: flex;
            gap: 1rem;
            margin-top: 1.5rem;
        }
        
        .btn {
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .btn-primary {
            background: var(--accent-primary);
            color: white;
        }
        
        .btn-primary:hover {
            background: #2563eb;
            transform: translateY(-1px);
        }
        
        .btn-secondary {
            background: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
        }
        
        .btn-secondary:hover {
            border-color: var(--accent-primary);
        }
        
        /* Loading State */
        .loading {
            text-align: center;
            padding: 4rem;
            color: var(--text-secondary);
        }
        
        .loading-spinner {
            width: 40px;
            height: 40px;
            border: 3px solid var(--border-color);
            border-top-color: var(--accent-primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                gap: 1rem;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .lead-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div>
                <h1>Canadian Public Sector Training Leads</h1>
                <p class="header-subtitle">AI-Powered Sales Intelligence Dashboard</p>
            </div>
            <div class="ai-badge">
                <span>🤖</span>
                <span>AI Search Active</span>
            </div>
        </div>
    </header>
    
    <div class="stats-grid" id="stats-grid">
        <div class="stat-card">
            <div class="stat-value" id="total-leads">0</div>
            <div class="stat-label">Total Opportunities</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="urgent-leads">0</div>
            <div class="stat-label">Urgent (Tier 1)</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="total-value">$0M</div>
            <div class="stat-label">Total Pipeline Value</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="last-update">--:--</div>
            <div class="stat-label">Last AI Search</div>
        </div>
    </div>
    
    <div class="filters">
        <button class="filter-btn active" onclick="filterLeads('all')">All Leads</button>
        <button class="filter-btn" onclick="filterLeads('tier-1')">Tier 1 - Urgent</button>
        <button class="filter-btn" onclick="filterLeads('tier-2')">Tier 2 - High Priority</button>
        <button class="filter-btn" onclick="filterLeads('federal')">Federal</button>
        <button class="filter-btn" onclick="filterLeads('provincial')">Provincial</button>
        <button class="filter-btn" onclick="filterLeads('municipal')">Municipal</button>
    </div>
    
    <div class="leads-container" id="leads-container">
        <div class="loading">
            <div class="loading-spinner"></div>
            <p>AI is searching for opportunities...</p>
        </div>
    </div>
    
    <script>
        let allLeads = [];
        let currentFilter = 'all';
        
        async function loadLeads() {
            try {
                const response = await fetch('http://localhost:5000/api/leads');
                const data = await response.json();
                
                allLeads = data.leads || [];
                updateStats(data);
                displayLeads();
                
            } catch (error) {
                console.error('Error loading leads:', error);
                document.getElementById('leads-container').innerHTML = 
                    '<div class="error">Error loading leads. Please refresh.</div>';
            }
        }
        
        async function loadStats() {
            try {
                const response = await fetch('http://localhost:5000/api/stats');
                const stats = await response.json();
                
                document.getElementById('total-leads').textContent = stats.total_leads || 0;
                document.getElementById('urgent-leads').textContent = stats.urgent_leads || 0;
                document.getElementById('total-value').textContent = `$${stats.total_value?.toFixed(1) || 0}M`;
                
            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }
        
        function updateStats(data) {
            document.getElementById('last-update').textContent = 
                data.last_update ? new Date(data.last_update).toLocaleTimeString() : '--:--';
        }
        
        function filterLeads(filter) {
            currentFilter = filter;
            
            // Update active button
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            displayLeads();
        }
        
        function displayLeads() {
            const container = document.getElementById('leads-container');
            
            let filteredLeads = allLeads;
            
            if (currentFilter === 'tier-1') {
                filteredLeads = allLeads.filter(l => l.tier?.includes('Tier 1'));
            } else if (currentFilter === 'tier-2') {
                filteredLeads = allLeads.filter(l => l.tier?.includes('Tier 2'));
            } else if (currentFilter === 'federal') {
                filteredLeads = allLeads.filter(l => l.organization?.includes('Government of Canada'));
            } else if (currentFilter === 'provincial') {
                filteredLeads = allLeads.filter(l => 
                    ['Ontario', 'British Columbia', 'Alberta', 'Quebec'].some(prov => 
                        l.organization?.includes(prov)
                    )
                );
            } else if (currentFilter === 'municipal') {
                filteredLeads = allLeads.filter(l => 
                    l.organization?.includes('City') || l.organization?.includes('Municipal')
                );
            }
            
            if (filteredLeads.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No leads match the selected filter.</p>';
                return;
            }
            
            container.innerHTML = filteredLeads.map(lead => `
                <div class="lead-card">
                    <div class="lead-header">
                        <div>
                            <div class="lead-org">${lead.organization}</div>
                            <h2 class="lead-title">${lead.opportunity}</h2>
                        </div>
                        <div class="lead-badges">
                            <span class="tier-badge ${lead.tier?.toLowerCase().replace(/[^a-z0-9]/g, '-')}">${lead.tier}</span>
                            ${lead.ai_confidence ? `<span class="confidence-badge">AI: ${(lead.ai_confidence * 100).toFixed(0)}%</span>` : ''}
                        </div>
                    </div>
                    
                    <p class="lead-description">${lead.description}</p>
                    
                    <div class="lead-grid">
                        <div class="lead-info">
                            <div class="lead-info-label">Deadline</div>
                            <div class="lead-info-value">📅 ${lead.deadline}</div>
                        </div>
                        <div class="lead-info">
                            <div class="lead-info-label">Budget Range</div>
                            <div class="lead-info-value">💰 ${lead.budget_range}</div>
                        </div>
                        <div class="lead-info">
                            <div class="lead-info-label">Contact</div>
                            <div class="lead-info-value">📧 ${lead.contact}</div>
                        </div>
                        <div class="lead-info">
                            <div class="lead-info-label">Win Probability</div>
                            <div class="lead-info-value">📊 ${lead.win_probability || 'TBD'}</div>
                        </div>
                    </div>
                    
                    <div class="analysis-section">
                        <h3 class="analysis-title">Critical Analysis</h3>
                        <p class="analysis-content">${lead.critical_analysis}</p>
                    </div>
                    
                    ${lead.competitive_landscape ? `
                        <div class="analysis-section">
                            <h3 class="analysis-title">Competitive Landscape</h3>
                            <p class="analysis-content">${lead.competitive_landscape}</p>
                        </div>
                    ` : ''}
                    
                    ${lead.key_requirements && lead.key_requirements.length > 0 ? `
                        <div class="analysis-section">
                            <h3 class="analysis-title">Key Requirements</h3>
                            <div class="requirements-list">
                                ${lead.key_requirements.map(req => 
                                    `<span class="requirement-tag">${req}</span>`
                                ).join('')}
                            </div>
                        </div>
                    ` : ''}
                    
                    ${lead.next_steps && lead.next_steps.length > 0 ? `
                        <div class="analysis-section">
                            <h3 class="analysis-title">Recommended Next Steps</h3>
                            <ol style="margin-left: 1.5rem; color: var(--text-secondary);">
                                ${lead.next_steps.map(step => `<li>${step}</li>`).join('')}
                            </ol>
                        </div>
                    ` : ''}
                    
                    <div class="lead-actions">
                        <a href="${lead.source}" target="_blank" class="btn btn-primary">
                            <span>🔗</span>
                            <span>View Source</span>
                        </a>
                        <button class="btn btn-secondary" onclick="alert('Contact: ${lead.contact}\\n\\nDecision Makers:\\n${(lead.decision_makers || []).join('\\n')}')">
                            <span>👥</span>
                            <span>View Contacts</span>
                        </button>
                    </div>
                </div>
            `).join('');
        }
        
        // Load data on page load
        loadLeads();
        loadStats();
        
        // Refresh every 5 minutes
        setInterval(() => {
            loadLeads();
            loadStats();
        }, 300000);
        
        // Add refresh functionality
        document.addEventListener('keydown', (e) => {
            if (e.key === 'r' && e.ctrlKey) {
                e.preventDefault();
                loadLeads();
                loadStats();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎯 Canadian Public Sector Lead Generation Frontend")
    print("🤖 AI-Powered Sales Intelligence Dashboard")
    print("="*60)
    print("✅ Starting frontend server...")
    print("🌐 Dashboard: http://localhost:5001")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=False)