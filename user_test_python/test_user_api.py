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
       
        # Цикл проверки успешности регистрации
        for _ in range(number):
            # Регистрация пользователя
            user = do_register()
            if 'type' in user["0"]['json']:
                logging.error(user["0"]['json']['type'])
                assert False
            else:
                logging.info(
                    f'Пользователь успешно зарегестрирован:\
                    "email" : {user["0"]["email"]},\
                        "name": {user["0"]["name"]},\
                            "password" : {user["0"]["password"]}'
                            )
                assert True
        break


def test_do_login():
    """
    Тест метода  doLogin
    Необходимость использования таймера указана в docstring test_doregister
    """
    logging.info('-'*15 + 'Запуск test_dologin')
    
    # Заводим таймер для защиты от ошибок на сервере
    timing = time.time()
    
    # Цикл с таймером на 10 сек
    while True:

        # Проверка времени выполнения цикла
        if time.time() - timing > 10.0:
            logging.error('Превышено время ожидания')
            assert False

        # Регистрация нового пользователя
        user = do_register()

        # Авторизация зарегестрированного пользователя
        response_json = do_login(user["0"]["email"], user["0"]["password"])
        
        # Проверка успешности авторизации
        if response_json['result']:
            logging.info(f'Авторизация пользователя выполнена успешно\
                "email" : {user["0"]["email"]}, "password" : {user["0"]["password"]}')
            assert True
            break
        else:
            logging.error(f'Ошибка авторизации пользователя : {response_json}')
            assert False
            
                
def test_createtask():
    """Тест метода CreaTetask"""
    logging.info('-'*15 + 'Запуск test_createtask')
    
    # Заводим таймер для защиты от ошибок на сервере
    timing = time.time()

    # Цикл с таймером на 10 сек
    while True:

        # Проверка времени выполнения цикла
        if time.time() - timing > 10.0:
            logging.error('Превышено время ожидания')
            assert False
        
        # Извлечение параметров task_title, task_description, email_owner
        params_test = get_params_test()
       
        # Регистрация нового пользователя
        user = do_register()

        # Создание задачи для нового пользователя
        response_json = create_task(
            params_test['task_title'],
            params_test['task_description'],
            params_test['manager_email'],
            user["0"]['email']
            )

        # Проверка успешности создания задачи
        if response_json['message'] == 'Задача успешно создана!':
            logging.info(f'Задача успешно создана: {response_json}')
            assert True
            # Возврат id задачи в массиве
            return [response_json['id_task']]
        else:
            logging.error(f'Ошибка создания задачи : {response_json}')
            assert False


def test_create_company(users_num=1):
    """Тест метода CreateCompany

    Args:
        users_num: количество пользователей в компании
    """
    logging.info('-'*15 + 'Запуск test_create_company')
    
    # Таймер
    timing = time.time()
    while True:
        # проверка времени выполнения цикла
        if time.time() - timing > 10.0:
            logging.error('Превышено время ожидания')
            assert False

        # Извлечение параметров company_name, company_type, email_owner
        params_test = get_params_test()
        
        # Регистрация новых пользователей
        user = do_register(users_num)
       
        # Создание списка email пользователей
        email_user_list = [user[str(num)]['email'] for num in range(users_num)]
        
        # Запрос на создание компании
        response_json = create_company(
            params_test['company_name'],
            params_test['company_type'],
            email_user_list,
            params_test['manager_email']
            )

        # Проверка успешности создания компании
        if response_json['type'] == 'success':
            logging.info(f'Компания успешно создана: {response_json}')
            assert True
            # Возврат id компании в массиве
            return [response_json['id_company']]
        else:
            logging.error(f'Ошибка создания компании: {response_json}')
            assert False


def test_create_user(users_num=1):
    """Тест метода CreateUser
    
    Args:
        users_num: количество пользователей в компании
        
    """
    logging.info('-'*15 + 'Запуск test_create_user')

    # Таймер
    timing = time.time()
    while True:
        # проверка времени выполнения цикла
        if time.time() - timing > 10.0:
            logging.error('Превышено время ожидания')
            assert False

        # Генерация данных нового пользователя
        email, name, password = random_user_generator()

        # Получение id задания рандомному пользователю в виде массива
        task = test_createtask()

        # Получение id рандомной компании в виде массива
        company = test_create_company()

        # Запрос на создание пользователя
        response_json = create_user(email, name, task, company)

        # Проверка успешности создания пользователя
        if 'type' in response_json:
            logging.error(f'Ошибка создания пользователя: {response_json}')
            assert False
        else:
            logging.info(f'Пользователь успешно создан: {response_json}')
            assert True
            break
