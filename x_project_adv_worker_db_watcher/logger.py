import os
import logging
dir_path = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger('x_project_adv_worker_db_watcher')
logger.setLevel(logging.DEBUG)
# logger.propagate = False
fh = logging.FileHandler(dir_path + '/../test.log', 'w')
fh.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
logger.addHandler(consoleHandler)