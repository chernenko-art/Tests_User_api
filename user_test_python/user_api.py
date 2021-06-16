from requests import get, put, post, delete
import logging

from requests.api import request
from conftest import level_logging, url_adress


# Конфигурация логов
FORMAT = '%(asctime)s,%(msecs)d %(levelname)-8s \
    [%(filename)s:%(lineno)d:%(funcName)-20s] %(message)s'
logging.basicConfig(level=level_logging(),
                    format=FORMAT,
                    datefmt='%m-%d %H:%M',
                    filename='user_tests.log'
                    )


def valid_response(response: dict):
    """Проверка header ответа сервера

    Args:
        response (dict): response json

    Returns:
        bool: Результат проверки (True, False)
    """
    
    logging.info('Проверка ответа от сервера')

    # Проверка status_code
    logging.info(f'Status code = {response.status_code}')
    if response.status_code != 200:
        logging.error(f'Status Code = {response.status_code}')
        return False
    
    # Проверка наличия 'application/json' в 'content-type'
    content_type = response.headers['content-type']
    logging.debug(f'Response headers: {response.headers}')
    header_list = [elem.strip() for elem in content_type.split(';')]
    if 'application/json' not in header_list:
        logging.error(f'"application/json" отсутствует в "content-type"')
        return False
    else:
        logging.debug(f'Response body = {response.json()}')
        logging.debug(f'Header "content-type" = [{response.headers["content-type"]}]')
        logging.info('Проверка ответа от сервера успешно выполнена')
        return True


def random_user_generator()->tuple:
    """Получение данных рандомного пользователя
    с помощью api https://randomuser.me/

    Returns:
        tuple: данные пользователя (email, name, password)
    """
    
    logging.info('Запуск получения данных рандомного пользователя')
    url = 'https://randomuser.me/api'
    
    # Отправка запроса получение данных рандомного пользователя
    logging.info(f'Установка соединения с {url}')
    response = get(url)

    # Проверка валидности ответа на запрос
    if valid_response(response):
        response_body = response.json()
        email = response_body['results'][0]['email']
        logging.debug(f'Получен "email" : "{email}"')
        name = response_body['results'][0]['login']['username']
        logging.debug(f'Получен "name" : "{name}"')
        password = response_body['results'][0]['login']['password']
        logging.debug(f'Получен  "password" : "{password}"')
        logging.info(f'Получены данные рандомного пользователя:\
             "email" : "{email}", "name" : "{name}", "password" : "{password}"')
        return email, name, password
    else:
        logging.error('Ошибка в получении данных рандомного пользователя')


def do_register(number: int  = 1) -> dict:
    """Метод doRegister (запрос на регистрацию пользователя)

    Args:
        number (int, optional): количество пользователей. Defaults to 1.

    Returns:
        dict: данные пользователя (json, email, name, password)
    """
 
    endpoint = '/tasks/rest/doregister'

    # Словарь для хранения данных, зарегестрированных пользователей
    user_params_dict = {}
    # Переменная для генерации ключей user_params_dict
    key_user = 0

    # Цикл регистрации пользователей
    for _ in range(number):
        logging.info('Вызов метода doRegister')
        
        # Запрос данных рандомного пользователя
        email, name, password = random_user_generator()
        
        # Отправка запроса на регистрацию пользователя
        logging.info(f'Установка соединения с {url_adress() + endpoint}')
        response = post(url_adress() + endpoint, json={
            "email": email,
            "name": name,
            "password": password
        })
        logging.info(f'Отправлен запрос на регистрацию пользователя:\
            "name" : "{name}", "email" : "{email}", "password" : "{password}"')
        
        # Проверка валидности ответа на запрос
        if valid_response(response):
            user_params_dict[str(key_user)] = {
                "json" : response.json(),
                "email": email,
                "name": name,
                "password": password
                }
            # Генерация ключа следующего пользователя
            key_user += 1
        else:
            logging.error('Ошибка в методе doregister')
    
    # Возврат словаря с данными зарегестрированных пользователей
    return user_params_dict


def do_login(email: str, password) -> dict:
    """Метод doLogin (запрос на авторизацию пользователя)

    Args:
        email (str): email пользователя
        password: password пользователя

    Returns:
        dict: response json
    """

    logging.info('Вызов метода doLogin')
    endpoint = '/tasks/rest/dologin'
    
    # Отправка запроса на авторизацию пользователя
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    response = post(url_adress() + endpoint, params={
        "email": email,
        "password": password
    })
    logging.info(f'Отправлен запрос на авторизацию пользователя:\
         "email" : "{email}", "password" : {password}')
    
    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе doLogin')
    

