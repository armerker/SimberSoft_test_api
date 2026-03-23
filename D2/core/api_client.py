import os
from typing import List
from config import WP_FULL_URL, WP_USER, WP_PASSWORD
from core.models import PostModel, PostCreate, CommentModel, CommentCreate
from core.request_wrapper import RequestWrapper


class WordPressAPI:
    def __init__(self):
        self.url = WP_FULL_URL
        self.auth = (WP_USER, WP_PASSWORD)
        self.user_id = int(os.getenv("WP_USER_ID", 1))
        self.client = RequestWrapper(self.auth)

    # ============ ПОСТЫ ============

    def create_post(self, data: PostCreate) -> PostModel:
        """Создает новый пост."""
        url = f"{self.url}/wp/v2/posts"
        response = self.client.post(url, json=data.model_dump())
        assert response.status_code == 201
        return PostModel(**response.json())

    def get_all_posts(self, per_page: int = 100) -> List[PostModel]:
        """Получает все посты (с пагинацией)."""
        all_posts = []
        page = 1

        while True:
            url = f"{self.url}/wp/v2/posts&page={page}&per_page={per_page}"
            response = self.client.get(url)
            if response.status_code != 200:
                break
            posts = response.json()
            if not posts:
                break
            all_posts.extend([PostModel(**post) for post in posts])

            total_pages = int(response.headers.get('X-WP-TotalPages', 0))
            if page >= total_pages:
                break
            page += 1
        return all_posts

    def get_post_raw(self, post_id: int):
        """Возвращает сырой объект response для проверок ошибок."""
        url = f"{self.url}/wp/v2/posts/{post_id}"
        return self.client.get(url)

    def get_post(self, post_id: int) -> PostModel:
        """Получает пост по ID."""
        url = f"{self.url}/wp/v2/posts/{post_id}"
        response = self.client.get(url)
        return PostModel(**response.json())

    def update_post(self, post_id: int, title: str = None, content: str = None) -> PostModel:
        """Обновляет заголовок и/или содержание поста."""
        url = f"{self.url}/wp/v2/posts/{post_id}"
        data = {}
        if title:
            data["title"] = title
        if content:
            data["content"] = content
        response = self.client.put(url, json=data)
        return PostModel(**response.json())

    def delete_post(self, post_id: int) -> PostModel:
        """Удаляет пост (перемещает в корзину)."""
        url = f"{self.url}/wp/v2/posts/{post_id}"
        response = self.client.delete(url)
        return PostModel(**response.json())

    def get_posts_paginated(self, page: int, per_page: int):
        """Получает посты с параметрами пагинации."""
        url = f"{self.url}/wp/v2/posts"
        params = {"page": page, "per_page": per_page}
        return self.client.get(url, params=params)

    # ============ КОММЕНТАРИИ ============

    def create_comment(self, data: CommentCreate) -> CommentModel:
        """Создает новый комментарий."""
        url = f"{self.url}/wp/v2/comments"
        response = self.client.post(url, json=data.model_dump(exclude_none=True))
        assert response.status_code == 201
        return CommentModel(**response.json())

    def get_all_comments(self, per_page: int = 100):
        all_comments = []
        page = 1
        while True:
            params = {"page": page, "per_page": per_page, "status": "approve"}
            response = self.client.get(f"{self.url}/wp/v2/comments", params=params)

            if response.status_code != 200:
                break

            data = response.json()
            if not data:
                break

            all_comments.extend([CommentModel(**item) for item in data])

            total_pages = int(response.headers.get('X-WP-TotalPages', 0))
            if page >= total_pages:
                break
            page += 1
        return all_comments

    def get_comment(self, comment_id: int) -> CommentModel:
        """Получает комментарий по ID."""
        url = f"{self.url}/wp/v2/comments/{comment_id}"
        response = self.client.get(url)
        return CommentModel(**response.json())

    def get_comment_raw(self, comment_id: int):
        """Возвращает объект response без попытки создать модель."""
        url = f"{self.url}/wp/v2/comments/{comment_id}"
        return self.client.get(url)

    def update_comment(self, comment_id: int, content: str) -> CommentModel:
        """Обновляет текст комментария."""
        url = f"{self.url}/wp/v2/comments/{comment_id}"
        response = self.client.put(url, json={"content": content})
        return CommentModel(**response.json())

    def delete_comment(self, comment_id: int) -> CommentModel:
        """Удаляет комментарий (перемещает в корзину)."""
        url = f"{self.url}/wp/v2/comments/{comment_id}"
        response = self.client.delete(url)
        return CommentModel(**response.json())