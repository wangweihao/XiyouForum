# coding:utf-8

import sys
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/handle')

import unittest
import login
import redis

red = redis.Redis(host='127.0.0.1', port=6379, db=0)


class test_login(unittest.TestCase):
    def setUp(self):
        self.req = {}
        self.req['email']    = '123@qq.com'
        self.req['passwd']   = '123123'

    def testRegister(self):
        result, err_code, info, ret_data = login.login(self.req, red)
        print info
        self.assertTrue(result)

