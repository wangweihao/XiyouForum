# coding:utf8

import sys
import logging

sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/config')

from argument import *
import model
from sqlalchemy import func

logger = logging.getLogger('log')

def load_articles(page, mtype):
    if mtype == 1:
        print 'new'
        arti = model.db.session.query(model.Article.id,
                                  model.Article.title, func.left(model.Article.content, 110),
                                  model.Article.scan_time, model.Article.agree_time,
                                  model.Article.time, model.Article.uid).\
                                order_by(model.Article.time.desc()).slice((page - 1)*30,page * 30).all()
    elif mtype == 2:
        print 'hot'
        arti = model.db.session.query(model.Article.id,
                                  model.Article.title, func.left(model.Article.content, 110),
                                  model.Article.scan_time, model.Article.agree_time,
                                  model.Article.time, model.Article.uid).\
                                order_by(model.Article.scan_time.desc()).slice((page - 1)*30,page * 30).all()

    ret = []
    for item in arti:
        one_arti = {
            'article' : item
        }
        id        = item[0]
        uid       = item[6]
        categorys = []
        userinfo  = model.db.session.query(model.User.nickname).filter_by(id=uid).first()
        category  = model.db.session.query(model.Article_Category_Rela.cid).filter_by(aid=id).all()
        for item in category:
            categorys.append(model.db.session.query(model.Category.category).filter_by(id=item[0]).first()[0])
        one_arti['category'] = categorys
        one_arti['nickname'] = userinfo[0]
        ret.append(one_arti)

    print ret

    return ret