import uuid
from src.common.database import Database
import datetime



class Post(object):

    def __init__(self, blog_id, title, content, author, created_date=datetime.datetime.utcnow(), _id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.created_date = created_date
        self._id = uuid.uuid4().hex if _id is None else _id  # use id if we already have

    def save_to_mongo(self):
        Database.insert(collection="posts",
                        data=self.json())

    def json(self):
        return {
            "_id": self._id,
            "blog_id": self.blog_id,
            "author": self.author,
            "content": self.content,
            "title": self.title,
            "created_date": self.created_date
        }

    """@classmethod when you are defining a method that uses the class but not self. 
    When you don't need to access the self, 
    but you need to access the class, use a @classmethod."""
    # return one post
    @classmethod
    def from_mongo(cls, id):
        post_data = Database.find_one(collection="posts", query={"_id": id})
        return cls(**post_data)

    """@staticmethod when you are defining a method that is related to the class 
    but does not use it or self. When you don't need to access either, use a @staticmethod."""
    # return all the posts that are from a specific blog
    @staticmethod
    def from_blog(id): # id = blog id
        return [post for post in Database.find(collection="posts", query={"blog_id": id})]