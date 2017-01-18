# coding:utf8

import sys
import logging

sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/config')

from argument import *
import model

logger = logging.getLogger('log')

def loadSelfHome(req):
    info     = 'handle success'
    ret_data = {}
    try:
        userinfo = model.db.session.query(model.UserInfo.sex, model.UserInfo.school,
                                          model.UserInfo.specialty, model.UserInfo.address,
                                          model.UserInfo.qq, model.UserInfo.wechat,
                                          model.UserInfo.email, model.UserInfo.selfIntro,
                                          model.UserInfo.aWordIntro, model.UserInfo.head_url).filter_by(uid=req['uid']).first()
    except Exception as e:
        info = 'db err: get userinfo'
        logger.error(info)
        logger.error(e.message)

        return False, DB_ERR_HAND, info, ret_data

    ret_data['sex']        = userinfo.sex
    ret_data['school']     = userinfo.school
    ret_data['specialty']  = userinfo.specialty
    ret_data['address']    = userinfo.address
    ret_data['qq']         = userinfo.qq
    ret_data['wechat']     = userinfo.wechat
    ret_data['email']      = userinfo.email
    ret_data['selfIntro']  = userinfo.selfIntro
    ret_data['aWordIntro'] = userinfo.aWordIntro
    ret_data['head_url']   = userinfo.head_url

    return True, SUCCESS, info, ret_data
