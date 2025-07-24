"""
Advanced Web Search Integration Example
======================================

This file shows how to integrate real web search APIs to find Canadian public sector
training opportunities. In production, you would use one of these approaches:

1. Google Custom Search API
2. Bing Web Search API
3. SerpAPI (aggregates multiple search engines)
4. Web scraping with Selenium for dynamic content
"""

import os
from datetime import datetime, timedelta

class AdvancedTrainingLeadSearcher:
    """
    Production-ready lead searcher using real web search APIs
    """
    
    def __init__(self):
        # API keys would be stored in environment variables
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.google_cx = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
        self.bing_api_key = os.getenv('BING_API_KEY')
        
    def search_with_google(self, query, num_results=10):
        """
        Use Google Custom Search API to find training opportunities
        
        Setup:
        1. Create a Google Cloud project
        2. Enable Custom Search API
        3. Create a custom search engine at https://cse.google.com
        4. Get your API key and search engine ID
        """
        import requests
        
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': self.google_api_key,
            'cx': self.google_cx,
            'q': query,
            'num': num_results,
            'dateRestrict': 'd30',  # Last 30 days
            'gl': 'ca',  # Canada
            'lr': 'lang_en|lang_fr'  # English and French
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            results = response.json()
            return self._parse_google_results(results)
        return []
    
    def search_with_bing(self, query, market='en-CA'):
        """
        Use Bing Web Search API for finding opportunities
        
        Setup:
        1. Create Azure account
        2. Create Bing Search resource
        3. Get API key from Azure portal
        """
        import requests
        
        headers = {'Ocp-Apim-Subscription-Key': self.bing_api_key}
        params = {
            'q': query,
            'mkt': market,
            'freshness': 'Month',  # Recent results
            'count': 20
        }
        
        url = 'https://api.cognitive.microsoft.com/bing/v7.0/search'
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            return self._parse_bing_results(response.json())
        return []
    
    def search_with_serpapi(self, query):
        """
        Use SerpAPI for comprehensive search results
        
        SerpAPI aggregates results from multiple search engines
        and handles proxies, CAPTCHAs, etc.
        """
        from serpapi import GoogleSearch
        
        params = {
            "q": query,
            "location": "Canada",
            "hl": "en",
            "gl": "ca",
            "google_domain": "google.ca",
            "api_key": os.getenv('SERPAPI_KEY'),
            "num": 20,
            "tbs": "qdr:m"  # Past month
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        return self._parse_serp_results(results)
    
    def extract_training_leads(self, search_results):
        """
        Extract actionable training leads from search results
        """
        leads = []
        
        for result in search_results:
            # Analyze the result to determine if it's a training opportunity
            if self._is_training_opportunity(result):
                lead = {
                    'organization': self._extract_organization(result),
                    'opportunity': result['title'],
                    'deadline': self._estimate_deadline(result),
                    'tier': self._calculate_tier(result),
                    'contact': self._extract_contact(result),
                    'source': result['link'],
                    'status': 'New',
                    'notes': result.get('snippet', '')[:200],
                    'date_found': datetime.now().strftime('%Y-%m-%d')
                }
                leads.append(lead)
        
        return leads
    
    def _is_training_opportunity(self, result):
        """
        Use NLP or keyword matching to determine if this is a real opportunity
        """
        indicators = [
            'grant recipient', 'awarded funding', 'training program',
            'seeking providers', 'RFP', 'tender', 'mandatory training',
            'digital transformation', 'system implementation',
            'compliance deadline', 'certification required'
        ]
        
        text = f"{result.get('title', '')} {result.get('snippet', '')}".lower()
        return any(indicator in text for indicator in indicators)
    
    def _extract_organization(self, result):
        """
        Extract organization name from search result
        Could use NER (Named Entity Recognition) for better accuracy
        """
        # Simple extraction from title or URL
        title = result.get('title', '')
        if '-' in title:
            return title.split('-')[0].strip()
        return 'Unknown Organization'
    
    def _estimate_deadline(self, result):
        """
        Estimate deadline based on content analysis
        """
        snippet = result.get('snippet', '').lower()
        
        # Look for deadline indicators
        if any(word in snippet for word in ['urgent', 'immediate', 'asap']):
            days = 14
        elif any(word in snippet for word in ['deadline', 'by july', 'summer']):
            days = 30
        elif 'q3' in snippet or 'fall' in snippet:
            days = 60
        else:
            days = 45
        
        return (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
    
    def _calculate_tier(self, result):
        """
        Calculate urgency tier based on various factors
        """
        snippet = result.get('snippet', '').lower()
        
        # Tier 1 indicators
        if any(word in snippet for word in ['urgent', 'immediate', 'deadline approaching']):
            return 'Tier 1 - Urgent'
        
        # Tier 2 indicators
        if any(word in snippet for word in ['new', 'announced', 'launching']):
            return 'Tier 2 - High Priority'
        
        return 'Tier 3 - Standard'
    
    def run_comprehensive_search(self):
        """
        Run a comprehensive search using multiple strategies
        """
        all_leads = []
        
        # Define search queries for different types of opportunities
        search_queries = {
            'grant_recipients': [
                '"grant recipient" training "professional development" site:canada.ca 2024',
                'ESDC "skills development" "funding awarded" 2024',
                '"Indigenous Services Canada" grant training "capacity building"'
            ],
            'digital_transformations': [
                '"Government of Canada" "digital transformation" "employee training"',
                'CRA "modernization" "staff training" announcement',
                '"Service Canada" "new system" training rollout'
            ],
            'compliance_mandates': [
                'AODA "compliance training" deadline 2024 Ontario',
                '"mandatory training" "all staff" government Canada 2024',
                '"Truth and Reconciliation" training requirement government'
            ],
            'sector_specific': [
                'healthcare "training mandate" Ontario 2024',
                '"emergency services" certification training Canada',
                'education "professional development" requirement 2024'
            ]
        }
        
        # Run searches across all categories
        for category, queries in search_queries.items():
            print(f"\nSearching for {category.replace('_', ' ').title()}...")
            
            for query in queries:
                # Use multiple search engines for comprehensive results
                results = []
                
                # Google Search
                if self.google_api_key:
                    results.extend(self.search_with_google(query))
                
                # Bing Search
                if self.bing_api_key:
                    results.extend(self.search_with_bing(query))
                
                # Extract leads from results
                leads = self.extract_training_leads(results)
                all_leads.extend(leads)
                
                print(f"  Found {len(leads)} leads for: {query[:50]}...")
        
        # Remove duplicates and sort by priority
        all_leads = self._deduplicate_and_sort(all_leads)
        
        return all_leads
    
    def _deduplicate_and_sort(self, leads):
        """
        Remove duplicate leads and sort by priority
        """
        import pandas as pd
        
        if not leads:
            return []
        
        df = pd.DataFrame(leads)
        df = df.drop_duplicates(subset=['opportunity'], keep='first')
        
        # Sort by tier and deadline
        df['tier_rank'] = df['tier'].map({
            'Tier 1 - Urgent': 0,
            'Tier 2 - High Priority': 1,
            'Tier 3 - Standard': 2
        })
        
        df = df.sort_values(['tier_rank', 'deadline'])
        
        return df.to_dict('records')


# Example usage:
if __name__ == "__main__":
    # This would be used in production with real API keys
    searcher = AdvancedTrainingLeadSearcher()
    
    print("=" * 60)
    print("ADVANCED CANADIAN PUBLIC SECTOR TRAINING LEAD SEARCH")
    print("=" * 60)
    print("\nThis example shows how to integrate real web search APIs.")
    print("To use in production:")
    print("1. Sign up for Google Custom Search API")
    print("2. Get Bing Search API key from Azure")
    print("3. Consider SerpAPI for easier integration")
    print("4. Set API keys as environment variables")
    print("\nWith real APIs, you would find hundreds of current opportunities!")
    print("=" * 60)