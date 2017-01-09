# coding:utf-8

import sys

import redis
import unittest

class test_register(unittest.TestCase):
    def setUp(self):
        self.host='127.0.0.1'
        self.port=6379

        self.red = redis.Redis(host=self.host, port=self.port, db=0)


    def testRegister(self):
        self.red.hset('hello', 'nickname', '王虎')
        self.red.hset('hello', 'head_url', 'www.baidu.com')
        self.red.hset('hello', 'reputation', '100')

