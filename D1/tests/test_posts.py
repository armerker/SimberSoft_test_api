import pytest
import sys
import os
import allure

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


@allure.title("TC-01. Создание нового поста")
@allure.description("Проверка создания поста с обязательными полями")
@allure.feature("Posts")
@allure.story("Create post")
def test_tc01_create_post(api, db, post_data):
    """TC-01. Создание нового поста с обязательными полями"""

    with allure.step("Создание поста через API"):
        response = api.create_post(
            title=post_data['title'],
            content=post_data['content'],
        )

    with allure.step("Проверка статуса ответа"):
        assert response.status_code == 201

    with allure.step("Проверка тела ответа"):
        response_json = response.json()
        assert response_json['title']['raw'] == post_data['title']
        assert response_json['content']['raw'] == post_data['content']
        assert "id" in response_json

    with allure.step("Получение ID созданного поста"):
        post_id = response_json["id"]
        assert isinstance(post_id, int)
        allure.attach(str(post_id), name="Post ID", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверка наличия поста в БД"):
        db_post = db.get_post(post_id)
        assert db_post is not None

    with allure.step("Проверка полей поста в БД"):
        assert db_post['post_title'] == post_data['title']
        assert db_post['post_content'] == post_data["content"]
        assert db_post['post_status'] == "publish"
        assert db_post['post_author'] == 1
        assert db_post['post_date'] is not None
        assert db_post['post_modified'] is not None
        assert db_post['post_type'] == "post"
        assert db_post['comment_count'] == 0

    with allure.step("Очистка - удаление тестового поста"):
        api.delete_post(post_id)


@allure.title("TC-02. Редактирование поста")
@allure.description("Проверка обновления заголовка и содержания")
@allure.feature("Posts")
@allure.story("Update post")
def test_tc02_update(api, db, test_post):
    """TC-02. Редактирование существующего поста"""

    with allure.step("Получение ID тестового поста из фикстуры"):
        post_id = test_post
        allure.attach(str(post_id), name="Post ID", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Получение данных поста до редактирования"):
        orig_post = db.get_post(post_id)
        orig_date = orig_post['post_date']
        orig_modif = orig_post['post_modified']
        orig_type = orig_post['post_type']
        orig_author = orig_post['post_author']
        orig_comment_count = orig_post['comment_count']

        allure.attach(
            f"Дата создания: {orig_date}\nАвтор: {orig_author}\nТип: {orig_type}",
            name="Original post data",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Подготовка новых данных для обновления"):
        new_title = "ИЗМЕНЕНО: Тестовый пост"
        new_content = "Это содержание было обновлено через API"

    with allure.step("Отправка запроса на обновление поста"):
        response = api.update_post(post_id, new_title, new_content)

    with allure.step("Проверка статуса ответа"):
        assert response.status_code == 200

    with allure.step("Проверка ответа API"):
        response_json = response.json()
        assert response_json['id'] == post_id
        assert response_json['title']['raw'] == new_title
        assert response_json['content']['raw'] == new_content

    with allure.step("Проверка обновленных данных в БД"):
        db_post = db.get_post(post_id)
        assert db_post['post_title'] == orig_post['post_title']
        assert db_post['post_content'] == orig_post['post_content']
        assert db_post["post_date"] == orig_date
        assert db_post['post_author'] == orig_author
        assert db_post['post_type'] == orig_type
        assert db_post['comment_count'] == orig_comment_count

        allure.attach(
            f"Заголовок после: {db_post['post_title']}\nСодержание после: {db_post['post_content'][:50]}...",
            name="Updated post data",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.title("TC-03. Удаление поста")
@allure.description("Проверка удаления поста в корзину")
@allure.feature("Posts")
@allure.story("Delete post")
def test_tc03_delete_post(api, db, delete_post_data):
    """TC-03. Удаление поста"""

    with allure.step("Создание поста для удаления"):
        response = api.create_post(
            title=delete_post_data['title'],
            content=delete_post_data['content'],
        )
        assert response.status_code == 201
        response_json = response.json()
        post_id = response_json['id']
        allure.attach(str(post_id), name="Post ID to delete", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Отправка запроса на удаление поста"):
        delete_response = api.delete_post(post_id)
        delete_response_json = delete_response.json()

    with allure.step("Проверка статуса ответа"):
        assert delete_response.status_code == 200

    with allure.step("Проверка ответа API при удалении"):
        assert delete_response_json['title']['raw'] == delete_post_data['title']
        assert delete_response_json['content']['raw'] == delete_post_data['content']
        assert delete_response_json['id'] == post_id

    with allure.step("Проверка статуса поста в БД"):
        db_post = db.get_post(post_id)
        assert db_post['post_status'] == 'trash'
        allure.attach(f"Статус поста: {db_post['post_status']}", name="Post status",
                      attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверка GET запроса после удаления"):
        get_response = api.get_post(post_id)
        assert get_response.status_code == 200
        allure.attach(f"GET статус: {get_response.status_code}", name="GET after delete",
                      attachment_type=allure.attachment_type.TEXT)