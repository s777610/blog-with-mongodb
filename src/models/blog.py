import uuid
from src.common.database import Database
from src.models.post import Post
import datetime

class Blog(object):
    def __init__(self, author, title, description, author_id, _id=None):
        self.author = author
        self.title = title
        self.description = description
        self.author_id = author_id
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self, title, content, date=datetime.datetime.utcnow()):
        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=date)
        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection="blogs",
                        data=self.json())

    def json(self):
        return {
            "author": self.author,
            "author_id": self.author_id,
            "title": self.title,
            "description": self.description,
            "_id": self._id
        }

    @classmethod
    def from_mongo(cls, _id):  # blog id
        blog_data = Database.find_one(collection="blogs",
                                      query={"_id": _id})
        """It is a general Python construct. 
        Double asterisks in front of a dictionary 
        treats the dictionary keys and values as 
        names and arguments for a method."""
        return cls(**blog_data)
        # return cls(author=blog_data["author"], return an object in order to call method
        #           title=blog_data["title"],   such as get the post for viewing
        #           description=blog_data["description"],
        #           _id=blog_data["_id"])

    @classmethod
    def find_by_author_id(cls, author_id):
        blogs = Database.find(collection="blogs",
                              query={"author_id": author_id})
        return [cls(**blog) for blog in blogs]
