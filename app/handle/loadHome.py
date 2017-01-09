# coding:utf8

import sys
import logging

sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/config')

from argument import *
import model

logger = logging.getLogger('log')

def load_home(page, mtype):
    if mtype == 1:
        print 'main'
        ques = model.db.session.query(model.Question.id,
                                  model.Question.title,
                                  model.Question.scan_time, model.Question.agree_time,
                                  model.Question.time, model.Question.is_resolve,
                                  model.Question.answer_num, model.Question.uid).\
                                order_by(model.Question.time.desc()).slice((page - 1)*30,page * 30).all()
    elif mtype == 2:
        print 'hot'
        ques = model.db.session.query(model.Question.id,
                                  model.Question.title,
                                  model.Question.scan_time, model.Question.agree_time,
                                  model.Question.time, model.Question.is_resolve,
                                  model.Question.answer_num, model.Question.uid).\
                                order_by(model.Question.scan_time.desc()).slice((page - 1)*30,page * 30).all()
    elif mtype == 3:
        print 'unansered'
        ques = model.db.session.query(model.Question.id,
                                  model.Question.title,
                                  model.Question.scan_time, model.Question.agree_time,
                                  model.Question.time, model.Question.is_resolve,
                                  model.Question.answer_num, model.Question.uid).\
                                filter_by(answer_num=0).order_by(model.Question.time.desc()).slice((page - 1) * 30, page * 30).all()


    ret = []
    for item in ques:
        one_ques = {
            'question' : item
        }
        id        = item[0]
        uid       = item[7]
        categorys = []
        userinfo  = model.db.session.query(model.User.nickname).filter_by(id=uid).first()
        category  = model.db.session.query(model.Question_Category_Rela.cid).filter_by(qid=id).all()
        for item in category:
            categorys.append(model.db.session.query(model.Category.category).filter_by(id=item[0]).first()[0])
        one_ques['category'] = categorys
        one_ques['nickname'] = userinfo[0]
        ret.append(one_ques)

    hot_articles = model.db.session.execute("select a.id, a.title, a.agree_time, b.comment_num from articles as a "
                                 "left join  (select aid, count(aid) as comment_num from comments group by aid) as b "
                                 "on a.id=b.aid order by agree_time desc limit 5;").fetchall()

    print '============='
    print hot_articles
    print '============='

    return ret, hot_articles