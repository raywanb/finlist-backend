#!/usr/bin/env python3
"""
Simplified Article Crawler with GPT Researcher
A single file that handles web crawling and article generation
"""

import asyncio
import logging
import argparse
import signal
import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database directly
from database import db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

# Prompt template
TOPIC_PROMPT = """
Latest articles from this past day {date} in the {sector} sector. Focus on {topics}. 
Include news about the latest news, breakthroughs, and applications in various industries.
Provide a overview of the articles and their implications for their stocks and global markets.
The articles should be from reputable sources and include a summary of the key points.
"""

# Predefined sectors
SECTORS = {
    "technology": {
        "name": "Technology",
        "topics": "AI, machine learning, semiconductors, cloud computing, cybersecurity, fintech"
    },
    # "healthcare": {
    #     "name": "Healthcare", 
    #     "topics": "biotech, pharmaceuticals, medical devices, AI in healthcare, drug development"
    # },
    "finance": {
        "name": "Finance",
        "topics": "fintech, digital banking, cryptocurrency, blockchain, investment trends"
    },
    # "energy": {
    #     "name": "Energy",
    #     "topics": "renewable energy, electric vehicles, battery technology, clean energy"
    # },
    # "automotive": {
    #     "name": "Automotive",
    #     "topics": "electric vehicles, autonomous driving, automotive technology, EV charging"
    # }
}

def get_current_date():
    """Get current date in YYYY-MM-DD format"""
    return datetime.now().strftime("%Y-%m-%d")

def format_prompt(sector: str, topics: str = None, date: str = None) -> str:
    """Format the TOPIC_PROMPT with specific parameters"""
    if date is None:
        date = get_current_date()
    
    if topics is None and sector in SECTORS:
        topics = SECTORS[sector]["topics"]
    elif topics is None:
        topics = "latest developments and trends"
    
    sector_name = SECTORS.get(sector, {}).get("name", sector.title())
    
    return TOPIC_PROMPT.format(
        date=date,
        sector=sector_name,
        topics=topics
    )

class ArticleCrawler:
    """Simplified web crawler agent using GPT Researcher"""
    
    def __init__(self, crawl_interval: int = 86400):  # Changed default to 24 hours
        self.crawl_interval = crawl_interval
        self.is_running = False
        self.current_sector_index = 0
        self.sector_keys = list(SECTORS.keys())
        
    async def crawl_for_articles(self, sector: str = "technology") -> List[Dict[str, Any]]:
        """Use GPT Researcher to crawl for articles based on sector"""
        try:
            from gpt_researcher import GPTResearcher
            
            query = format_prompt(sector)
            logger.info(f"Researching {sector} sector with query: {query[:100]}...")
            
            researcher = GPTResearcher(
                query=query, 
                report_type="research_report"
            )
            
            logger.info("Conducting research...")
            research_result = await researcher.conduct_research()
            
            logger.info("Generating report...")
            report = await researcher.write_report()
            
            article = self._convert_report_to_article(report, sector)
            return [article] if article else []
            
        except ImportError:
            logger.error("GPT Researcher not installed. Please install it with: pip install gpt-researcher")
            return []
        except Exception as e:
            logger.error(f"Error in GPT Researcher: {str(e)}")
            return []
    
    def _convert_report_to_article(self, report: str, sector: str) -> Optional[Dict[str, Any]]:
        """Convert GPT Researcher report to article format"""
        try:
            lines = report.strip().split('\n')
            title = lines[0] if lines and lines[0].strip() else f"{SECTORS.get(sector, {}).get('name', sector.title())} Sector Analysis - {get_current_date()}"
            
            title = title.replace('#', '').strip()
            if len(title) > 500:
                title = title[:497] + "..."
            
            content = report.strip()
            author = "AI Research Assistant"
            category = SECTORS.get(sector, {}).get("name", sector.title())
            
            return {
                "title": title,
                "content": content,
                "author": author,
                "category": category,
                "source_url": "Generated by GPT Researcher",
                "published_date": get_current_date()
            }
            
        except Exception as e:
            logger.error(f"Error converting report to article: {str(e)}")
            return None
    
    async def process_and_save_articles(self, articles: List[Dict[str, Any]]) -> int:
        """Process crawled articles and save them to the database"""
        saved_count = 0
        
        for article in articles:
            try:
                required_fields = ["title", "content", "author", "category"]
                if not all(field in article for field in required_fields):
                    logger.warning(f"Skipping article with missing fields: {article.get('title', 'Unknown')}")
                    continue
                
                existing_article = await db.get_article_by_title(article["title"], exact_match=True)
                if existing_article:
                    logger.info(f"Article already exists: {article['title']}")
                    continue
                
                article_data = {
                    "title": article["title"],
                    "content": article["content"],
                    "author": article["author"],
                    "category": article["category"]
                }
                
                if "source_url" in article:
                    article_data["source_url"] = article["source_url"]
                
                saved_article = await db.create_article(article_data)
                if saved_article:
                    saved_count += 1
                    logger.info(f"Successfully saved article: {article['title']}")
                else:
                    logger.error(f"Failed to save article: {article['title']}")
                    
            except Exception as e:
                logger.error(f"Error processing article {article.get('title', 'Unknown')}: {str(e)}")
                continue
        
        return saved_count
    
    async def run_crawling_cycle(self, sector: str = "technology"):
        """Run one complete crawling cycle"""
        try:
            logger.info(f"Starting crawling cycle for {sector} sector...")
            
            articles = await self.crawl_for_articles(sector)
            
            if not articles:
                logger.info("No new articles found in this cycle")
                return
            
            logger.info(f"Found {len(articles)} potential articles")
            
            saved_count = await self.process_and_save_articles(articles)
            
            logger.info(f"Crawling cycle complete. Saved {saved_count}/{len(articles)} articles")
            
        except Exception as e:
            logger.error(f"Error in crawling cycle: {str(e)}")
    
    async def run_crawling_cycle_all_sectors(self):
        """Run crawling cycle for all sectors"""
        try:
            logger.info("Starting crawling cycle for all sectors...")
            total_saved = 0
            
            for sector in self.sector_keys:
                try:
                    logger.info(f"Processing sector: {sector}")
                    articles = await self.crawl_for_articles(sector)
                    
                    if articles:
                        saved_count = await self.process_and_save_articles(articles)
                        total_saved += saved_count
                        logger.info(f"Saved {saved_count} articles for {sector} sector")
                    else:
                        logger.info(f"No articles found for {sector} sector")
                    
                    # Add a small delay between sectors to avoid overwhelming the API
                    await asyncio.sleep(30)
                    
                except Exception as e:
                    logger.error(f"Error processing sector {sector}: {str(e)}")
                    continue
            
            logger.info(f"All sectors crawling complete. Total saved: {total_saved} articles")
            
        except Exception as e:
            logger.error(f"Error in all sectors crawling cycle: {str(e)}")
    
    async def start_periodic_crawling(self, sector: str = "technology", all_sectors: bool = False):
        """Start the periodic crawling process"""
        self.is_running = True
        
        if all_sectors:
            logger.info(f"Starting periodic crawling for all sectors every {self.crawl_interval} seconds")
        else:
            logger.info(f"Starting periodic crawling for {sector} sector every {self.crawl_interval} seconds")
        
        while self.is_running:
            try:
                if all_sectors:
                    await self.run_crawling_cycle_all_sectors()
                else:
                    await self.run_crawling_cycle(sector)
                
                await asyncio.sleep(self.crawl_interval)
                
            except asyncio.CancelledError:
                logger.info("Crawling task cancelled")
                break
            except Exception as e:
                logger.error(f"Unexpected error in crawling loop: {str(e)}")
                await asyncio.sleep(60)
    
    def stop_crawling(self):
        """Stop the periodic crawling process"""
        self.is_running = False
        logger.info("Stopping periodic crawling")