def create_task(task_title: str, task_description: str, \
                email_owner: str, email_assign: str) -> dict:
    """Метод CreateTask (создание задачи пользователю)

    Args:
        task_title (str): заголовок задачи
        task_description (str): описание задачи
        email_owner (str): email автора
        email_assign (str): email исполнителя

    Returns:
        dict: response json
    """
    
    logging.info('Вызов метода CreateTask')
    endpoint = '/tasks/rest/createtask'
    
    # Отправка запроса на создание задачи
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    response = post(url_adress() + endpoint, json={
        "task_title": task_title,
        "task_description": task_description,
        "email_owner": email_owner,
        "email_assign": email_assign
    })
    logging.info(f'Отправлен запрос на создание задачи пользователю: {email_assign}')
    
    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе CreateTask')


def create_company(company_name: str, company_type: str, \
                   company_users: str, email_owner: str) -> dict:
    """Метод CreateCompany (создание компании с привязкой пользователей)

    Args:
        company_name (str): название компании
        company_type (str): тип компании (ООО, ИП, ОАО)
        company_users (list): email сотрудников
        email_owner (str): email автора

    Returns:
        dict: response json
    """
    
    logging.info('Вызов метода CreateCompany')
    endpoint = '/tasks/rest/createcompany'
    
    # Отправка запроса на создание компании
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    response = post(url_adress() + endpoint, json={
        "company_name": company_name,
        "company_type": company_type,
        "company_users": company_users,
        "email_owner": email_owner
    })
    logging.info(f'Отправлен запрос на создание компании: {company_name}')
    
    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе CreateCompany')


def create_user(email: str, name: str, tasks: list, companies: list, \
                params: dict = None) -> dict:
    """Метод CreateUser (создание пользователей c привязкой к задаче)

    Args:
        email (str): email пользователя
        name (str): имя пользователя
        tasks (list): список id уже существующих задач
        companies (list): перечень id компаний
        params (dict, optional): остальные параметры пользователя. Defaults to None.

    Returns:
        dict: response json
    """
    
    logging.info('Вызов метода CreateUser')
    endpoint = '/tasks/rest/createuser'

    # Формирование входных параметров запроса
    user_params = {"email": email, "name": name,
                   "tasks": tasks, "companies": companies}
    if params:
        user_params.update(params)
             
    # Отправка запроса на создание пользователя
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    response = post(url_adress() + endpoint, json=user_params)
    logging.info(f'Отправлен запрос на создание пользователя: {user_params}')
    
    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе CreateCompany')


def create_user_with_task(email: str, name: str, tasks: list, companies: list = None,
                          params: dict = None) -> dict:
    """Метод CreateUser (создание пользователя и создание задачи для него)

    Args:
        email (str): email пользователя
        name (str): имя пользователя
        tasks (list): список новых задач пользователя [{title:foo, description:foo}]
        companies (list, optional): перечень id компаний
        params (dict, optional): остальные параметры пользователя. Defaults to None.

    Returns:
        dict: response json
    """

    logging.info('Вызов метода CreateUser')
    endpoint = '/tasks/rest/createuserwithtasks'

    # Формирование входных параметров запроса
    user_params = {"email": email, "name": name,
                   "tasks": tasks, "companies": companies}
    if params:
        user_params.update(params)

    # Отправка запроса на создание пользователя
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    response = post(url_adress() + endpoint, json=user_params)
    logging.info(f'Отправлен запрос на создание пользователя: {user_params}')

    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе CreateCompany')


def add_avatar(email: str, avatar: str) -> dict:
    """Метод addAvatar (добавление аватара пользователю)

    Args:
        email (str): email пользователя
        avatar (str): путь к картинке (jpg, png)

    Returns:
        dict: response json
    """

    logging.info('Вызов метода addAvatar')
    endpoint = '/tasks/rest/addavatar'

    # Отправка запроса на добавление аватара пользователю
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    response = post(url_adress() + endpoint, 
                    data={"email": email}, files={'avatar': avatar})

    logging.info(f'Отправлен запрос на добавление аватара пользователю: "email" : "{email}"')

    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе addAvatar')


def delele_avatar(email: str) -> dict:
    """Метод DeleteAvatar (удаление аватара пользователю)

    Args:
        email (str): email пользователя

    Returns:
        dict: response json
    """

    logging.info('Вызов метода addAvatar')
    endpoint = '/tasks/rest/deleteavatar'

    # Отправка запроса на добавление аватара пользователю
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    response = post(url_adress() + endpoint,
                    data={"email": email})

    logging.info(
        f'Отправлен запрос на удаление аватара пользователю: "email" : "{email}"')

    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе DeleteAvatar')


