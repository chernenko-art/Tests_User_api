import pytest
import logging
import time

from requests.api import request
from user_api import *
from conftest import *


# Конфигурация логов
FORMAT = '%(asctime)s,%(msecs)d %(levelname)-8s \
    [%(filename)s:%(lineno)d:%(funcName)-20s] %(message)s'
logging.basicConfig(level=level_logging(),
                    format=FORMAT,
                    datefmt='%m-%d %H:%M',
                    filename='user_tests.log'
                    )


def test_do_register(number: int = 1):
    """Тест метода doRegister

    Args:
        number (int, optional): количество пользователей. Defaults to 1.
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
    """Тест метода  doLogin"""
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
    """Тест метода CreaTetask

    Returns:
        list: id задачи
    """
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


def test_create_company(users_num: int = 1):
    """Тест метода CreateCompany

    Args:
        users_num (int, optional): количество пользователей в компании. Defaults to 1.

    Returns:
        list: id компании
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


def test_create_user():
    """Тест метода CreateUser

    Returns:
        tuple: email, name, task, company, optional_params
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

        # Получение параметров пользователя и запрос на создание
        optional_params = optional_user_params()
        response_json = create_user(email, name, task, company, optional_params)

        # Проверка успешности создания пользователя
        if 'type' in response_json:
            logging.error(f'Ошибка создания пользователя: {response_json}')
            assert False
        else:
            logging.info(f'Пользователь успешно создан: {response_json}')
            assert True
            return email, name, task, company, optional_params


def test_create_user_with_task():
    """Тест метода CreateUser

    Returns:
        tuple: email, name, task, company, optional_params
    """
    logging.info('-'*15 + 'Запуск test_create_user_with_task')

    # Таймер
    timing = time.time()
    while True:
        # проверка времени выполнения цикла
        if time.time() - timing > 10.0:
            logging.error('Превышено время ожидания')
            assert False

        # Генерация данных нового пользователя
        email, name, password = random_user_generator()

        # Получение списка параметров задачи
        params_test = get_params_test()
        task = [params_test['task_json']]

        # Получение id рандомной компании в виде массива
        company = test_create_company()

        # Получение параметров пользователя и запрос на создание
        optional_params = optional_user_params()       
        response_json = create_user_with_task(email, name, task, company, optional_params)

        # Проверка успешности создания пользователя
        if 'type' in response_json:
            logging.error(f'Ошибка создания пользователя: {response_json}')
            assert False
        else:
            logging.info(f'Пользователь успешно создан: {response_json}')
            assert True
            return email, name, task, company, optional_params


def test_add_avatar():
    """Тест метода  addAvatar

    Returns:
        str: email пользователя
    """
    logging.info('-'*15 + 'Запуск test_add_avatar')

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

        # Получение файла изображения
        avatar = avatar_file()
        
        # Запрос на добавление аватара пользователю
        response_json = add_avatar(user["0"]["email"], avatar)

        # Проверка успешности добавления аватара пользователю
        if response_json['status'] == 'ok':
            logging.info(f'Аватар добавлен пользователю: {user["0"]["email"]}')
            assert True
            return user["0"]["email"]
        else:
            logging.error(f'Ошибка test_add_avatar : {response_json}')
            assert False


def test_delele_avatar():
    """Тест метода  DeleteAvatar"""
    logging.info('-'*15 + 'Запуск test_delele_avatar')

    # Заводим таймер для защиты от ошибок на сервере
    timing = time.time()

    # Цикл с таймером на 10 сек
    while True:

        # Проверка времени выполнения цикла
        if time.time() - timing > 10.0:
            logging.error('Превышено время ожидания')
            assert False
        
        # Создание аватара пользователя, получение email
        email_user = test_add_avatar()
        
        # Запрос на удаление аватара пользователя
        response_json = delele_avatar(email_user)

        # Проверка успешности добавления аватара пользователю
        if response_json['status'] == 'ok':
            logging.info(f'Аватар  пользователя {email_user} удален успешно.')
            assert True
            break
        else:
            logging.error(f'Ошибка test_add_avatar : {response_json}')
            assert False


def test_magic_search():
    """Тест метода  MagicSearch"""
    logging.info('-'*15 + 'Запуск test_magic_search')

    # Заводим таймер для защиты от ошибок на сервере
    timing = time.time()

    # Цикл с таймером на 10 сек
    while True:

        # Проверка времени выполнения цикла
        if time.time() - timing > 10.0:
            logging.error('Превышено время ожидания')
            assert False

        # Определение параметров поиска
        email, name, task, company, optional_params = test_create_user()

        # Поиск по заданным параметрам
        search_params = ' '.join([email, name, str(company[0])])
        response_json = magic_search(search_params)
        
        # Проверка успешности выполнения поиска
        if 'code_error' in response_json:
            logging.error(f'Ошибка test_magic_search : {response_json}')
            assert False
        else:
            logging.info(f'Поиск выполнен успешно. Результаты поиска: {response_json}')
            assert True
            break         


def test_user_one_field():
    """Тест метода UserOneField    """
    logging.info('-'*15 + 'Запуск test_user_one_field')

    # Таймер
    timing = time.time()
    while True:
        # проверка времени выполнения цикла
        if time.time() - timing > 10.0:
            logging.error('Превышено время ожидания')
            assert False

        # Регистрация нового пользователя
        user = do_register()

        # Запрос на изменение поля 'hobby' пользователя
        response_json = user_one_field(user['0']["email"])

        # Проверка успешности создания пользователя
        if response_json['message'] == 'Пользователь с таким email не найден!':
            logging.error(f'Ошибка изменения параметров пользователя: {response_json}')
            assert False
        else:
            logging.info(f'Параметры пользователя успешно изменены: {response_json}')
            assert True
            return


def test_get_company():
    """Тест метода getCompany"""
    logging.info('-'*15 + 'Запуск test_get_company')

    # Таймер
    timing = time.time()
    while True:
        # проверка времени выполнения цикла
        if time.time() - timing > 10.0:
            logging.error('Превышено время ожидания')
            assert False

        # Создание компании и получение id
        id_company = test_create_company()

        # Запрос на поиск компании
        response_json = get_company(*id_company)

        # Проверка успешности создания пользователя
        if response_json['type'] == 'error':
            logging.error(f'Ошибка поиска компании: {response_json}')
            assert False
        else:
            logging.info(f'Компания найдена: {response_json}')
            assert True
            return

def test_get_user():
    """Тест метода getUser"""
    logging.info('-'*15 + 'Запуск test_get_user')

    # Таймер
    timing = time.time()
    while True:
        # проверка времени выполнения цикла
        if time.time() - timing > 10.0:
            logging.error('Превышено время ожидания')
            assert False

        # Регистрация нового пользователя
        user = do_register()

        # Запрос на поиск компании
        response_json = get_user(user['0']["email"])

        # Проверка успешности создания пользователя
        if 'type' in response_json:
            logging.error(f'Ошибка поиска пользователя: {response_json}')
            assert False
        else:
            logging.info(f'Пользователь найден: {response_json}')
            assert True
            return


def test_get_user_full():
    """Тест метода getUserfull"""
    logging.info('-'*15 + 'Запуск test_get_user_full')

    # Таймер
    timing = time.time()
    while True:
        # проверка времени выполнения цикла
        if time.time() - timing > 10.0:
            logging.error('Превышено время ожидания')
            assert False

        # Регистрация нового пользователя
        user = do_register()

        # Запрос на поиск компании
        response_json = get_user_full(user['0']["email"])

        # Проверка успешности создания пользователя
        if 'type' in response_json:
            logging.error(f'Ошибка поиска пользователя: {response_json}')
            assert False
        else:
            logging.info(f'Пользователь найден: {response_json}')
            assert True
            return


def test_metod_api_lis():
    """Тест метода MetodApiList"""
    logging.info('-'*15 + 'Запуск test_metod_api_lis')

    # Таймер
    timing = time.time()
    while True:
        # проверка времени выполнения цикла
        if time.time() - timing > 10.0:
            logging.error('Превышено время ожидания')
            assert False

        # Запрос на получение перечня методов api
        response_json = metod_api_list()

        # Проверка успешности создания пользователя
        if 'resources' in response_json:
            logging.info(f'Перечнь методов api получен: {response_json}')
            assert True
            return
            
        else:
            logging.error(f'Ошибка получения перечня методов api: {response_json}')
            assert False


def test_update_task():
    """Тест метода UpdateTask"""
    logging.info('-'*15 + 'Запуск test_update_task')
    
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
        id_task_list = test_createtask()
        
        # Обновление задачи
        response_json = update_task(params_test['manager_email'], user["0"]['email'],
                                    *id_task_list, params_test['task_title'], params_test['task_description'])

        # Проверка успешности создания задачи
        if response_json['type'] == 'error':
            logging.error(f'Ошибка создания задачи: {response_json}')
            assert False  
        else:
            logging.info(f'Задача успешно изменена: {response_json}')
            assert True
            break


def test_add_task_in_cron():
    """Тест метода AddTaskInCron"""
    logging.info('-'*15 + 'Запуск test_add_task_in_cron')

    # Заводим таймер для защиты от ошибок на сервере
    timing = time.time()

    # Цикл с таймером на 10 сек
    while True:

        # Проверка времени выполнения цикла
        if time.time() - timing > 10.0:
            logging.error('Превышено время ожидания')
            assert False

        # Извлечение параметров email_owner, hours, minutes, month, days, day_weeks
        params_test = get_params_test()
        
        # Создание задачи для нового пользователя
        id_task_list = test_createtask()

        # Создание запуска задачи по расписанию
        request_params = [
            params_test['manager_email'],
            *id_task_list,
            params_test['task_json']['hours'],
            params_test['task_json']['minutes'],
            params_test['task_json']['month'],
            params_test['task_json']['days'],
            params_test['task_json']['day_weeks']
        ]
        response_json = add_task_in_cron(*request_params)

        # Проверка успешности создания задачи
        if response_json['type'] == 'error':
            logging.error(f'Ошибка создания задачи по расписанию: {response_json}')
            assert False
        else:
            logging.info(f'Расписание запуска задачи успешно создано: {response_json}')
            assert True
            break


def test_del_task():
    """Тест метода delTask"""
    logging.info('-'*15 + 'Запуск test_del_task')

    # Заводим таймер для защиты от ошибок на сервере
    timing = time.time()

    # Цикл с таймером на 10 сек
    while True:

        # Проверка времени выполнения цикла
        if time.time() - timing > 10.0:
            logging.error('Превышено время ожидания')
            assert False

        # Извлечение параметров email_owner
        params_test = get_params_test()
        
        # Создание задачи для нового пользователя
        id_task_list = test_createtask()

        # Удаление задачи пользователю
        response_json = del_task(params_test['manager_email'], *id_task_list)

        # Проверка успешности удаления задачи
        if response_json['type'] == 'error':
            logging.info(f'Ошибка удаления задачи пользователю: {response_json}')
            assert False
        else:
            logging.error(f'Задача успешно удалена: {response_json}')
            assert True
            break
            