# Global crawler instance
crawler = ArticleCrawler()

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print("\n🛑 Received shutdown signal. Stopping crawler...")
    crawler.stop_crawling()
    sys.exit(0)

async def main():
    parser = argparse.ArgumentParser(description='Article Crawler with GPT Researcher')
    parser.add_argument('--test', action='store_true', 
                       help='Run a single test cycle instead of continuous crawling')
    parser.add_argument('--interval', type=int, default=86400,  # Changed default to 24 hours
                       help='Crawling interval in seconds (default: 86400 = 24 hours)')
    parser.add_argument('--sector', type=str, default='technology',
                       choices=list(SECTORS.keys()),
                       help='Sector to research (default: technology)')
    parser.add_argument('--all-sectors', action='store_true',
                       help='Crawl all sectors instead of just one')
    
    args = parser.parse_args()
    
    # Validate environment variables
    if not all([SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY]):
        print("❌ Missing environment variables. Please check your .env file:")
        print(f"   SUPABASE_URL: {'✅' if SUPABASE_URL else '❌'}")
        print(f"   SUPABASE_KEY: {'✅' if SUPABASE_KEY else '❌'}")
        print(f"   OPENAI_API_KEY: {'✅' if OPENAI_API_KEY else '❌'}")
        sys.exit(1)
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🚀 Article Crawler with GPT Researcher")
    
    if args.all_sectors:
        print("📊 Sectors: All sectors")
        print("🔍 Topics: All predefined topics")
    else:
        print(f"📊 Sector: {SECTORS[args.sector]['name']}")
        print(f"🔍 Topics: {SECTORS[args.sector]['topics']}")
    
    print(f"⏰ Crawling interval: {args.interval} seconds ({args.interval // 3600} hours)")
    
    try:
        if args.test:
            print("🧪 Running test cycle...")
            if args.all_sectors:
                await crawler.run_crawling_cycle_all_sectors()
            else:
                await crawler.run_crawling_cycle(args.sector)
            print("✅ Test cycle complete!")
        else:
            print("🔄 Starting continuous crawling...")
            await crawler.start_periodic_crawling(args.sector, args.all_sectors)
            
    except KeyboardInterrupt:
        print("\n🛑 Crawler stopped by user")
    except Exception as e:
        print(f"💥 Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 