import pytest
from requests import get
import json
import logging


path_json_file = './config.json'
json_file = open(path_json_file, 'r').read()
json_body = json.loads(json_file)


def url_adress():
    """Получение url из config.json

    Returns:
        str: url adress
    """
    schema = json_body['user']['schema']
    host = json_body['user']['host']
    port = json_body['user']['port']
    return f'{schema}://{host}:{port}'
    

def level_logging():
    """Считывание level logging из config.json

    Returns:
        getattr: атрибут level функции logging
    """
    numeric_level = getattr(logging, json_body["log"]["level"].upper(), None)
    return numeric_level


def get_params_test():
    """Получение параметров для теста

    Returns:
        tuple: manager_email, manager_password, task_json, task_title, task_description,\
            company_name, company_type
    """
    logging.info(f'Получение параметров для теста из config.json: {json_body["test_params"]}')
    return {
        'manager_email': json_body['test_params']['manager']['email'],
        'manager_password': json_body['test_params']['manager']['password'],
        'task_json': json_body['test_params']['task'],
        'task_title': json_body['test_params']['task']['title'],
        'task_description': json_body['test_params']['task']['description'],
        'company_name': json_body['test_params']['company']['name'],
        'company_type': json_body['test_params']['company']['type']
        }


def optional_user_params():
    """Получение опциональных параметров пользователя

    Returns:
        dict: hobby, adres, name1, surname1, fathername1, cat, dog, parrot,\
            cavy, hamster, squirrel, phone, inn, gender, birthday, date_start
    """
    logging.info(f'Получение опциональных параметров пользователя \
        из config.json: {json_body["test_params"]["user"]}')
    return json_body['test_params']['user']


def avatar_file(num_avatar=1):
    """Получение пути к файлу avatar из config.json

    Args:
        num_avatar (int, optional): номер картинки для аватара

    Returns:
        BufferedReader: open file
    """
    if num_avatar == 1:
        avatar_path = json_body['test_params']['avatar']['avatar_1']
        avatar = open(avatar_path, 'rb')
    else:
        avatar_path = json_body['test_params']['avatar']['avatar_2']
        avatar = open(avatar_path, 'rb')
    return avatar
