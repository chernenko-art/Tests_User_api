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


def test_do_register(number=1):
    """
    Тест метода doRegister
    
    Args:
        number: количество пользователей    

    """
    logging.info('-'*15 + 'Запуск test_doregister')
    
    # Заводим таймер для защиты от ошибок на сервере
    timing = time.time()
    
    # Цикл с таймером на 10 сек
    while True:

        # Проверка времени выполнения цикла
        if time.time() - timing > 10.0: 
            logging.error('Превышено время ожидания')
            assert False
            break
       
        # Цикл проверки успешности регистрации
        for _ in range(number):
            # Регистрация пользователя
            _do_register = do_register()
            if 'type' in _do_register["0"]['json']:
                logging.error(_do_register["0"]['json']['type'])
                assert False
            else:
                logging.info(
                    f'Пользователь успешно зарегестрирован:\
                    "email" : {_do_register["0"]["email"]},\
                        "name": {_do_register["0"]["name"]},\
                            "password" : {_do_register["0"]["password"]}'
                            )
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
            assert False
            break
        _do_register = do_register()
        response_json = do_login(_do_register["email"], _do_register["password"])
        if response_json['result']:
            logging.info(f'Авторизация пользователя выполнена успешно\
                "email" : {_do_register["email"]}, "password" : {_do_register["password"]}')
            assert True
            break
        else:
            logging.debug(f'response_json_login = {response_json}')
            logging.error('Ошибка авторизации пользователя')
            assert False
            
                
def test_createtask():
    """Тест метода CreaTetask"""
    logging.info('-'*15 + 'Запуск test_createtask')
    timing = time.time()  # заводим таймер
    while True:
        if time.time() - timing > 10.0:  # проверка времени выполнения цикла
            logging.error('Превышено время ожидания')
            assert False
            break
        params_test = get_params_test()
        _do_register = do_register()
        response_json = create_task(
            params_test['task_title'],
            params_test['task_description'],
            params_test['manager_email'],
            _do_register['email']
            )
        if response_json['message'] == 'Задача успешно создана!':
            logging.info(f'Задача успешно создана: {response_json}')
            assert True
            break
        else:
            logging.debug(f'response_json_login = {response_json}')
            logging.error('Ошибка создания задачи')
            assert False
