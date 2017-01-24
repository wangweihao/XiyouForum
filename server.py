# coding:utf-8
import sys

sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/config')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/handle')

from flask import redirect
from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
from flask import abort
from flaskext.markdown import Markdown
#from gevent.wsgi import WSGIServer
from werkzeug.utils import secure_filename
from markdown.extensions import Extension

from utils import check_result
from utils import getSessionInfo
from handle import user_login
from handle import user_quit
from handle import user_register
from handle import new_questions
from handle import hot_questions
from handle import unanswer_questions
from handle import write_question
from handle import agree_question
from handle import write_article
from handle import new_articles
from handle import hot_articles

from config   import *
from argument import *

import logging
import json
import markdown
import time
import os
import redis
import uuid
import sys


reload(sys)
sys.setdefaultencoding('utf-8')

red = redis.Redis(host='127.0.0.1', port=6379, db=0)

UPLOAD_FOLDER      = '/Users/wwh/PycharmProjects/XiyouForum/static/upload_image'
UPLOAD_HEAD_FOLDER = '/Users/wwh/PycharmProjects/XiyouForum/static/upload_head'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

server = Flask(__name__)

Markdown(server)

server.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ww13659218813@localhost:3306/XiyouForum?charset=utf8'
# server.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Ww13659218813@localhost:3306/XiyouForum'
server.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
server.config['UPLOAD_FOLDER']             = UPLOAD_FOLDER
server.config['UPLOAD_HEAD_FOLDER']        = UPLOAD_HEAD_FOLDER


logger = logging.getLogger('log')

@server.route('/', methods=['GET'])
def hello_world():
    cookie      = request.cookies
    sessionInfo = {}
    info        = ''
    page        = 1

    req = request.args

    if req.has_key('page'):
        page = req['page']

    import loadHome
    ques, hot_articles = loadHome.load_home(int(page), 1)

    if cookie.has_key('session_id'):
        sessionInfo = getSessionInfo(red, cookie['session_id'], ['nickname', 'head_url', 'reputation', 'authority'])

    return render_template('home.html', questions=ques, type='questions', user=sessionInfo, url='/', hot_articles=hot_articles)


@server.route('/questions/<type>', methods=['GET'])
def questions(type):
    ret = 0
    if type == 'newest':
        ret = new_questions(request, red)
    elif type == 'hottest':
        ret = hot_questions(request, red)
    elif type == 'unanswered':
        ret = unanswer_questions(request, red)

    return ret

@server.route('/articles/<type>', methods=['GET'])
def articles(type):
    if type == 'new':
        ret = new_articles(request, red)
    elif type == 'hot':
        ret = hot_articles(request, red)

    return ret

@server.route('/api/user/<handle>', methods=['POST'])
def user_handle(handle):
    ret = 0
    if handle == 'login':
        ret = user_login(request, red)
    elif handle == 'quit':
        ret = user_quit(request, red)
    elif handle == 'register':
        ret =  user_register(request, red)
    elif handle == 'ask':
        ret = write_question(request, red)
    elif handle == 'agree_ques':
        ret = agree_question(request, red)
    elif handle == 'oppos_ques':
        pass
    elif handle == 'agree_answ':
        pass
    elif handle == 'oppos_answ':
        pass
    elif handle == 'write_article':
        ret = write_article(request, red)

    return ret


@server.route('/write/<name>', methods=['GET'])
def write(name):
    if name == 'question':
        return render_template('write.html')
    elif name == 'article':
        return render_template('writeArticle.html')


@server.route('/a/<aid>', methods=['GET'])
def scan_article(aid):
    cookie = request.cookies
    sessionInfo = {}

    if cookie.has_key('session_id'):
        session_id  = cookie['session_id']
        sessionInfo = getSessionInfo(red, session_id, ['nickname', 'head_url', 'authority'])

    import loadArticle
    result, mtype, info, ret_data = loadArticle.loadArticle(aid)

    if result == True:
        arti      = ret_data['article']
        comments  = ret_data['comments']
        title     = arti[0]
        content   = markdown.markdown(arti[1], extensions=['markdown.extensions.extra'])
        scan_time = arti[2]
        agree_time= arti[3]
        time      = arti[4]

        return render_template('article.html', user=sessionInfo, comments=comments, title=title, content=content, scan_time=scan_time,
                               agree_time=agree_time, time=time, aid=aid, comment_num=len(comments))
    else:
        return abort()

@server.route('/q/<qid>', methods=['GET'])
def scan_question(qid):
    cookie = request.cookies
    sessionInfo = {}

    if cookie.has_key('session_id'):
        session_id  = cookie['session_id']
        sessionInfo = getSessionInfo(red, session_id, ['nickname', 'head_url', 'authority'])

    import loadQuestion
    result, mtype, info, ret_data = loadQuestion.loadQuestion(qid)

    if result == True:
        ques       = ret_data['question']
        answers    = ret_data['answers']
        title      = ques[0]
        content    = markdown.markdown(ques[1], extensions=['markdown.extensions.extra'])
        scan_time  = ques[2]
        agree_time = ques[4]
        time       = ques[5]

        return render_template('question.html', user=sessionInfo, url='/', title=title,
                                content=content, answers=answers, answer_num=len(answers), scan_time=scan_time,
                                agree_time=agree_time, time=time, qid=qid)
    else:
        return abort()


