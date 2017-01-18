# coding:utf8

import sys
import logging

sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/config')

from argument import *
import model

logger = logging.getLogger('log')

def updateUserInfo(req, userinfo, content):
    info = ''
    ret_data = {}
    uid = req['uid']

    try:
        if userinfo == 'head_url':
            model.db.session.query(model.UserInfo).filter_by(uid=uid).update(dict(head_url=content))
        elif userinfo == 'sex':
            model.db.session.query(model.UserInfo).filter_by(uid=uid).update(dict(sex=content))
        elif userinfo == 'school':
            model.db.session.query(model.UserInfo).filter_by(uid=uid).update(dict(school=content))
        elif userinfo == 'specialty':
            model.db.session.query(model.UserInfo).filter_by(uid=uid).update(dict(specialty=content))
        elif userinfo == 'address':
            model.db.session.query(model.UserInfo).filter_by(uid=uid).update(dict(address=content))
        elif userinfo == 'qq':
            model.db.session.query(model.UserInfo).filter_by(uid=uid).update(dict(qq=content))
        elif userinfo == 'wechat':
            model.db.session.query(model.UserInfo).filter_by(uid=uid).update(dict(wechat=content))
        elif userinfo == 'email':
            model.db.session.query(model.UserInfo).filter_by(uid=uid).update(dict(email=content))
        elif userinfo == 'selfIntro':
            model.db.session.query(model.UserInfo).filter_by(uid=uid).update(dict(selfIntro=content))
        elif userinfo == 'aWordIntro':
            model.db.session.query(model.UserInfo).filter_by(uid=uid).update(dict(aWordIntro=content))

        model.db.session.commit()
    except Exception as e:
        print e.message
        info = 'db err:update UserInfo'
        logger.error(info)
        logger.error(e.message)

        return False, DB_ERR_HAND, info, ret_data


    return True, SUCCESS, info, ret_data