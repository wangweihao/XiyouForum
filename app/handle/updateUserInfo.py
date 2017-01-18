# coding:utf8

import sys
import logging

sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/config')

from argument import *
import model

logger = logging.getLogger('log')

def updateUserInfo(req, info, content):
    info = ''
    ret_data = {}
    uid = req['uid']

    try:
        model.db.session.query(model.UserInfo).filter_by(uid=uid).update(dict(head_url=content))
        model.db.session.commit()
    except Exception as e:
        print e.message
        info = 'db err:update UserInfo'
        logger.error(info)
        logger.error(e.message)

        return False, DB_ERR_HAND, info, ret_data


    return True, SUCCESS, info, ret_data