import pytest
import allure
from core.models import CommentCreate, CommentModel, PostCreate


@allure.title("TC-04. Создание нового комментария")
def test_tc04_create_comment(api, db, post_factory, comment_payload_factory) -> None:
    post = post_factory()
    payload = comment_payload_factory(post.id)

    comment = api.create_comment(payload)

    assert comment.id > 0
    assert comment.post == payload.post
    assert comment.content.raw == payload.content
    assert comment.author_name == payload.author_name

    db_comment = db.get_comment(comment.id)
    assert db_comment is not None
    assert db_comment['comment_post_ID'] == payload.post
    assert db_comment['comment_author'] == payload.author_name

    api.delete_comment(comment.id)
    api.delete_post(post.id)

@allure.title("TC-05. Редактирование текста комментария")
def test_tc05_update_comment(api, db, test_comment, comment_payload_factory) -> None:
    comment_id = test_comment.id

    orig_comment = db.get_comment(comment_id)
    orig_date = orig_comment['comment_date']
    orig_post_id = orig_comment['comment_post_ID']
    orig_author = orig_comment['comment_author']

    new_data = comment_payload_factory(post_id=orig_post_id)
    new_content = new_data.content

    updated_comment = api.update_comment(comment_id, new_content)

    assert updated_comment.id == comment_id
    assert updated_comment.content.raw == new_content

    db_comment = db.get_comment(comment_id)
    assert db_comment['comment_content'] == new_content
    assert db_comment['comment_date'] == orig_date
    assert db_comment['comment_post_ID'] == orig_post_id
    assert db_comment['comment_author'] == orig_author

@allure.title("TC-06. Удаление комментария (перемещение в корзину)")
def test_tc06_delete_comment(api, db, post_factory, comment_payload_factory) -> None:
    post = post_factory()
    payload = comment_payload_factory(post.id)

    comment = api.create_comment(payload)
    comment_id = comment.id

    assert db.get_comment(comment_id) is not None

    deleted_comment = api.delete_comment(comment_id)

    assert deleted_comment.id == comment_id
    assert deleted_comment.content.raw == payload.content

    db_comment = db.get_comment(comment_id)
    assert db_comment is not None
    assert db_comment['comment_approved'] == 'trash'

    api.delete_post(post.id)
