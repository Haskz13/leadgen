import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import pandas as pd
import json
import time

class CanadianPublicSectorScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.training_signals = [
            'training', 'professional development', 'skills development',
            'capacity building', 'learning', 'workshop', 'certification',
            'digital transformation', 'change management', 'upskilling',
            'reskilling', 'competency', 'education', 'course',
            'formation', 'développement professionnel', 'apprentissage'
        ]
        
    def scrape_open_canada_grants(self):
        """Scrape grants from Open Canada Data Portal for training-related funding"""
        leads = []
        
        try:
            # Open Canada API for grants and contributions
            base_url = "https://search.open.canada.ca/grants/ajax/"
            
            for keyword in ['training', 'professional development', 'skills', 'digital']:
                params = {
                    'search_text': keyword,
                    'page': 0,
                    'sort': 'score desc',
                    'search_year': '2024'
                }
                
                response = requests.get(base_url, params=params, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for grant in data.get('items', [])[:20]:  # Limit to 20 per keyword
                        # Check if grant is training-related
                        description = grant.get('description_en', '').lower()
                        if any(signal in description for signal in self.training_signals):
                            lead = {
                                'organization': grant.get('recipient_legal_name', 'Unknown'),
                                'opportunity': f"Grant Recipient: {grant.get('project_title_en', 'Training Grant')} - ${grant.get('agreement_value', 'N/A')}",
                                'deadline': self._estimate_deadline_from_grant(grant),
                                'tier': self._calculate_tier_from_date(self._estimate_deadline_from_grant(grant)),
                                'contact': grant.get('recipient_city', '') + ', ' + grant.get('recipient_province', ''),
                                'source': f"https://search.open.canada.ca/grants/record/{grant.get('ref_number', '')}",
                                'status': 'New',
                                'notes': f"Funding program: {grant.get('program_name_en', 'N/A')}",
                                'date_found': datetime.now().strftime('%Y-%m-%d')
                            }
                            leads.append(lead)
                
                time.sleep(1)  # Be respectful with API calls
                
        except Exception as e:
            print(f"Error scraping Open Canada grants: {e}")
            
        return leads
    
    def scrape_canada_ca_news(self):
        """Scrape actual news from Canada.ca news releases"""
        leads = []
        
        try:
            # Canada.ca news API endpoint
            url = "https://www.canada.ca/content/canadasite/api/nws/fds/en/web-feeds/news.json"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for item in data.get('entries', [])[:50]:  # Check last 50 news items
                    title = item.get('title', '').lower()
                    description = item.get('description', '').lower()
                    
                    # Check if news is training-related
                    if any(signal in title + description for signal in self.training_signals):
                        lead = {
                            'organization': self._extract_department(item),
                            'opportunity': item.get('title', ''),
                            'deadline': (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d'),
                            'tier': 'Tier 2 - High Priority',
                            'contact': 'See department website',
                            'source': item.get('link', ''),
                            'status': 'New',
                            'notes': 'Recent government announcement',
                            'date_found': datetime.now().strftime('%Y-%m-%d')
                        }
                        leads.append(lead)
                        
        except Exception as e:
            print(f"Error scraping Canada.ca news: {e}")
            
        return leads
    
    def scrape_provincial_sites(self):
        """Scrape provincial government sites for training initiatives"""
        leads = []
        
        provincial_sources = [
            {
                'name': 'Ontario Newsroom',
                'url': 'https://news.ontario.ca/en/search',
                'params': {'q': 'training', 'sort': 'published_date'}
            },
            {
                'name': 'BC Gov News',
                'url': 'https://news.gov.bc.ca/search',
                'params': {'q': 'training'}
            },
            {
                'name': 'Alberta Government',
                'url': 'https://www.alberta.ca/news.aspx',
                'params': {}
            }
        ]
        
        for source in provincial_sources:
            try:
                # This is a simplified example - in production, you'd parse each site's structure
                print(f"Checking {source['name']}...")
                # Real implementation would parse each provincial site
                # For now, we'll skip to avoid complex site-specific parsing
            except Exception as e:
                print(f"Error scraping {source['name']}: {e}")
                
        return leads
    
    def scrape_indigenous_organizations(self):
        """Scrape Indigenous organization websites and news"""
        leads = []
        
        # List of Indigenous organizations to monitor
        indigenous_sources = [
            'https://www.afn.ca/news/',
            'https://www.metisnation.ca/news',
            'https://www.itk.ca/news/',
            'https://nwac.ca/news/'
        ]
        
        # In production, implement actual scraping for each source
        # For now, using API where available
        
        return leads
    
    def scrape_crown_corporations(self):
        """Scrape Crown corporation websites for training needs"""
        leads = []
        
        crown_corps = [
            {'name': 'Canada Post', 'news_url': 'https://www.canadapost-postescanada.ca/cpc/en/our-company/news-and-media.page'},
            {'name': 'VIA Rail', 'news_url': 'https://www.viarail.ca/en/about-via-rail/media-room'},
            {'name': 'CBC/Radio-Canada', 'news_url': 'https://cbc.radio-canada.ca/en/media-centre'},
            {'name': 'Canada Mortgage and Housing Corporation', 'news_url': 'https://www.cmhc-schl.gc.ca/en/media-newsroom'}
        ]
        
        # In production, implement actual scraping for each Crown corporation
        
        return leads
    
    def scrape_municipal_websites(self):
        """Scrape major Canadian municipal websites"""
        leads = []
        
        municipalities = [
            {'name': 'Toronto', 'url': 'https://www.toronto.ca/news/'},
            {'name': 'Montreal', 'url': 'https://montreal.ca/en/news'},
            {'name': 'Vancouver', 'url': 'https://vancouver.ca/news-calendar/news.aspx'},
            {'name': 'Calgary', 'url': 'https://www.calgary.ca/media.html'},
            {'name': 'Ottawa', 'url': 'https://ottawa.ca/en/news'}
        ]
        
        # In production, implement actual scraping for each municipality
        
        return leads
    
    def scrape_sector_specific_sources(self):
        """Scrape sector-specific sources for training needs"""
        leads = []
        
        # Healthcare sector
        # Education sector  
        # Public safety sector
        # Environmental sector
        # Transportation sector
        
        # Each sector would have its own scraping logic
        
        return leads
    
    def _extract_department(self, news_item):
        """Extract department name from news item"""
        dept = news_item.get('department', {})
        if isinstance(dept, dict):
            return dept.get('title', 'Government of Canada')
        return 'Government of Canada'
    
    def _estimate_deadline_from_grant(self, grant):
        """Estimate training deadline from grant information"""
        # If grant was recently awarded, training likely needed soon
        agreement_date = grant.get('agreement_start_date', '')
        if agreement_date:
            try:
                start_date = datetime.strptime(agreement_date[:10], '%Y-%m-%d')
                # Assume training needed within 60 days of grant start
                deadline = start_date + timedelta(days=60)
                return deadline.strftime('%Y-%m-%d')
            except:
                pass
        
        # Default to 45 days from now
        return (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d')
    
    def _calculate_tier_from_date(self, deadline_str):
        """Calculate urgency tier based on deadline"""
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
            days_until = (deadline - datetime.now()).days
            
            if days_until <= 30:
                return 'Tier 1 - Urgent'
            elif days_until <= 60:
                return 'Tier 2 - High Priority'
            else:
                return 'Tier 3 - Standard'
        except:
            return 'Tier 3 - Standard'
    
    def get_all_leads(self):
        """Aggregate leads from all sources"""
        all_leads = []
        
        print("Searching Open Canada Data Portal for grant recipients...")
        all_leads.extend(self.scrape_open_canada_grants())
        
        print("Scanning Government of Canada news...")
        all_leads.extend(self.scrape_canada_ca_news())
        
        print("Checking provincial government sites...")
        all_leads.extend(self.scrape_provincial_sites())
        
        print("Scanning Indigenous organizations...")
        all_leads.extend(self.scrape_indigenous_organizations())
        
        print("Checking Crown corporations...")
        all_leads.extend(self.scrape_crown_corporations())
        
        print("Scanning municipal websites...")
        all_leads.extend(self.scrape_municipal_websites())
        
        print("Checking sector-specific sources...")
        all_leads.extend(self.scrape_sector_specific_sources())
        
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
        
        print(f"Total leads found: {len(all_leads)}")
        return all_leads