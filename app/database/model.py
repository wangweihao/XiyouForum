#coding:utf-8

import sys

sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/')

import server

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(server.server, use_native_unicode='utf-8')

class User(db.Model):
    __tablename__ = 'users'
    id        = db.Column(db.Integer, primary_key=True)
    email     = db.Column(db.String(48), unique=True, nullable=False)
    passwd    = db.Column(db.String(48), nullable=False)
    nickname  = db.Column(db.String(32), unique=True, nullable=False)
    authority = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<user %r>' % self.email

class UserInfo(db.Model):
    __tablename__ = 'userinfo'
    id        = db.Column(db.Integer, primary_key=True)
    uid       = db.Column(db.Integer, index=True)
    sex       = db.Column(db.Integer)
    school    = db.Column(db.String(40))
    specialty = db.Column(db.String(40))
    address   = db.Column(db.String(40))
    qq        = db.Column(db.String(40))
    wechat    = db.Column(db.String(40))
    email     = db.Column(db.String(40))
    selfIntro = db.Column(db.String(200))
    aWordIntro= db.Column(db.String(100))
    time      = db.Column(db.DateTime, default=datetime.now())
    head_url  = db.Column(db.String(64), server_default='http://img.xiyouforum.cn/head_img/default.png')
    reputation= db.Column(db.Integer, server_default='0')

    def __repr__(self):
        return '<userinfo %r>' % self.id

class Question(db.Model):
    __tablename__ = 'questions'
    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(50), nullable=False)
    content    = db.Column(db.TEXT, nullable=False)
    scan_time  = db.Column(db.Integer, nullable=False, default=0)
    agree_time = db.Column(db.Integer, nullable=False, default=0)
    time       = db.Column(db.DateTime, default=datetime.now())
    is_resolve = db.Column(db.Integer, default=0)
    answer_num = db.Column(db.Integer, default=0)
    uid        = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<title %r>' % self.title

class Question_collect(db.Model):
    __tablename__ = 'question_collect'
    id  = db.Column(db.Integer, primary_key=True)
    qid = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.Integer, nullable=False)

class Question_follow(db.Model):
    __tablename__ = 'question_follow'
    id  = db.Column(db.Integer, primary_key=True)
    qid = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.Integer, nullable=False)

class Answer(db.Model):
    __tablename__ = 'answers'
    id         = db.Column(db.Integer, primary_key=True)
    content    = db.Column(db.TEXT, nullable=False)
    agree_time = db.Column(db.Integer, default=0, nullable=False)
    time       = db.Column(db.DateTime, nullable=False, default=datetime.now())
    uid        = db.Column(db.Integer, nullable=False)
    qid        = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<content %r>' % self.content

class Article(db.Model):
    __tablename__ = 'articles'
    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(50), nullable=False)
    content    = db.Column(db.TEXT, nullable=False)
    scan_time  = db.Column(db.Integer, nullable=False, default=0)
    agree_time = db.Column(db.Integer, nullable=False, default=0)
    time       = db.Column(db.DateTime, nullable=False, default=datetime.now())
    uid        = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<title %r>' % self.title

class Comment(db.Model):
    __tablename__ = 'comments'
    id      = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.TEXT, nullable=False)
    time    = db.Column(db.DateTime, nullable=False, default=datetime.now())
    aid     = db.Column(db.Integer, nullable=False)
    uid     = db.Column(db.Integer, nullable=False)

class Classify(db.Model):
    __tablename__ = 'classify'
    id         = db.Column(db.Integer, primary_key=True)
    classify   = db.Column(db.String(20), index=True, nullable=False)

class Category(db.Model):
    __tablename__ = 'category'
    id        = db.Column(db.Integer, primary_key=True)
    category  = db.Column(db.String(20), index=True)
    cid       = db.Column(db.Integer, nullable=False)

class Question_Category_Rela(db.Model):
    __tablename__ = 'question_category_rela'
    id  = db.Column(db.Integer, primary_key=True)
    qid = db.Column(db.Integer, nullable=False, index=True)
    cid = db.Column(db.Integer, nullable=False, index=True)

class Article_Category_Rela(db.Model):
    __tablename__ = 'article_category_rela'
    id  = db.Column(db.Integer, primary_key=True)
    aid = db.Column(db.Integer, nullable=False, index=True)
    cid = db.Column(db.Integer, nullable=False, index=True)
#
# db.drop_all()
# db.create_all()
#
# print 'hello world'