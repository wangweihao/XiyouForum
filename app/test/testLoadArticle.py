# coding:utf-8

import sys
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/handle')

import unittest
import loadArticle

class testLoadArticle(unittest.TestCase):
    def setUp(self):
        self.aid = 1

    def testLoadArticle(self):
        result, err_code, info, ret_data = loadArticle.loadArticle(self.aid)
        print ret_data
        print info
        self.assertTrue(result)