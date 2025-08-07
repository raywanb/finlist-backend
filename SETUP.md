# Stock Analysis API Setup Guide

## Prerequisites
- Python 3.8+
- Supabase account and project
- pgvector extension enabled in Supabase
- OpenAI API key

## Step 1: Set up Supabase Database

### 1.1 Enable pgvector extension
In your Supabase dashboard:
1. Go to your project
2. Navigate to Database → Extensions
3. Enable the `pgvector` extension (this is crucial for vector similarity search)

### 1.2 Create the database schema
1. Go to SQL Editor in your Supabase dashboard
2. Copy and paste the contents of `schema.sql`
3. Run the SQL script

This will create:
- `articles` table with vector embeddings support (1536 dimensions for OpenAI ada-002)
- `users` table with article references
- **pgvector functions** for efficient similarity search:
  - `match_articles()` - Pure semantic search using cosine similarity
  - `hybrid_search_articles()` - Combined semantic + category filtering
- Proper GIN indexes for vector performance
- Sample data for testing

## Step 2: Configure Environment Variables

Create a `.env` file in your project root:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
OPENAI_API_KEY=your_openai_api_key
```

You can find these values in:
- Supabase dashboard under Settings → API
- OpenAI dashboard at https://platform.openai.com/account/api-keys

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Run the Application

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Step 5: Test the API

The API will be available at `http://localhost:8000`

### Available Endpoints:

#### Articles
- `GET /api/v1/articles/` - Get all articles
- `GET /api/v1/articles/{id}` - Get specific article
- `POST /api/v1/articles/` - Create new article
- `POST /api/v1/articles/search` - **Semantic search using pgvector + OpenAI ada-002**
- `POST /api/v1/articles/hybrid-search` - **Hybrid search (semantic + category)**
- `GET /api/v1/articles/category/{category}` - Search by category
- `GET /api/v1/categories/` - Get all categories

#### Users (Placeholder endpoints)
- `POST /api/v1/users/` - Create user (not implemented)
- `GET /api/v1/users/{id}` - Get user (not implemented)
- `GET /api/v1/users/{id}/articles` - Get user articles (not implemented)

### Interactive API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation.

## Testing Examples

### Create an Article
```bash
curl -X POST "http://localhost:8000/api/v1/articles/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Apple Stock Analysis",
    "content": "Apple continues to dominate the smartphone market with strong iPhone sales and growing services revenue.",
    "category": "Technology",
    "author": "John Doe"
  }'
```

### Semantic Search (using OpenAI ada-002 + pgvector)
```bash
curl -X POST "http://localhost:8000/api/v1/articles/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "electric vehicles",
    "limit": 5
  }'
```

### Hybrid Search (semantic + category)
```bash
curl -X POST "http://localhost:8000/api/v1/articles/hybrid-search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "artificial intelligence",
    "limit": 5
  }' \
  -G \
  -d "category=Technology"
```

### Get Articles by Category
```bash
curl "http://localhost:8000/api/v1/articles/category/Technology"
```

## Key Features

### 🚀 **OpenAI + pgvector Integration**
- **OpenAI text-embedding-ada-002 model** for high-quality embeddings
- **1536-dimensional vectors** for superior semantic understanding
- **Native vector similarity search** using PostgreSQL's pgvector extension
- **Cosine similarity** calculations performed at the database level
- **GIN indexes** for optimal vector search performance

### 🔍 **Search Capabilities**
1. **Semantic Search**: Find articles based on meaning, not just keywords
2. **Hybrid Search**: Combine semantic search with category filtering
3. **Category Filtering**: Traditional filtering by article category
4. **Configurable thresholds**: Adjust similarity thresholds (default: 0.78)

### 📊 **Performance Optimizations**
- Vector indexes for fast similarity calculations
- Efficient RPC functions for complex queries
- Proper indexing on frequently queried columns
- OpenAI's optimized embedding model for better semantic understanding

## Notes

1. **OpenAI Embeddings**: The system uses OpenAI's `text-embedding-ada-002` model for generating 1536-dimensional embeddings, which provides superior semantic understanding compared to smaller models.

2. **pgvector Functions**: 
   - `match_articles()`: Pure semantic search with configurable threshold
   - `hybrid_search_articles()`: Semantic search with optional category filtering

3. **Performance**: The schema includes proper GIN indexes for optimal vector search performance.

4. **Security**: Row Level Security (RLS) is enabled with basic policies. You may want to customize these based on your authentication requirements.

5. **Future Enhancements**: User authentication and password hashing will need to be implemented when you're ready to add login functionality.

6. **API Costs**: Using OpenAI's embedding API will incur costs based on the number of tokens processed. Monitor your usage at https://platform.openai.com/usage.

## Troubleshooting

1. **pgvector not available**: Make sure you've enabled the pgvector extension in Supabase. This is essential for vector search functionality.

2. **OpenAI API errors**: Verify your OpenAI API key is correct and has sufficient credits.

3. **Vector dimension mismatch**: The schema uses 1536 dimensions for OpenAI's text-embedding-ada-002 model. If you change models, update the vector dimension in the schema.

4. **Connection errors**: Verify your Supabase URL and API key are correct.

5. **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`.

6. **Search not working**: Ensure the pgvector functions (`match_articles`, `hybrid_search_articles`) were created successfully in your database.

7. **Rate limiting**: OpenAI has rate limits. Consider implementing caching for frequently searched queries.

## References

- [Supabase pgvector Documentation](https://supabase.com/docs/guides/ai/examples/nextjs-vector-search)
- [OpenAI Embeddings API Documentation](https://platform.openai.com/docs/guides/embeddings)
- [pgvector GitHub Repository](https://github.com/pgvector/pgvector) 