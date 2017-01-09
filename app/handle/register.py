# coding:utf8

import sys
import logging

sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/config')

from argument import *
import model
import datetime

logger = logging.getLogger('log')


def register(req):
    info = ''
    ret_data = {}

    email_count = model.db.session.query(model.User).filter_by(email=req['email']).count()
    if email_count != 0:
        info = '该邮箱已注册.'
        logger.error(info)
        return False, DB_ERR_DUP_EML, info, ret_data
    name_count  = model.db.session.query(model.User).filter_by(nickname=req['nickname']).count()
    if name_count  != 0:
        info = '该花名已注册.'
        logger.error(info)
        return False, DB_ERR_DUP_NAM, info, ret_data

    try:
        user = model.User(email=req['email'], passwd=req['passwd'], nickname=req['nickname'])
        model.db.session.add(user)
        model.db.session.commit()

        user = model.db.session.query(model.User.id).filter_by(email=req['email']).one()

        userinfo = model.UserInfo(uid=user.id, sex=0, address='')
        model.db.session.add(userinfo)
        model.db.session.commit()

    except Exception as e:
        print e
        info = '系统正忙,请稍后再试.'
        logger.error(info)
        logger.error(e.message)
        logger.error(e.args)
        return False, DB_ERR_HAND, info, ret_data

    info = '注册成功.'
    logger.info(info)

    return True, SUCCESS, info, ret_data