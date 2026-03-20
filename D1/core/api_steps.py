import allure
from core.api_client import WordPressAPI

class WordPressSteps:
    def __init__(self):
        self.api = WordPressAPI()
        self.user_id = self.api.user_id


    def create_post(self, data):
        with allure.step(f"Создание поста: {data.title}"):
            return self.api.create_post(data)

    def get_post(self, post_id):
        with allure.step(f"Получение поста ID: {post_id}"):
            return self.api.get_post(post_id)

    def update_post(self, post_id, **kwargs):
        with allure.step(f"Обновление поста ID: {post_id}"):
            return self.api.update_post(post_id, **kwargs)

    def delete_post(self, post_id):
        with allure.step(f"Удаление поста ID: {post_id} (в корзину)"):
            return self.api.delete_post(post_id)


    def create_comment(self, data):
        with allure.step(f"Создание комментария для поста ID: {data.post}"):
            return self.api.create_comment(data)

    def get_comment(self, comment_id):
        with allure.step(f"Получение комментария ID: {comment_id}"):
            return self.api.get_comment(comment_id)

    def update_comment(self, comment_id, content):
        with allure.step(f"Обновление текста комментария ID: {comment_id}"):
            return self.api.update_comment(comment_id, content)

    def delete_comment(self, comment_id):
        with allure.step(f"Удаление комментария ID: {comment_id} (в корзину)"):
            return self.api.delete_comment(comment_id)
