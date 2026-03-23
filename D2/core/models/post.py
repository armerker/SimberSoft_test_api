from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import re



class ContentModel(BaseModel):
    rendered: str

    @property
    def clean(self) -> str:
        """Возвращает чистый заголовок без HTML"""
        return re.sub(r'<[^>]+>', '', self.rendered).strip()

    protected: bool


class TitleModel(BaseModel):
    rendered: str


class ExcerptModel(BaseModel):
    rendered: str

    @property
    def clean(self) -> str:
        """Возвращает чистый заголовок без HTML"""
        return re.sub(r'<[^>]+>', '', self.rendered).strip()

    protected: bool

class PostModel(BaseModel):
    id : int
    title: TitleModel
    content: ContentModel
    excerpt: ExcerptModel
    author: int
    format: str
    status: str
    date: datetime
    modified: datetime

class PostCreate(BaseModel):
    title: str
    content: str
    status: str = "publish"


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None








