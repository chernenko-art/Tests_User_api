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

        # Проверка времени выполнения цикла
        if time.time() - timing > 10.0:
            logging.error('Превышено время ожидания')
            assert False

        # Регистрация пользователя
        logging.info('1. Регистрация пользователя')
        user = do_register()
        user_email = user['0']['email']
        user_password = user['0']['password']

        # Вход в систему под пользователем
        logging.info('2. Вход в систему под пользователем')
        do_login(user_email, user_password)

        # Создание аватара пользователя
        logging.info('3. Создание аватара пользователя')
        # Получение файла изображения
        avatar = avatar_file()
        add_avatar(user_email, avatar)

        # Вход в систему под менеджером
        logging.info('4. Вход в систему под менеджером')
        # Получение данных авторизации менеджера
        params_test = get_params_test()  
        manager_email = params_test['manager_email']
        manager_password = params_test['manager_password']
        do_login(manager_email, manager_password)
       
        # Создание компании с привязкой пользователя
        logging.info('5. Создание компании с привязкой пользователя')
        company_name = params_test['company_name']
        company_type = params_test['company_type']
        company_users = [user_email]
        company_params = create_company(company_name, company_type, company_users, manager_email)
        id_company = company_params['id_company']

        # Создание задачи пользователю
        logging.info('6. Создание задачи пользователю')
        task_title = params_test['task_title']
        task_description = params_test['task_description']
        task_params = create_task(task_title, task_description, manager_email, user_email)
        id_task = task_params['id_task']

        # Вход в систему под пользователем
        logging.info('7. Вход в систему под пользователем')
        do_login(user_email, user_password)

        # Удаление аватара пользователя
        logging.info('8. Удаление аватара пользователя')
        delele_avatar(user_email)

        # Создание нового аватара пользователя
        logging.info('9. Создание нового аватара пользователя')
        # Получение файла изображения
        avatar = avatar_file(2)
        add_avatar(user_email, avatar)

        # Просмотр задач, и привязанных компаний
        logging.info('10. Просмотр задач, и привязанных компаний')
        search_result = magic_search(user_email)
        
        # Сравнение результатов поиска с фактическими
        check_email_user = None
        check_task_title = None
        check_company_name = None
        
        if search_result['foundCount'] >= 1:
            for elem in range(len(search_result['results'])):
                
                # Проверка email пользователя
                for key in search_result['results'][elem]:
                    if search_result['results'][elem][key] == user_email:
                        check_email_user = search_result['results'][elem][key]
                
                # Проверка задачи пользователя
                for task_elem in range(len(search_result['results'][elem]['tasks'])):
                    if search_result['results'][elem]['tasks'][task_elem]['name'] == task_title:
                        check_task_title = search_result['results'][elem]['tasks'][task_elem]['name']
                
                # Проверка компании пользователя
                for c_elem in range(len(search_result['results'][elem]['companies'])):
                    if search_result['results'][elem]['companies'][c_elem]['name'] == company_name:
                        check_company_name = search_result['results'][elem]['companies'][c_elem]['name']
            
            assert user_email == check_email_user and task_title == check_task_title \
                and company_name == check_company_name
            logging.info('test_case_1 успешно пройден')
            break
        
        else:
            logging.error('Совпадений не найдено, test_case_1 провален')
            assert False