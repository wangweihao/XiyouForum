# coding:utf-8

import logging
import json
from config import *

def config_log():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [line:%(lineno)-4d] \
                                %(levelname)-5s %(filename)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=LOG_PATH,
                        filemode='w+')

def check_result(result, mtype, info, data):
    if result == True:
        return json.dumps({"status":"ok",
                           "info"  : info,
                           "data"  : data})
    else:
        return json.dumps({"status":"error",
                           "type"  : mtype,
                           "info"  : info,
                           "data"  : data
                          })

def getSessionInfo(red, session_id, keys):
    ret_data = {}
    for key in keys:
        ret_data[key] = red.hget(session_id, key)

    return ret_data