def magic_search(query: str, company_type: str = None, fullSimilarity: bool = None,
                 taskStatus: str = None, include: list = None, maxCount: int = None) -> dict:
    """Метод MagicSearch (поиск по сотрудникам или компаниям)

    Args:
        query (str): основные критерии поиска:
            * по пользователю (name, email, birthday, name1, surname1, fathername1, phone, adres, inn);
            * по компании (name, inn, ogrn, kpp, adress, phone).
        company_type (str, optional): где искать (USER, COMPANY).
        fullSimilarity (bool, optional): искать по полному совпадению (True, False).
        taskStatus (str, optional): поиск по статусу задачи (ALL, ACTUAL, COMPLETE, FAIL).
        include (list, optional): дополнительная информация о контрагенте (ALL, USER, TASK, COMPANY, WHY).
        maxCount (int, optional): количество результатов, возвращаемых в ответе (max value = 30).
    Returns:
        dict: response json
    """

    logging.info('Вызов метода MagicSearch')
    endpoint = '/tasks/rest/magicsearch'

    # Определение параметров запроса
    request_params = {"query": query}
    # Проверка передачи опциональных параметров
    if company_type != None:
        request_params.update({"company_type": company_type})
    if fullSimilarity != None:
        request_params.update({"fullSimilarity": fullSimilarity})
    if taskStatus != None:
        request_params.update({"taskStatus": taskStatus})
    if include != None:
        request_params.update({"include": include})
    if maxCount != None:
        request_params.update({"maxCount": maxCount})
    
    # Отправка запроса на выполнение поиска
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    response = post(url_adress() + endpoint, json=request_params)

    logging.info(f'Отправлен запрос на выполение поиска: {request_params}')

    # Проверка валидности ответа на запрос
    logging.info(f'Status code = {response.status_code}')
    logging.debug(f'Response headers: {response.headers}')
    content_type = response.headers['content-type']
    header_list = [elem.strip() for elem in content_type.split(';')]
    if 'application/json' not in header_list:
        logging.error(f'"application/json" отсутствует в "content-type"')
    else:
        logging.debug(f'Response body = {response.json()}')
        return response.json()


def user_one_field(email: str, field: str = 'hobby', value: str = 'fitness') -> dict:
    """Метод UserOneField (изменение 1 поля пользователя)

    Args:
        email (str): email пользователя
        field (str): поле для изменения. Defaults to 'hobby'.
        value (str): значение поля field. Defaults to 'fitness'.

    Returns:
        dict: response json
    """

    logging.info('Вызов метода UserOneField')
    endpoint = '/tasks/rest/useronefield'

    # Отправка запроса на изменение поля пользователя
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    json_request = {"email": email, "field": field, "value": value}
    response = post(url_adress() + endpoint, json=json_request)

    logging.info(
        f'Отправлен запрос на изменение поля пользователя: {json_request}')

    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе UserOneField')


def get_company(id_company: int) -> dict:
    """Метод getCompany (поиск компании по id_company)

    Args:
        id_company (int): id_company

    Returns:
        dict: response json
    """

    logging.info('Вызов метода getCompany')
    endpoint = '/tasks/rest/getcompany'

    # Отправка запроса на изменение поля пользователя
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    json_request = {"id_company": id_company}
    response = get(url_adress() + endpoint, json=json_request)

    logging.info(f'Отправлен запрос на поиск компании: {json_request}')

    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе getCompany')


def get_company(id_company: int) -> dict:
    """Метод getCompany (поиск компании по id_company)

    Args:
        id_company (int): id_company

    Returns:
        dict: response json
    """

    logging.info('Вызов метода getCompany')
    endpoint = '/tasks/rest/getcompany'

    # Отправка запроса на изменение поля пользователя
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    json_request = {"id_company": id_company}
    response = get(url_adress() + endpoint, json=json_request)

    logging.info(f'Отправлен запрос на поиск компании: {json_request}')

    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе getCompany')


def get_user(email: str) -> dict:
    """Метод getUser (поиск пользователя по email)

    Args:
        email (str): email пользователя

    Returns:
        dict: response json
    """

    logging.info('Вызов метода getUser')
    endpoint = '/tasks/rest/getuser'

    # Отправка запроса на изменение поля пользователя
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    json_request = {"email": email}
    response = get(url_adress() + endpoint, json=json_request)

    logging.info(f'Отправлен запрос на поиск пользователя: {json_request}')

    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе getUser')


def get_user_full(email: str) -> dict:
    """Метод getUserfull (поиск полной информации о пользователя по email)

    Args:
        email (str): email пользователя

    Returns:
        dict: response json
    """

    logging.info('Вызов метода getUserfull')
    endpoint = '/tasks/rest/getuserfull'

    # Отправка запроса на изменение поля пользователя
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    json_request = {"email": email}
    response = get(url_adress() + endpoint, json=json_request)

    logging.info(f'Отправлен запрос на поиск пользователя: {json_request}')

    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе getUserfull')


