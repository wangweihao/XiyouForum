# coding:utf-8

import sys
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/handle')

import unittest
import loadHome

class testLoadQuestion(unittest.TestCase):
    def setUp(self):
        self.page  = 1
        self.mtype = 1

    def testLoadQuestion(self):
        ret_data, hot_articles = loadHome.load_home(self.page, self.mtype)
        print ret_data
        print hot_articles