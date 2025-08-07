#!/usr/bin/env python3
"""
Test script for the Article Crawler
Helps test different crawler configurations
"""

import asyncio
import sys
import os
from crawler import ArticleCrawler, SECTORS

async def test_single_sector():
    """Test crawling for a single sector"""
    print("🧪 Testing single sector crawling...")
    crawler = ArticleCrawler()
    
    # Test with technology sector
    await crawler.run_crawling_cycle("technology")
    print("✅ Single sector test complete!")

async def test_all_sectors():
    """Test crawling for all sectors"""
    print("🧪 Testing all sectors crawling...")
    crawler = ArticleCrawler()
    
    await crawler.run_crawling_cycle_all_sectors()
    print("✅ All sectors test complete!")

async def test_specific_sector(sector: str):
    """Test crawling for a specific sector"""
    if sector not in SECTORS:
        print(f"❌ Invalid sector: {sector}")
        print(f"Available sectors: {list(SECTORS.keys())}")
        return
    
    print(f"🧪 Testing {sector} sector crawling...")
    crawler = ArticleCrawler()
    
    await crawler.run_crawling_cycle(sector)
    print(f"✅ {sector} sector test complete!")

def test_scheduler():
    """Test the scheduler functionality"""
    print("🧪 Testing scheduler functionality...")
    crawler = ArticleCrawler()
    
    # Test scheduler with a short delay
    print("📅 Starting scheduler test (will run in 10 seconds)...")
    crawler.start_scheduler("09:00", "technology", False)
    
    # Let it run for a bit to test
    import time
    time.sleep(15)
    
    crawler.stop_scheduler()
    print("✅ Scheduler test complete!")

def print_usage():
    """Print usage information"""
    print("🚀 Article Crawler Test Script")
    print("\nUsage:")
    print("  python test_crawler.py single          # Test single sector (technology)")
    print("  python test_crawler.py all             # Test all sectors")
    print("  python test_crawler.py sector <name>   # Test specific sector")
    print("  python test_crawler.py scheduler       # Test scheduler functionality")
    print("\nAvailable sectors:")
    for key, value in SECTORS.items():
        print(f"  - {key}: {value['name']}")

async def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    
    command = sys.argv[1].lower()
    
    if command == "single":
        await test_single_sector()
    elif command == "all":
        await test_all_sectors()
    elif command == "sector":
        if len(sys.argv) < 3:
            print("❌ Please specify a sector name")
            print(f"Available sectors: {list(SECTORS.keys())}")
            return
        sector = sys.argv[2].lower()
        await test_specific_sector(sector)
    elif command == "scheduler":
        test_scheduler()
    else:
        print(f"❌ Unknown command: {command}")
        print_usage()

if __name__ == "__main__":
    asyncio.run(main()) 