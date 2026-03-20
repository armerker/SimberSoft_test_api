import allure


@allure.title("TC-04. Создание нового комментария")
@allure.description("Проверка создания комментария к существующему посту")
@allure.feature("Comments")
@allure.story("Create comment")
def test_tc04_create_comment(api, db, comment_data):
    """TC-04. Создание нового комментария"""

    with allure.step("Подготовка данных для комментария"):
        allure.attach(
            f"Post ID: {comment_data['post_id']}\n"
            f"Content: {comment_data['content']}\n"
            f"Author: {comment_data['author_name']}\n"
            f"Email: {comment_data['author_email']}\n"
            f"URL: {comment_data['author_url']}",
            name="Comment data",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Отправка запроса на создание комментария"):
        response = api.create_comment(
            post_id=comment_data['post_id'],
            content=comment_data['content'],
            author_name=comment_data['author_name'],
            author_email=comment_data['author_email'],
            author_url=comment_data['author_url']
        )

    with allure.step("Проверка статуса ответа"):
        assert response.status_code == 201
        allure.attach(f"Status code: {response.status_code}", name="Response status",
                      attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверка тела ответа"):
        response_json = response.json()
        assert "id" in response_json
        comment_id = response_json['id']
        assert isinstance(comment_id, int)
        assert response_json['post'] == comment_data['post_id']
        assert response_json['content']['raw'] == comment_data['content']
        assert response_json['author_name'] == comment_data['author_name']
        assert response_json['author_email'] == comment_data['author_email']
        assert response_json['author_url'] == comment_data['author_url']

        allure.attach(str(comment_id), name="Comment ID", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверка наличия комментария в БД"):
        db_comment = db.get_comment(comment_id)
        assert db_comment is not None

    with allure.step("Проверка полей комментария в БД"):
        assert db_comment['comment_post_ID'] == comment_data['post_id']
        assert db_comment['comment_content'] == comment_data['content']
        assert db_comment['comment_author'] == comment_data['author_name']
        assert db_comment['comment_author_email'] == comment_data['author_email']
        assert db_comment['comment_author_url'] == comment_data['author_url']
        assert db_comment['comment_approved'] in ["0", "1"]
        assert db_comment['comment_date'] is not None
        assert db_comment['user_id'] == 0

        allure.attach(
            f"Post ID: {db_comment['comment_post_ID']}\n"
            f"Status: {db_comment['comment_approved']}\n"
            f"Date: {db_comment['comment_date']}",
            name="DB comment data",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Очистка - удаление тестового комментария"):
        api.delete_comment(comment_id)


@allure.title("TC-05. Редактирование комментария")
@allure.description("Проверка обновления текста существующего комментария")
@allure.feature("Comments")
@allure.story("Update comment")
def test_tc05_update_comment(api, db, test_comment, comment_data):
    """TC-05. Редактирование текста существующего комментария"""

    with allure.step("Получение ID тестового комментария из фикстуры"):
        comment_id = test_comment
        allure.attach(str(comment_id), name="Comment ID", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Получение данных комментария до редактирования"):
        orig_comment = db.get_comment(comment_id)
        orig_date = orig_comment['comment_date']
        orig_post_id = orig_comment['comment_post_ID']
        orig_author = orig_comment['comment_author']
        orig_email = orig_comment['comment_author_email']
        orig_url = orig_comment['comment_author_url']
        orig_approved = orig_comment['comment_approved']

        allure.attach(
            f"Original content: {orig_comment['comment_content'][:50]}...\n"
            f"Date: {orig_date}\n"
            f"Author: {orig_author}\n"
            f"Status: {orig_approved}",
            name="Original comment data",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Подготовка нового текста комментария"):
        new_content = "Этот комментарий был отредактирован через API"
        allure.attach(new_content, name="New content", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Отправка запроса на обновление комментария"):
        update_response = api.update_comment(comment_id, new_content)

    with allure.step("Проверка статуса ответа"):
        assert update_response.status_code == 200

    with allure.step("Проверка ответа API"):
        update_response_json = update_response.json()
        assert update_response_json['id'] == comment_id
        assert update_response_json['content']['raw'] == new_content

    with allure.step("Принудительный коммит для сохранения в БД"):
        db.connection.commit()

    with allure.step("Проверка обновленных данных в БД"):
        db_comment = db.get_comment(comment_id)
        assert db_comment['comment_content'] == new_content
        assert db_comment['comment_date'] == orig_date
        assert db_comment['comment_post_ID'] == orig_post_id
        assert db_comment['comment_author'] == orig_author
        assert db_comment['comment_author_email'] == orig_email
        assert db_comment['comment_author_url'] == orig_url
        assert db_comment['comment_approved'] == orig_approved

        allure.attach(
            f"Updated content: {db_comment['comment_content'][:50]}...\n"
            f"Date unchanged: {db_comment['comment_date'] == orig_date}\n"
            f"Author unchanged: {db_comment['comment_author'] == orig_author}",
            name="Updated comment data",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.title("TC-06. Удаление комментария")
@allure.description("Проверка удаления комментария")
@allure.feature("Comments")
@allure.story("Delete comment")
def test_tc06_delete_comment(api, db, delete_comment_data):
    """TC-06. Удаление существующего комментария"""

    with allure.step("Создание комментария для удаления"):
        create_response = api.create_comment(
            post_id=delete_comment_data['post_id'],
            content=delete_comment_data['content'],
            author_name=delete_comment_data['author_name'],
            author_email=delete_comment_data['author_email'],
            author_url=delete_comment_data['author_url']
        )
        assert create_response.status_code == 201
        comment_id = create_response.json()['id']
        allure.attach(str(comment_id), name="Comment ID to delete", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверка наличия комментария в БД"):
        assert db.get_comment(comment_id) is not None

    with allure.step("Отправка запроса на удаление комментария"):
        delete_response = api.delete_comment(comment_id)
        delete_response_json = delete_response.json()

    with allure.step("Проверка статуса ответа"):
        assert delete_response.status_code == 200

    with allure.step("Проверка ответа API при удалении"):
        assert delete_response_json['id'] == comment_id
        assert delete_response_json['content']['raw'] == delete_comment_data['content']

    with allure.step("Принудительный коммит"):
        db.connection.commit()

    with allure.step("Проверка статуса комментария в БД"):
        db_comment = db.get_comment(comment_id)
        assert db_comment is not None
        assert db_comment['comment_approved'] == 'trash'
        allure.attach(f"Comment status: {db_comment['comment_approved']}", name="Comment status after delete",
                      attachment_type=allure.attachment_type.TEXT)