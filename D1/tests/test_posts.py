import pytest
import sys
import os
from core.models.post import PostCreate, PostModel  # ← добавить PostModel

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_tc01_create_post(api, db, post_data: PostCreate) -> None:
    """TC-01. Создание нового поста"""
    post = api.create_post(post_data)

    assert post.id > 0
    assert post.title.clean == post_data.title
    assert post.content.clean == post_data.content
    assert post.status == "publish"

    db_post = db.get_post(post.id)
    assert db_post is not None
    assert db_post['post_title'] == post_data.title
    assert db_post['post_content'] == post_data.content
    assert db_post['post_status'] == "publish"
    assert db_post['post_author'] == 1

    api.delete_post(post.id)


def test_tc02_update(api, db, test_post: PostModel) -> None:
    """TC-02. Редактирование существующего поста"""
    post_id = test_post.id  # ← берем id из модели

    orig_post = db.get_post(post_id)
    orig_date = orig_post['post_date']
    orig_type = orig_post['post_type']
    orig_author = orig_post['post_author']
    orig_comment_count = orig_post['comment_count']

    new_title = "ИЗМЕНЕНО: Тестовый пост"
    new_content = "Это содержание было обновлено через API"

    updated_post = api.update_post(post_id, new_title, new_content)

    assert updated_post.id == post_id
    assert updated_post.title.clean == new_title
    assert updated_post.content.clean == new_content

    db_post = db.get_post(post_id)
    assert db_post['post_title'] == new_title
    assert db_post['post_content'] == new_content
    assert db_post["post_date"] == orig_date
    assert db_post['post_author'] == orig_author
    assert db_post['post_type'] == orig_type
    assert db_post['comment_count'] == orig_comment_count


def test_tc03_delete_post(api, db, delete_post_data: PostCreate) -> None:
    """TC-03. Удаление поста"""
    post = api.create_post(delete_post_data)
    post_id = post.id

    deleted_post = api.delete_post(post_id)

    assert deleted_post.id == post_id
    assert deleted_post.title.clean == delete_post_data.title
    assert deleted_post.content.clean == delete_post_data.content

    db_post = db.get_post(post_id)
    assert db_post is not None
    assert db_post['post_status'] == 'trash'

    get_post = api.get_post(post_id)
    assert get_post.id == post_id