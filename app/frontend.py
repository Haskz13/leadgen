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
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
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
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(10px);
        }
        
        .header-content {
            max-width: 1600px;
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
            font-size: 1.75rem;
            font-weight: 700;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.02em;
        }
        
        .logo-subtitle {
            color: var(--text-secondary);
            font-size: 0.875rem;
            font-weight: 400;
        }
        
        /* Stats Cards */
        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.25rem;
            max-width: 1600px;
            margin: 2rem auto;
            padding: 0 2rem;
        }
        
        .stat-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.75rem;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--accent-primary), transparent);
            transform: translateX(-100%);
            transition: transform 0.6s ease;
        }
        
        .stat-card:hover::before {
            transform: translateX(100%);
        }
        
        .stat-card:hover {
            transform: translateY(-2px);
            border-color: var(--accent-primary);
            box-shadow: var(--shadow-lg);
        }
        
        .stat-icon {
            width: 40px;
            height: 40px;
            background: rgba(59, 130, 246, 0.1);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1rem;
            font-size: 1.25rem;
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
            letter-spacing: -0.02em;
        }
        
        .stat-label {
            color: var(--text-secondary);
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 500;
        }
        
        .tier-1 { color: var(--accent-danger); }
        .tier-2 { color: var(--accent-warning); }
        .tier-3 { color: var(--accent-success); }
        
        /* Filters */
        .filters-container {
            max-width: 1600px;
            margin: 0 auto 2rem;
            padding: 0 2rem;
        }
        
        .filters {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.75rem;
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
            padding: 0.875rem 1rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 10px;
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
            padding: 0.875rem 1.5rem;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 0.875rem;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            letter-spacing: 0.01em;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, var(--accent-primary), #2563eb);
            color: white;
            box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);
        }
        
        .btn-primary:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 8px -1px rgba(59, 130, 246, 0.4);
        }
        
        .btn-secondary {
            background: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
        }
        
        .btn-secondary:hover {
            background: var(--bg-hover);
            border-color: var(--accent-primary);
        }
        
        /* Main Content */
        .main-container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 0 2rem 2rem;
        }
        
        /* Lead Cards */
        .leads-grid {
            display: grid;
            gap: 1.25rem;
        }
        
        .lead-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.75rem;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .lead-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: transparent;
            transition: background 0.3s ease;
        }
        
        .lead-card:hover {
            background: var(--bg-hover);
            transform: translateX(4px);
            box-shadow: var(--shadow-lg);
        }
        
        .lead-card.tier-1::after { background: var(--accent-danger); }
        .lead-card.tier-2::after { background: var(--accent-warning); }
        .lead-card.tier-3::after { background: var(--accent-success); }
        
        .lead-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 1.25rem;
            gap: 1rem;
        }
        
        .lead-org {
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
            line-height: 1.3;
        }
        
        .lead-title {
            color: var(--accent-primary);
            font-size: 0.9375rem;
            margin-bottom: 1.25rem;
            line-height: 1.5;
            font-weight: 500;
        }
        
        .lead-link {
            color: var(--accent-primary);
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            font-size: 0.875rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .lead-link:hover {
            text-decoration: underline;
            gap: 0.5rem;
        }
        
        .lead-meta {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1.25rem;
            margin-bottom: 1.25rem;
        }
        
        .meta-item {
            display: flex;
            flex-direction: column;
            gap: 0.375rem;
        }
        
        .meta-label {
            color: var(--text-dim);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
        }
        
        .meta-value {
            color: var(--text-secondary);
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        .tier-badge {
            display: inline-block;
            padding: 0.375rem 0.875rem;
            border-radius: 24px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            white-space: nowrap;
        }
        
        .tier-badge.urgent {
            background: rgba(239, 68, 68, 0.15);
            color: var(--accent-danger);
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        
        .tier-badge.high {
            background: rgba(245, 158, 11, 0.15);
            color: var(--accent-warning);
            border: 1px solid rgba(245, 158, 11, 0.3);
        }
        
        .tier-badge.standard {
            background: rgba(16, 185, 129, 0.15);
            color: var(--accent-success);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        
        .lead-analysis {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(139, 92, 246, 0.05));
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1.25rem;
        }
        
        .analysis-title {
            color: var(--accent-primary);
            font-size: 0.8125rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.75rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .analysis-content {
            color: var(--text-primary);
            font-size: 0.9375rem;
            line-height: 1.6;
        }
        
        .lead-description {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1.25rem;
        }
        
        .description-title {
            color: var(--text-secondary);
            font-size: 0.8125rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.75rem;
            font-weight: 600;
        }
        
        .description-content {
            color: var(--text-primary);
            font-size: 0.875rem;
            line-height: 1.6;
        }
        
        .lead-actions {
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
            align-items: center;
        }
        
        .lead-status {
            flex: 1;
            min-width: 140px;
        }
        
        .status-select {
            width: 100%;
            padding: 0.625rem 0.875rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-primary);
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        .notes-input {
            width: 100%;
            padding: 0.875rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            color: var(--text-primary);
            font-size: 0.875rem;
            resize: vertical;
            min-height: 80px;
            margin-top: 0.75rem;
            font-family: inherit;
            line-height: 1.5;
        }
        
        /* Loading State */
        .loading {
            text-align: center;
            padding: 6rem 2rem;
            color: var(--text-secondary);
        }
        
        .loading-spinner {
            display: inline-block;
            width: 48px;
            height: 48px;
            border: 3px solid var(--border-color);
            border-top-color: var(--accent-primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 1.5rem;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 6rem 2rem;
            color: var(--text-secondary);
        }
        
        .empty-state h3 {
            font-size: 1.75rem;
            margin-bottom: 1rem;
            color: var(--text-primary);
            font-weight: 600;
        }
        
        .empty-state p {
            font-size: 1.125rem;
            line-height: 1.6;
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
            
            .lead-header {
                flex-direction: column;
            }
            
            .stats-container {
                grid-template-columns: 1fr 1fr;
            }
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .lead-card {
            animation: fadeIn 0.3s ease-out;
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="logo">
                <div>
                    <h1>LeadGen Intelligence</h1>
                    <div class="logo-subtitle">Canadian Public Sector Training Opportunities</div>
                </div>
            </div>
            <div style="display: flex; gap: 1rem; align-items: center;">
                <span style="color: var(--text-dim); font-size: 0.875rem;" id="last-update"></span>
                <button class="btn btn-primary" onclick="refreshLeads()">
                    <span>🔄</span> Refresh Leads
                </button>
            </div>
        </div>
    </header>
    
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-value" id="total-leads">0</div>
            <div class="stat-label">Total Opportunities</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon" style="background: rgba(239, 68, 68, 0.1);">🔴</div>
            <div class="stat-value tier-1" id="urgent-leads">0</div>
            <div class="stat-label">Urgent (< 30 days)</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon" style="background: rgba(245, 158, 11, 0.1);">🟡</div>
            <div class="stat-value tier-2" id="high-leads">0</div>
            <div class="stat-label">High Priority</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon" style="background: rgba(16, 185, 129, 0.1);">🟢</div>
            <div class="stat-value tier-3" id="standard-leads">0</div>
            <div class="stat-label">Standard</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon" style="background: rgba(59, 130, 246, 0.1);">✨</div>
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
                    <option value="Federal Government">Federal Government</option>
                    <option value="Provincial Government">Provincial Government</option>
                    <option value="Municipal">Municipal</option>
                    <option value="Digital Transformation">Digital Transformation</option>
                    <option value="Grant Recipients">Grant Recipients</option>
                    <option value="Indigenous">Indigenous Initiatives</option>
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
            <p style="margin-top: 1rem; font-size: 1.125rem;">Searching for training opportunities...</p>
            <p style="margin-top: 0.5rem; color: var(--text-dim);">This may take a moment as we search across Canadian government sources</p>
        </div>
        
        <div id="empty-state" class="empty-state" style="display: none;">
            <h3>No training opportunities found</h3>
            <p>Try adjusting your filters or refresh to search again.</p>
            <p style="margin-top: 1rem; color: var(--text-dim);">The system searches real Canadian government sources only.</p>
        </div>
        
        <div id="leads-container" class="leads-grid" style="display: none;">
        </div>
    </div>
    
    <script>
        let allLeads = [];
        let leadStatuses = JSON.parse(localStorage.getItem('leadStatuses') || '{}');
        let leadNotes = JSON.parse(localStorage.getItem('leadNotes') || '{}');
        
        function formatLeadCard(lead) {
            const status = leadStatuses[lead.opportunity] || lead.status;
            const notes = leadNotes[lead.opportunity] || '';
            const tierClass = lead.tier.includes('Tier 1') ? 'urgent' : 
                             lead.tier.includes('Tier 2') ? 'high' : 'standard';
            const cardTierClass = lead.tier.includes('Tier 1') ? 'tier-1' : 
                                 lead.tier.includes('Tier 2') ? 'tier-2' : 'tier-3';
            
            const criticalAnalysis = lead.critical_analysis || 'Standard professional development opportunity';
            
            // Format deadline nicely
            const deadlineDate = new Date(lead.deadline);
            const formattedDeadline = deadlineDate.toLocaleDateString('en-CA', { 
                year: 'numeric', 
                month: 'short', 
                day: 'numeric' 
            });
            
            // Calculate days until deadline
            const today = new Date();
            const daysUntil = Math.ceil((deadlineDate - today) / (1000 * 60 * 60 * 24));
            const daysText = daysUntil > 0 ? `${daysUntil} days` : 'Overdue';
            
            return `
                <div class="lead-card ${cardTierClass}">
                    <div class="lead-header">
                        <div style="flex: 1;">
                            <div class="lead-org">${lead.organization}</div>
                            <div class="lead-title">${lead.opportunity}</div>
                        </div>
                        <span class="tier-badge ${tierClass}">${lead.tier}</span>
                    </div>
                    
                    <div class="lead-meta">
                        <div class="meta-item">
                            <span class="meta-label">Deadline</span>
                            <span class="meta-value">${formattedDeadline} (${daysText})</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Type</span>
                            <span class="meta-value">${lead.opportunity_type || 'General'}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Category</span>
                            <span class="meta-value">${lead.search_type || 'General'}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Contact</span>
                            <span class="meta-value">${lead.contact}</span>
                        </div>
                    </div>
                    
                    ${criticalAnalysis !== 'Standard professional development opportunity' ? `
                    <div class="lead-analysis">
                        <div class="analysis-title">
                            <span>🎯</span> Critical Sales Analysis
                        </div>
                        <div class="analysis-content">${criticalAnalysis}</div>
                    </div>
                    ` : ''}
                    
                    ${lead.notes ? `
                    <div class="lead-description">
                        <div class="description-title">Description</div>
                        <div class="description-content">${lead.notes}</div>
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
                              placeholder="Add notes, next steps, key contacts, proposal ideas..." 
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
                    '<p style="color: var(--accent-danger); font-size: 1.125rem;">⚠️ Error loading leads</p>' +
                    '<p style="margin-top: 0.5rem;">Please check if the backend is running on port 5000</p>';
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
                document.getElementById('loading').innerHTML = 
                    '<p style="color: var(--accent-danger);">⚠️ Error refreshing leads</p>';
            }
        }
        
        function exportLeads() {
            const filteredLeads = allLeads.map(lead => ({
                ...lead,
                status: leadStatuses[lead.opportunity] || lead.status,
                notes: leadNotes[lead.opportunity] || lead.notes || ''
            }));
            
            const csv = [
                ['Organization', 'Opportunity', 'Type', 'Category', 'Deadline', 'Days Until', 'Tier', 'Contact', 'Source', 'Status', 'Critical Analysis', 'Notes'],
                ...filteredLeads.map(lead => {
                    const deadlineDate = new Date(lead.deadline);
                    const daysUntil = Math.ceil((deadlineDate - new Date()) / (1000 * 60 * 60 * 24));
                    
                    return [
                        lead.organization,
                        lead.opportunity,
                        lead.opportunity_type || 'General',
                        lead.search_type || 'General',
                        lead.deadline,
                        daysUntil,
                        lead.tier,
                        lead.contact,
                        lead.source,
                        lead.status,
                        lead.critical_analysis || 'Standard professional development opportunity',
                        lead.notes
                    ];
                })
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