# coding:utf8

import sys
import logging

sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/config')

from argument import *
import model

logger = logging.getLogger('log')

def writeComment(req):
    info = ''
    ret_data = {}
    aid = req['aid']

    try:
        comm = model.Comment(content=req['content'], uid=req['uid'], aid=aid)
        model.db.session.add(comm)
        model.db.session.commit()
        ret_data['cid'] = comm.id
    except Exception as e:
        info = 'write answer error : handle database failure'
        print e
        logger.error(info)
        logger.error(e.message)

        return False, DB_ERR_HAND, info, ret_data

    info = 'write answer success'
    # logger.info(info)

    return True, SUCCESS, info, ret_data