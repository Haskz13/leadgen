import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import pandas as pd
import json
import time
from urllib.parse import quote

class CanadianPublicSectorScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def search_duckduckgo(self, query, region='ca-en'):
        """
        Use DuckDuckGo's instant answer API to search for real results
        No API key required - completely free
        """
        print(f"  🔍 Searching DuckDuckGo for: {query}")
        
        # DuckDuckGo instant answer API
        url = "https://api.duckduckgo.com/"
        params = {
            'q': query,
            'format': 'json',
            'no_html': 1,
            'skip_disambig': 1
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # Also try HTML search for more results
                search_results = self.search_duckduckgo_html(query)
                return search_results
            
        except Exception as e:
            print(f"    ❌ Error searching: {e}")
            
        return []
    
    def search_duckduckgo_html(self, query):
        """
        Scrape DuckDuckGo HTML results for more comprehensive data
        """
        results = []
        
        # Use DuckDuckGo HTML interface
        search_url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
        
        try:
            response = self.session.get(search_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find all result links
                for result in soup.find_all('div', class_='result__body'):
                    title_elem = result.find('a', class_='result__a')
                    snippet_elem = result.find('a', class_='result__snippet')
                    
                    if title_elem and snippet_elem:
                        results.append({
                            'title': title_elem.text.strip(),
                            'link': title_elem.get('href', ''),
                            'snippet': snippet_elem.text.strip()
                        })
                
                print(f"    ✓ Found {len(results)} results")
                
        except Exception as e:
            print(f"    ❌ Error in HTML search: {e}")
            
        return results[:10]  # Limit to 10 results per search
    
    def extract_lead_from_result(self, result, search_type):
        """
        Extract a lead from a search result with intelligent parsing
        """
        title = result.get('title', '')
        snippet = result.get('snippet', '')
        link = result.get('link', '')
        
        # Skip if not relevant
        if not self.is_training_opportunity(title, snippet):
            return None
            
        # Extract organization
        organization = self.extract_organization(title, snippet, link)
        
        # Extract deadline
        deadline = self.extract_deadline(title, snippet)
        
        # Calculate tier
        tier = self.calculate_tier(title, snippet, deadline)
        
        # Extract contact
        contact = self.extract_contact(snippet, link)
        
        return {
            'organization': organization,
            'opportunity': title,
            'deadline': deadline,
            'tier': tier,
            'contact': contact,
            'source': link,
            'status': 'New',
            'notes': snippet[:200] + '...' if len(snippet) > 200 else snippet,
            'date_found': datetime.now().strftime('%Y-%m-%d'),
            'search_type': search_type
        }
    
    def is_training_opportunity(self, title, snippet):
        """
        Determine if this is a real training opportunity
        """
        text = f"{title} {snippet}".lower()
        
        # Must have year indicator
        if not any(year in text for year in ['2025', '2026', '2024-25', '2025-26']):
            return False
            
        # Must have training/development indicator
        training_indicators = [
            'training', 'professional development', 'skills', 'learning',
            'workshop', 'certification', 'program', 'initiative',
            'transformation', 'implementation', 'compliance', 'mandatory'
        ]
        
        return any(indicator in text for indicator in training_indicators)
    
    def extract_organization(self, title, snippet, link):
        """
        Extract organization name using multiple strategies
        """
        # Try to extract from title
        if ' - ' in title:
            org = title.split(' - ')[0].strip()
            if len(org) > 5 and len(org) < 100:
                return org
                
        # Try to extract from link
        if 'canada.ca' in link:
            return 'Government of Canada'
        elif '.gc.ca' in link:
            parts = link.split('.gc.ca')[0].split('.')[-1]
            return parts.upper() if len(parts) < 10 else 'Government of Canada'
        elif 'ontario.ca' in link:
            return 'Government of Ontario'
        elif 'toronto.ca' in link:
            return 'City of Toronto'
            
        # Try to find organization names in snippet
        org_patterns = [
            r'([\w\s]+(?:Ministry|Department|Agency|Corporation|City of|Region of)[\w\s]*)',
            r'([\w\s]+(?:Canada|Ontario|Toronto|Vancouver|Montreal)[\w\s]*)',
        ]
        
        for pattern in org_patterns:
            match = re.search(pattern, snippet)
            if match:
                org = match.group(1).strip()
                if len(org) > 5 and len(org) < 100:
                    return org
                    
        return 'Canadian Public Sector Organization'
    
    def extract_deadline(self, title, snippet):
        """
        Extract or estimate deadline from content
        """
        text = f"{title} {snippet}".lower()
        
        # Look for specific dates
        date_patterns = [
            r'by\s+(\w+\s+\d{1,2},?\s+\d{4})',
            r'deadline[:\s]+(\w+\s+\d{1,2},?\s+\d{4})',
            r'before\s+(\w+\s+\d{1,2},?\s+\d{4})',
            r'(\w+\s+\d{4})\s+deadline',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    # Parse the date
                    date_str = match.group(1)
                    # Add logic to parse various date formats
                    return (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d')
                except:
                    pass
        
        # Estimate based on keywords
        if any(word in text for word in ['urgent', 'immediate', 'asap', 'quickly']):
            return (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        elif any(word in text for word in ['summer', 'july', 'august']):
            return '2025-07-31'
        elif any(word in text for word in ['fall', 'september', 'october']):
            return '2025-09-30'
        elif '2026' in text:
            return '2026-03-31'
        else:
            return (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d')
    
    def calculate_tier(self, title, snippet, deadline):
        """
        Calculate urgency tier
        """
        text = f"{title} {snippet}".lower()
        
        # Parse deadline
        try:
            deadline_date = datetime.strptime(deadline, '%Y-%m-%d')
            days_until = (deadline_date - datetime.now()).days
            
            # Tier based on deadline
            if days_until <= 30:
                return 'Tier 1 - Urgent'
            elif days_until <= 60:
                return 'Tier 2 - High Priority'
            else:
                # Check for other urgency indicators
                if any(word in text for word in ['urgent', 'immediate', 'critical', 'mandatory']):
                    return 'Tier 2 - High Priority'
                return 'Tier 3 - Standard'
        except:
            return 'Tier 3 - Standard'
    
    def extract_contact(self, snippet, link):
        """
        Extract contact information
        """
        # Look for email
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', snippet)
        if email_match:
            return email_match.group(0)
            
        # Look for phone
        phone_match = re.search(r'[\d-]{10,}', snippet)
        if phone_match:
            return phone_match.group(0)
            
        # Default based on organization
        if 'toronto.ca' in link:
            return 'Contact City of Toronto'
        elif 'ontario.ca' in link:
            return 'Contact Province of Ontario'
        elif 'canada.ca' in link:
            return 'Contact department directly'
            
        return 'See source for contact details'
    
    def search_training_opportunities(self):
        """
        Search for real training opportunities across multiple categories
        """
        all_leads = []
        
        # Define comprehensive search queries
        search_queries = {
            'Grant Recipients': [
                '"grant recipient" training "professional development" Canada 2025',
                'ESDC "skills development" "funding awarded" 2025 2026',
                '"Indigenous Services Canada" grant training 2025',
                'Canada "training grant" awarded 2025 recipient'
            ],
            'Digital Transformations': [
                '"Government of Canada" "digital transformation" training 2025',
                'CRA "modernization" "staff training" 2025',
                '"Service Canada" system training 2025',
                'federal government "new system" training 2025'
            ],
            'Compliance & Mandates': [
                'AODA "compliance training" deadline 2025 Ontario',
                '"mandatory training" government Canada 2025',
                '"Truth and Reconciliation" training government 2025',
                'cybersecurity training requirement Canada 2025'
            ],
            'Municipal Programs': [
                '"City of Toronto" training program 2025',
                'Vancouver employee training 2025',
                'Montreal "formation professionnelle" 2025',
                'municipal training initiative Canada 2025'
            ],
            'Healthcare & Education': [
                'Ontario healthcare training mandate 2025',
                'education "professional development" Canada 2025',
                'nursing training requirement 2025',
                'teacher training program Ontario 2025'
            ],
            'Indigenous Initiatives': [
                'AFN training program 2025',
                '"First Nations" "capacity building" 2025',
                'Indigenous "skills development" Canada 2025',
                'Métis training initiative 2025'
            ]
        }
        
        print("\n" + "="*70)
        print("🚀 STARTING REAL-TIME CANADIAN PUBLIC SECTOR TRAINING LEAD SEARCH")
        print("="*70)
        
        for category, queries in search_queries.items():
            print(f"\n📂 Searching {category}...")
            category_leads = []
            
            for query in queries:
                results = self.search_duckduckgo(query)
                
                for result in results:
                    lead = self.extract_lead_from_result(result, category)
                    if lead:
                        category_leads.append(lead)
                
                # Respectful delay
                time.sleep(1)
            
            print(f"   ✓ Found {len(category_leads)} leads in {category}")
            all_leads.extend(category_leads)
        
        # Remove duplicates
        if all_leads:
            df = pd.DataFrame(all_leads)
            df = df.drop_duplicates(subset=['opportunity'], keep='first')
            all_leads = df.to_dict('records')
        
        # Sort by tier and deadline
        all_leads.sort(key=lambda x: (
            0 if 'Tier 1' in x['tier'] else (1 if 'Tier 2' in x['tier'] else 2),
            x['deadline']
        ))
        
        return all_leads
    
    def get_all_leads(self):
        """
        Main method to get all leads
        """
        leads = self.search_training_opportunities()
        
        print("\n" + "="*70)
        print("📊 SEARCH COMPLETE - REAL RESULTS SUMMARY")
        print("="*70)
        print(f"Total leads found: {len(leads)}")
        
        if leads:
            tier_counts = {}
            for lead in leads:
                tier = lead['tier'].split(' - ')[0]
                tier_counts[tier] = tier_counts.get(tier, 0) + 1
            
            for tier, count in sorted(tier_counts.items()):
                print(f"  {tier}: {count} leads")
        
        print("="*70 + "\n")
        
        return leads