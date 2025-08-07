from pydantic import BaseModel, EmailStr, field_serializer
from typing import List, Optional
from datetime import datetime
import numpy as np

class ArticleBase(BaseModel):
    title: str
    content: str
    category: str
    author: str
    source_url: Optional[str] = None

class ArticleCreate(ArticleBase):
    pass

class Article(ArticleBase):
    id: int
    date: datetime
    embeddings: Optional[List[float]] = None
    
    @field_serializer('date')
    def serialize_date(self, value: datetime) -> str:
        return value.isoformat()
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    articles: Optional[List[int]] = None
    
    class Config:
        from_attributes = True

class SearchQuery(BaseModel):
    query: str
    limit: Optional[int] = 10

class CategoryFilter(BaseModel):
    category: str
    limit: Optional[int] = 10 