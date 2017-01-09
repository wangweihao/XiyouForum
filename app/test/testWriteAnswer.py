# coding:utf-8

import sys
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/handle')

import unittest
import writeAnswer


class testWriteAnswer(unittest.TestCase):
    def setUp(self):
        self.req = {}
        self.req['content']    = '看c++primer'
        self.req['uid'] = 1
        self.req['qid'] = 1

    def testWriteQuestion(self):
        result, err_code, info, ret_data = writeAnswer.writeAnswer(self.req)
        print info
        self.assertTrue(result)