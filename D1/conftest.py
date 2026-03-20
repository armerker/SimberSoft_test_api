import pytest
import sys
import os
from faker import Faker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.api_steps import WordPressSteps
from core.db_client import WordPressDB
from core.models import PostCreate, CommentCreate, PostModel

fake = Faker("ru_RU")

@pytest.fixture(scope="function")
def api() -> WordPressSteps:
    """Инициализирует обертку WordPressSteps для работы с API через Allure-шаги."""
    return WordPressSteps()

@pytest.fixture(scope="function")
def db() -> WordPressDB:
    """Создает подключение к БД и закрывает его после завершения теста."""
    db = WordPressDB()
    yield db
    db.close()

@pytest.fixture
def post_payload_factory():
    """Возвращает функцию для генерации случайных данных поста (модель PostCreate)."""
    def _make_payload(**kwargs):
        payload = {
            "title": fake.sentence(nb_words=5),
            "content": fake.paragraph(nb_sentences=3),
            "status": "publish"
        }
        payload.update(kwargs)
        return PostCreate(**payload)
    return _make_payload

@pytest.fixture
def post_data(post_payload_factory) -> PostCreate:
    """Фикстура, возвращающая один готовый набор случайных данных для поста."""
    return post_payload_factory()

@pytest.fixture
def post_factory(api, post_payload_factory):
    """Возвращает функцию для создания реального поста в WordPress через API."""
    def _create_post(**kwargs):
        payload = post_payload_factory(**kwargs)
        return api.create_post(payload)
    return _create_post

@pytest.fixture
def comment_payload_factory():
    """Возвращает функцию для генерации данных комментария (требует post_id)."""
    def _make_payload(post_id, **kwargs):
        payload = {
            "post": post_id,
            "content": fake.sentence(),
            "author_name": fake.name(),
            "author_email": fake.email(),
            "author_url": fake.url()
        }
        payload.update(kwargs)
        return CommentCreate(**payload)
    return _make_payload

@pytest.fixture
def comment_factory(api, comment_payload_factory):
    """Возвращает функцию для создания реального комментария через API."""
    def _create_comment(post_id, **kwargs):
        payload = comment_payload_factory(post_id, **kwargs)
        return api.create_comment(payload)
    return _create_comment

@pytest.fixture
def test_post(api, post_factory) -> PostModel:
    """Создает пост перед тестом и автоматически удаляет его после (yield)."""
    post = post_factory()
    yield post
    api.delete_post(post.id)

@pytest.fixture
def test_comment(api, test_post, comment_factory):
    """Создает комментарий к test_post и автоматически удаляет его после теста."""
    comment = comment_factory(test_post.id)
    yield comment
    api.delete_comment(comment.id)
