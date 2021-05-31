import pytest
from requests import get, post, put, delete
import logging
import sys
sys.path.append("/home/chernenkoac/prog/test_users_api/user_test_python")
from conftest import level_logging, url_adress


# Конфигурация логов
logging.basicConfig(level=level_logging(),
                    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='user_tests.log'
                    )

user_email = 'python_user@gmail.com'
user_name = 'Reno'
user_password = 123


def test_doRegister():
    '''Тест регистрации пользователя'''
    logging.info('Запуск do_register')
    endpoint = '/tasks/rest/doregister'
    response = post(url_adress() + endpoint, json = {
        "email" : user_email,
        "name": user_name,
        "password": user_password
    })
    logging.debug(f'Post запрос {url_adress() + endpoint} вернул response header - {response.headers}')
    response_body = response.json()
    logging.debug(f'Post запрос {url_adress() + endpoint} вернул response body - {response.json()}')
    assert 'type' not in response_body
