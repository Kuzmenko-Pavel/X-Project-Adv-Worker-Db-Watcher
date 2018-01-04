from threading import Thread
from queue import Queue
import time

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
            while not self.need_exit:
                try:
                    job = self.__queue.get(block=False, timeout=1)
                    print(job)
                    time.sleep(5)
                except Queue.Empty:
                    time.sleep(0.1)

    def message_processing(self, unused_channel, basic_deliver, properties, body):
        try:
            if basic_deliver.exchange == 'getmyad':
                key = basic_deliver.routing_key
                if key == 'campaign.start':
                    try:
                        self.loader.load_campaign({'guid': body.decode(encoding='UTF-8')})
                        logger.info('Campaign %s Start', body.decode(encoding='UTF-8'))
                    except Exception as e:
                        logger.error(exception_message(exc=str(e), key=str(key), body=body.decode(encoding='UTF-8')))

                elif key == 'campaign.stop':
                    try:
                        self.loader.stop_campaign(guid=body.decode(encoding='UTF-8'))
                        logger.info('Campaign %s Stop', body.decode(encoding='UTF-8'))
                    except Exception as e:
                        logger.error(exception_message(exc=str(e), key=str(key), body=body.decode(encoding='UTF-8')))

                elif key == 'campaign.update':
                    try:
                        self.loader.load_campaign({'guid': body.decode(encoding='UTF-8')})
                        logger.info('Campaign %s Update', body.decode(encoding='UTF-8'))
                    except Exception as e:
                        logger.error(exception_message(exc=str(e), key=str(key), body=body.decode(encoding='UTF-8')))

                elif key == 'informer.update':
                    try:
                        self.loader.load_domain({'guid': body.decode(encoding='UTF-8')})
                        self.loader.load_informer({'guid': body.decode(encoding='UTF-8')})
                        logger.info('Informer %s Update', body.decode(encoding='UTF-8'))
                    except Exception as e:
                        logger.error(exception_message(exc=str(e), key=str(key), body=body.decode(encoding='UTF-8')))

                elif key == 'informer.stop':
                    try:
                        self.loader.stop_informer(body.decode(encoding='UTF-8'))
                        logger.info('Informer %s Update', body.decode(encoding='UTF-8'))
                    except Exception as e:
                        logger.error(exception_message(exc=str(e), key=str(key), body=body.decode(encoding='UTF-8')))

                elif key == 'domain.stop':
                    try:
                        self.loader.stop_domain(body.decode(encoding='UTF-8'))
                        logger.info('Informer %s Update', body.decode(encoding='UTF-8'))
                    except Exception as e:
                        logger.error(exception_message(exc=str(e), key=str(key), body=body.decode(encoding='UTF-8')))

                elif key == 'account.update':
                    try:
                        self.loader.load_domain_category_by_account({'login': body.decode(encoding='UTF-8')})
                        self.loader.load_account({'login': body.decode(encoding='UTF-8')})
                        logger.info('Account %s Update', body.decode(encoding='UTF-8'))
                    except Exception as e:
                        logger.error(exception_message(exc=str(e), key=str(key), body=body.decode(encoding='UTF-8')))

                elif key == 'rating.informer':
                    try:
                        self.loader.load_offer_informer_rating()
                        logger.info('Rating Informer %s Update', body.decode(encoding='UTF-8'))
                    except Exception as e:
                        logger.error(exception_message(exc=str(e), key=str(key), body=body.decode(encoding='UTF-8')))

                # # elif key == 'rating.campaign':
                # #     pass
                # #     self.loader.load_campaign_rating()
                #
                elif key == 'rating.offer':
                    try:
                        self.loader.load_offer_rating()
                        logger.info('Rating Offer %s Update', body.decode(encoding='UTF-8'))
                    except Exception as e:
                        logger.error(exception_message(exc=str(e), key=str(key), body=body.decode(encoding='UTF-8')))
                else:
                    logger.debug('Received message # %s from %s - %s: %s %s', basic_deliver.delivery_tag,
                                 basic_deliver.exchange, basic_deliver.routing_key, properties.app_id, body)
            else:
                logger.debug('Received message # %s from %s - %s: %s %s', basic_deliver.delivery_tag,
                             basic_deliver.exchange, basic_deliver.routing_key, properties.app_id, body)
        except Exception as e:
            logger.error(exception_message(exc=str(e)))
