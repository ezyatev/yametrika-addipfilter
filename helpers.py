import argparse
import logging
import os
from urllib.parse import urlencode

from twisted.python import log

API_URL = 'https://api-metrika.yandex.ru'


def get_request_url(path, params=None):
    if params is None:
        params = {}
    request_url = '{}{}?{}'.format(API_URL, path, urlencode(params))
    return bytes(request_url, encoding='utf8')


def get_clientip_filters(filters):
    result = []
    for f in filters:
        for k, v in f.items():
            if k == 'attr' and v == 'client_ip':
                result.append(f['id'])
    return result


def start_logging_observer(logfile):
    logger = logging.getLogger()
    file_handler = logging.FileHandler(logfile)
    logger.addHandler(file_handler)
    logger.setLevel(logging.WARNING)

    # Output twisted messages to Python standard library module.
    observer = log.PythonLoggingObserver()
    observer.start()


def create_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", help="Режим: add или delete.", default="add"),
    parser.add_argument("--ip", help="IP-адрес для создания фильтра."),
    parser.add_argument("--status", help="Статус фильтра: active или disabled.", default="active"),
    parser.add_argument("--action", help="Тип фильтра: include или exclude.", default="exclude"),
    parser.add_argument("--logfile", help="Текстовой файл для записи отчета.", default="log.txt"),
    parser.add_argument("--token",
                        help="Токен для работы с API. Можно запросить по ссылке: "
                             "https://oauth.yandex.ru/authorize?response_type=token&client_id=<ID приложения>",
                        default=os.environ.get('TOKEN', '')),
    return parser