@server.route('/comment/article', methods=['POST'])
def comment_article():
    req_data   = request.get_data()
    info = ''
    ret_data = {}

    if request.cookies.has_key('session_id'):
        session_id = request.cookies['session_id']
    else:
        info = 'user not login'
        return check_result(False, USER_NOT_LOGIN, info, ret_data)

    sessionInfo = getSessionInfo(red, session_id, ['uid'])

    if not session_id:
        info = 'user not login'
        return check_result(False, USER_NOT_LOGIN, info, ret_data)

    try:
        req = json.loads(req_data)
    except ValueError as e:
        info = 'register failed:json analyse failure'
        logger.error(info)
        return check_result(False, JSON_ERR_ANALY, info, ret_data)

    req['uid'] = sessionInfo['uid']

    import writeComment
    result, mtype, info, ret_data = writeComment.writeComment(req)

    return check_result(result, mtype, info, ret_data)


@server.route('/answer/question', methods=['POST'])
def answer_question():
    req_data   = request.get_data()
    info = ''
    ret_data = {}

    if request.cookies.has_key('session_id'):
        session_id = request.cookies['session_id']
    else:
        info = 'user not login'
        return check_result(False, USER_NOT_LOGIN, info, ret_data)

    sessionInfo = getSessionInfo(red, session_id, ['uid'])

    if not session_id:
        info = 'user not login'
        return check_result(False, USER_NOT_LOGIN, info, ret_data)

    try:
        req = json.loads(req_data)
    except ValueError as e:
        info = 'register failed:json analyse failure'
        logger.error(info)
        return check_result(False, JSON_ERR_ANALY, info, ret_data)

    req['uid'] = sessionInfo['uid']

    import writeAnswer
    result, mtype, info, ret_data = writeAnswer.writeAnswer(req)

    return check_result(result, mtype, info, ret_data)

@server.route('/activity', methods=['GET'])
def activity():
    cookie = request.cookies
    sessionInfo = {}

    if cookie.has_key('session_id'):
        session_id  = cookie['session_id']
        sessionInfo = getSessionInfo(red, session_id, ['nickname', 'head_url', 'authority'])


    return render_template('activity.html', user=sessionInfo)

@server.route('/selfhome', methods=['GET'])
def self_home():
    req_data   = request.get_data()
    info = ''
    req  = {}
    ret_data = {}

    if request.cookies.has_key('session_id'):
        session_id = request.cookies['session_id']
    else:
        info = 'user not login'
        return check_result(False, USER_NOT_LOGIN, info, ret_data)

    sessionInfo = getSessionInfo(red, session_id, ['uid', 'nickname', 'head_url', 'authority'])

    if not session_id:
        info = 'user not login'
        return check_result(False, USER_NOT_LOGIN, info, ret_data)

    req['uid'] = sessionInfo['uid']

    import loadSelfHome
    result, mtype, info, ret_data = loadSelfHome.loadSelfHome(req)
    check_result(result, mtype, info, ret_data)

    return render_template('selfhome.html', user=sessionInfo, userinfo=ret_data)


@server.route('/update/userinfo', methods=['POST'])
def update_userinfo():
    req_data = request.get_data()
    info     = ''
    ret_data = {}

    if request.cookies.has_key('session_id'):
        session_id = request.cookies['session_id']
    else:
        info = 'user not login'
        return check_result(False, USER_NOT_LOGIN, info, ret_data)

    sessionInfo = getSessionInfo(red, session_id, ['uid'])

    if not session_id:
        info = 'user not login'
        return check_result(False, USER_NOT_LOGIN, info, ret_data)

    try:
        req = json.loads(req_data)
    except ValueError as e:
        info = 'register failed:json analyse failure'
        logger.error(info)
        return check_result(False, JSON_ERR_ANALY, info, ret_data)

    req['uid'] = sessionInfo['uid']

    import updateUserInfo
    result, mtype, info, ret_data = updateUserInfo.updateUserInfo(req, req['userinfo'], req['content'])

    return check_result(result, mtype, info, ret_data)


@server.route('/upload/head', methods=['POST'])
def upload_head():
    info = ''
    ret_data = {}
    req  = {}

    if request.cookies.has_key('session_id'):
        session_id = request.cookies['session_id']
    else:
        info = 'user not login'
        return check_result(False, USER_NOT_LOGIN, info, ret_data)

    sessionInfo = getSessionInfo(red, session_id, ['uid'])

    if not session_id:
        info = 'user not login'
        return check_result(False, USER_NOT_LOGIN, info, ret_data)

    req['uid'] = sessionInfo['uid']

    print 'upload'
    if request.method == 'POST':
        try:
            file = request.files['File1']
        except Exception as e:
            print e
            print e.message

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(server.config['UPLOAD_HEAD_FOLDER'], filename))

        ret = {
                "success":1,
                "message":"success",
                "url":"http://" + HOST + ":" + str(PORT) + "/static/upload_head/" + filename
        }

        import updateUserInfo
        result, mtype, info, ret_data = updateUserInfo.updateUserInfo(req, 'head_url', ret['url'])

        red.hset(session_id, 'head_url', ret['url'])

        ret = json.dumps(ret)
        response = make_response(ret)
        response.headers['Access-Control-Allow-Origin'] = '*'

        return response

@server.route('/upload/image', methods=['POST'])
def upload_image():
    print 'upload image'
    if request.method == 'POST':
        file = request.files['editormd-image-file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(server.config['UPLOAD_FOLDER'], filename))

        ret = {
                "success":1,
                "message":"success",
                "url":"http://" + HOST + ":" + str(PORT) + "/static/upload_image/" + filename
        }
        ret = json.dumps(ret)
        print ret
        response = make_response(ret)
        response.headers['Access-Control-Allow-Origin'] = '*'

        return response

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    from utils import config_log
    config_log()
    while True:
        try:
            server.run(host=HOST, port=PORT)
            #http_server = WSGIServer((HOST, PORT), server)
            #http_server.serve_forever()
        except Exception as e:
            print e