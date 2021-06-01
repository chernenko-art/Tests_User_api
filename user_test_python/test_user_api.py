import pytest
import logging
import time
from user_api import *
from conftest import *


# Конфигурация логов
FORMAT = '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d:%(funcName)-20s] %(message)s'
logging.basicConfig(level=level_logging(),
                    format=FORMAT,
                    datefmt='%m-%d %H:%M',
                    filename='user_tests.log'
                    )


def test_do_register():
    """
    Тест метода doRegister

    Тест реальзован при помощи проверки ответа об успешной регистрации 
    в бесконечном цикле, для предотвращения зацикливания, при возникновении
    непредвиденной ошибки, используется таймер на 10 сек.     

    """
    logging.info('-'*15 + 'Запуск test_doregister')
    timing = time.time() # заводим таймер
    while True:
        if time.time() - timing > 10.0:  # проверка времени выполнения цикла
            logging.error('Превышено время ожидания')
            break
        response_json, email, name, password = do_register()
        if 'type' in response_json:
            logging.error(response_json['type'])
            assert False
        else:
            logging.info(f'Пользователь успешно зарегестрирован:\
                "email" : {email}, "name": {name}, "password" : {password}')
            assert True
            break


def test_do_login():
    """
    Тест метода  doLogin
    Необходимость использования таймера указана в docstring test_doregister
    """
    logging.info('-'*15 + 'Запуск test_dologin')
    timing = time.time()  # заводим таймер
    while True:
        if time.time() - timing > 10.0:  # проверка времени выполнения цикла
            logging.error('Превышено время ожидания')
            break
        response_json_reg, email, name, password = do_register()
        response_json_log = do_login(email, password)
        if response_json_log['result']:
            logging.info(f'Авторизация пользователя выполнена успешно\
                "email" : {email}, "password" : {password}')
            assert True
        else:
            logging.debug(f'response_json_login = {response_json_log}')
            logging.error('Ошибка авторизации пользователя')
            assert False
            
                
def test_createtask():
    """Тест метода CreaTetask"""
    logging.info('-'*15 + 'Запуск CreaTetask')
    timing = time.time()  # заводим таймер
    while True:
        if time.time() - timing > 10.0:  # проверка времени выполнения цикла
            logging.error('Превышено время ожидания')
            break
        params_test = get_params_test()
        json_body, email_assign, name, password = do_register()
        response_json = create_task(
            params_test['task_title'],
            params_test['task_description'],
            params_test['manager_email'],
            email_assign
            )
        if response_json['message'] == 'Задача успешно создана!':
            logging.info(f'Задача успешно создана: {response_json}')
            assert True
            break
        else:
            logging.debug(f'response_json_login = {response_json}')
            logging.error('Ошибка создания задачи')
            assert False

