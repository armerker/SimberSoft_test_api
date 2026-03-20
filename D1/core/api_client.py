import requests
from config import WP_FULL_URL, WP_USER, WP_PASSWORD

class WordPressAPI:

    def __init__(self):
        self.url = WP_FULL_URL
        self.auth = (WP_USER,WP_PASSWORD)

    def create_post(self,title,content):
        data ={
            "title":title,
            'content':content,
            "status": "publish"
        }

        response = requests.post(f"{self.url}/wp/v2/posts",auth=self.auth,json=data)

        return response

    def get_post(self,post_id):

        response = requests.get(f"{self.url}/wp/v2/posts/{post_id}",auth = self.auth)

        return response

    def update_post(self,post_id,title,content):

        data = {
            "title":title,
            'content':content
        }

        response =  requests.put(
            f"{self.url}/wp/v2/posts/{post_id}",
            auth=self.auth,
            json=data
        )

        return response

    def delete_post(self,post_id):

        response = requests.delete(
            f"{self.url}/wp/v2/posts/{post_id}",
            auth=self.auth
        )

        return response

    def create_comment(self,post_id,content,author_name="тестировщик",author_email=None, author_url=None):

        data = {
            "post":post_id,
            "content":content,
            "author_name":author_name
        }
        if author_email:
            data["author_email"] = author_email
        if author_url:
            data["author_url"] = author_url
        response = requests.post(
            f"{self.url}/wp/v2/comments",
            auth=self.auth,
            json=data
        )

        return response

    def get_comment(self,comment_id):
        response = requests.get(
            f"{self.url}/wp/v2/comments/{comment_id}",
            auth = self.auth
        )

        return response

    def update_comment(self,comment_id,content):
        data = {'content':content}

        response = requests.put(
            f"{self.url}/wp/v2/comments/{comment_id}",
            auth = self.auth,
            json = data
        )

        return response

    def delete_comment(self,comment_id):
        response = requests.delete(
            f"{self.url}/wp/v2/comments/{comment_id}",
            auth = self.auth
        )

        return response

