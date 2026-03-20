# core/models/post.py

import re
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PostTitle(BaseModel):
    rendered: str

    @property
    def clean(self) -> str:
        """Возвращает чистый заголовок без HTML"""
        return re.sub(r'<[^>]+>', '', self.rendered).strip()


class PostContent(BaseModel):
    rendered: str
    protected: bool = False

    @property
    def clean(self) -> str:
        """Возвращает чистое содержание без HTML"""
        return re.sub(r'<[^>]+>', '', self.rendered).strip()


class PostModel(BaseModel):
    id: int
    title: PostTitle
    content: PostContent
    status: str
    author: int
    date: datetime
    modified: datetime


class PostCreate(BaseModel):
    title: str
    content: str
    status: str = "publish"


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None