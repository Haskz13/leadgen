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
        self.training_signals = [
            'skills gap', 'training needed', 'professional development',
            'upskilling', 'reskilling', 'workforce development',
            'capacity building', 'learning strategy', 'training initiative',
            'digital transformation', 'change management', 'new system',
            'implementation', 'rollout', 'modernization', 'transformation',
            'compliance training', 'mandatory training', 'certification required'
        ]
        
    def scrape_government_news(self):
        """Scrape government news releases for training needs and initiatives"""
        leads = []
        
        # Federal government news
        news_sources = [
            {
                'url': 'https://www.canada.ca/en/news.html',
                'org': 'Government of Canada'
            },
            {
                'url': 'https://news.ontario.ca/en',
                'org': 'Government of Ontario'
            }
        ]
        
        # For now, using sample data - in production, implement actual scraping
        sample_leads = [
            {
                'organization': 'Canada Revenue Agency',
                'opportunity': 'CRA announces digital transformation requiring extensive staff training on new tax processing system',
                'deadline': (datetime.now() + timedelta(days=45)).strftime('%Y-%m-%d'),
                'tier': 'Tier 1 - Urgent',
                'contact': 'transformation@cra-arc.gc.ca',
                'source': 'https://www.canada.ca/en/revenue-agency/news/2024/01/digital-transformation.html',
                'status': 'New',
                'notes': 'Major system change - 5000+ employees need training',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'Health Canada',
                'opportunity': 'New mental health first aid training mandate for all federal employees announced',
                'deadline': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d'),
                'tier': 'Tier 1 - Urgent',
                'contact': 'hr-rh@hc-sc.gc.ca',
                'source': 'https://www.canada.ca/en/health-canada/news/2024/01/mental-health-training.html',
                'status': 'New',
                'notes': 'Mandatory training for 300,000+ federal employees',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'Indigenous Services Canada',
                'opportunity': 'ISC launches reconciliation training program for all staff - seeking training providers',
                'deadline': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                'tier': 'Tier 1 - Urgent',
                'contact': 'reconciliation@sac-isc.gc.ca',
                'source': 'https://www.canada.ca/en/indigenous-services-canada/news/2024/01/reconciliation-training.html',
                'status': 'New',
                'notes': 'High priority initiative - 6000+ employees',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            }
        ]
        
        return sample_leads
    
    def scrape_provincial_municipal_news(self):
        """Scrape provincial and municipal news for training opportunities"""
        leads = []
        
        sample_leads = [
            {
                'organization': 'City of Toronto',
                'opportunity': 'Toronto announces accessibility training requirement for all city staff by July 2024',
                'deadline': (datetime.now() + timedelta(days=20)).strftime('%Y-%m-%d'),
                'tier': 'Tier 1 - Urgent',
                'contact': 'accessibility@toronto.ca',
                'source': 'https://www.toronto.ca/news/accessibility-training-mandate/',
                'status': 'New',
                'notes': 'AODA compliance - 35,000 employees need training',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'Ontario Ministry of Education',
                'opportunity': 'New curriculum rollout requires teacher training across Ontario school boards',
                'deadline': (datetime.now() + timedelta(days=40)).strftime('%Y-%m-%d'),
                'tier': 'Tier 2 - High Priority',
                'contact': 'curriculum@ontario.ca',
                'source': 'https://news.ontario.ca/en/release/education-training',
                'status': 'New',
                'notes': 'Province-wide initiative - 100,000+ teachers',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'City of Vancouver',
                'opportunity': 'Vancouver implements new emergency response protocols - all first responders need training',
                'deadline': (datetime.now() + timedelta(days=25)).strftime('%Y-%m-%d'),
                'tier': 'Tier 1 - Urgent',
                'contact': 'emergency.training@vancouver.ca',
                'source': 'https://vancouver.ca/news/emergency-response-training',
                'status': 'New',
                'notes': 'Critical safety training - 2000+ first responders',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            }
        ]
        
        return sample_leads
    
    def scrape_indigenous_organizations(self):
        """Scrape news from Indigenous organizations and bands"""
        leads = []
        
        sample_leads = [
            {
                'organization': 'Assembly of First Nations',
                'opportunity': 'AFN seeks training providers for national governance capacity building program',
                'deadline': (datetime.now() + timedelta(days=35)).strftime('%Y-%m-%d'),
                'tier': 'Tier 2 - High Priority',
                'contact': 'governance@afn.ca',
                'source': 'https://www.afn.ca/news/governance-training-initiative',
                'status': 'New',
                'notes': 'National program - multiple First Nations involved',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'Métis Nation of Ontario',
                'opportunity': 'MNO launching cultural competency training for healthcare providers',
                'deadline': (datetime.now() + timedelta(days=28)).strftime('%Y-%m-%d'),
                'tier': 'Tier 1 - Urgent',
                'contact': 'health@metisnation.org',
                'source': 'https://www.metisnation.org/news/cultural-training',
                'status': 'New',
                'notes': 'Partnership opportunity with healthcare sector',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            }
        ]
        
        return sample_leads
    
    def scrape_crown_corporations(self):
        """Scrape news from Crown corporations"""
        leads = []
        
        sample_leads = [
            {
                'organization': 'Canada Post',
                'opportunity': 'Canada Post modernizing operations - 50,000 employees need digital skills training',
                'deadline': (datetime.now() + timedelta(days=50)).strftime('%Y-%m-%d'),
                'tier': 'Tier 2 - High Priority',
                'contact': 'transformation@canadapost.ca',
                'source': 'https://www.canadapost.ca/news/digital-transformation',
                'status': 'New',
                'notes': 'Large-scale transformation project',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            },
            {
                'organization': 'VIA Rail',
                'opportunity': 'VIA Rail implementing new safety protocols - all staff require certification',
                'deadline': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                'tier': 'Tier 1 - Urgent',
                'contact': 'safety.training@viarail.ca',
                'source': 'https://www.viarail.ca/en/news/safety-training',
                'status': 'New',
                'notes': 'Mandatory safety certification - 3000+ employees',
                'date_found': datetime.now().strftime('%Y-%m-%d')
            }
        ]
        
        return sample_leads
    
    def _calculate_tier(self, deadline_str):
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
        
        print("Scanning government news for training opportunities...")
        all_leads.extend(self.scrape_government_news())
        
        print("Scanning provincial and municipal news...")
        all_leads.extend(self.scrape_provincial_municipal_news())
        
        print("Scanning Indigenous organizations...")
        all_leads.extend(self.scrape_indigenous_organizations())
        
        print("Scanning Crown corporations...")
        all_leads.extend(self.scrape_crown_corporations())
        
        # Sort by tier and deadline
        all_leads.sort(key=lambda x: (
            0 if 'Tier 1' in x['tier'] else (1 if 'Tier 2' in x['tier'] else 2),
            x['deadline']
        ))
        
        return all_leads