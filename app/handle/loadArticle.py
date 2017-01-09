# coding:utf8

import sys
import logging

sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/config')

from argument import *
import model
import markdown

logger = logging.getLogger('log')


def loadArticle(aid):
    info = 'handle success'
    ret_data = {}

    try:
        arti = model.db.session.query(model.Article.title, model.Article.content, model.Article.scan_time,
                                      model.Article.agree_time, model.Article.time, model.Article.uid).filter_by(id=aid).one()
    except Exception as e:
        info = 'db err:query article'
        print e.message
        logger.error(info)
        logger.error(e.message)

        return False, DB_ERR_HAND, info, ret_data

    try:
        model.db.session.query(model.Article).filter_by(id=aid).update(dict(scan_time=arti[2]+1))
        model.db.session.commit()
    except Exception as e:
        print e.message
        info = 'db err:update scan_time'
        logger.error(info)
        logger.error(e.message)

        return False, DB_ERR_HAND, info, ret_data


    try:
        comments = model.db.session.query(model.Comment.content, model.Comment.time, model.Comment.aid,
                                              model.Comment.uid).filter_by(aid=aid).order_by(model.Comment.time).all()
    except Exception as e:
        print e.message
        info = 'db err:query comments'
        logger.error(info)
        logger.error(e.message)

    comm = []
    for comment in comments:
        user = model.db.session.query(model.User.id, model.User.nickname).filter_by(id=comment[3]).one()
        one_comment = {}
        one_comment['user']       = user
        one_comment['comment']    = list(comment)
        one_comment['comment'][0] = markdown.markdown(comment[0], extensions=['markdown.extensions.extra'])
        comm.append(one_comment)

    ret_data['article']  = arti
    ret_data['comments'] = comm


    return True, SUCCESS, info, ret_data