# coding:utf8

import sys
import logging

sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/config')

from argument import *
import model
import uuid

logger = logging.getLogger('log')

def login(req, red):
    info = ''
    ret_data = {}

    email_count = model.db.session.query(model.User).\
        filter_by(email=req['email']).count()
    if email_count == 0:
        info = "该邮箱未注册"
        logger.error(info)

        return False, DB_ERR_NO_EML, info, ret_data

    user_count  = model.db.session.query(model.User).\
        filter_by(email=req['email'], passwd=req['passwd']).count()
    if user_count == 0:
        info = "密码错误"
        logger.error(info)

        return False, DB_ERR_NO_PWD, info, ret_data
    elif user_count == 1:
        try:
            user = model.db.session.query(model.User.id, model.User.nickname, model.User.authority).\
                filter_by(email=req['email'], passwd=req['passwd']).one()
            ret_data['nickname']  = user.nickname
            ret_data['authority'] = user.authority
            info = "登录成功"
            logger.info(info)
        except Exception as e:
            info = '系统错误，请稍后再试'
            logger.error(info)
            logger.error(e.message)
            return False, DB_ERR_NO_PWD, info, ret_data

        try:
            userinfo = model.db.session.query(model.UserInfo.head_url, model.UserInfo.reputation).filter_by(uid=user.id).one()
            ret_data['head_url']   = userinfo.head_url
            ret_data['reputation'] = userinfo.reputation
        except Exception as e:
            info = '登录失败，请稍后再试'
            logger.error(info)
            logger.error(e.message)
            return False, DB_ERR_NO_PWD, info, ret_data

        session_id = uuid.uuid4()
        ret_data['session_id'] = str(session_id)
        red.hset(session_id, 'uid',        user.id)
        red.hset(session_id, 'nickname',   ret_data['nickname'])
        red.hset(session_id, 'head_url',   ret_data['head_url'])
        red.hset(session_id, 'reputation', ret_data['reputation'])
        red.hset(session_id, 'authority',  ret_data['authority'])

        return True,  SUCCESS, info, ret_data