from flask import Flask, render_template_string, jsonify, request
import requests
import json

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Canadian Public Sector Training Leads - Sales Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            background: #f0f2f5; 
            color: #333;
        }
        .header {
            background: #1a237e;
            color: white;
            padding: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 { font-size: 24px; font-weight: 500; }
        .stats {
            display: flex;
            gap: 30px;
            font-size: 14px;
        }
        .stat-item {
            text-align: center;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            display: block;
        }
        .container { 
            max-width: 1200px; 
            margin: 20px auto; 
            padding: 0 20px;
        }
        .filters {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            display: flex;
            gap: 15px;
            align-items: center;
            flex-wrap: wrap;
        }
        .filter-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        .filter-group label {
            font-size: 12px;
            color: #666;
            font-weight: 500;
        }
        select, input {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        .btn {
            background: #1a237e;
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
        }
        .btn:hover { background: #283593; }
        .btn-secondary {
            background: #fff;
            color: #1a237e;
            border: 1px solid #1a237e;
        }
        .btn-secondary:hover { background: #f5f5f5; }
        .leads-table {
            background: white;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        table { 
            width: 100%; 
            border-collapse: collapse; 
        }
        th { 
            background: #f8f9fa; 
            color: #333;
            font-weight: 600;
            text-align: left;
            padding: 15px;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 2px solid #e0e0e0;
        }
        td { 
            padding: 15px;
            border-bottom: 1px solid #f0f0f0;
            font-size: 14px;
        }
        tr:hover { background: #f8f9fa; }
        .tier-1 { 
            background: #d32f2f; 
            color: white; 
            padding: 4px 8px; 
            border-radius: 4px; 
            font-size: 12px;
            font-weight: 500;
        }
        .tier-2 { 
            background: #f57c00; 
            color: white; 
            padding: 4px 8px; 
            border-radius: 4px; 
            font-size: 12px;
            font-weight: 500;
        }
        .tier-3 { 
            background: #388e3c; 
            color: white; 
            padding: 4px 8px; 
            border-radius: 4px; 
            font-size: 12px;
            font-weight: 500;
        }
        .status-new { color: #1976d2; font-weight: 500; }
        .status-contacted { color: #f57c00; font-weight: 500; }
        .status-in-progress { color: #388e3c; font-weight: 500; }
        .status-closed { color: #616161; font-weight: 500; }
        .opportunity { 
            max-width: 400px; 
            line-height: 1.4;
        }
        .notes-input {
            width: 100%;
            padding: 4px 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 13px;
        }
        .action-buttons {
            display: flex;
            gap: 5px;
        }
        .btn-small {
            padding: 4px 8px;
            font-size: 12px;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        .last-update {
            text-align: right;
            font-size: 12px;
            color: #666;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <h1>🎯 Canadian Public Sector Training Leads</h1>
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-value" id="total-leads">0</span>
                    <span>Total Leads</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value" id="urgent-leads">0</span>
                    <span>Urgent</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value" id="new-leads">0</span>
                    <span>New</span>
                </div>
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="filters">
            <div class="filter-group">
                <label>Tier</label>
                <select id="tier-filter">
                    <option value="">All Tiers</option>
                    <option value="Tier 1">Tier 1 - Urgent</option>
                    <option value="Tier 2">Tier 2 - High Priority</option>
                    <option value="Tier 3">Tier 3 - Standard</option>
                </select>
            </div>
            <div class="filter-group">
                <label>Status</label>
                <select id="status-filter">
                    <option value="">All Status</option>
                    <option value="New">New</option>
                    <option value="Contacted">Contacted</option>
                    <option value="In Progress">In Progress</option>
                    <option value="Closed">Closed</option>
                </select>
            </div>
            <div class="filter-group">
                <label>Organization</label>
                <input type="text" id="org-filter" placeholder="Search organization...">
            </div>
            <button class="btn" onclick="refreshLeads()">🔄 Refresh</button>
            <button class="btn btn-secondary" onclick="exportLeads()">📥 Export CSV</button>
        </div>
        
        <div class="last-update" id="last-update"></div>
        
        <div class="leads-table">
            <div id="loading" class="loading">Loading leads...</div>
            <table id="leads-table" style="display: none;">
                <thead>
                    <tr>
                        <th>Organization</th>
                        <th>Opportunity</th>
                        <th>Deadline</th>
                        <th>Tier</th>
                        <th>Contact</th>
                        <th>Status</th>
                        <th>Notes</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="leads-tbody">
                </tbody>
            </table>
        </div>
    </div>
    
    <script>
        let allLeads = [];
        let leadStatuses = {};
        let leadNotes = {};
        
        // Load saved data from localStorage
        const savedStatuses = localStorage.getItem('leadStatuses');
        const savedNotes = localStorage.getItem('leadNotes');
        if (savedStatuses) leadStatuses = JSON.parse(savedStatuses);
        if (savedNotes) leadNotes = JSON.parse(savedNotes);
        
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
                document.getElementById('leads-table').style.display = 'table';
            } catch (error) {
                console.error('Error loading leads:', error);
                document.getElementById('loading').textContent = 'Error loading leads. Please refresh.';
            }
        }
        
        function updateStats() {
            const total = allLeads.length;
            const urgent = allLeads.filter(l => l.tier.includes('Tier 1')).length;
            const newLeads = allLeads.filter(l => 
                (leadStatuses[l.opportunity] || l.status) === 'New'
            ).length;
            
            document.getElementById('total-leads').textContent = total;
            document.getElementById('urgent-leads').textContent = urgent;
            document.getElementById('new-leads').textContent = newLeads;
        }
        
        function displayLeads() {
            const tbody = document.getElementById('leads-tbody');
            const tierFilter = document.getElementById('tier-filter').value;
            const statusFilter = document.getElementById('status-filter').value;
            const orgFilter = document.getElementById('org-filter').value.toLowerCase();
            
            const filteredLeads = allLeads.filter(lead => {
                if (tierFilter && !lead.tier.includes(tierFilter)) return false;
                if (statusFilter && (leadStatuses[lead.opportunity] || lead.status) !== statusFilter) return false;
                if (orgFilter && !lead.organization.toLowerCase().includes(orgFilter)) return false;
                return true;
            });
            
            tbody.innerHTML = filteredLeads.map(lead => {
                const status = leadStatuses[lead.opportunity] || lead.status;
                const notes = leadNotes[lead.opportunity] || lead.notes;
                const tierClass = lead.tier.includes('Tier 1') ? 'tier-1' : 
                                 lead.tier.includes('Tier 2') ? 'tier-2' : 'tier-3';
                
                return `
                    <tr>
                        <td><strong>${lead.organization}</strong></td>
                        <td class="opportunity">${lead.opportunity}</td>
                        <td>${lead.deadline}</td>
                        <td><span class="${tierClass}">${lead.tier}</span></td>
                        <td>${lead.contact}</td>
                        <td>
                            <select class="status-select" onchange="updateStatus('${lead.opportunity}', this.value)">
                                <option value="New" ${status === 'New' ? 'selected' : ''}>New</option>
                                <option value="Contacted" ${status === 'Contacted' ? 'selected' : ''}>Contacted</option>
                                <option value="In Progress" ${status === 'In Progress' ? 'selected' : ''}>In Progress</option>
                                <option value="Closed" ${status === 'Closed' ? 'selected' : ''}>Closed</option>
                            </select>
                        </td>
                        <td>
                            <input type="text" class="notes-input" value="${notes}" 
                                   onblur="updateNotes('${lead.opportunity}', this.value)"
                                   placeholder="Add notes...">
                        </td>
                        <td class="action-buttons">
                            <a href="${lead.source}" target="_blank" class="btn btn-small">View</a>
                        </td>
                    </tr>
                `;
            }).join('');
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
            document.getElementById('leads-table').style.display = 'none';
            document.getElementById('loading').textContent = 'Refreshing leads...';
            
            try {
                await fetch('http://localhost:5000/api/refresh');
                await loadLeads();
            } catch (error) {
                console.error('Error refreshing leads:', error);
                document.getElementById('loading').textContent = 'Error refreshing. Please try again.';
            }
        }
        
        function exportLeads() {
            const filteredLeads = allLeads.map(lead => ({
                ...lead,
                status: leadStatuses[lead.opportunity] || lead.status,
                notes: leadNotes[lead.opportunity] || lead.notes
            }));
            
            const csv = [
                ['Organization', 'Opportunity', 'Deadline', 'Tier', 'Contact', 'Source', 'Status', 'Notes'],
                ...filteredLeads.map(lead => [
                    lead.organization,
                    lead.opportunity,
                    lead.deadline,
                    lead.tier,
                    lead.contact,
                    lead.source,
                    lead.status,
                    lead.notes
                ])
            ].map(row => row.map(cell => `"${cell}"`).join(',')).join('\\n');
            
            const blob = new Blob([csv], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `training-leads-${new Date().toISOString().split('T')[0]}.csv`;
            a.click();
        }
        
        // Filter event listeners
        document.getElementById('tier-filter').addEventListener('change', displayLeads);
        document.getElementById('status-filter').addEventListener('change', displayLeads);
        document.getElementById('org-filter').addEventListener('input', displayLeads);
        
        // Load leads on page load
        loadLeads();
        
        // Auto-refresh every 5 minutes
        setInterval(loadLeads, 5 * 60 * 1000);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(port=5001, debug=True)