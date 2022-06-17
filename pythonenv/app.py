from datetime import datetime
from flask import Flask, redirect, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from forms import RegistrationForms, LoginForms

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    image = db.Column(db.String(20), nullable=False, default='pic.jpg')
    email = db.Column(db.String(200), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


posts = [
    {'author': 'Martin Yanev', 'title': 'Post 1', 'content': 'Electrical Engineering',
     'date_posted': 'January 05, 2022'},
    {'author': 'Adekunle Gold', 'title': 'Post 2', 'content': 'Music', 'date_posted': 'Febrary 05, 2022'},
    {'author': 'Sonola Moyo', 'title': 'Post 3', 'content': 'Electrical/Electronic Engineering',
     'date_posted': 'March 05, 2022'}
]


@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForms()
    if form.validate_on_submit():
        flash(f'User:{form.username.data}!, success')
        redirect(url_for('/home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForms()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'Hurray User has being logged in')
            redirect(url_for('/home'))
    return render_template('login.html', title='Login', form=form)


# create database
db.create_all()
db.drop_all()
db.create_all()

# create users
user1 = User(username='John', email='john@gmail.com', password='john')
user2 = User(username='Moyo', email='moyo@gmail.com', password='moyo')
user3 = User(username='Sonola', email='sonola@gmail.com', password='sonola')
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.commit()

# create posts
post1 = Post(title='Post01', content='Moyo\'s first post', user_id=user2.id)
post2 = Post(title='Post02', content='Moyo\'s second post', user_id=user2.id)
post3 = Post(title='Post03', content='John\'s first post', user_id=user1.id)
db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
