
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '5488e829facb277d841f86a26685f17c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# To display the User's photo, Name and Post


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='Author', lazy=True)
    # db.relationship means query runs in the background
    # 'backref' allows us - when a post is made, we can use the Author attribute to get the user who created the post.
    # the 'lazy' attribute tells us when the SQLalchamy loads the data from the database

    def __repr__(self):
        return "User('{}', '{}', '{}')".format(self.username, self.email, self.image_file)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "post('{}','{}')".format(self.title, self.date_posted)


posts = [
    {
        'Author': 'Rounak Singh',
        'Tpye': 'Blogpost',
        'Title': 'My first post',
        'content': 'To be filled',
        'date_posted': 'Feb 1, 2021'

    },
    {
        'Author': 'Bobby Patel',
        'Tpye': 'Blogpost 2',
        'Title': 'My second post',
        'content': 'To be filled',
        'date_posted': 'Feb 2, 2021'

    }

]


@ app.route("/")
@ app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@ app.route("/about")
def about():
    return render_template('about.html', title='About')


@ app.route("/register", methods=['GET', 'POST'])
def register():
    form1 = RegistrationForm()
    if form1.validate_on_submit():
        flash('Account created for {}!', 'success').format(form1.username.data)
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form1)


@ app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
