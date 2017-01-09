# coding:utf-8

import sys
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/handle')

import unittest
import register

class test_register(unittest.TestCase):
    def setUp(self):
        self.req = {}
        self.req['email']    = '123@qq.com'
        self.req['passwd']   = '123123'
        self.req['nickname'] = '小虎2'

    def testRegister(self):
        result, err_code, info, ret_data = register.register(self.req)
        print info
        self.assertTrue(result)

