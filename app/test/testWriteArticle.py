# coding:utf-8

import sys
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/handle')

import unittest
import writeArticle


class testWriteArticle(unittest.TestCase):
    def setUp(self):
        self.req = {}
        self.req['title']    = '如何学习Java'
        self.req['content']  = '如何学习Java'
        self.req['tab']      = 'c++;java;python;erlang'
        self.req['uid']      = 1

    def testWriteQuestion(self):
        result, err_code, info, ret_data = writeArticle.writeArticle(self.req)
        print info
        self.assertTrue(result)