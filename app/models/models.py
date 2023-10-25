from app import db
from sqlalchemy import ForeignKey

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable = False)
    first_name = db.Column(db.String(50), unique=False, nullable = False)
    last_name = db.Column(db.String(50), unique=False, nullable = False)
    password = db.Column(db.String(200), unique=False, nullable = False)
    posts = db.relationship('Post')

class Topic(db.Model):
    __tablename__ = 'topic'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(50))

    user = db.Column(
        db.Integer,
        ForeignKey('user.id'),
        nullable = False,
    )

    topic = db.Column(
        db.Integer,
        ForeignKey('topic.id'),
        nullable = False,
    )

    user_obj = db.relationship('User')
    topic_obj = db.relationship('Topic')


class Coment(db.Model):
    __tablename__ = 'coment'

    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(50))
    user = db.Column(
        db.Integer,
        ForeignKey('user.id'),
        nullable = False,
    )

    post = db.Column(
        db.Integer,
        ForeignKey('post.id'),
        nullable = False,
    )

    post_obj = db.relationship('Post')
    user_obj = db.relationship('User')