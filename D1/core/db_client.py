import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class WordPressDB:
    def __init__(self):

        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
        except Error as e:
            print(e)

    def get_post(self,post_id):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM wp_posts WHERE ID = %s", (post_id,))
            result = cursor.fetchone()
            return result


    def get_comment(self,comment_id):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM wp_comments WHERE comment_ID = %s", (comment_id,))
            result = cursor.fetchone()
            return result

    def close(self):
        self.connection.close()