def metod_api_list() -> dict:
    """Метод MetodApiList (получение перечня методов api)

    Returns:
        dict: response json
    """

    logging.info('Вызов метода MetodApiList')
    endpoint = '/tasks/rest/list'

    # Отправка запроса на изменение поля пользователя
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    response = get(url_adress() + endpoint)

    logging.info('Отправлен запрос на получение перечня методов api')

    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе MetodApiList')


def update_task(email_owner: str, email_assign: str, \
                id_task: int, task_title: str, task_description: str) -> dict:
    """Метод UpdateTask (обновление задачи пользователю)

    Args:
        email_owner (str): email исполнителя 
        email_assign (str): email автора
        id_task (int): идентификатор задачи
        task_title (str): заголовок задачи
        task_description (str): описание задачи

    Returns:
        dict: response json
    """

    logging.info('Вызов метода UpdateTask')
    endpoint = '/tasks/rest/updatetask'

    # Отправка запроса на изменение поля пользователя
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    json_request = {
        "email_owner": email_owner,
        "email_assign": email_assign,
        "id_task": id_task,
        "task_title": task_title,
        "task_description": task_description
        }
    response = post(url_adress() + endpoint, json=json_request)

    logging.info(f'Отправлен запрос на обновление задачи пользователя: {json_request}')

    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе UpdateTask')


def add_task_in_cron(email_owner: str, task_id: int, hours: int,
                minutes: int, month: int, days: int, day_weeks: int) -> dict:
    """Метод AddTaskInCron (создание запуска задачи по расписанию)

    Args:
        email_owner (str): email исполнителя 
        task_id (int): идентификатор задачи
        hours (int): часов на выполнение
        minutes (int): минут на выполнение
        month (int): месяцев на выполнение
        days (int): дней на выполнение
        day_weeks (int): дней недели на выполнение

    Returns:
        dict: response json
    """

    logging.info('Вызов метода AddTaskInCron')
    endpoint = '/tasks/rest/addtaskincron'

    # Отправка запроса на изменение поля пользователя
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    json_request = {
        "email_owner": email_owner,
        "task_id": task_id,
        "hours": hours,
        "minutes": minutes,
        "month": month,
        "days": days,
        "day_weeks": day_weeks
    }
    response = post(url_adress() + endpoint, params=json_request)

    logging.info(f'Отправлен запрос на запуск задачи по расписанию: {json_request}')

    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе AddTaskInCron')


def del_task(email_owner: str, task_id: int) -> dict:
    """Метод delTask (удаление задачи пользователю)

    Args:
        email_owner (str): email исполнителя 
        task_id (int): идентификатор задачи

    Returns:
        dict: response json
    """

    logging.info('Вызов метода delTask')
    endpoint = '/tasks/rest/deletetask'

    # Отправка запроса на изменение поля пользователя
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    json_request = {"email_owner": email_owner, "task_id": task_id}
    response = delete(url_adress() + endpoint, params=json_request)

    logging.info(
        f'Отправлен запрос на удаление задачи пользователю: {json_request}')

    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе delTask')


def full_update_user(email: str, name: str, tasks: list, companies: list,
                params: dict) -> dict:
    """Метод FullUpdateUser (обновление всех данных пользователя)

    Args:
        email (str): email пользователя
        name (str): имя пользователя
        tasks (list): список id уже существующих задач
        companies (list): перечень id компаний
        params (dict): остальные параметры пользователя

    Returns:
        dict: response json
    """

    logging.info('Вызов метода FullUpdateUser')
    endpoint = '/tasks/rest/fullupdateuser'

    # Формирование входных параметров запроса
    request_params = {"email": email, "name": name, "tasks": tasks,
                      "companies": companies}
    request_params.update(params)

    # Отправка запроса на обновление всех данных пользователя
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    response = put(url_adress() + endpoint, json=request_params)
    logging.info(f'Отправлен запрос на обновление данных пользователя: {request_params}')

    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе FullUpdateUser')


def del_users(email: str) -> dict:
    """Метод delUsers (удаление пользователя)

    Args:
        email (str): email пользователя 

    Returns:
        dict: response json
    """

    logging.info('Вызов метода delUsers')
    endpoint = '/tasks/rest/deleteuser'

    # Отправка запроса на удаление пользователя
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    json_request = {"email": email}
    response = delete(url_adress() + endpoint, params=json_request)

    logging.info(f'Отправлен запрос на удаление пользователя: {json_request}')

    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе delUsers')
