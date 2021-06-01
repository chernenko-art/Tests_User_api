# from requests import get, put, post, delete
import logging
import time
from conftest import level_logging,  url_adress
from user_api import *


# Конфигурация логов
FORMAT = '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d:%(funcName)-20s] %(message)s'
logging.basicConfig(level=level_logging(),
                    format=FORMAT,
                    datefmt='%m-%d %H:%M',
                    filename='user_tests.log'
                    )


def test_doregister():
    """
    Тест метода doRegister

    Тест реальзован при помощи проверки ответа об успешной регистрации 
    в бесконечном цикле, для предотвращения зацикливания, при возникновении
    непредвиденной ошибки используется таймер на 10 сек.     

    """
    logging.info('-'*15 + 'Запуск test_doregister')
    timing = time.time() # заводим таймер
    while True:
        if time.time() - timing > 10.0:  # проверка времени выполнения цикла
            logging.error('Превышено время ожидания')
            break
        response_body = doregister()
        if 'type' in response_body:
            logging.error('-'*15 + response_body[type])
        else:
            logging.info('-'*15 + f'Пользователь успешно зарегестрирован:\
                "name" : "{response_body["name"]}",\
                    "email" : "{response_body["email"]}",\
                        "password" : "{response_body["password"]}")')
            assert True
            break


def test_createtask():
    """Тест метода CreaTetask"""
    pass

