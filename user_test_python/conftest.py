import pytest
from requests import get
# from _pytest.fixtures import fixture
import json
import logging


path_json_file = './config.json'
json_file = open(path_json_file, 'r').read()
json_body = json.loads(json_file)


def url_adress():
    """Получение url из config.json"""
    schema = json_body['user']['schema']
    host = json_body['user']['host']
    port = json_body['user']['port']
    return f'{schema}://{host}:{port}'
    

def level_logging():
    """Считывание level logging из config.json"""
    numeric_level = getattr(logging, json_body["log"]["level"].upper(), None)
    return numeric_level


def get_params_test():
    """Получение параметров для теста"""
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
