import time
from threading import Thread

from x_project_adv_worker_db_watcher.logger import logger, exception_message
from x_project_adv_worker_db_watcher.parent_db.loader import Loader


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
            if key == 'campaign.start':
                try:
                    self.loader.load_campaign({'guid': body})
                    logger.info('Campaign %s Start', body)
                except Exception as e:
                    logger.error(exception_message(exc=str(e), key=str(key), body=body))

            elif key == 'campaign.stop':
                try:
                    self.loader.stop_campaign(guid=body)
                    logger.info('Campaign %s Stop', body)
                except Exception as e:
                    logger.error(exception_message(exc=str(e), key=str(key), body=body))

            elif key == 'campaign.update':
                try:
                    self.loader.load_campaign({'guid': body})
                    logger.info('Campaign %s Update', body)
                except Exception as e:
                    logger.error(exception_message(exc=str(e), key=str(key), body=body))

            elif key == 'campaign.thematic':
                try:
                    # self.loader.load_campaign({'guid': body})
                    logger.info('Campaign %s Thematic Update', body)
                except Exception as e:
                    logger.error(exception_message(exc=str(e), key=str(key), body=body))

            elif key == 'informer.update':
                try:
                    self.loader.load_domain({'guid': body})
                    self.loader.load_informer({'guid': body})
                    logger.info('Informer %s Update', body)
                except Exception as e:
                    logger.error(exception_message(exc=str(e), key=str(key), body=body))

            elif key == 'informer.stop':
                try:
                    self.loader.stop_informer(body)
                    logger.info('Informer %s Update', body)
                except Exception as e:
                    logger.error(exception_message(exc=str(e), key=str(key), body=body))

            elif key == 'domain.stop':
                try:
                    self.loader.stop_domain(body.decode(encoding='UTF-8'))
                    logger.info('Informer %s Update', body)
                except Exception as e:
                    logger.error(exception_message(exc=str(e), key=str(key), body=body))

            elif key == 'account.update':
                try:
                    self.loader.load_domain_category_by_account({'login': body})
                    self.loader.load_account({'login': body})
                    logger.info('Account %s Update', body)
                except Exception as e:
                    logger.error(exception_message(exc=str(e), key=str(key), body=body))

            elif key == 'rating.informer':
                try:
                    self.loader.load_offer_informer_rating()
                    logger.info('Rating Informer %s Update', body)
                except Exception as e:
                    logger.error(exception_message(exc=str(e), key=str(key), body=body))

            # # elif key == 'rating.campaign':
            # #     pass
            # #     self.loader.load_campaign_rating()
            #
            elif key == 'rating.offer':
                try:
                    self.loader.load_offer_rating()
                    logger.info('Rating Offer %s Update', body)
                except Exception as e:
                    logger.error(exception_message(exc=str(e), key=str(key), body=body))
            else:
                logger.debug('Received message # %s: %s', key, body)
        except Exception as e:
            logger.error(exception_message(exc=str(e)))
