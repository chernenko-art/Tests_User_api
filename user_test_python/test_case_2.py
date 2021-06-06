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


def test_case_2():
    """  Тест-кейс test_case_2 включает в себя следующую последовательность действий:

    1. Создание 5 пользователей и задач для них, с помощью метода create_user_with_task()
    2. Изменение 1 поля каждого пользователя
    3. Вход в систему под менеджером
    4. Поиск пользователей по созданной задаче
    5. Проверка выполнения задач пользователями
    6. Добавление новой задачи пользователям

    """
    logging.info('-'*15 + 'Запуск test_case_2')

    # Заводим таймер для защиты от ошибок на сервере
    timing = time.time()

    # Цикл с таймером на 10 сек
    while True:

        # Проверка времени выполнения цикла
        if time.time() - timing > 10.0:
            logging.error('Превышено время ожидания')
            assert False

        # Создание 5 пользователей и задач для них
        logging.info('1. Создание 5 пользователей и задач для них')
        # Получение данных о задаче
        params_test = get_params_test()
        task_1 = params_test['task_json']
        # Массив для хранения данных созданных пользователей
        user_list = []
        for _ in range(5):
            # Запрос случайных данных пользователей
            user_email, user_name, password = random_user_generator()        
            create_user_with_task(user_email, user_name, [task_1])
            # Добавление email пользователя в массив
            user_list.append(user_email)

        # Изменение поля 'hobby' каждого пользователя
        logging.info('2. Изменение 1 поля каждого пользователя')
        for email in user_list:
            user_one_field(email)

        # Вход в систему под менеджером
        logging.info('3. Вход в систему под менеджером')
        # Получение данных авторизации менеджера  
        manager_email = params_test['manager_email']
        manager_password = params_test['manager_password']
        do_login(manager_email, manager_password)

        # Поиск пользователей по созданной задаче
        logging.info('4. Поиск пользователей по созданной задаче')
        search_params = ' '.join(user_list)
        search_result = magic_search(search_params)
        
        # Проверка выполнения задач пользователями
        logging.info('5. Проверка выполнения задач пользователями')
        # Проверка задач всех пользователей
        for i in range(len(search_result['results'])):
            user = search_result['results'][i]['email']
            task = search_result['results'][i]['tasks'][0]
            if 'status' in task:
                logging.info(f"Статус задачи {task['name']} пользователя {user} - task['status']")
            else:
                logging.error(f"Отсутствует поле 'status' в задаче пользователя {user}")
                assert False

        # Добавление новой задачи пользователям
        logging.info('6. Добавление новой задачи пользователям')
        task_2 = {"title": "Спринт 85", "description": "Провести fuctional test"}
        for email in user_list:
            create_task(task_2['title'], task_2['description'], manager_email, email)
        
        # Проверка успешности выполения test_case_2
        # Обновление поиска пользователей по созданым задачам
        search_result = magic_search(search_params)
        # Определение заданного массива задач и пользователей
        spec_list = {}
        for email in user_list:
            # Определение заданного перечня задач
            spec_tasks = [task_1['title'], task_2['title']]
            spec_list.update({email: spec_tasks})

        # Определение фактического массива задач и пользователей
        result_list = {} 
        # Сбор полученных данных пользователей
        if search_result['foundCount'] >= 1:
            for i in range(len(search_result['results'])):
                email = search_result['results'][i]['email']
                if email in user_list:
                    tasks = search_result['results'][i]['tasks']
                    task_list = []
                    for task in tasks:
                        task_list.append(task['name'])
                    # реверс в списке, т.к. в response обратный порядок задач
                    result_list.update({email: task_list[::-1]})

            # Сравнение заданного массива задач и пользователей с фактическим
            assert  spec_list == result_list
            logging.info(f'test_case_2 успешно пройден')
            break
        else:
            logging.error('test_case_2 провален')
            assert False
