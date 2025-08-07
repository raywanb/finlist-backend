# Article Crawler with GPT Researcher

A simplified, single-file crawler that automatically generates stock analysis articles using GPT Researcher and saves them to your Supabase database.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Make sure your `.env` file has:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
OPENAI_API_KEY=your_openai_api_key
```

### 3. Test the System
```bash
# Test with technology sector
python crawler.py --test --sector technology

# Test with healthcare sector  
python crawler.py --test --sector healthcare
```

### 4. Run Continuous Crawling
```bash
# Run continuous crawling for all sectors (default - 24 hours)
python crawler.py --all-sectors

# Run continuous crawling for technology sector only
python crawler.py --sector technology

# Run for specific sector
python crawler.py --sector healthcare

# Run with custom interval (12 hours)
python crawler.py --all-sectors --interval 43200

# Run single test cycle for all sectors
python crawler.py --test --all-sectors

# Run single test cycle for specific sector
python crawler.py --test --sector energy
```

## 📊 Available Sectors

| Sector | Focus Areas |
|--------|-------------|
| **technology** | AI, machine learning, semiconductors, cloud computing, cybersecurity, fintech |
| **healthcare** | biotech, pharmaceuticals, medical devices, AI in healthcare, drug development |
| **finance** | fintech, digital banking, cryptocurrency, blockchain, investment trends |
| **energy** | renewable energy, electric vehicles, battery technology, clean energy |
| **automotive** | electric vehicles, autonomous driving, automotive technology, EV charging |

## 🔧 How It Works

### **Single File Structure** (`crawler.py`)
Everything is contained in one file:
- Environment variable loading
- Prompt template and sector definitions
- GPT Researcher integration
- Database operations
- CLI interface

### **Process Flow:**
1. **Prompt Generation** → Uses your custom prompt template
2. **GPT Researcher** → Conducts web research based on prompt
3. **Report Generation** → Creates comprehensive analysis
4. **Article Conversion** → Converts report to article format
5. **Database Save** → Saves to Supabase with automatic embeddings
6. **API Availability** → Article immediately available through your API

## 📁 File Structure

```
├── crawler.py              # Single file containing everything
├── database.py             # Database operations (existing)
├── models.py               # Pydantic models (existing)
├── routes.py               # API routes (existing)
├── main.py                 # FastAPI app (existing)
└── CRAWLER_README.md       # This file
```

## 🧪 Testing

### Using the Test Script
```bash
# Test all sectors at once
python test_crawler.py all

# Test single sector (technology)
python test_crawler.py single

# Test specific sector
python test_crawler.py sector healthcare
python test_crawler.py sector finance

# Test scheduler functionality
python test_crawler.py scheduler
```

### Test Individual Sectors
```bash
python crawler.py --test --sector technology
python crawler.py --test --sector healthcare
python crawler.py --test --sector finance
```

### Test All Sectors
```bash
python crawler.py --test --all-sectors
```

### Test Single Cycle
```bash
python crawler.py --test --sector energy
```

## 🔄 Scheduled Operation

### Default Behavior (Daily at 9 AM)
The crawler now runs once per day at 9:00 AM and processes all sectors by default.

### Start Scheduled Crawling
```bash
# Default: technology sector, every hour
python crawler.py

# Custom sector and interval
python crawler.py --sector healthcare --interval 7200  # 2 hours
```

### Stop Crawling
Press `Ctrl+C` to gracefully stop the crawler.

## 📝 Generated Article Format

Each generated article includes:
- **Title**: Extracted from report or auto-generated
- **Content**: Full GPT Researcher report
- **Author**: "AI Research Assistant"
- **Category**: Mapped from sector
- **Embeddings**: Automatically generated using OpenAI
- **Date**: Current date

## ⚙️ Configuration

### Custom Sectors
Add new sectors directly in `crawler.py`:
```python
SECTORS = {
    "your_sector": {
        "name": "Your Sector Name",
        "topics": "topic1, topic2, topic3"
    }
}
```

### Custom Prompts
Modify the `TOPIC_PROMPT` in `crawler.py` to change the research focus.

### Crawling Interval
Set the interval in seconds:
```bash
python crawler.py --interval 1800  # 30 minutes
```

## 🐛 Troubleshooting

### GPT Researcher Not Installed
```bash
pip install gpt-researcher
```

### Missing Environment Variables
The crawler will check and display which variables are missing:
```bash
python crawler.py
# Output: ❌ Missing environment variables. Please check your .env file:
#    SUPABASE_URL: ❌
#    SUPABASE_KEY: ❌
#    OPENAI_API_KEY: ❌
```

### OpenAI API Issues
- Check your `OPENAI_API_KEY` in `.env`
- Ensure you have sufficient credits
- Check rate limits

### Database Connection Issues
- Verify Supabase credentials in `.env`
- Check network connectivity
- Ensure database schema is set up

## 📈 Monitoring

The crawler provides detailed logging:
- Research progress
- Article generation status
- Database save operations
- Error handling

## 🔒 Security Considerations

- Store API keys securely in `.env`
- Monitor OpenAI usage and costs
- Implement rate limiting if needed
- Consider content filtering for generated articles

## 🚀 Production Deployment

### Docker (Recommended)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "crawler.py"]
```

### Systemd Service
Create `/etc/systemd/system/article-crawler.service`:
```ini
[Unit]
Description=Article Crawler Service
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/your/app
ExecStart=/usr/bin/python3 crawler.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Cron Job
```bash
# Run every hour
0 * * * * cd /path/to/your/app && python crawler.py --test --sector technology
```

## 📞 Support

For issues or questions:
1. Check the logs for error messages
2. Verify all environment variables are set
3. Test with `--test` flag first
4. Ensure GPT Researcher is properly installed

## 🔄 Integration with API

The generated articles are automatically available through your existing API endpoints:
- `GET /api/v1/articles/` - List all articles
- `GET /api/v1/articles/search` - Semantic search
- `GET /api/v1/articles/category/{category}` - Filter by category

## 🎯 Key Features

- **Single File**: Everything in one `crawler.py` file
- **No Config Classes**: Direct environment variable imports
- **Simple CLI**: Easy command-line interface
- **Automatic Embeddings**: OpenAI embeddings generated automatically
- **Duplicate Detection**: Prevents duplicate articles
- **Error Handling**: Comprehensive error handling and logging
- **Graceful Shutdown**: Handles Ctrl+C properly
- **Multi-Sector Support**: Crawl all sectors or specific sectors
- **Daily Scheduling**: Runs once per day by default (24-hour intervals)
- **Sector Rotation**: Processes all sectors in sequence with delays
- **Test Script**: Easy testing with `test_crawler.py`

## 🆕 New Features (v2.0)

### Daily Crawling Schedule
- **Default Interval**: Changed from 1 hour to 24 hours (86400 seconds)
- **All Sectors**: New `--all-sectors` flag to crawl all sectors
- **Sector Rotation**: Processes each sector with 30-second delays between them

### Enhanced Testing
- **Test Script**: New `test_crawler.py` for easy testing
- **All Sectors Test**: Test all sectors at once
- **Individual Sector Tests**: Test specific sectors

### Docker Updates
- **Updated Dockerfile**: Now runs with `--all-sectors` by default
- **24-hour Schedule**: Docker container runs daily instead of hourly 