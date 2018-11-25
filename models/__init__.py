from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True,index=True)
    password = db.Column(db.String(100), index=True)
    register_time = db.Column(db.DateTime, nullable=False, default =datetime.now())
        

class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title =  db.Column(db.String(50))
    username = db.Column(db.String(50))
    user_id = db.Column(db.Integer, index=True)
    content = db.Column(db.Text)
    datetime = db.Column(db.DateTime, nullable=False, default =datetime.now())
    def generate_url():
        self.url = '/'+self.username + '/'+self.title


