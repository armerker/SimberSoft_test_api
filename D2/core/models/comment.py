from pydantic import BaseModel, field_validator
from typing import Optional, Dict, Any
from datetime import datetime


class CommentContent(BaseModel):
    rendered: str
    raw: Optional[str] = None


class CommentAvatarUrls(BaseModel):
    """Аватары автора — ключи как в API"""
    size_24: str
    size_48: str
    size_96: str

    @field_validator('size_24', 'size_48', 'size_96', mode='before')
    def convert_keys(cls, v, info):
        """Преобразуем ключи из API в имена полей"""
        if isinstance(v, dict):
            return {
                'size_24': v.get('24', ''),
                'size_48': v.get('48', ''),
                'size_96': v.get('96', '')
            }
        return v


class CommentModel(BaseModel):
    id: int
    post: int
    author_name: str
    author_email: Optional[str] = ""
    author_url: Optional[str] = ""
    content: CommentContent
    status: str
    author_avatar_urls: Optional[Dict[str, str]] = None
    date: Optional[datetime] = None
    date_gmt: Optional[datetime] = None
    link: Optional[str] = None
    type: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None
    _links: Optional[Dict[str, Any]] = None

    @field_validator('author_avatar_urls', mode='before')
    def parse_avatar_urls(cls, v):
        """Принимаем любые ключи"""
        if isinstance(v, dict):
            return v
        return v


class CommentCreate(BaseModel):
    post: int
    content: str
    author_name: Optional[str] = None
    author_email: Optional[str] = None
    author_url: Optional[str] = None


class CommentUpdate(BaseModel):
    """Модель для обновления комментария"""
    content: Optional[str] = None
    author_name: Optional[str] = None
    author_email: Optional[str] = None
    author_url: Optional[str] = None
    status: Optional[str] = None