# coding:utf8

import sys
import logging

sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/config')

from argument import *
import model
import markdown

logger = logging.getLogger('log')

def loadQuestion(qid):
    info = 'handle success'
    ret_data = {}

    try:
        ques = model.db.session.query(model.Question.title, model.Question.content, model.Question.scan_time,
                                      model.Question.answer_num, model.Question.agree_time, model.Question.time).\
                                      filter_by(id=qid).first()
    except Exception as e:
        info = 'db err:query question'
        logger.error(info)
        logger.error(e.message)

        return False, DB_ERR_HAND, info, ret_data

    try:
        model.db.session.query(model.Question).filter_by(id=qid).update(dict(scan_time=ques[2]+1))
        model.db.session.commit()
    except Exception as e:
        print e.message
        info = 'db err:update scan_time'
        logger.error(info)
        logger.error(e.message)

        return False, DB_ERR_HAND, info, ret_data

    try:
        answers = model.db.session.query(model.Answer.id, model.Answer.content, model.Answer.agree_time,
                                         model.Answer.time, model.Answer.uid).filter_by(qid=qid).\
                                         order_by(model.Answer.agree_time.desc()).all()
    except Exception as e:
        print e.message
        info = 'db err:query answers'
        logger.error(info)
        logger.error(e.message)

    answ = []
    for answer in answers:
        user = model.db.session.query(model.User.id, model.User.nickname).filter_by(id=answer[4]).one()
        one_answer = {}
        one_answer['user'] = user
        one_answer['answer'] = list(answer)
        one_answer['answer'][1] = markdown.markdown(one_answer['answer'][1], extensions=['markdown.extensions.extra'])
        answ.append(one_answer)

    ret_data['answers']  = answ
    ret_data['question'] = ques

    print ret_data
    print ret_data['question']
    # print ret_data['answers']
    # for i in ret_data['answers']:
    #     print i['answer'][0]
    #     print i['user'][1]

    return True, SUCCESS, info, ret_data