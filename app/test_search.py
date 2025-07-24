#!/usr/bin/env python3
"""
Quick test to see if web searching is working
"""

from scraper import CanadianPublicSectorScraper
import json

def test_single_search():
    scraper = CanadianPublicSectorScraper()
    
    # Test a simple search
    query = '"Government of Canada" training program 2025'
    print(f"\n🔍 Testing search for: {query}")
    
    results = scraper.search_web_scrape(query)
    
    print(f"\n📊 Raw search results: {len(results)} found")
    for i, result in enumerate(results[:3]):
        print(f"\n--- Result {i+1} ---")
        print(f"Title: {result.get('title', 'N/A')}")
        print(f"Link: {result.get('link', 'N/A')}")
        print(f"Snippet: {result.get('snippet', 'N/A')[:200]}...")
        
        # Test lead extraction
        lead = scraper.extract_lead_from_result(result, "Test Category")
        if lead:
            print(f"✅ Extracted as lead: {lead['organization']} - {lead['tier']}")
        else:
            print("❌ Not extracted as lead")

if __name__ == "__main__":
    test_single_search()