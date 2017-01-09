# coding:utf-8

import sys
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/handle')

import unittest
import loadArticles

class testLoadArticles(unittest.TestCase):
    def setUp(self):
        self.page  = 1
        self.mtype = 2

    def testLoadArticles(self):
        ret_data = loadArticles.load_articles(self.page, self.mtype)
        print ret_data
        for i in ret_data:
            print i