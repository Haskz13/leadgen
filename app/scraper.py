import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import pandas as pd

class CanadianPublicSectorScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.training_keywords = [
            'training', 'workshop', 'professional development', 'learning',
            'course', 'certification', 'skills development', 'capacity building',
            'formation', 'développement professionnel', 'apprentissage'
        ]
        
    def scrape_buyandsell(self):
        """Scrape Canada's official procurement site for training opportunities"""
        leads = []
        base_url = "https://buyandsell.gc.ca/procurement-data/search/site"
        
        # Search for training-related tenders
        for keyword in self.training_keywords[:3]:  # Start with first 3 keywords
            try:
                search_url = f"{base_url}?f%5B0%5D=sm_facet_procurement_data%3Adata_data_tender_notice&keywords={keyword}"
                response = requests.get(search_url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # Parse tender notices
                    results = soup.find_all('div', class_='search-result')[:10]  # Limit to 10 per keyword
                    
                    for result in results:
                        title_elem = result.find('h3', class_='title')
                        if title_elem:
                            lead = {
                                'organization': 'Government of Canada',
                                'opportunity': title_elem.text.strip(),
                                'deadline': self._extract_deadline(result),
                                'tier': self._calculate_tier(result),
                                'contact': 'See source link',
                                'source': 'https://buyandsell.gc.ca' + title_elem.find('a')['href'] if title_elem.find('a') else '',
                                'status': 'New',
                                'notes': '',
                                'date_found': datetime.now().strftime('%Y-%m-%d')
                            }
                            leads.append(lead)
            except Exception as e:
                print(f"Error scraping buyandsell for {keyword}: {e}")
                
        return leads
    
    def scrape_merx(self):
        """Scrape MERX for Canadian public sector training opportunities"""
        leads = []
        # MERX requires more complex authentication, so we'll simulate with placeholder data
        # In production, you'd implement proper MERX API access or selenium-based scraping
        
        # Placeholder implementation
        sample_leads = [
            {
                'organization': 'Ontario Ministry of Health',
                'opportunity': 'Healthcare Professional Training Services RFP',
                'deadline': (datetime.now() + timedelta(days=21)).strftime('%Y-%m-%d'),
                'tier': 'Tier 1 - Urgent',
                'contact': 'procurement@health.gov.on.ca',
                'source': 'https://www.merx.com/sample-rfp-12345',
                'status': 'New',
                'notes': '',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'City of Toronto',
                'opportunity': 'Diversity & Inclusion Training for Municipal Staff',
                'deadline': (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d'),
                'tier': 'Tier 1 - Urgent',
                'contact': 'purchasing@toronto.ca',
                'source': 'https://www.merx.com/sample-rfp-12346',
                'status': 'New',
                'notes': '',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            }
        ]
        
        return sample_leads
    
    def scrape_news(self):
        """Scrape news sources for training mandates and announcements"""
        leads = []
        # Implement news scraping for CBC, government press releases, etc.
        # For now, returning sample data
        
        sample_news_leads = [
            {
                'organization': 'Indigenous Services Canada',
                'opportunity': 'New funding for Indigenous youth skills training announced',
                'deadline': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                'tier': 'Tier 2 - High Priority',
                'contact': 'Contact ISC regional office',
                'source': 'https://www.canada.ca/en/indigenous-services-canada/news/sample',
                'status': 'New',
                'notes': 'Federal funding announcement - follow up for training provider opportunities',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            }
        ]
        
        return sample_news_leads
    
    def _extract_deadline(self, soup_element):
        """Extract deadline from procurement notice"""
        # Look for deadline patterns
        text = soup_element.text
        deadline_patterns = [
            r'closing.*?(\d{4}-\d{2}-\d{2})',
            r'deadline.*?(\d{4}-\d{2}-\d{2})',
            r'due.*?(\d{4}-\d{2}-\d{2})'
        ]
        
        for pattern in deadline_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        # Default to 30 days from now if no deadline found
        return (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    
    def _calculate_tier(self, soup_element):
        """Calculate urgency tier based on deadline and other factors"""
        deadline_str = self._extract_deadline(soup_element)
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
            days_until = (deadline - datetime.now()).days
            
            if days_until <= 14:
                return 'Tier 1 - Urgent'
            elif days_until <= 30:
                return 'Tier 2 - High Priority'
            else:
                return 'Tier 3 - Standard'
        except:
            return 'Tier 3 - Standard'
    
    def get_all_leads(self):
        """Aggregate leads from all sources"""
        all_leads = []
        
        print("Scraping Buy and Sell...")
        all_leads.extend(self.scrape_buyandsell())
        
        print("Scraping MERX...")
        all_leads.extend(self.scrape_merx())
        
        print("Scraping news sources...")
        all_leads.extend(self.scrape_news())
        
        # Remove duplicates based on opportunity title
        df = pd.DataFrame(all_leads)
        if not df.empty:
            df = df.drop_duplicates(subset=['opportunity'], keep='first')
            all_leads = df.to_dict('records')
        
        return all_leads