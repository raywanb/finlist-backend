from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from models import Article, ArticleCreate, User, UserCreate, SearchQuery, CategoryFilter
from database import db
from datetime import datetime

router = APIRouter()

# Article routes
@router.post("/articles/", response_model=Article)
async def create_article(article: ArticleCreate):
    """Create a new article"""
    try:
        article_data = article.dict()
        # Let the database handle the date with its default value
        
        result = await db.create_article(article_data)
        if result:
            return Article(**result)
        else:
            raise HTTPException(status_code=500, detail="Failed to create article")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/articles/", response_model=List[Article])
async def get_articles(limit: int = 50):
    """Get all articles with optional limit"""
    try:
        articles = await db.get_all_articles(limit)
        return [Article(**article) for article in articles]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/articles/{article_id}", response_model=Article)
async def get_article(article_id: int):
    """Get a specific article by ID"""
    try:
        article = await db.get_article(article_id)
        if article:
            return Article(**article)
        else:
            raise HTTPException(status_code=404, detail="Article not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/articles/title/{title}", response_model=Article)
async def get_article_by_title(title: str, exact_match: bool = True):
    """Get a specific article by title (exact match or partial match)"""
    try:
        article = await db.get_article_by_title(title, exact_match)
        if article:
            return Article(**article)
        else:
            raise HTTPException(status_code=404, detail="Article not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/articles/search-title/{title}", response_model=List[Article])
async def search_articles_by_title(title: str, limit: int = 10):
    """Search articles by title (partial match, returns multiple results)"""
    try:
        articles = await db.search_articles_by_title(title, limit)
        return [Article(**article) for article in articles]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/articles/search", response_model=List[Article])
async def search_articles(search_query: SearchQuery):
    """Search articles using semantic search with pgvector"""
    try:
        articles = await db.search_articles_semantic(search_query.query, search_query.limit)
        return [Article(**article) for article in articles]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/articles/hybrid-search", response_model=List[Article])
async def hybrid_search_articles(search_query: SearchQuery, category: Optional[str] = None):
    """Hybrid search combining semantic search with category filtering"""
    try:
        articles = await db.hybrid_search(search_query.query, category, search_query.limit)
        return [Article(**article) for article in articles]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/articles/category/{category}", response_model=List[Article])
async def get_articles_by_category(category: str, limit: int = 10):
    """Get articles by category"""
    try:
        articles = await db.search_articles_by_category(category, limit)
        return [Article(**article) for article in articles]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories/", response_model=List[str])
async def get_categories():
    """Get all available categories"""
    try:
        categories = await db.get_categories()
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# User routes (basic structure for future implementation)
@router.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    """Create a new user (placeholder for future implementation)"""
    # This is a placeholder - in a real implementation, you'd hash the password
    # and store the user in the database
    raise HTTPException(status_code=501, detail="User creation not implemented yet")

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get a specific user by ID (placeholder for future implementation)"""
    raise HTTPException(status_code=501, detail="User retrieval not implemented yet")

@router.get("/users/{user_id}/articles", response_model=List[Article])
async def get_user_articles(user_id: int):
    """Get articles by a specific user (placeholder for future implementation)"""
    raise HTTPException(status_code=501, detail="User articles retrieval not implemented yet") 