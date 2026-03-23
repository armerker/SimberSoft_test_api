import pytest
import sys
import os
from faker import Faker
from datetime import datetime
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.api_client import WordPressAPI
from core.db_client import WordPressDB
from core.models import PostCreate, CommentCreate, PostModel

fake = Faker("ru_RU")

@pytest.fixture(scope="function")
def api() -> WordPressAPI:
    """Инициализирует обертку WordPressSteps для работы с API через Allure-шаги."""
    return WordPressAPI()

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

@pytest.fixture
def create_test_posts(db):
    created_ids = []

    def _generate(count=5, **kwargs):
        for i in range(count):
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            payload = {
                "post_title": f"Test Post {i} {fake.word()}",
                "post_content": "Content",
                "post_status": "publish",
                "post_author": 1,
                "post_excerpt": "",
                "to_ping": "",
                "pinged": "",
                "post_content_filtered": "",
                "post_date": now,
                "post_date_gmt": now,
                "post_modified": now,
                "post_modified_gmt": now,
                **kwargs
            }

            post_id = db.insert_post(payload)
            created_ids.append(post_id)
        return created_ids

    yield _generate


    for post_id in created_ids:
        db.delete_post(post_id)

@pytest.fixture
def create_test_comments(db):
    created_ids = []

    def _generate(count=3, **kwargs):
        for i in range(count):
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            payload = {
                "comment_post_ID": 1,
                "comment_author": f"[AUTOTEST] User {i}",
                "comment_content": f"Test Comment Content {i}",
                "comment_date": now,
                "comment_date_gmt": now,
                "comment_approved": "1",
                "comment_agent": "Pytest",
                "comment_type": "comment",
                **kwargs
            }

            comment_id = db.insert_comments(payload)
            created_ids.append(comment_id)
        return created_ids

    yield _generate

    for cid in created_ids:
        db.delete_comments(cid)