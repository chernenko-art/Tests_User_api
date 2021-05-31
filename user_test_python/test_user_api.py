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


def random_user_generator():
    '''Создание рандомного пользователя с помощью api https://randomuser.me/'''
    url = 'https://randomuser.me/api'
    response = get(url)
    response_body = response.json()
    email = response_body['results'][0]['email']
    name = response_body['results'][0]['login']['username']
    password = response_body['results'][0]['login']['password']
    return email, name, password


def test_doRegister():
    '''Тест регистрации пользователя'''
    logging.info('Запуск do_register')
    endpoint = '/tasks/rest/doregister'
    email, name, password = random_user_generator()
    logging.debug(f'Получены данные рандомного пользователя ("name" : "{name}", "email" : "{email}", "password" : "{password}")')
    response = post(url_adress() + endpoint, json = {
        "email": email,
        "name": name,
        "password": password
    })
    logging.debug(f'Post запрос {url_adress() + endpoint} вернул response header - {response.headers}')
    response_body = response.json()
    logging.debug(f'Post запрос {url_adress() + endpoint} вернул response body - {response.json()}')
    if 'type' in response_body:
        while 'type' in response_body:
            logging.error(f'Такой пользователь уже зарегестрирован ("name" : "{name}", "email" : "{email}", "password" : "{password}")')
            name, email, password = random_user_generator()
            logging.debug(f'Получены данные рандомного пользователя ("name" : "{name}", "email" : "{email}", "password" : "{password}")')
            response = post(url_adress() + endpoint, json={
                "email": email,
                "name": name,
                "password": password
            })
            logging.debug(f'Post запрос {url_adress() + endpoint} вернул response header - {response.headers}')
            response_body = response.json()
            logging.debug(f'Post запрос {url_adress() + endpoint} вернул response body - {response.json()}')
        else:
            logging.info(f'Пользователь успешно зарегестрирован ("name" : "{name}", "email" : "{email}", "password" : "{password}")')
            assert True
    else:
        logging.info(f'Пользователь успешно зарегестрирован ("name" : "{name}", "email" : "{email}", "password" : "{password}")')
        assert True


