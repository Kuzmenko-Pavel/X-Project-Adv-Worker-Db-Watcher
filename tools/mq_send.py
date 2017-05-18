import sys
import os
import argparse
from trafaret_config import commandline
import pika
from x_project_adv_worker_db_watcher.utils import TRAFARET_CONF


class MQ(object):
    '''
    Класс отвечает за отправку сообщений в RabbitMQ.
    '''

    def __init__(self, config):
        self.connection = pika.BlockingConnection(pika.URLParameters(config['amqp']))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='getmyad', exchange_type='topic', passive=True)

    def campaign_start(self, campaign_id):
        ''' Отправляет уведомление о запуске рекламной кампании ``campaign_id`` '''

        self.channel.basic_publish('getmyad', 'campaign.start', campaign_id)
        print("AMQP Campaign start %s" % campaign_id)

    def campaign_stop(self, campaign_id):
        ''' Отправляет уведомление об остановке рекламной кампании ``campaign_id`` '''

        self.channel.basic_publish('getmyad', 'campaign.stop', campaign_id)
        print("AMQP Campaign stop %s" % campaign_id)

    def campaign_update(self, campaign_id):
        ''' Отправляет уведомление об обновлении рекламной кампании ``campaign_id`` '''
        self.channel.basic_publish('getmyad', 'campaign.update', campaign_id)
        print("AMQP Campaign update %s" % campaign_id)

    def informer_update(self, informer_id):
        ''' Отправляет уведомление о том, что информер ``informer_id`` был изменён '''
        self.channel.basic_publish('getmyad', 'informer.update', informer_id)
        print("AMQP Informer update %s" % informer_id)

    def account_update(self, login):
        ''' Отправляет уведомление об изменении в аккаунте ``login`` '''
        self.channel.basic_publish('getmyad', 'account.update', login)
        print("AMQP Account update %s" % login)


def main(argv):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    ap = argparse.ArgumentParser(description='Great Description To Be Here')
    ap.add_argument('-m', "--message", action='store', dest='message_type', help='send message type',
                    choices=['campaign.start', 'campaign.stop', 'campaign.update', 'informer.update'], required=True)

    ap.add_argument('-i', "--id", action='store', dest='item_id', help='item id', required=True, type=str)

    commandline.standard_argparse_options(ap.add_argument_group('configuration'),
                                          default_config=dir_path + '/../conf.yaml')

    options = ap.parse_args(argv)
    print(options)
    config = commandline.config_from_options(options, TRAFARET_CONF)

    sender = MQ(config)
    if options.message_type == 'campaign.start':
        sender.campaign_start(options.item_id)

    elif options.message_type == 'campaign.stop':
        sender.campaign_stop(options.item_id)

    elif options.message_type == 'campaign.update':
        sender.campaign_update(options.item_id)

    elif options.message_type == 'informer.update':
        sender.informer_update(options.item_id)

    elif options.message_type == 'account.update':
        sender.account_update(options.item_id)


if __name__ == '__main__':
    main(sys.argv[1:])
