import pytest
from requests import get
from _pytest.fixtures import fixture
import json
import logging


path_json_file = '/home/chernenkoac/prog/test_users_api/user_test_python/config.json'
json_file = open(path_json_file, 'r').read()
json_body = json.loads(json_file)


def url_adress():
    '''Получение url из config.json'''
    schema = json_body['user']['schema']
    host = json_body['user']['host']
    port = json_body['user']['port']
    return f'{schema}://{host}:{port}'
    

def level_logging():
    """Считывание level logging из config.json"""
    numeric_level = getattr(logging, json_body["log"]["level"].upper(), None)
    return numeric_level
