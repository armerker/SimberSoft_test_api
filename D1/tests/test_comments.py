import pytest
import sys
import os
from core.models import CommentCreate, CommentModel, PostCreate

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_tc04_create_comment(api, db, comment_data: CommentCreate) -> None:
    """TC-04. Создание нового комментария"""

    # Создаем пост
    post = api.create_post(PostCreate(
        title="Пост для комментария",
        content="Содержание"
    ))

    # Привязываем комментарий к этому посту
    comment_data.post = post.id

    #  Используем модель
    comment = api.create_comment(comment_data)

    assert comment.id > 0
    assert comment.post == comment_data.post
    assert comment.content.raw == comment_data.content
    assert comment.author_name == comment_data.author_name

    db_comment = db.get_comment(comment.id)
    assert db_comment is not None

    api.delete_comment(comment.id)
    api.delete_post(post.id)


def test_tc05_update_comment(api, db, test_comment: int) -> None:
    """TC-05. Редактирование комментария"""
    comment_id = test_comment

    orig_comment = db.get_comment(comment_id)
    orig_date = orig_comment['comment_date']
    orig_post_id = orig_comment['comment_post_ID']
    orig_author = orig_comment['comment_author']

    new_content = "Этот комментарий был отредактирован через API"

    updated_comment = api.update_comment(comment_id, new_content)

    assert updated_comment.id == comment_id
    assert updated_comment.content.raw == new_content

    db_comment = db.get_comment(comment_id)
    assert db_comment['comment_content'] == new_content
    assert db_comment['comment_date'] == orig_date
    assert db_comment['comment_post_ID'] == orig_post_id
    assert db_comment['comment_author'] == orig_author


def test_tc06_delete_comment(api, db, delete_comment_data: CommentCreate) -> None:
    """TC-06. Удаление комментария"""

    # Создаем пост
    post = api.create_post(PostCreate(
        title="Пост для удаления комментария",
        content="Содержание"
    ))

    delete_comment_data.post = post.id

    #  Используем модель
    comment = api.create_comment(delete_comment_data)
    comment_id = comment.id

    assert db.get_comment(comment_id) is not None

    deleted_comment = api.delete_comment(comment_id)

    assert deleted_comment.id == comment_id
    assert deleted_comment.content.raw == delete_comment_data.content

    db_comment = db.get_comment(comment_id)
    assert db_comment is not None
    assert db_comment['comment_approved'] == 'trash'

    api.delete_post(post.id)