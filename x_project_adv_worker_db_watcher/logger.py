import linecache
import sys
import logging
import os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger('x_project_adv_worker_db_watcher')
logger.setLevel(logging.DEBUG)
# fh = logging.FileHandler(dir_path + '/../test.log', 'w')
# fh.setLevel(logging.DEBUG)
# logger.addHandler(fh)
consoleHandler = logging.StreamHandler()
logger.addHandler(consoleHandler)


def exception_message(*args, **kwargs):
    params = json.dumps({'args': args, 'kwargs': kwargs})
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {} PARAMS: {}'.format(filename, lineno, line.strip(), exc_obj, params)
