# coding:utf8

import json
import logging
import time

from argument import *
from utils import check_result
from utils import getSessionInfo
from flask import make_response
from flask import render_template

logger = logging.getLogger('log')

def user_login(request, red):
    ret_data = {}
    req_data = request.get_data()
    print req_data
    try:
        req = json.loads(req_data)
    except ValueError:
        info = 'register failed:json analyse failure'
        logger.error(info)
        return check_result(False, JSON_ERR_ANALY, info, ret_data)

    import login
    result, mtype, info, ret_data = login.login(req, red)

    print ret_data

    response = make_response(check_result(result, mtype, info, ret_data))
    if result == True:
        response.set_cookie('session_id', ret_data['session_id'], expires=time.time()+30*60*60*24)
        response.set_cookie('nickname',   ret_data['nickname'],   expires=time.time()+30*60*60*24)
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response

def user_quit(request, red):
    cookie = request.cookies
    red.delete(cookie['session_id'])

    print '退出登录'

    response = make_response()
    response.set_cookie('session_id', '', expires=time.time())
    response.set_cookie('nickname',   '', expires=time.time())
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response

def user_register(request, red):
    ret_data = {}
    req_data = request.get_data()

    try:
        req  = json.loads(req_data)
    except ValueError as e:
        info = 'register failed:json analyse failure'
        logger.error(info)
        return check_result(False, JSON_ERR_ANALY, info, ret_data)

    import register
    result, mtype, info, ret_data = register.register(req)

    response = make_response(check_result(result, mtype, info, ret_data))
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response

def new_questions(request, red):
    args = request.args
    cookie = request.cookies
    page = 0
    sessionInfo = {}

    if not args.has_key('page'):
        page = 1
    else:
        page = args['page']

    import loadHome
    ques, hot_articles = loadHome.load_home(int(page), 1)

    if cookie.has_key('session_id'):
        sessionInfo = getSessionInfo(red, cookie['session_id'], ['nickname', 'head_url', 'reputation', 'authority'])

    return render_template('home.html', questions=ques, type='questions', user=sessionInfo, url='/questions/newest',
                           hot_articles=hot_articles)


def hot_questions(request, red):
    args = request.args
    cookie = request.cookies
    page = 0
    sessionInfo = {}

    if not args.has_key('page'):
        page = 1
    else:
        page = args['page']

    import loadHome
    ques, hot_articles = loadHome.load_home(int(page), 2)

    if cookie.has_key('session_id'):
        sessionInfo = getSessionInfo(red, cookie['session_id'], ['nickname', 'head_url', 'reputation', 'authority'])

    return render_template('home.html', questions=ques, type='questions-hot', user=sessionInfo, url='/questions/hottest',
                           hot_articles=hot_articles)


def unanswer_questions(request, red):
    args = request.args
    cookie = request.cookies
    page = 0
    sessionInfo = {}

    if not args.has_key('page'):
        page = 1
    else:
        page = args['page']

    import loadHome
    ques, hot_articles = loadHome.load_home(int(page), 3)

    if cookie.has_key('session_id'):
        sessionInfo = getSessionInfo(red, cookie['session_id'], ['nickname', 'head_url', 'reputation', 'authority'])

    return render_template('home.html', questions=ques, type='questions-unans', user=sessionInfo, url='/questions/unanswered',
                           hot_articles=hot_articles)

def write_question(request, red):
    ret_data = {}
    req_data = request.get_data()
    try:
        req = json.loads(req_data)
    except ValueError:
        info = 'register failed:json analyse failure'
        logger.error(info)
        return check_result(False, JSON_ERR_ANALY, info, ret_data)

    session_id = request.cookies['session_id']
    sessionInfo = getSessionInfo(red, session_id, ['uid'])

    req['uid'] = sessionInfo['uid']

    import writeQuestion
    result, mtype, info, ret_data = writeQuestion.writeQuestion(req)

    response = make_response(check_result(result, mtype, info, ret_data))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

def agree_question(request, red):
    agree = 0
    ret_data = {}
    req_data = request.get_data()
    try:
        req = json.loads(req_data)
    except ValueError:
        info = 'register failed:json analyse failure'
        logger.error(info)
        return check_result(False, JSON_ERR_ANALY, info, ret_data)

    import voteQuestion
    result, mtype, info, ret_data = voteQuestion.voteQuestion(req, agree)

    response = make_response(check_result(request, mtype, info, ret_data))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

def write_article(request, red):
    ret_data = {}
    req_data = request.get_data()
    try:
        req = json.loads(req_data)
    except ValueError:
        info = 'register failed:json analyse failure'
        logger.error(info)
        return check_result(False, JSON_ERR_ANALY, info, ret_data)

    session_id  = request.cookies['session_id']
    sessionInfo = getSessionInfo(red, session_id, ['uid'])

    req['uid'] = sessionInfo['uid']

    import writeArticle
    result, mtype, info, ret_data = writeArticle.writeArticle(req)

    response = make_response(check_result(result, mtype, info, ret_data))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

def new_articles(request, red):
    args = request.args
    cookie = request.cookies
    page = 0
    sessionInfo = {}

    if not args.has_key('page'):
        page = 1
    else:
        page = args['page']

    import loadArticles
    arti = loadArticles.load_articles(int(page), 1)

    print '=================='
    print arti
    print '=================='

    if cookie.has_key('session_id'):
        sessionInfo = getSessionInfo(red, cookie['session_id'], ['nickname', 'head_url', 'reputation', 'authority'])

    return render_template('articles.html', articles=arti, user=sessionInfo, type='new')


def hot_articles(request, red):
    args = request.args
    cookie = request.cookies
    page = 0
    sessionInfo = {}

    if not args.has_key('page'):
        page = 1
    else:
        page = args['page']

    import loadArticles
    arti = loadArticles.load_articles(int(page), 2)

    if cookie.has_key('session_id'):
        sessionInfo = getSessionInfo(red, cookie['session_id'], ['nickname', 'head_url', 'reputation', 'authority'])

    return render_template('articles.html', articles=arti, user=sessionInfo, type='hot')
