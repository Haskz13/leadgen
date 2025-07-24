#!/usr/bin/env python3
"""Quick test to check scraper functionality"""

import sys
import time
from scraper import CanadianPublicSectorScraper

def test_scraper():
    print("Testing scraper with timeout...")
    scraper = CanadianPublicSectorScraper()
    
    # Test a single search
    start_time = time.time()
    print("\nSearching for training opportunities...")
    
    try:
        # Just do one quick search
        results = scraper.search_web_scrape("canada government training 2025", timeout=5)
        elapsed = time.time() - start_time
        
        print(f"\nSearch completed in {elapsed:.2f} seconds")
        print(f"Found {len(results)} results")
        
        if results:
            print("\nFirst result:")
            print(f"Title: {results[0].get('title', 'N/A')}")
            print(f"Link: {results[0].get('link', 'N/A')}")
        else:
            print("\nNo results found")
            
    except Exception as e:
        print(f"\nError during search: {e}")
        
    print("\nTest complete")

if __name__ == "__main__":
    test_scraper()