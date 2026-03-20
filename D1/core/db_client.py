import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
from typing import Optional, Dict, Any


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

    def get_comment(self, comment_id: int) -> Optional[Dict[str, Any]]:
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM wp_comments WHERE comment_ID = %s", (comment_id,))
            result = cursor.fetchone()
            return result

    def close(self) -> None:
        if self.connection:
            self.connection.close()