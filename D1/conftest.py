from http.client import responses

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.api_client import WordPressAPI
from core.db_client import WordPressDB

@pytest.fixture(scope = "function")
def api():
    """Фикстура для API клиента"""
    return WordPressAPI()
@pytest.fixture(scope = "function")
def db():
    """Фикстиру для бд клиета"""
    db = WordPressDB()
    yield db
    db.close()

@pytest.fixture
def post_data():
    """Фикстура с тестовыми данными для поста"""
    return {
        "title" : "Тестовый пост от 19.03.2026",
        "content" : "Это содержание тестового поста, созданного через API для проверки создания постов",
        "status" : "publish"
    }
@pytest.fixture
def comment_data():
    """Фикстура с тестовыми данными для комента"""
    return {
        "post_id" : 1,
        "content" : "Тестовый комментарий",
        "author_name" : "Автоматический тестер",
        "author_email" : "autotester@example.com",
        "author_url" : "https://example.com",
    }
@pytest.fixture
def delete_post_data():
    """Фикстура данных пост для удаления"""
    return {
        "title": "Тестовый пост для удаления",
        "content": "Это содержание тестового поста для удаления",
        "status": "publish"

    }

@pytest.fixture
def delete_comment_data():
    """Фикстура данных коммент для удаления"""
    return {
        "post_id": 1,
        "content": "Тестовый комментарий для удаления",
        "author_name": "Автоматический тестер для удаления",
        "author_email": "autotester@example.com",
        "author_url": "https://example.com",

    }


@pytest.fixture
def test_post(api,db):
    """Фикстура создает посл для тестов потом удаляет"""
    response = api.create_post(title="тестовый пост",content="содержание тестового поста")

    post_id = response.json()["id"]
    db_post = db.get_post(post_id)
    if db_post is None:
        print(f"❌ ПОСТ НЕ СОЗДАЛСЯ В БД! ID: {post_id}")

    yield post_id

    api.delete_post(post_id)
@pytest.fixture
def test_comment(api,db):
    """Фикстура создает и удаляет комент"""
    response = api.create_comment(
        post_id = 1,
        content = " тестовый контент",
        author_name = "тестер",
        author_email =  "autotester@example.com",
        author_url =  "https://example.com"

    )

    comment_id = response.json()["id"]
    yield comment_id
    api.delete_comment(comment_id)