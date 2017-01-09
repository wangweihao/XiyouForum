# coding:utf8

import sys
import logging

sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/config')

from argument import *
import model

logger = logging.getLogger('log')

def voteQuestion(req, type):
    result = ''
    mtype  = ''
    info   = ''
    ret_data = {}

    return ret_data, mtype, info, ret_data