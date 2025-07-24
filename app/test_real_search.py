#!/usr/bin/env python3
"""Test script to verify real web search is working"""

from scraper import CanadianPublicSectorScraper
import json

def test_real_search():
    print("Testing real web search functionality...")
    print("=" * 70)
    
    scraper = CanadianPublicSectorScraper()
    
    # Test a single search query
    test_query = "canada government training 2025"
    print(f"\nTest Query: {test_query}")
    print("-" * 70)
    
    results = scraper.search_web_scrape(test_query)
    
    print(f"\nResults found: {len(results)}")
    
    if results:
        print("\nFirst 3 results:")
        for i, result in enumerate(results[:3], 1):
            print(f"\n{i}. Title: {result.get('title', 'N/A')}")
            print(f"   Link: {result.get('link', 'N/A')}")
            print(f"   Snippet: {result.get('snippet', 'N/A')[:100]}...")
            
            # Test lead extraction
            lead = scraper.extract_lead_from_result(result, "Test Category")
            if lead:
                print(f"   ✅ Extracted as valid lead:")
                print(f"      Organization: {lead['organization']}")
                print(f"      Tier: {lead['tier']}")
                print(f"      Analysis: {lead.get('critical_analysis', 'N/A')[:100]}...")
            else:
                print(f"   ❌ Not identified as valid training opportunity")
    else:
        print("\n⚠️ No results found. This could be due to:")
        print("   - Search engines blocking automated requests")
        print("   - Network connectivity issues")
        print("   - Need for different search terms")
    
    print("\n" + "=" * 70)
    print("Test complete.")

if __name__ == "__main__":
    test_real_search()