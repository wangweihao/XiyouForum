# coding:utf-8

import sys
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/database')
sys.path.append('/Users/wwh/PycharmProjects/XiyouForum/app/handle')

import unittest
import loadQuestion

class testLoadQuestion(unittest.TestCase):
    def setUp(self):
        self.qid = 10

    def testLoadQuestion(self):
        result, err_code, info, ret_data = loadQuestion.loadQuestion(self.qid)
        self.assertTrue(result)