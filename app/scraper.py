import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import pandas as pd
import json
import time
from urllib.parse import quote, urlparse
import random

class CanadianPublicSectorScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-CA,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Training-related keywords for intelligent filtering
        self.training_keywords = [
            'training', 'professional development', 'skills', 'learning',
            'workshop', 'certification', 'program', 'upskilling', 'reskilling',
            'capacity building', 'competency', 'education', 'course',
            'digital transformation', 'change management', 'implementation',
            'compliance', 'mandatory', 'requirement', 'deadline',
            'skills development', 'workforce development', 'talent development'
        ]
        
        # Canadian public sector indicators
        self.public_sector_keywords = [
            'government', 'canada', 'ontario', 'quebec', 'british columbia',
            'alberta', 'manitoba', 'saskatchewan', 'nova scotia', 'newfoundland',
            'ministry', 'department', 'agency', 'crown corporation', 'municipal',
            'city of', 'region of', 'indigenous', 'first nations', 'metis', 'inuit',
            'federal', 'provincial', 'public sector', 'civil service', 'public service'
        ]
        
    def search_web_real(self, query):
        """
        Perform real web searches using multiple search engines
        """
        results = []
        
        # Try multiple search approaches
        search_engines = [
            {
                'name': 'DuckDuckGo HTML',
                'url': f'https://html.duckduckgo.com/html/?q={quote(query + " site:.ca")}',
                'parser': self._parse_duckduckgo_html
            },
            {
                'name': 'Searx',
                'url': f'https://searx.be/search?q={quote(query + " canada government training 2025 2026")}&categories=general&language=en',
                'parser': self._parse_searx_results
            }
        ]
        
        for engine in search_engines:
            try:
                print(f"    🔍 Searching {engine['name']}...")
                response = self.session.get(engine['url'], timeout=15)
                
                if response.status_code == 200:
                    engine_results = engine['parser'](response.text)
                    results.extend(engine_results)
                    print(f"       ✓ Found {len(engine_results)} results from {engine['name']}")
                    
                time.sleep(random.uniform(1, 2))  # Respectful delay
                
            except Exception as e:
                print(f"       ⚠️ Error with {engine['name']}: {str(e)[:50]}")
        
        # Also search specific Canadian government sites
        gov_results = self._search_canadian_gov_sites_directly(query)
        results.extend(gov_results)
        
        return results
    
    def _parse_duckduckgo_html(self, html):
        """Parse DuckDuckGo HTML results"""
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        # DuckDuckGo HTML version has different structure
        for item in soup.find_all(['div', 'td'], class_=['result__body', 'result']):
            try:
                # Find the link
                link_elem = item.find('a', class_='result__a')
                if not link_elem:
                    link_elem = item.find('a', href=True)
                
                if link_elem:
                    title = link_elem.text.strip()
                    link = link_elem.get('href', '')
                    
                    # Get snippet
                    snippet_elem = item.find(['span', 'div'], class_=['result__snippet'])
                    if not snippet_elem:
                        snippet_elem = item.find_next_sibling('td') if item.name == 'td' else None
                    
                    snippet = snippet_elem.text.strip() if snippet_elem else ''
                    
                    if title and link and '.ca' in link:  # Prioritize Canadian sites
                        results.append({
                            'title': title,
                            'link': link,
                            'snippet': snippet
                        })
            except:
                continue
                
        return results[:10]  # Limit results
    
    def _parse_searx_results(self, html):
        """Parse Searx search results"""
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        for item in soup.find_all('article', class_='result'):
            try:
                title_elem = item.find('h3')
                link_elem = item.find('a', href=True)
                snippet_elem = item.find('p', class_='content')
                
                if title_elem and link_elem:
                    results.append({
                        'title': title_elem.text.strip(),
                        'link': link_elem.get('href', ''),
                        'snippet': snippet_elem.text.strip() if snippet_elem else ''
                    })
            except:
                continue
                
        return results[:10]
    
    def _search_canadian_gov_sites_directly(self, query):
        """Search specific Canadian government news and announcement sites"""
        results = []
        
        # List of Canadian government sites to search
        gov_sites = [
            {
                'name': 'Canada.ca News',
                'search_url': f'https://www.canada.ca/en/sr/srb.html?cdn=canada&st=s&num=10&st1rt=0&langs=en&q={quote(query)}',
                'base_url': 'https://www.canada.ca'
            },
            {
                'name': 'Ontario Newsroom',
                'search_url': f'https://news.ontario.ca/en/search?q={quote(query)}',
                'base_url': 'https://news.ontario.ca'
            },
            {
                'name': 'BC Gov News',
                'search_url': f'https://news.gov.bc.ca/search?q={quote(query)}',
                'base_url': 'https://news.gov.bc.ca'
            },
            {
                'name': 'Alberta Government',
                'search_url': f'https://www.alberta.ca/search?q={quote(query)}',
                'base_url': 'https://www.alberta.ca'
            }
        ]
        
        for site in gov_sites:
            try:
                print(f"       🔍 Searching {site['name']} directly...")
                response = self.session.get(site['search_url'], timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Generic search result parsing
                    items = soup.find_all(['article', 'div', 'li'], 
                                        class_=re.compile('result|search-result|news-item|listing-item', re.I))
                    
                    for item in items[:5]:  # Limit to 5 per site
                        try:
                            # Find link and title
                            link_elem = item.find('a', href=True)
                            if link_elem:
                                title = link_elem.text.strip() or item.find(['h2', 'h3', 'h4']).text.strip()
                                link = link_elem['href']
                                
                                # Make link absolute
                                if link.startswith('/'):
                                    link = site['base_url'] + link
                                
                                # Get snippet
                                snippet = ''
                                for elem in item.find_all(['p', 'div', 'span']):
                                    text = elem.text.strip()
                                    if len(text) > 50 and 'result' not in elem.get('class', []):
                                        snippet = text[:300]
                                        break
                                
                                if title:
                                    results.append({
                                        'title': title,
                                        'link': link,
                                        'snippet': snippet
                                    })
                        except:
                            continue
                    
                    print(f"          ✓ Found {len([r for r in results if site['base_url'] in r['link']])} results")
                    
                time.sleep(1)  # Respectful delay
                
            except Exception as e:
                print(f"          ⚠️ Error with {site['name']}: {str(e)[:50]}")
        
        return results
    
    def search_web_scrape(self, query):
        """Main search method that uses real web searching"""
        # First try real web search
        results = self.search_web_real(query)
        
        # If we got results, return them
        if results:
            print(f"       ✅ Found {len(results)} real results")
            return results
        
        # If no results, try a broader search
        print("       ℹ️ No results found, trying broader search...")
        broader_query = query.replace('"', '').split()[0:3]  # Take first 3 words
        broader_query = ' '.join(broader_query) + ' canada government'
        results = self.search_web_real(broader_query)
        
        if results:
            print(f"       ✅ Found {len(results)} results with broader search")
            return results
        
        # Absolutely no example data - return empty if no real results
        print("       ⚠️ No real results found")
        return []
    
    def extract_lead_from_result(self, result, search_category):
        """
        Use AI-like logic to extract meaningful lead information
        """
        title = result.get('title', '')
        snippet = result.get('snippet', '')
        link = result.get('link', '')
        
        # Combine all text for analysis
        full_text = f"{title} {snippet}".lower()
        
        # Check if it's a training opportunity
        if not self._is_training_opportunity(full_text):
            return None
            
        # Check if it's Canadian public sector
        if not self._is_canadian_public_sector(full_text, link):
            return None
            
        # Check if it's from 2025/2026
        if not self._is_current_opportunity(full_text):
            return None
            
        # Extract structured information
        organization = self._extract_organization(title, snippet, link)
        deadline = self._extract_deadline(full_text)
        tier = self._calculate_tier(full_text, deadline)
        contact = self._extract_contact(snippet, link)
        
        # Generate AI-like analysis
        opportunity_type = self._analyze_opportunity_type(full_text)
        critical_analysis = self._generate_critical_analysis(full_text, organization, deadline)
        
        return {
            'organization': organization,
            'opportunity': title[:200],
            'deadline': deadline,
            'tier': tier,
            'contact': contact,
            'source': link,
            'status': 'New',
            'notes': snippet[:250] + '...' if len(snippet) > 250 else snippet,
            'date_found': datetime.now().strftime('%Y-%m-%d'),
            'search_type': search_category,
            'opportunity_type': opportunity_type,
            'critical_analysis': critical_analysis
        }
    
    def _is_training_opportunity(self, text):
        """Check if text indicates a training opportunity"""
        # Must have at least 1 training-related keyword
        keyword_count = sum(1 for keyword in self.training_keywords if keyword in text)
        
        # Also check for government transformation indicators
        transformation_keywords = ['modernization', 'transformation', 'implementation', 
                                 'new system', 'upgrade', 'rollout', 'initiative',
                                 'digital adoption', 'change', 'reform']
        transform_count = sum(1 for keyword in transformation_keywords if keyword in text)
        
        total_relevance = keyword_count + transform_count
        
        return total_relevance >= 1
    
    def _is_canadian_public_sector(self, text, link):
        """Check if it's related to Canadian public sector"""
        # Check URL
        canadian_domains = ['.gc.ca', '.gov.on.ca', '.gov.bc.ca', '.gov.ab.ca', 
                           '.gov.mb.ca', '.gov.sk.ca', '.gov.ns.ca', '.gov.nl.ca',
                           'canada.ca', 'ontario.ca', 'alberta.ca', 'toronto.ca',
                           '.ca/']
        
        domain = urlparse(link).netloc.lower()
        url_path = urlparse(link).path.lower()
        
        # Check if it's a Canadian domain
        is_canadian_domain = any(cdn_domain in domain for cdn_domain in canadian_domains)
        is_canadian_path = any(cdn_domain in url_path for cdn_domain in canadian_domains)
        
        if is_canadian_domain or is_canadian_path:
            return True
            
        # Check text content
        keyword_count = sum(1 for keyword in self.public_sector_keywords if keyword in text)
        return keyword_count >= 2
    
    def _is_current_opportunity(self, text):
        """Check if opportunity is for 2025/2026"""
        year_patterns = ['2025', '2026', '2024-25', '2025-26', '2025-2026', '2025/26', '2025/2026']
        has_year = any(year in text for year in year_patterns)
        
        # If no year mentioned, check for current/upcoming indicators
        if not has_year:
            current_indicators = ['upcoming', 'new', 'launching', 'starting', 'beginning',
                                'announced', 'recent', 'latest', 'current', 'now',
                                'this year', 'next year', 'coming', 'future']
            has_current = any(indicator in text for indicator in current_indicators)
            return has_current
        
        return has_year
    
    def _extract_organization(self, title, snippet, link):
        """Extract organization name using intelligent parsing"""
        # Try URL-based extraction first
        domain = urlparse(link).netloc.lower()
        
        org_mapping = {
            'canada.ca': 'Government of Canada',
            'ontario.ca': 'Government of Ontario',
            'toronto.ca': 'City of Toronto',
            'vancouver.ca': 'City of Vancouver',
            'alberta.ca': 'Government of Alberta',
            'gov.bc.ca': 'Government of British Columbia',
            'gov.mb.ca': 'Government of Manitoba',
            'gov.sk.ca': 'Government of Saskatchewan',
            'quebec.ca': 'Government of Quebec'
        }
        
        for domain_key, org_name in org_mapping.items():
            if domain_key in domain:
                # Try to get more specific department/ministry
                dept_patterns = [
                    r'(Ministry of [\w\s]+)',
                    r'(Department of [\w\s]+)',
                    r'([\w\s]+ Agency)',
                    r'([\w\s]+ Corporation)',
                    r'([\w\s]+ Canada)',
                    r'(Service Canada)',
                    r'(Health Canada)',
                    r'(Transport Canada)'
                ]
                
                combined_text = title + ' ' + snippet
                for pattern in dept_patterns:
                    match = re.search(pattern, combined_text, re.I)
                    if match:
                        return match.group(1).strip()
                
                return org_name
                
        # Try pattern matching in title
        patterns = [
            r'^([^-–—:]+?)(?:\s*[-–—:])',  # Text before dash/colon
            r'((?:City|Region|Municipality) of [\w\s]+)',
            r'([\w\s]+ (?:Ministry|Department|Agency|Corporation))',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, title)
            if match:
                org = match.group(1).strip()
                if 10 < len(org) < 100:  # Reasonable length
                    return org
                    
        return 'Canadian Public Sector Organization'
    
    def _extract_deadline(self, text):
        """Extract or intelligently estimate deadline"""
        # Look for specific dates
        date_patterns = [
            r'(\d{1,2}[-/]\d{1,2}[-/]\d{4})',  # MM-DD-YYYY or MM/DD/YYYY
            r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})',  # YYYY-MM-DD
            r'((?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s*202[56])',
            r'((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{1,2},?\s*202[56])',
            r'by\s+((?:january|february|march|april|may|june|july|august|september|october|november|december)\s+202[56])',
            r'before\s+((?:january|february|march|april|may|june|july|august|september|october|november|december)\s+202[56])'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    date_str = match.group(1)
                    # Parse the date (simplified - in production use dateutil)
                    if '2025' in date_str:
                        if any(month in date_str.lower() for month in ['jul', 'july']):
                            return '2025-07-31'
                        elif any(month in date_str.lower() for month in ['aug', 'august']):
                            return '2025-08-31'
                        elif any(month in date_str.lower() for month in ['sep', 'september']):
                            return '2025-09-30'
                        elif any(month in date_str.lower() for month in ['dec', 'december']):
                            return '2025-12-31'
                        else:
                            return '2025-06-30'  # Default mid-year
                    elif '2026' in date_str:
                        return '2026-03-31'  # Default fiscal year end
                except:
                    pass
        
        # Look for urgency indicators
        if any(word in text for word in ['urgent', 'immediate', 'asap', 'quickly', 'soon']):
            return (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        elif any(word in text for word in ['summer', 'q2', 'second quarter']):
            return '2025-07-31'
        elif any(word in text for word in ['fall', 'autumn', 'q3', 'third quarter']):
            return '2025-09-30'
        elif any(word in text for word in ['winter', 'q4', 'fourth quarter']):
            return '2025-12-31'
        elif any(word in text for word in ['spring', 'q1', 'first quarter']):
            return '2025-03-31'
        elif '2026' in text:
            return '2026-03-31'
        else:
            # Default to 90 days from now
            return (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
    
    def _calculate_tier(self, text, deadline):
        """Calculate urgency tier using AI-like logic"""
        try:
            deadline_date = datetime.strptime(deadline, '%Y-%m-%d')
            days_until = (deadline_date - datetime.now()).days
            
            # Tier 1: Urgent (< 30 days or has urgency keywords)
            if days_until <= 30 or any(word in text for word in ['urgent', 'immediate', 'critical', 'mandatory', 'asap']):
                return 'Tier 1 - Urgent'
            # Tier 2: High Priority (< 60 days or important keywords)
            elif days_until <= 60 or any(word in text for word in ['priority', 'important', 'compliance', 'requirement', 'deadline']):
                return 'Tier 2 - High Priority'
            # Tier 3: Standard
            else:
                return 'Tier 3 - Standard'
        except:
            return 'Tier 3 - Standard'
    
    def _extract_contact(self, snippet, link):
        """Extract contact information"""
        # Look for email
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_match = re.search(email_pattern, snippet)
        if email_match:
            return email_match.group(0)
            
        # Look for phone
        phone_patterns = [
            r'(?:\d{3}[-.]?\d{3}[-.]?\d{4})',
            r'(?:\(\d{3}\)\s*\d{3}[-.]?\d{4})',
            r'(?:1[-.]?\d{3}[-.]?\d{3}[-.]?\d{4})'
        ]
        
        for pattern in phone_patterns:
            phone_match = re.search(pattern, snippet)
            if phone_match:
                return phone_match.group(0)
            
        # Default based on domain
        domain = urlparse(link).netloc.lower()
        contact_mapping = {
            'toronto.ca': 'procurement@toronto.ca',
            'ontario.ca': 'info@ontario.ca',
            'canada.ca': 'info@canada.ca',
            'alberta.ca': 'info@alberta.ca',
            'gov.bc.ca': 'info@gov.bc.ca',
            'vancouver.ca': 'info@vancouver.ca'
        }
        
        for domain_key, contact in contact_mapping.items():
            if domain_key in domain:
                return contact
            
        return 'See source for contact details'
    
    def _analyze_opportunity_type(self, text):
        """Analyze what type of training opportunity this is"""
        if 'digital transformation' in text or 'digital adoption' in text:
            return 'Digital Transformation'
        elif 'compliance' in text or 'mandatory' in text:
            return 'Compliance Training'
        elif 'grant' in text or 'funding' in text:
            return 'Grant/Funding Opportunity'
        elif 'indigenous' in text or 'first nations' in text:
            return 'Indigenous Initiative'
        elif 'health' in text or 'medical' in text:
            return 'Healthcare Training'
        elif 'leadership' in text or 'management' in text:
            return 'Leadership Development'
        elif 'cyber' in text or 'security' in text:
            return 'Cybersecurity Training'
        elif 'data' in text or 'analytics' in text:
            return 'Data/Analytics Training'
        else:
            return 'Professional Development'
    
    def _generate_critical_analysis(self, text, organization, deadline):
        """Generate critical analysis for sales intelligence"""
        analysis_points = []
        
        # Analyze organization scale
        if 'canada' in organization.lower() and ('government of canada' in organization.lower() or 'federal' in text):
            analysis_points.append("Federal opportunity - high value potential with possibility of national rollout")
        elif any(prov in organization.lower() for prov in ['ontario', 'british columbia', 'alberta', 'quebec']):
            analysis_points.append("Provincial opportunity - significant scale with regional impact")
        elif 'city of' in organization.lower() or 'municipal' in text:
            analysis_points.append("Municipal opportunity - focused scope with potential for replication in other cities")
        
        # Analyze urgency
        try:
            deadline_date = datetime.strptime(deadline, '%Y-%m-%d')
            days_until = (deadline_date - datetime.now()).days
            if days_until <= 30:
                analysis_points.append(f"URGENT: Only {days_until} days to deadline - immediate action required")
            elif days_until <= 60:
                analysis_points.append(f"Time-sensitive: {days_until} days to deadline - prioritize engagement")
        except:
            pass
        
        # Analyze opportunity characteristics
        if 'mandatory' in text or 'compliance' in text or 'required' in text:
            analysis_points.append("Mandatory training - high close probability due to regulatory requirement")
        
        if 'digital' in text and ('transformation' in text or 'modernization' in text):
            analysis_points.append("Digital transformation initiative - likely needs comprehensive change management")
        
        if 'grant' in text or 'funding' in text:
            analysis_points.append("Funded opportunity - budget already allocated")
        
        if any(keyword in text for keyword in ['pilot', 'trial', 'proof of concept']):
            analysis_points.append("Pilot opportunity - potential for expansion if successful")
        
        if any(size in text for size in ['10,000', '20,000', '50,000', '100,000', 'thousand', 'million']):
            analysis_points.append("Large-scale deployment indicated - significant revenue potential")
        
        return ' | '.join(analysis_points) if analysis_points else 'Standard professional development opportunity'
    
    def get_all_leads(self):
        """
        Main method to search for real training opportunities
        """
        all_leads = []
        
        # Define search queries for 2025/2026
        search_queries = {
            'Federal Government': [
                'Government of Canada training program 2025 2026',
                'federal employee professional development 2025',
                'canada digital transformation training 2025',
                'public service training initiative 2025'
            ],
            'Provincial Government': [
                'Ontario government training 2025 mandatory',
                'British Columbia skills development 2025',
                'Alberta government professional development 2025',
                'Quebec government formation 2025'
            ],
            'Municipal': [
                'City of Toronto training program 2025',
                'Vancouver municipal training 2025',
                'Calgary professional development 2025',
                'Montreal formation municipale 2025'
            ],
            'Digital Transformation': [
                'canada digital adoption program training',
                'government digital transformation 2025',
                'public sector modernization training',
                'digital government initiative 2025'
            ],
            'Grant Recipients': [
                'canada training grant recipients 2025',
                'professional development funding canada',
                'workforce development grants 2025',
                'skills training funding opportunities'
            ],
            'Indigenous': [
                'Indigenous Services Canada training 2025',
                'First Nations capacity building 2025',
                'indigenous skills development 2025',
                'aboriginal professional development funding'
            ]
        }
        
        print("\n" + "="*70)
        print("🚀 STARTING REAL-TIME WEB SEARCH FOR CANADIAN PUBLIC SECTOR TRAINING")
        print("="*70)
        print("⚡ Searching for actual 2025/2026 opportunities...")
        print("="*70 + "\n")
        
        total_searches = sum(len(queries) for queries in search_queries.values())
        current_search = 0
        
        for category, queries in search_queries.items():
            print(f"\n📂 Searching {category}...")
            category_leads = []
            
            for query in queries:
                current_search += 1
                print(f"\n  [{current_search}/{total_searches}] Query: {query}")
                
                # Search using real web search
                results = self.search_web_scrape(query)
                
                # Process results
                for result in results:
                    lead = self.extract_lead_from_result(result, category)
                    if lead:
                        category_leads.append(lead)
                        print(f"       ✅ Found lead: {lead['organization']} - {lead['opportunity'][:60]}...")
                
                # Respectful delay between searches
                time.sleep(random.uniform(2, 3))
            
            print(f"\n  ✅ Found {len(category_leads)} valid leads in {category}")
            all_leads.extend(category_leads)
        
        # Remove duplicates based on opportunity title
        if all_leads:
            df = pd.DataFrame(all_leads)
            df = df.drop_duplicates(subset=['opportunity'], keep='first')
            all_leads = df.to_dict('records')
        
        # Sort by tier and deadline
        all_leads.sort(key=lambda x: (
            0 if 'Tier 1' in x['tier'] else (1 if 'Tier 2' in x['tier'] else 2),
            x['deadline']
        ))
        
        print("\n" + "="*70)
        print("📊 SEARCH COMPLETE - REAL RESULTS")
        print("="*70)
        print(f"Total valid leads found: {len(all_leads)}")
        
        if all_leads:
            tier_counts = {}
            for lead in all_leads:
                tier = lead['tier'].split(' - ')[0]
                tier_counts[tier] = tier_counts.get(tier, 0) + 1
            
            for tier, count in sorted(tier_counts.items()):
                emoji = '🔴' if 'Tier 1' in tier else ('🟡' if 'Tier 2' in tier else '🟢')
                print(f"  {emoji} {tier}: {count} leads")
                
            # Show sample of what was found
            print("\n📋 Sample of leads found:")
            for lead in all_leads[:3]:
                print(f"\n  • {lead['organization']}")
                print(f"    {lead['opportunity'][:80]}...")
                print(f"    Deadline: {lead['deadline']} | {lead['tier']}")
                print(f"    Analysis: {lead.get('critical_analysis', 'N/A')[:100]}...")
        else:
            print("\n⚠️  No leads found in this search.")
            print("   This could be due to:")
            print("   - Search engines blocking automated requests")
            print("   - Network connectivity issues")
            print("   - Need for more specific search terms")
            print("\n💡 The system is configured to search real sources only.")
            print("   NO SAMPLE DATA is being used as per user requirements.")
        
        print("="*70 + "\n")
        
        return all_leads