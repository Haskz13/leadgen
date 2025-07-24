import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time

class RealCanadianOpportunityScraper:
    """
    Scrapes REAL opportunities from actual Canadian government sources
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.opportunities = []
    
    def scrape_canada_buyandsell(self):
        """Scrape real opportunities from BuyandSell.gc.ca"""
        print("🔍 Searching BuyandSell.gc.ca for training opportunities...")
        
        # Search for training-related tenders
        search_terms = ["training", "professional development", "learning", "education"]
        base_url = "https://buyandsell.gc.ca/procurement-data/search/site"
        
        for term in search_terms:
            try:
                url = f"{base_url}/{term}"
                response = requests.get(url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Parse actual tender listings
                    results = soup.find_all('div', class_='search-result')
                    for result in results[:5]:  # Get first 5 per search
                        title_elem = result.find('h3')
                        if title_elem and 'training' in title_elem.text.lower():
                            self.opportunities.append({
                                'source': 'BuyandSell.gc.ca',
                                'title': title_elem.text.strip(),
                                'url': 'https://buyandsell.gc.ca' + title_elem.find('a')['href'],
                                'type': 'Federal'
                            })
            except Exception as e:
                print(f"Error searching {term}: {e}")
    
    def scrape_merx(self):
        """Scrape real opportunities from MERX"""
        print("🔍 Searching MERX for training opportunities...")
        
        try:
            # MERX public opportunities
            url = "https://www.merx.com/public/solicitations"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Look for training-related opportunities
                listings = soup.find_all('div', class_='tender-list-item')
                for listing in listings[:10]:
                    title = listing.find('h4')
                    if title and any(word in title.text.lower() for word in ['training', 'learning', 'development']):
                        self.opportunities.append({
                            'source': 'MERX',
                            'title': title.text.strip(),
                            'url': 'https://www.merx.com' + listing.find('a')['href'],
                            'type': 'Various'
                        })
        except Exception as e:
            print(f"Error scraping MERX: {e}")
    
    def scrape_ontario_tenders(self):
        """Scrape real opportunities from Ontario Tenders Portal"""
        print("🔍 Searching Ontario Tenders Portal...")
        
        try:
            url = "https://www.doingbusiness.mgs.gov.on.ca/mbs/psb/psb.nsf/English/BidsOpen"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Parse Ontario government tenders
                # Implementation depends on actual site structure
                pass
        except Exception as e:
            print(f"Error scraping Ontario: {e}")
    
    def search_with_duckduckgo(self):
        """Use DuckDuckGo to find real opportunities"""
        print("🔍 Searching with DuckDuckGo for recent opportunities...")
        
        queries = [
            "site:buyandsell.gc.ca training RFP 2025",
            "site:merx.com professional development tender",
            "Canadian government training contract opportunity",
            "site:*.gc.ca request for proposal training 2025"
        ]
        
        for query in queries:
            try:
                url = f"https://duckduckgo.com/html/?q={query}"
                response = requests.get(url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    results = soup.find_all('div', class_='result')
                    for result in results[:3]:
                        link = result.find('a', class_='result__a')
                        if link:
                            self.opportunities.append({
                                'source': 'Web Search',
                                'title': link.text.strip(),
                                'url': link['href'],
                                'type': 'Found via search'
                            })
            except Exception as e:
                print(f"Error with search {query}: {e}")
    
    def get_all_real_opportunities(self):
        """Get all real opportunities from multiple sources"""
        print("\n" + "="*60)
        print("🚀 SEARCHING FOR REAL CANADIAN TRAINING OPPORTUNITIES")
        print("="*60)
        
        # Scrape from multiple real sources
        self.scrape_canada_buyandsell()
        self.scrape_merx()
        self.scrape_ontario_tenders()
        self.search_with_duckduckgo()
        
        print(f"\n✅ Found {len(self.opportunities)} REAL opportunities")
        print("="*60)
        
        return self.opportunities

# Test the real scraper
if __name__ == "__main__":
    scraper = RealCanadianOpportunityScraper()
    real_opps = scraper.get_all_real_opportunities()
    
    print("\nREAL OPPORTUNITIES FOUND:")
    for i, opp in enumerate(real_opps[:10], 1):
        print(f"\n{i}. {opp['title']}")
        print(f"   Source: {opp['source']}")
        print(f"   URL: {opp['url']}")
        print(f"   Type: {opp['type']}")