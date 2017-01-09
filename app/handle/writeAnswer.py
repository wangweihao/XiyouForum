# coding:utf8

import sys
import logging
import datetime

sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/config')

from argument import *
import model

logger = logging.getLogger('log')

def writeAnswer(req):
    info = ''
    ret_data = {}
    qid = req['qid']

    try:
        answ = model.Answer(content=req['content'], uid=req['uid'], qid=qid)
        model.db.session.add(answ)
        model.db.session.commit()
        ret_data['aid'] = answ.id
    except Exception as e:
        info = 'write answer error : handle database failure'
        print e
        # logger.error(info)
        # logger.error(e.message)

        return False, DB_ERR_HAND, info, ret_data

    info = 'write answer success'
    # logger.info(info)

    try:
        answer_num = model.db.session.query(model.Question.answer_num).filter_by(id=qid).one()
    except Exception as e:
        print e.message
        info = 'db err:obtain answer_num'
        logger.error(info)
        logger.error(e.message)

        return False, DB_ERR_HAND, info, ret_data

    try:
        model.db.session.query(model.Question).filter_by(id=req['qid']).update(dict(answer_num=answer_num[0]+1))
        model.db.session.commit()
    except Exception as e:
        print e.message
        info = 'db err:update scan_time'
        logger.error(info)
        logger.error(e.message)

        return False, DB_ERR_HAND, info, ret_data

    return True, SUCCESS, info, ret_data