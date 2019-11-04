import time
from threading import Thread

from x_project_adv_worker_db_watcher.logger import logger, exception_message
from x_project_adv_worker_db_watcher.loader import Loader


class Worker(Thread):
    def __init__(self, queue, db_session, parent_db_session, config):
        super(Worker, self).__init__()
        self.__queue = queue
        self.need_exit = False
        self.session = db_session
        self.parent_session = parent_db_session
        self.config = config
        self.loader = Loader(self.session, self.parent_session, self.config['loader'])
        self.setDaemon(True)
        self.start()

    def run(self):
        try:
            self.loader.all()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))
        finally:
            logger.info('Starting Worker')
            while not self.need_exit:
                if not self.__queue.empty():
                    job = self.__queue.get()
                    self.message_processing(*job)
                    self.__queue.task_done()
                else:
                    time.sleep(1)
            logger.info('Stopping Worker')

    def message_processing(self, key, body):
        try:
            logger.info('Received message # %s: %s', key, body)
            if key == 'block.load':
                self.loader.load_block(**body)
            elif key == 'block.update':
                self.loader.load_block(**body)
            elif key == 'block.delete':
                self.loader.delete_block(**body)
            elif key == 'campaign.load':
                self.loader.load_campaign(**body)
            elif key == 'campaign.update':
                self.loader.load_campaign(**body)
            elif key == 'campaign.delete':
                self.loader.delete_campaign(**body)
            elif key == 'offer.update':
                self.loader.load_offer(**body)
            elif key == 'offer.delete':
                self.loader.delete_offer(**body)
            elif key == 'reload.all':
                self.loader.truncate()
                self.loader.all()
            elif key == 'rating.update':
                self.loader.load_rating()

        except Exception as e:
            logger.error(exception_message(exc=str(e)))
