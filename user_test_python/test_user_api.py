import pytest
from requests import get, post, put, delete
import logging
import json

path_json_file = '/home/chernenkoac/prog/test_users_api/user_test_python/config.json'


def level_logging():
    """Считывание level logging из config.json"""
    json_file = open(path_json_file, 'r').read()
    json_body = json.loads(json_file)
    numeric_level = getattr(logging, json_body["log"]["level"].upper(), None)
    return numeric_level

#Конфигурация логов
logging.basicConfig(level=level_logging(),
                    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='user_tests.log'
                    )

user_email = 'python_user@gmail.com'
user_name = 'Reno'
user_password = 123
url = 'http://users.bugred.ru'


def test_doRegister():
    '''Тест регистрации пользователя'''
    logging.info('Запуск do_register')
    endpoint = '/tasks/rest/doregister'
    response = post(url + endpoint, json = {
        "email" : user_email,
        "name": user_name,
        "password": user_password
    })
    logging.debug(f'Post запрос {url + endpoint} вернул response header - {response.headers}')
    response_body = response.json()
    logging.debug(f'Post запрос {url + endpoint} вернул response body - {response.json()}')
    assert 'type' not in response_body
