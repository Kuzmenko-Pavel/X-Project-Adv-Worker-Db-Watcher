import sys
import os
import argparse
from daemonize import Daemonize
from trafaret_config import commandline
from x_project_adv_worker_db_watcher.logger import logger, fh
from x_project_adv_worker_db_watcher.utils import TRAFARET_CONF
from x_project_adv_worker_db_watcher.watcher import Watcher
from x_project_adv_worker_db_watcher.models import DBSession, get_engine, check_table

pid = "./test.pid"

config = None


def action():
    global config
    engine = get_engine(config)
    try:
        check_table(engine)
    except Exception as e:
        logger.error(e)

    watcher = Watcher(config, DBSession)
    try:
        watcher.run()
    except KeyboardInterrupt:
        watcher.stop()


def main(argv):
    global config
    dir_path = os.path.dirname(os.path.realpath(__file__))
    keep_fds = [fh.stream.fileno()]
    ap = argparse.ArgumentParser(description='Great Description To Be Here')
    commandline.standard_argparse_options(ap.add_argument_group('configuration'),
                                          default_config=dir_path + '/../conf.yaml')
    options = ap.parse_args(argv)
    config = commandline.config_from_options(options, TRAFARET_CONF)

    daemon = Daemonize(app="x_project_adv_worker_db_watcher", pid=pid, action=action, keep_fds=keep_fds, logger=logger,
                       verbose=True, foreground=True, chdir=dir_path + '/../')
    daemon.start()

if __name__ == '__main__':
    main(sys.argv[1:])
