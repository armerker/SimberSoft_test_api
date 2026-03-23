import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
from typing import Optional, Dict, Any, List
from random import randint

class WordPressDB:
    def __init__(self) -> None:
        self.connection: Optional[mysql.connector.MySQLConnection] = None
        self.connect()

    def connect(self) -> None:
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.connection.autocommit = True
        except Error as e:
            print(e)

    def get_post(self, post_id: int) -> Optional[Dict[str, Any]]:
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM wp_posts WHERE ID = %s", (post_id,))
            result = cursor.fetchone()
            return result

    def get_all_posts(self, status: str = "publish", post_type: str = "post") -> List[Dict[str, Any]]:
        """Получает все посты из БД с фильтрацией по статусу и типу."""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT * FROM wp_posts 
                WHERE post_status = %s AND post_type = %s
                ORDER BY ID
            """, (status, post_type))
            return cursor.fetchall()

    def get_all_comment(self, approved: str = "1") -> List[Dict[str, Any]]:
        """Получает все одобренные комментарии."""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT * FROM wp_comments 
                WHERE comment_approved = %s
                ORDER BY comment_ID
            """, (approved,))
            return cursor.fetchall()

    def get_comment(self, comment_id: int) -> Optional[Dict[str, Any]]:
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM wp_comments WHERE comment_ID = %s", (comment_id,))
            result = cursor.fetchone()
            return result

    def delete_post(self,post_id: int) -> None:
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("DELETE FROM wp_posts WHERE ID = %s",(post_id,))


    def delete_comments(self, comment_id: int) -> None:
        """Удаляет комментарий по его правильному ключу."""
        with self.connection.cursor() as cursor:
            # ВАЖНО: колонка называется comment_ID, а не ID
            cursor.execute("DELETE FROM wp_comments WHERE comment_ID = %s", (comment_id,))

    def insert_post(self, data: Dict[str, Any]) -> int:
        """Универсальная вставка поста. Принимает словарь {колонка: значение}"""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO wp_posts ({columns}) VALUES ({placeholders})"

        with self.connection.cursor() as cursor:
            cursor.execute(query, list(data.values()))
            return cursor.lastrowid


    def insert_comments(self, data: Dict[str, Any]) -> int:
        """Универсальная вставка поста. Принимает словарь {колонка: значение}"""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO wp_comments ({columns}) VALUES ({placeholders})"

        with self.connection.cursor() as cursor:
            cursor.execute(query, list(data.values()))
            return cursor.lastrowid

    def get_non_existent_post_id(self) -> int:
        """Находит ID, которого точно нет в таблице wp_posts."""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT MAX(ID) as max_id FROM wp_posts")
            result = cursor.fetchone()
            max_id = result['max_id'] if result['max_id'] is not None else 0
            return max_id + randint(100,1000)

    def get_non_existent_comment_id(self) -> int:
        """Находит ID, которого точно нет в таблице wp_posts."""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT MAX(comment_ID) as max_id FROM wp_comments")
            result = cursor.fetchone()
            max_id = result['max_id'] if result['max_id'] is not None else 0
            return max_id + randint(100,1000)

    def close(self) -> None:
        if self.connection:
            self.connection.close()