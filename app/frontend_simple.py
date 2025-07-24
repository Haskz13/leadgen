from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Lead Generation Dashboard</title>
    <style>
        body { 
            background: #1a1a1a; 
            color: white; 
            font-family: Arial, sans-serif; 
            margin: 20px;
        }
        h1 { color: #3b82f6; }
        .lead { 
            background: #2a2a2a; 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 8px;
            border-left: 4px solid #3b82f6;
        }
        .loading { color: #666; }
    </style>
</head>
<body>
    <h1>Canadian Public Sector Training Leads</h1>
    <div id="leads">
        <p class="loading">Loading leads...</p>
    </div>
    
    <script>
        fetch('http://localhost:5000/api/leads')
            .then(r => r.json())
            .then(data => {
                const container = document.getElementById('leads');
                if (data.leads && data.leads.length > 0) {
                    container.innerHTML = data.leads.map(lead => `
                        <div class="lead">
                            <h3>${lead.organization}</h3>
                            <p><strong>${lead.opportunity}</strong></p>
                            <p>${lead.description}</p>
                            <p>Deadline: ${lead.deadline} | ${lead.tier}</p>
                        </div>
                    `).join('');
                } else {
                    container.innerHTML = '<p>No leads found</p>';
                }
            })
            .catch(err => {
                document.getElementById('leads').innerHTML = '<p>Error loading leads</p>';
            });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("Starting frontend on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=False)