# importing the flask library
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # create a flask app using an object of the Flask class

# specifies the configurations of the database we are using
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

# we create the attributes in the database by creating a column (i.e. each col is a defined by a class)
# creating the database


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # column 1: id
    title = db.Column(db.String(100), nullable=False)  # column 1: title
    content = db.Column(db.Text, nullable=False)  # column 1: content
    author = db.Column(db.String(30), nullable=False,
                       default='N/A')  # column 1: author
    # column 1: publising date
    publish_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog Post ' + str(self.id)


# the routing of the website is done using the routing decorators


# defining a URL (this specific line defines the base URL of the website)
# the function that comes immediately after the route method is executed and consequently it's contents are shown


# to add a content within a div tag just like in HTML, we can create a list of dicts, using Jynga syntax,
# we can access it and perform operations upon it to structure it upon our web page
all_posts = [
    {
        'Title': 'Starship project by Elon Musk',
        'Content': 'This project of SpaceX led by Elon Musk aims at making humans multi-planetary species',
        'Author': 'Yogesh Pandey'
    },
    {
        'Title': 'Artemis project by NASA',
        'Content': 'This NASA project aims at conducting the first ever woman led moon landing mission'
    }
]


# to get information from the URL itself (use this syntax within the app router)

# use below two method syntaxes for dynamic URL's


'''@app.route('/')
def usingHTML():
    return "<h1>Home Page</h1>"            #we can also use HTML tags (but it is recommended to use another file
                                           #for that, and then including that file using templates
'''

# using a template to include an HTML file inside this app (using render_template function)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():

    # check if a new post is to be created then we request the title and content from the user and store it
    # into the database. Then create BlogPost object and pass the parameters to create a new instance of a post
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form
        new_post = BlogPost(
            title=post_title, content=post_content, author='Yogesh Pandey')
        # to add new post into the database in current session
        db.session.add(new_post)
        db.session.commit()  # save the changes permanently
        return redirect('/posts')

        # if no new post is intended to be created, then we just show the posts and order them by date of posting
    else:
        all_posts = BlogPost.query.order_by(BlogPost.publish_date).all()
        return render_template('posts.html', posts=all_posts)


@app.route('/homepage/<string:username>')
def custom(username):
    return "The creator of this application:" + username


@app.route('/homepage/Users/<string:name>/photoID/<int:id>')
def userDetails(name, id):
    return "The photo ID of " + name + " is " + str(id)


# demo of GET and POST commands through HTTPS


@app.route('/getwebpage', methods=['GET'])
def getRequest():
    return "You're ONLY getting this web page"

# routing method for deleting a post. We need to provide an id for a specific post in order to delete it.
# if the post is not present, then a 404 ERROR is thrown. After deleting the post, we commit the changes in the DB


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


# routing method for edititg a post by using id
# we provide both GET and POST methods to access and hence make changes in the DB
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    # if I request for the post to be edited, then the if block is executed
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

# create a new route for a page where a user can only get access to compose an article, and after he is done,
# he could press the post button which would take him to the list of all posts


@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post.author = request.form['author']
        new_post = BlogPost(
            title=post_title, content=post_content, author='Yogesh Pandey')
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')


if __name__ == "__main__":
    app.run(debug=True)
