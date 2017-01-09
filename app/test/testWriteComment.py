# coding:utf-8

import sys
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/handle')

import unittest
import writeComment

class testWriteComment(unittest.TestCase):
    def setUp(self):
        self.req = {}
        self.req['content'] = 'hello world'
        self.req['aid']     = 1
        self.req['uid']     = 1

    def testWriteComment(self):
        result, err_code, info, ret_data = writeComment.writeComment(self.req)
        print err_code
        print info
        print ret_data
        self.assertTrue(result)
