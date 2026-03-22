import pytest
import allure
import sys
import os
from core.models.post import PostCreate, PostModel  # ← добавить PostModel

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


@allure.title("TC-01. Создание нового поста")
def test_tc01_create_post(api, db, post_payload_factory) -> None:
    payload = post_payload_factory()
    post = api.create_post(payload)

    assert post.id > 0
    assert post.title.clean == payload.title
    assert post.content.clean == payload.content
    assert post.status == "publish"

    db_post = db.get_post(post.id)
    assert db_post is not None
    assert db_post['post_title'] == payload.title
    assert db_post['post_content'] == payload.content
    assert db_post['post_status'] == payload.status
    assert db_post['post_author'] == api.user_id

    api.delete_post(post.id)

@allure.title("TC-02. Редактирование существующего поста")
def test_tc02_update(api, db, test_post, post_payload_factory) -> None:
    """TC-02. Редактирование существующего поста с полной проверкой сохранности данных"""
    post_id = test_post.id


    orig_post = db.get_post(post_id)
    orig_date = orig_post['post_date']
    orig_type = orig_post['post_type']
    orig_author = orig_post['post_author']
    orig_comment_count = orig_post['comment_count']


    new_data = post_payload_factory()


    updated_post = api.update_post(post_id, title=new_data.title, content=new_data.content)


    assert updated_post.id == post_id
    assert updated_post.title.clean == new_data.title
    assert updated_post.content.clean == new_data.content

    # Проверки БД (твои важные ассерты)
    db_post = db.get_post(post_id)
    assert db_post['post_title'] == new_data.title
    assert db_post['post_content'] == new_data.content
    assert db_post["post_date"] == orig_date
    assert db_post['post_author'] == orig_author
    assert db_post['post_type'] == orig_type
    assert db_post['comment_count'] == orig_comment_count


@allure.title("TC-03. Удаление поста (перемещение в корзину)")
def test_tc03_delete_post(api, db, post_payload_factory) -> None:
    """TC-03. Удаление поста"""

    payload = post_payload_factory()
    post = api.create_post(payload)
    post_id = post.id


    deleted_post = api.delete_post(post_id)

    assert deleted_post.id == post_id
    assert deleted_post.title.clean == payload.title

    db_post = db.get_post(post_id)
    assert db_post is not None
    assert db_post['post_status'] == 'trash'

    get_post = api.get_post(post_id)
    assert get_post.id == post_id
    assert get_post.status == 'trash'