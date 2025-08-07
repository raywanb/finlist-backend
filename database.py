from supabase import create_client, Client
import os
from typing import List, Optional, Dict, Any
import numpy as np
from openai import OpenAI
from datetime import datetime
import json

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

class DatabaseManager:
    def __init__(self):
        self.supabase = supabase
        self.openai_client = openai_client
    
    def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for text using OpenAI's text-embedding-ada-002 model"""
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Failed to generate embeddings: {str(e)}")
    
    def _convert_datetime_to_string(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert datetime objects to ISO format strings for JSON serialization"""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, datetime):
                    data[key] = value.isoformat()
                elif isinstance(value, dict):
                    data[key] = self._convert_datetime_to_string(value)
                elif isinstance(value, list):
                    data[key] = [self._convert_datetime_to_string(item) if isinstance(item, dict) else item for item in value]
        return data
    
    def _convert_embeddings_string_to_list(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert embeddings string back to list of floats"""
        if isinstance(data, dict):
            for key, value in data.items():
                if key == 'embeddings' and isinstance(value, str):
                    try:
                        # Remove brackets and split by comma, then convert to float
                        embeddings_str = value.strip('[]')
                        data[key] = [float(x.strip()) for x in embeddings_str.split(',')]
                    except:
                        data[key] = None
                elif isinstance(value, dict):
                    data[key] = self._convert_embeddings_string_to_list(value)
                elif isinstance(value, list):
                    data[key] = [self._convert_embeddings_string_to_list(item) if isinstance(item, dict) else item for item in value]
        return data
    
    async def create_article(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new article with embeddings"""
        # Generate embeddings from title and content
        text_for_embedding = f"{article_data['title']} {article_data['content']}"
        embeddings = self.generate_embeddings(text_for_embedding)
        
        # Add embeddings to article data
        article_data['embeddings'] = embeddings
        
        # Insert into database
        result = self.supabase.table('articles').insert(article_data).execute()
        if result.data:
            # Convert datetime to string and embeddings string to list
            result_data = self._convert_datetime_to_string(result.data[0])
            result_data = self._convert_embeddings_string_to_list(result_data)
            return result_data
        return None
    
    async def get_article(self, article_id: int) -> Optional[Dict[str, Any]]:
        """Get article by ID"""
        result = self.supabase.table('articles').select('*').eq('id', article_id).execute()
        if result.data:
            result_data = self._convert_datetime_to_string(result.data[0])
            result_data = self._convert_embeddings_string_to_list(result_data)
            return result_data
        return None
    
    async def get_article_by_title(self, title: str, exact_match: bool = True) -> Optional[Dict[str, Any]]:
        """Get article by title (exact match or partial match)"""
        if exact_match:
            # Exact match
            result = self.supabase.table('articles').select('*').eq('title', title).execute()
        else:
            # Partial match using ILIKE (case-insensitive)
            result = self.supabase.table('articles').select('*').ilike('title', f'%{title}%').execute()
        
        if result.data:
            result_data = self._convert_datetime_to_string(result.data[0])
            result_data = self._convert_embeddings_string_to_list(result_data)
            return result_data
        return None
    
    async def search_articles_by_title(self, title: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search articles by title (partial match, returns multiple results)"""
        result = self.supabase.table('articles').select('*').ilike('title', f'%{title}%').limit(limit).execute()
        articles = []
        for article in result.data:
            article_data = self._convert_datetime_to_string(article)
            article_data = self._convert_embeddings_string_to_list(article_data)
            articles.append(article_data)
        return articles
    
    async def get_all_articles(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all articles with limit"""
        result = self.supabase.table('articles').select('*').limit(limit).execute()
        articles = []
        for article in result.data:
            article_data = self._convert_datetime_to_string(article)
            article_data = self._convert_embeddings_string_to_list(article_data)
            articles.append(article_data)
        return articles
    
    async def search_articles_semantic(self, query: str, limit: int = 10, match_threshold: float = 0.78) -> List[Dict[str, Any]]:
        """Search articles using pgvector similarity search with OpenAI embeddings"""
        # Generate embeddings for the search query
        query_embedding = self.generate_embeddings(query)
        
        # Use pgvector's cosine similarity search
        # This uses the native pgvector extension for efficient similarity search
        result = self.supabase.rpc(
            'match_articles',
            {
                'query_embedding': query_embedding,
                'match_threshold': match_threshold,
                'match_count': limit
            }
        ).execute()
        
        articles = []
        for article in (result.data or []):
            article_data = self._convert_datetime_to_string(article)
            article_data = self._convert_embeddings_string_to_list(article_data)
            articles.append(article_data)
        return articles
    
    async def search_articles_by_category(self, category: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search articles by category"""
        result = self.supabase.table('articles').select('*').eq('category', category).limit(limit).execute()
        articles = []
        for article in result.data:
            article_data = self._convert_datetime_to_string(article)
            article_data = self._convert_embeddings_string_to_list(article_data)
            articles.append(article_data)
        return articles
    
    async def get_categories(self) -> List[str]:
        """Get all unique categories"""
        result = self.supabase.table('articles').select('category').execute()
        categories = [article['category'] for article in result.data]
        return list(set(categories))
    
    async def hybrid_search(self, query: str, category: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Hybrid search combining semantic search with category filtering"""
        query_embedding = self.generate_embeddings(query)
        
        # Build the search parameters
        search_params = {
            'query_embedding': query_embedding,
            'match_threshold': 0.78,
            'match_count': limit
        }
        
        # Add category filter if specified
        if category:
            search_params['category_filter'] = category
        
        # Use the hybrid search function
        result = self.supabase.rpc(
            'hybrid_search_articles',
            search_params
        ).execute()
        
        articles = []
        for article in (result.data or []):
            article_data = self._convert_datetime_to_string(article)
            article_data = self._convert_embeddings_string_to_list(article_data)
            articles.append(article_data)
        return articles

# Global database manager instance
db = DatabaseManager() 