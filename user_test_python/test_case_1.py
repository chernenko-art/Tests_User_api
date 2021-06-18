import pytest
import logging
import time
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


def test_case_1():
    """  Тест-кейс test_case_1 включает в себя следующую последовательность действий:

    1. Регистрация пользователя
    2. Вход в систему под пользователем
    3. Создание аватара пользователя
    4. Вход в систему под менеджером
    5. Создание компании с привязкой пользователя к компании
    6. Создание задачи пользователю
    7. Вход в систему под пользователем
    8. Удаление аватара пользователя
    9. Создание нового аватара пользовател
    10. Просмотр задач, и привязанных компаний

    """
    logging.info('-'*15 + 'Запуск test_case_1')

    # Заводим таймер для защиты от ошибок на сервере
    timing = time.time()

    # Цикл с таймером на 10 сек
    while True:
        try:
            # Проверка времени выполнения цикла
            if time.time() - timing > 10.0:
                logging.error('Превышено время ожидания')
                assert False

            # Регистрация пользователя
            logging.info('1. Регистрация пользователя')
            user = do_register()
            if 'type' in user["0"]["json"]:
                raise Exception(f'Error key "type" in response json do_register(): {user["0"]["json"]}')
            user_email = user['0']['email']
            user_password = user['0']['password']
                

            # Вход в систему под пользователем
            logging.info('2. Вход в систему под пользователем')
            login_json = do_login(user_email, user_password)
            if login_json["result"] == False:
                raise Exception(f'Error key "result" in response json do_login(): {login_json}')

            # Создание аватара пользователя
            logging.info('3. Создание аватара пользователя')
            # Получение файла изображения
            avatar = avatar_file()
            add_avatar_json = add_avatar(user_email, avatar)
            if add_avatar_json['status'] != 'ok':
                raise Exception(f'Error key "status" in response json add_avatar(): {add_avatar_json}')
                    
            # Вход в систему под менеджером
            logging.info('4. Вход в систему под менеджером')
            # Получение данных авторизации менеджера
            params_test = get_params_test()  
            manager_email = params_test['manager_email']
            manager_password = params_test['manager_password']
            login_json = do_login(manager_email, manager_password)
            if login_json["result"] == False:
                raise Exception(f'Error key "result" in response json do_login(): {login_json}')
                
            # Создание компании с привязкой пользователя
            logging.info('5. Создание компании с привязкой пользователя')
            company_name = params_test['company_name']
            company_type = params_test['company_type']
            company_users = [user_email]
            company_json = create_company(company_name, company_type, company_users, manager_email)
            if company_json['type'] != 'success':
                raise Exception(f'Error key "type" in response json create_company(): {company_json}')
                
            # Создание задачи пользователя
            logging.info('6. Создание задачи пользователю')
            task_title = params_test['task_title']
            task_description = params_test['task_description']
            task_json = create_task(task_title, task_description, manager_email, user_email)
            if task_json['message'] != 'Задача успешно создана!':
                raise Exception(f'Error key "message" in response json create_task(): {task_json}')
                
            # Вход в систему под пользователем
            logging.info('7. Вход в систему под пользователем')
            login_json = do_login(user_email, user_password)
            if login_json["result"] == False:
                raise Exception(f'Error key "result" in response json do_login(): {login_json}')

            # Удаление аватара пользователя
            logging.info('8. Удаление аватара пользователя')
            del_avatar_json = delele_avatar(user_email)
            if del_avatar_json['status'] != 'ok':
                raise Exception(f'Error key "status" in response delele_avatar(): {del_avatar_json}')
                
            # Создание нового аватара пользователя
            logging.info('9. Создание нового аватара пользователя')
            # Получение файла изображения
            avatar = avatar_file(2)
            add_avatar_json = add_avatar(user_email, avatar)
            if add_avatar_json['status'] != 'ok':
                raise Exception(f'Error key "status" in response json add_avatar(): {add_avatar_json}')
                
            # Просмотр задач, и привязанных компаний
            logging.info('10. Просмотр задач, и привязанных компаний')
            search_json = magic_search(user_email)
            if 'code_error' in search_json:
                raise Exception(f'Key "code_error" in response magic_search(): {search_json}')
                
            # Сравнение результатов поиска с фактическими
            check_email_user = None
            check_task_title = None
            check_company_name = None
            
            if search_json['foundCount'] >= 1:
                for elem in range(len(search_json['results'])):
                    
                    # Проверка email пользователя
                    for key in search_json['results'][elem]:
                        email = search_json['results'][elem][key]
                        if email == user_email:
                            check_email_user = email
                    
                    # Проверка задачи пользователя
                    tasks = search_json['results'][elem]['tasks']
                    for task in range(len(tasks)):
                        if tasks[task]['name'] == task_title:
                            check_task_title = tasks[task]['name']
                    
                    # Проверка компании пользователя
                    companies = search_json['results'][elem]['companies']
                    for company in range(len(companies)):
                        if companies[company]['name'] == company_name:
                            check_company_name = companies[company]['name']
                
                assert user_email == check_email_user and task_title == check_task_title \
                    and company_name == check_company_name
                logging.info(f'test_case_1 успешно пройден: \
                            {user_email} = {check_email_user}, \
                            {task_title} = {check_task_title}, \
                            {company_name} = {check_company_name}')
                break
            
            else:
                logging.error(f'test_case_1 провален \
                            {user_email} = {check_email_user}, \
                            {task_title} = {check_task_title}, \
                            {company_name} = {check_company_name}')
                assert False
        
        except Exception as err:
            logging.error(err)
            assert False

