
import allure
import sys
import os
from D2.core.api_client import WordPressAPI
from core.db_client import WordPressDB
from core.models.post import PostModel
from core.models.post import PostCreate, PostModel
from core.models.error import PostNotFoundError

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
@allure.title("TC-07. Получение списка всех постов")
def test_tc07_post_all(api, db) -> None:
    """TC-07: Получение списка всех постов"""

    api_posts = api.get_all_posts()

    db_posts = {p['ID']: p for p in db.get_all_posts(status="publish", post_type="post")}

    assert len(api_posts) == len(db_posts)


    for api_post in api_posts:
        db_post = db_posts.get(api_post.id)
        assert db_post is not None
        assert db_post['post_title'] == api_post.title.rendered
        assert db_post['post_status'] == api_post.status
        assert db_post['post_author'] == api_post.author

def test_tc08_post_id(api,db,post_factory) -> None:
    post = post_factory()
    post_id = post.id
    api_post = api.get_post(post_id)
    assert api_post.id == post_id

    db_post = db.get_post(post_id)
    assert post_id == db_post["ID"]

    assert db_post['post_title'] == post.title.rendered
    assert db_post['post_status'] == post.status
    assert db_post['post_author'] == post.author

def test_tc09_non_existent_post(api,db) -> None:
    non_existent_id = db.get_non_existent_post_id()

    non_existent_post = api.get_post_raw(non_existent_id)
    assert non_existent_post.status_code == 404
    error = PostNotFoundError(**non_existent_post.json())
    assert error.code == "rest_post_invalid_id"
    assert "Неверный ID записи." in error.message
    assert error.data.status == 404


@allure.title("TC-10: Получение постов с пагинацией")
def test_tc10_pagination(api, create_test_posts):

    create_test_posts(count=5, post_status="publish")

    res_p1 = api.get_posts_paginated(page=1, per_page=2)
    posts_p1 = res_p1.json()

    assert res_p1.status_code == 200
    assert len(posts_p1) == 2

    assert "X-WP-TotalPages" in res_p1.headers
    assert int(res_p1.headers["X-WP-TotalPages"]) >= 3

    res_p2 = api.get_posts_paginated(page=2, per_page=2)
    posts_p2 = res_p2.json()

    assert res_p2.status_code == 200
    assert len(posts_p2) == 2, "Должно быть 2 поста на второй странице"

    ids_p1 = {post["id"] for post in posts_p1}
    ids_p2 = {post["id"] for post in posts_p2}

    assert ids_p1.isdisjoint(ids_p2)