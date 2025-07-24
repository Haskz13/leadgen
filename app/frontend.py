from flask import Flask, render_template_string, jsonify, request
import requests
import json
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Canadian Public Sector Training Leads - Sales Intelligence Dashboard</title>
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
        }
        
        body { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
            background: var(--bg-primary); 
            color: var(--text-primary);
            line-height: 1.6;
        }
        
        /* Header */
        .header {
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 1.5rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .logo h1 {
            font-size: 1.5rem;
            font-weight: 600;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Stats Cards */
        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 2rem;
        }
        
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            border-color: var(--accent-primary);
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            color: var(--text-secondary);
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .tier-1 { color: var(--accent-danger); }
        .tier-2 { color: var(--accent-warning); }
        .tier-3 { color: var(--accent-success); }
        
        /* Filters */
        .filters-container {
            max-width: 1400px;
            margin: 0 auto 2rem;
            padding: 0 2rem;
        }
        
        .filters {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            align-items: end;
        }
        
        .filter-group {
            flex: 1;
            min-width: 200px;
        }
        
        .filter-label {
            display: block;
            color: var(--text-secondary);
            font-size: 0.875rem;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        .filter-input {
            width: 100%;
            padding: 0.75rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-primary);
            font-size: 0.875rem;
            transition: all 0.2s ease;
        }
        
        .filter-input:focus {
            outline: none;
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 8px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 0.875rem;
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
            background: transparent;
            color: var(--text-secondary);
            border: 1px solid var(--border-color);
        }
        
        .btn-secondary:hover {
            background: var(--bg-hover);
            color: var(--text-primary);
        }
        
        /* Main Content */
        .main-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 2rem 2rem;
        }
        
        /* Lead Cards */
        .leads-grid {
            display: grid;
            gap: 1rem;
        }
        
        .lead-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .lead-card:hover {
            background: var(--bg-hover);
            transform: translateX(4px);
        }
        
        .lead-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 1rem;
        }
        
        .lead-org {
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.25rem;
        }
        
        .lead-title {
            color: var(--accent-primary);
            font-size: 0.875rem;
            margin-bottom: 1rem;
            line-height: 1.5;
        }
        
        .lead-meta {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .meta-item {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }
        
        .meta-label {
            color: var(--text-dim);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .meta-value {
            color: var(--text-secondary);
            font-size: 0.875rem;
        }
        
        .tier-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .tier-badge.urgent {
            background: rgba(239, 68, 68, 0.2);
            color: #ef4444;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        
        .tier-badge.high {
            background: rgba(245, 158, 11, 0.2);
            color: #f59e0b;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }
        
        .tier-badge.standard {
            background: rgba(16, 185, 129, 0.2);
            color: #10b981;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        
        .lead-analysis {
            background: var(--bg-secondary);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .analysis-title {
            color: var(--text-secondary);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }
        
        .analysis-content {
            color: var(--text-primary);
            font-size: 0.875rem;
            line-height: 1.5;
        }
        
        .lead-actions {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        
        .lead-status {
            flex: 1;
            min-width: 120px;
        }
        
        .status-select {
            width: 100%;
            padding: 0.5rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-primary);
            font-size: 0.875rem;
        }
        
        .lead-link {
            text-decoration: none;
            color: var(--accent-primary);
            font-size: 0.875rem;
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
        }
        
        .lead-link:hover {
            text-decoration: underline;
        }
        
        .notes-input {
            width: 100%;
            padding: 0.75rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: var(--text-primary);
            font-size: 0.875rem;
            resize: vertical;
            min-height: 60px;
            margin-top: 0.5rem;
        }
        
        /* Loading State */
        .loading {
            text-align: center;
            padding: 4rem;
            color: var(--text-secondary);
        }
        
        .loading-spinner {
            display: inline-block;
            width: 40px;
            height: 40px;
            border: 3px solid var(--border-color);
            border-top-color: var(--accent-primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 4rem;
            color: var(--text-secondary);
        }
        
        .empty-state h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                gap: 1rem;
            }
            
            .filters {
                flex-direction: column;
            }
            
            .filter-group {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="logo">
                <h1>LeadGen Pro</h1>
                <span style="color: var(--text-secondary); font-size: 0.875rem;">Canadian Public Sector Training Intelligence</span>
            </div>
            <div style="display: flex; gap: 1rem; align-items: center;">
                <span style="color: var(--text-dim); font-size: 0.875rem;" id="last-update"></span>
                <button class="btn btn-primary" onclick="refreshLeads()">
                    <span>↻</span> Refresh
                </button>
            </div>
        </div>
    </header>
    
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-value" id="total-leads">0</div>
            <div class="stat-label">Total Opportunities</div>
        </div>
        <div class="stat-card">
            <div class="stat-value tier-1" id="urgent-leads">0</div>
            <div class="stat-label">Urgent (< 30 days)</div>
        </div>
        <div class="stat-card">
            <div class="stat-value tier-2" id="high-leads">0</div>
            <div class="stat-label">High Priority</div>
        </div>
        <div class="stat-card">
            <div class="stat-value tier-3" id="standard-leads">0</div>
            <div class="stat-label">Standard</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" style="color: var(--accent-primary);" id="new-leads">0</div>
            <div class="stat-label">New Leads</div>
        </div>
    </div>
    
    <div class="filters-container">
        <div class="filters">
            <div class="filter-group">
                <label class="filter-label">Search Type</label>
                <select class="filter-input" id="type-filter">
                    <option value="">All Types</option>
                    <option value="Grant Recipients">Grant Recipients</option>
                    <option value="Digital Transformations">Digital Transformations</option>
                    <option value="Compliance & Mandates">Compliance & Mandates</option>
                    <option value="Municipal Programs">Municipal Programs</option>
                    <option value="Healthcare & Education">Healthcare & Education</option>
                    <option value="Indigenous Initiatives">Indigenous Initiatives</option>
                </select>
            </div>
            <div class="filter-group">
                <label class="filter-label">Urgency Tier</label>
                <select class="filter-input" id="tier-filter">
                    <option value="">All Tiers</option>
                    <option value="Tier 1">Tier 1 - Urgent</option>
                    <option value="Tier 2">Tier 2 - High Priority</option>
                    <option value="Tier 3">Tier 3 - Standard</option>
                </select>
            </div>
            <div class="filter-group">
                <label class="filter-label">Status</label>
                <select class="filter-input" id="status-filter">
                    <option value="">All Status</option>
                    <option value="New">New</option>
                    <option value="Contacted">Contacted</option>
                    <option value="In Progress">In Progress</option>
                    <option value="Qualified">Qualified</option>
                    <option value="Proposal Sent">Proposal Sent</option>
                    <option value="Closed Won">Closed Won</option>
                    <option value="Closed Lost">Closed Lost</option>
                </select>
            </div>
            <div class="filter-group">
                <label class="filter-label">Organization</label>
                <input type="text" class="filter-input" id="org-filter" placeholder="Search organization...">
            </div>
            <button class="btn btn-secondary" onclick="exportLeads()">
                <span>📥</span> Export CSV
            </button>
        </div>
    </div>
    
    <div class="main-container">
        <div id="loading" class="loading">
            <div class="loading-spinner"></div>
            <p style="margin-top: 1rem;">Searching for training opportunities...</p>
        </div>
        
        <div id="empty-state" class="empty-state" style="display: none;">
            <h3>No leads found</h3>
            <p>Try adjusting your filters or refresh to search again.</p>
        </div>
        
        <div id="leads-container" class="leads-grid" style="display: none;">
        </div>
    </div>
    
    <script>
        let allLeads = [];
        let leadStatuses = JSON.parse(localStorage.getItem('leadStatuses') || '{}');
        let leadNotes = JSON.parse(localStorage.getItem('leadNotes') || '{}');
        
        function generateLeadAnalysis(lead) {
            // Generate intelligent analysis based on lead data
            let analysis = [];
            
            // Analyze organization size/impact
            if (lead.organization.includes('Canada') || lead.organization.includes('Federal')) {
                analysis.push("Federal level opportunity - potential for large-scale contract and repeat business across departments.");
            } else if (lead.organization.includes('Ontario') || lead.organization.includes('Toronto')) {
                analysis.push("Provincial/municipal opportunity - good for establishing regional presence.");
            }
            
            // Analyze urgency
            const deadline = new Date(lead.deadline);
            const daysUntil = Math.ceil((deadline - new Date()) / (1000 * 60 * 60 * 24));
            if (daysUntil <= 30) {
                analysis.push(`URGENT: Only ${daysUntil} days until deadline. Immediate action required.`);
            }
            
            // Analyze opportunity type
            if (lead.opportunity.toLowerCase().includes('digital transformation')) {
                analysis.push("Digital transformation project - likely needs change management and technical training.");
            }
            if (lead.opportunity.toLowerCase().includes('compliance') || lead.opportunity.toLowerCase().includes('mandatory')) {
                analysis.push("Compliance/mandatory training - high close probability as training is required by law.");
            }
            
            return analysis.join(" ");
        }
        
        function formatLeadCard(lead) {
            const status = leadStatuses[lead.opportunity] || lead.status;
            const notes = leadNotes[lead.opportunity] || '';
            const tierClass = lead.tier.includes('Tier 1') ? 'urgent' : 
                             lead.tier.includes('Tier 2') ? 'high' : 'standard';
            
            const analysis = generateLeadAnalysis(lead);
            
            return `
                <div class="lead-card">
                    <div class="lead-header">
                        <div>
                            <div class="lead-org">${lead.organization}</div>
                            <div class="lead-title">${lead.opportunity}</div>
                        </div>
                        <span class="tier-badge ${tierClass}">${lead.tier}</span>
                    </div>
                    
                    <div class="lead-meta">
                        <div class="meta-item">
                            <span class="meta-label">Deadline</span>
                            <span class="meta-value">${new Date(lead.deadline).toLocaleDateString('en-CA', { 
                                year: 'numeric', 
                                month: 'short', 
                                day: 'numeric' 
                            })}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Type</span>
                            <span class="meta-value">${lead.search_type || 'General'}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Contact</span>
                            <span class="meta-value">${lead.contact}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Found</span>
                            <span class="meta-value">${lead.date_found}</span>
                        </div>
                    </div>
                    
                    ${analysis ? `
                    <div class="lead-analysis">
                        <div class="analysis-title">Sales Intelligence</div>
                        <div class="analysis-content">${analysis}</div>
                    </div>
                    ` : ''}
                    
                    <div class="lead-actions">
                        <div class="lead-status">
                            <select class="status-select" onchange="updateStatus('${lead.opportunity}', this.value)">
                                <option value="New" ${status === 'New' ? 'selected' : ''}>New</option>
                                <option value="Contacted" ${status === 'Contacted' ? 'selected' : ''}>Contacted</option>
                                <option value="In Progress" ${status === 'In Progress' ? 'selected' : ''}>In Progress</option>
                                <option value="Qualified" ${status === 'Qualified' ? 'selected' : ''}>Qualified</option>
                                <option value="Proposal Sent" ${status === 'Proposal Sent' ? 'selected' : ''}>Proposal Sent</option>
                                <option value="Closed Won" ${status === 'Closed Won' ? 'selected' : ''}>Closed Won</option>
                                <option value="Closed Lost" ${status === 'Closed Lost' ? 'selected' : ''}>Closed Lost</option>
                            </select>
                        </div>
                        <a href="${lead.source}" target="_blank" class="lead-link">
                            View Source →
                        </a>
                    </div>
                    
                    <textarea class="notes-input" 
                              placeholder="Add notes, next steps, contact details..." 
                              onblur="updateNotes('${lead.opportunity}', this.value)">${notes}</textarea>
                </div>
            `;
        }
        
        async function loadLeads() {
            try {
                const response = await fetch('http://localhost:5000/api/leads');
                const data = await response.json();
                allLeads = data.leads || [];
                
                document.getElementById('last-update').textContent = 
                    data.last_update ? `Last updated: ${data.last_update}` : '';
                
                updateStats();
                displayLeads();
                
                document.getElementById('loading').style.display = 'none';
                if (allLeads.length === 0) {
                    document.getElementById('empty-state').style.display = 'block';
                    document.getElementById('leads-container').style.display = 'none';
                } else {
                    document.getElementById('empty-state').style.display = 'none';
                    document.getElementById('leads-container').style.display = 'grid';
                }
            } catch (error) {
                console.error('Error loading leads:', error);
                document.getElementById('loading').innerHTML = 
                    '<p style="color: var(--accent-danger);">Error loading leads. Please check if the backend is running.</p>';
            }
        }
        
        function updateStats() {
            const total = allLeads.length;
            const urgent = allLeads.filter(l => l.tier.includes('Tier 1')).length;
            const high = allLeads.filter(l => l.tier.includes('Tier 2')).length;
            const standard = allLeads.filter(l => l.tier.includes('Tier 3')).length;
            const newLeads = allLeads.filter(l => 
                (leadStatuses[l.opportunity] || l.status) === 'New'
            ).length;
            
            document.getElementById('total-leads').textContent = total;
            document.getElementById('urgent-leads').textContent = urgent;
            document.getElementById('high-leads').textContent = high;
            document.getElementById('standard-leads').textContent = standard;
            document.getElementById('new-leads').textContent = newLeads;
        }
        
        function displayLeads() {
            const container = document.getElementById('leads-container');
            const typeFilter = document.getElementById('type-filter').value;
            const tierFilter = document.getElementById('tier-filter').value;
            const statusFilter = document.getElementById('status-filter').value;
            const orgFilter = document.getElementById('org-filter').value.toLowerCase();
            
            const filteredLeads = allLeads.filter(lead => {
                if (typeFilter && lead.search_type !== typeFilter) return false;
                if (tierFilter && !lead.tier.includes(tierFilter)) return false;
                if (statusFilter && (leadStatuses[lead.opportunity] || lead.status) !== statusFilter) return false;
                if (orgFilter && !lead.organization.toLowerCase().includes(orgFilter)) return false;
                return true;
            });
            
            container.innerHTML = filteredLeads.map(lead => formatLeadCard(lead)).join('');
            
            if (filteredLeads.length === 0 && allLeads.length > 0) {
                container.innerHTML = '<div class="empty-state"><p>No leads match your filters.</p></div>';
            }
        }
        
        function updateStatus(opportunity, status) {
            leadStatuses[opportunity] = status;
            localStorage.setItem('leadStatuses', JSON.stringify(leadStatuses));
            updateStats();
        }
        
        function updateNotes(opportunity, notes) {
            leadNotes[opportunity] = notes;
            localStorage.setItem('leadNotes', JSON.stringify(leadNotes));
        }
        
        async function refreshLeads() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('leads-container').style.display = 'none';
            document.getElementById('empty-state').style.display = 'none';
            
            try {
                await fetch('http://localhost:5000/api/refresh');
                await loadLeads();
            } catch (error) {
                console.error('Error refreshing leads:', error);
            }
        }
        
        function exportLeads() {
            const filteredLeads = allLeads.map(lead => ({
                ...lead,
                status: leadStatuses[lead.opportunity] || lead.status,
                notes: leadNotes[lead.opportunity] || lead.notes || ''
            }));
            
            const csv = [
                ['Organization', 'Opportunity', 'Type', 'Deadline', 'Tier', 'Contact', 'Source', 'Status', 'Notes', 'Analysis'],
                ...filteredLeads.map(lead => [
                    lead.organization,
                    lead.opportunity,
                    lead.search_type || 'General',
                    lead.deadline,
                    lead.tier,
                    lead.contact,
                    lead.source,
                    lead.status,
                    lead.notes,
                    generateLeadAnalysis(lead)
                ])
            ].map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(',')).join('\\n');
            
            const blob = new Blob([csv], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `training-leads-${new Date().toISOString().split('T')[0]}.csv`;
            a.click();
        }
        
        // Event listeners
        document.getElementById('type-filter').addEventListener('change', displayLeads);
        document.getElementById('tier-filter').addEventListener('change', displayLeads);
        document.getElementById('status-filter').addEventListener('change', displayLeads);
        document.getElementById('org-filter').addEventListener('input', displayLeads);
        
        // Load leads on page load
        loadLeads();
        
        // Auto-refresh every 10 minutes
        setInterval(loadLeads, 10 * 60 * 1000);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(port=5001, debug=True)