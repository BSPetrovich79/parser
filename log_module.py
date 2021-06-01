# -*- coding: utf-8 -*-
import logging
import datetime


logging.basicConfig(level=logging.INFO)
logg = logging.getLogger()


def log(message, attach='attachment'):
    """
    Функция для логирования.
    Выводит  сообщения теста в лог и дублирует их в отчете allure.
    :param message: Заголовок сообщения
    :param attach: содержательная часть(опционально)
    """
    attach = str(attach)
    now = datetime.datetime.now().strftime("%H:%M:%S")
    logg.info(now + " " + message) if attach == 'attachment' or len(attach) > 200 \
        else logg.info(now + " " + message + ': ' + attach)
