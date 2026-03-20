import requests
import allure
from config import WP_FULL_URL, WP_USER, WP_PASSWORD
from core.models import PostModel, PostCreate, CommentModel, CommentCreate


class WordPressAPI:
    def __init__(self):
        self.url = WP_FULL_URL
        self.auth = (WP_USER, WP_PASSWORD)

    def _request(self, method: str, endpoint: str, expected_status: int = 200, **kwargs) -> dict:
        """Универсальный метод для отправки запросов с логированием в Allure.

        Args:
            method: HTTP метод (GET, POST, PUT, DELETE)
            endpoint: Путь эндпоинта (например /wp/v2/posts)
            expected_status: Ожидаемый статус код
            **kwargs: Параметры requests (json, params и т.д.)

        Returns:
            dict: JSON ответа сервера
        """
        url = f"{self.url}{endpoint}"

        # Логируем запрос в Allure
        with allure.step(f"{method} {endpoint}"):
            allure.attach(method, name="Method", attachment_type=allure.attachment_type.TEXT)
            allure.attach(url, name="URL", attachment_type=allure.attachment_type.TEXT)

            if "json" in kwargs:
                allure.attach(
                    str(kwargs["json"]),
                    name="Request Body",
                    attachment_type=allure.attachment_type.JSON
                )
            if "params" in kwargs:
                allure.attach(
                    str(kwargs["params"]),
                    name="Request Params",
                    attachment_type=allure.attachment_type.TEXT
                )

            # Отправляем запрос
            response = requests.request(method, url, auth=self.auth, **kwargs)

            # Логируем ответ
            allure.attach(
                str(response.status_code),
                name="Response Status",
                attachment_type=allure.attachment_type.TEXT
            )

            try:
                response_json = response.json()
                allure.attach(
                    str(response_json)[:1000],
                    name="Response Body",
                    attachment_type=allure.attachment_type.JSON
                )
            except:
                response_json = None
                allure.attach(
                    response.text[:1000],
                    name="Response Text",
                    attachment_type=allure.attachment_type.TEXT
                )

            # Проверяем статус
            assert response.status_code == expected_status, \
                f"Ожидался статус {expected_status}, получен {response.status_code}\n{response.text}"

            return response_json



    def create_post(self, data: PostCreate) -> PostModel:
        """Создает новый пост."""
        response_json = self._request(
            "POST",
            "/wp/v2/posts",
            expected_status=201,
            json=data.model_dump()
        )
        return PostModel(**response_json)

    def get_post(self, post_id: int) -> PostModel:
        """Получает пост по ID."""
        response_json = self._request(
            "GET",
            f"/wp/v2/posts/{post_id}"
        )
        return PostModel(**response_json)

    def update_post(self, post_id: int, title: str = None, content: str = None) -> PostModel:
        """Обновляет заголовок и/или содержание поста."""
        data = {}
        if title:
            data["title"] = title
        if content:
            data["content"] = content

        response_json = self._request(
            "PUT",
            f"/wp/v2/posts/{post_id}",
            json=data
        )
        return PostModel(**response_json)

    def delete_post(self, post_id: int) -> PostModel:
        """Удаляет пост (перемещает в корзину)."""
        response_json = self._request(
            "DELETE",
            f"/wp/v2/posts/{post_id}"
        )
        return PostModel(**response_json)


    def create_comment(self, data: CommentCreate) -> CommentModel:
        """Создает новый комментарий."""
        response_json = self._request(
            "POST",
            "/wp/v2/comments",
            expected_status=201,
            json=data.model_dump(exclude_none=True)
        )
        return CommentModel(**response_json)

    def get_comment(self, comment_id: int) -> CommentModel:
        """Получает комментарий по ID."""
        response_json = self._request(
            "GET",
            f"/wp/v2/comments/{comment_id}"
        )
        return CommentModel(**response_json)

    def update_comment(self, comment_id: int, content: str) -> CommentModel:
        """Обновляет текст комментария."""
        response_json = self._request(
            "PUT",
            f"/wp/v2/comments/{comment_id}",
            json={"content": content}
        )
        return CommentModel(**response_json)

    def delete_comment(self, comment_id: int) -> CommentModel:
        """Удаляет комментарий (перемещает в корзину)."""
        response_json = self._request(
            "DELETE",
            f"/wp/v2/comments/{comment_id}"
        )
        return CommentModel(**response_json)