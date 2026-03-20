from http.client import responses

import pytest
import sys
import os
from typing import Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.api_client import WordPressAPI
from core.db_client import WordPressDB
from core.models import PostCreate, CommentCreate, PostModel


@pytest.fixture(scope="function")
def api() -> WordPressAPI:
    """Фикстура для API клиента"""
    return WordPressAPI()


@pytest.fixture(scope="function")
def db() -> WordPressDB:
    """Фикстура для БД клиента"""
    db = WordPressDB()
    yield db
    db.close()


@pytest.fixture
def post_data() -> PostCreate:
    """Фикстура с тестовыми данными для поста"""
    return PostCreate(
        title="Тестовый пост от 19.03.2026",
        content="Это содержание тестового поста, созданного через API для проверки создания постов",
        status="publish"
    )


@pytest.fixture
def comment_data() -> CommentCreate:
    """Фикстура с тестовыми данными для комментария"""
    return CommentCreate(
        post=1,
        content="Тестовый комментарий",
        author_name="Автоматический тестер",
        author_email="autotester@example.com",
        author_url="https://example.com"
    )


@pytest.fixture
def delete_post_data() -> PostCreate:
    """Фикстура данных пост для удаления"""
    return PostCreate(
        title="Тестовый пост для удаления",
        content="Это содержание тестового поста для удаления",
        status="publish"
    )


@pytest.fixture
def delete_comment_data() -> CommentCreate:
    """Фикстура данных коммент для удаления"""
    return CommentCreate(
        post=1,
        content="Тестовый комментарий для удаления",
        author_name="Автоматический тестер для удаления",
        author_email="autotester@example.com",
        author_url="https://example.com"
    )


@pytest.fixture
def test_post(api, db) -> PostModel:
    """Фикстура создает пост для тестов и возвращает модель"""
    post_data = PostCreate(
        title="тестовый пост",
        content="содержание тестового поста"
    )
    post = api.create_post(post_data)

    db_post = db.get_post(post.id)
    if db_post is None:
        print(f"❌ ПОСТ НЕ СОЗДАЛСЯ В БД! ID: {post.id}")

    yield post

    api.delete_post(post.id)


@pytest.fixture
def test_comment(api, db) -> int:
    """Фикстура создает и удаляет комментарий"""
    # Сначала создаем пост
    post_data = PostCreate(
        title="Пост для комментария",
        content="Содержание для теста комментариев"
    )
    post = api.create_post(post_data)

    # Создаем комментарий
    comment_data = CommentCreate(
        post=post.id,
        content="тестовый контент",
        author_name="тестер",
        author_email="autotester@example.com",
        author_url="https://example.com"
    )
    comment = api.create_comment(comment_data)
    comment_id = comment.id

    yield comment_id

    api.delete_comment(comment_id)
    api.delete_post(post.id)