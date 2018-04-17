
from flask import Flask, render_template, request, session, make_response

from src.common.database import Database
from src.models.blog import Blog
from src.models.post import Post
from src.models.user import User

app = Flask(__name__)
app.secret_key = "Wilson"

@app.route('/')
def home_template():
    return render_template('home.html')

@app.route('/login')  # www.mysite.com/api/login
def login_template():
    return render_template("login.html")

@app.route('/register')  # www.mysite.com/api/register
def register_template():
    return render_template("register.html")

@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])  # only accept post requests on this endpoint
def login_user():
    # email is name of email in login.html,
    # request is something that is incoming to app,
    # website is going to make a request to app,
    # form is going to send some data(dict)
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)  # session email is user email
    else:
        session['email'] = None

    return render_template("profile.html", email=session['email'])

@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)

    return render_template("profile.html", email=session['email'])

@app.route('/blogs/<string:user_id>')  # access the user_id's blogs
@app.route('/blogs')  # access my own blogs
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])  # access my own blogs

    blogs = user.get_blogs()

    return render_template("user_blogs.html", blogs=blogs, email=user.email)


@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:  # 'POST'
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])
        new_blog = Blog(user.email, title, description, user._id)  #user.email = auther, user._id = authro_id
        new_blog.save_to_mongo()

        return make_response(user_blogs(user._id))

@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()  # a list of post

    return render_template('posts.html', posts=posts, blog_title=blog.title, blog_id=blog._id)

@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('new_post.html', blog_id=blog_id)
    else:  # 'POST'
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])

        new_post = Post(blog_id, title, content, user.email)  #user.email = auther
        new_post.save_to_mongo()

        return make_response(blog_posts(blog_id))

if __name__ == "__main__":
    app.run(debug=True)

