import requests
import os
from config import WP_FULL_URL, WP_USER, WP_PASSWORD
from core.models import PostModel, PostCreate, CommentModel, CommentCreate


class WordPressAPI:
    def __init__(self):
        self.url = WP_FULL_URL
        self.auth = (WP_USER, WP_PASSWORD)
        self.user_id = int(os.getenv("WP_USER_ID", 1))

    def create_post(self, data: PostCreate) -> PostModel:
        """Создает новый пост."""
        url = f"{self.url}/wp/v2/posts"
        response = requests.post(url, auth=self.auth, json=data.model_dump())
        assert response.status_code == 201
        return PostModel(**response.json())

    def get_post(self, post_id: int) -> PostModel:
        """Получает пост по ID."""
        url = f"{self.url}/wp/v2/posts/{post_id}"
        response = requests.get(url, auth=self.auth)
        return PostModel(**response.json())

    def update_post(self, post_id: int, title: str = None, content: str = None) -> PostModel:
        """Обновляет заголовок и/или содержание поста."""
        url = f"{self.url}/wp/v2/posts/{post_id}"
        data = {}
        if title:
            data["title"] = title
        if content:
            data["content"] = content
        response = requests.put(url, auth=self.auth, json=data)
        return PostModel(**response.json())

    def delete_post(self, post_id: int) -> PostModel:
        """Удаляет пост (перемещает в корзину)."""
        url = f"{self.url}/wp/v2/posts/{post_id}"
        response = requests.delete(url, auth=self.auth)
        return PostModel(**response.json())

    def create_comment(self, data: CommentCreate) -> CommentModel:
        """Создает новый комментарий."""
        url = f"{self.url}/wp/v2/comments"
        response = requests.post(url, auth=self.auth, json=data.model_dump(exclude_none=True))
        assert response.status_code == 201
        return CommentModel(**response.json())

    def get_comment(self, comment_id: int) -> CommentModel:
        """Получает комментарий по ID."""
        url = f"{self.url}/wp/v2/comments/{comment_id}"
        response = requests.get(url, auth=self.auth)
        return CommentModel(**response.json())

    def update_comment(self, comment_id: int, content: str) -> CommentModel:
        """Обновляет текст комментария."""
        url = f"{self.url}/wp/v2/comments/{comment_id}"
        response = requests.put(url, auth=self.auth, json={"content": content})
        return CommentModel(**response.json())

    def delete_comment(self, comment_id: int) -> CommentModel:
        """Удаляет комментарий (перемещает в корзину)."""
        url = f"{self.url}/wp/v2/comments/{comment_id}"
        response = requests.delete(url, auth=self.auth)
        return CommentModel(**response.json())