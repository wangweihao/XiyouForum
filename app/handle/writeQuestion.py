# coding:utf8

import sys
import logging

sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/config')

from argument import *
import model

logger = logging.getLogger('log')

def writeQuestion(req):
    info = ''
    ret_data = {}
    qid  = 0

    try:
        ques = model.Question(title=req['title'], content=req['content'], scan_time=0, agree_time=0, uid=req['uid'])
        model.db.session.add(ques)
        model.db.session.commit()
        qid = ques.id
    except Exception as e:
        info = '数据库错误，问题提交失败'
        logger.error(info)
        logger.error(e.message)

        return False, DB_ERR_HAND, info, ret_data

    try:
        tabArr = req['tab'].split(';')
    except KeyError as e:
        info = '请求错误'
        logger.error(info)
        logger.error(e.message)

        return False, DB_ERR_HAND, info, ret_data

    tab_list = []
    for tab in tabArr:
        cid = model.db.session.query(model.Category.id).filter_by(category=tab).first()
        if not cid:
            tb = model.Category(category=tab, cid=1)
            model.db.session.add(tb)
            model.db.session.commit()
            cid = tb.id
        else:
            cid = cid[0]
        tab_list.append(model.Question_Category_Rela(qid=qid, cid=cid))
    model.db.session.add_all(tab_list)
    model.db.session.commit()

    return True, SUCCESS, info, ret_data