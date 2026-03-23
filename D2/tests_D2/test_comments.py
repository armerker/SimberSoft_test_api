import os
import sys
import allure
from core.db_client import WordPressDB
from core.models.post import PostModel
from core.models.post import PostCreate, PostModel
from core.models.error import PostNotFoundError
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@allure.title("TC-11: Получение списка всех комментариев")
def test_tc11_get_all_comments(api, db, create_test_comments):
    # 1. Создаем 3 комментария
    create_test_comments(count=3)

    api_comments = api.get_all_comments()

    db_comments = {c['comment_ID']: c for c in db.get_all_comment(approved="1")}

    assert len(api_comments) == len(db_comments)

    for api_comm in api_comments:
        db_row = db_comments.get(api_comm.id)

        assert db_row is not None
        assert api_comm.author_name == db_row['comment_author']
        assert api_comm.status == "approved"
        assert api_comm.post == db_row['comment_post_ID']
        assert db_row['comment_content'] in api_comm.content.rendered

def test_tc12_comment_id(api,db,test_comment):
    comment = test_comment
    comment.id = test_comment.id
    api_comment = api.get_comment(test_comment.id)
    assert api_comment.id == comment.id

    db_comment = db.get_comment(comment.id)

    assert db_comment['comment_ID'] == comment.id
    assert api_comment.author_name == db_comment['comment_author']
    assert db_comment['comment_content'] in api_comment.content.rendered

def test_tc13_non_existing_comment_id(api,db,):
    comment_id = db.get_non_existent_comment_id()
    non_existent_comment = api.get_comment_raw(comment_id)
    assert non_existent_comment.status_code == 404
    error_json = non_existent_comment.json()

    assert error_json['code'] == "rest_comment_invalid_id"
    assert error_json['data']['status'] == 404





