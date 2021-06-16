 # Автотесты API [users.bugred.ru](http://users.bugred.ru/)
Автотесты реализованы при помощи **`Python`**. Для корректной работы кода, необходима установка библиотек `pytest`, `requests`.

 ## Описание

 Программа позволяет производить функциональное тестирования API [users.bugred.ru](http://users.bugred.ru/) с использованием следующего набора **автотестов**:

* **`test_metod_api_list()`** - тестирование метода *`MetodApiList`* (получение списка всех методов работы с API в формате `json`)
* **`test_get_company()`** - тестирование метода *`getCompany`* (получение информации о компании)
* **`test_create_company()`** - тестирование метода *`CreateCompany`* (создание новой компании)
* **`test_get_user()`** - тестирование метода *`getUser`* (получение информации о пользователе)
* **`test_get_user_full()`** - тестирование метода *`getUserfull`* (получение полной информации о пользователе, включая информацию о заданиях и компаниях)
* **`test_do_register()`** - тестирование метода *`doRegister`* (регистрация нового пользователя в системе)
* **`test_do_login()`** - тестирование метода *`doLogin`* (вход в систему под зарегестрированным пользователем)
* **`test_create_user()`** - тестирование метода *`CreateUser`* (создание нового пользователя с привязкой к существующей задаче)
* **`test_create_user_with_task()`** - тестирование метода *`CreateUserWithTasks`* (создание нового пользователя и задачи для него)
* **`test_user_one_field()`** - тестирование метода *`UserOneField`* (изменение данных одного поля пользователя)
* **`test_del_task()`** - тестирование метода *`delTask`* (удаление задачи пользователя)
* **`test_full_update_user()`** - тестирование метода *`FullUpdateUser`* (обновление всей информации о пользователе)
* **`test_del_users()`** - тестирование метода *`delUsers`* (удаление пользователя)
* **`test_add_avatar()`** - тестирование метода *`AddAvatar`* (загрузка аватара пользователя)
* **`test_delele_avatar()`** - тестирование метода *`DelAvatar`* (удаление аватара пользователя)
* **`test_magic_search()`** - тестирование метода *`MagicSearch`* (поиск по сотрудникам или компаниям) 
* **`test_createtask()`** - тестирование метода *`CreateTask`* (создание задачи пользователя)
* **`test_update_task()`** - тестирование метода *`UpdateTask`* (обновление задачи пользователя)
* **`test_add_task_in_cron()`** - тестирование метода *`AddTaskInCron`* (создание запуска задачи по расписанию)

**В программе реализованы два *тест-кейса*:**

* **`test_case_1()`**:
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

* **`test_case_2()`**:
    1. Создание 5 пользователей и задач для них
    2. Изменение 1 поля каждого пользователя
    3. Вход в систему под менеджером
    4. Поиск пользователей по созданной задаче
    5. Проверка выполнения задач пользователями
    6. Добавление новой задачи пользователям 

### *Справочно о работе программы*

* Тестирование методов реализовано через библиотеку `pytest`
* Получение данных для регистрации нового пользователя в методах *`doRegister`*, *`CreateUser`*, *`CreateUserWithTasks`* реализовано через API [randomuser.me](https://randomuser.me/)
* Для тестирования метода *`AddAvatar`* используются файлы изображений из дирректории `./image/` 
* В программе реализовано логирование, для просмотра логов используйте файл `user.test.log` (уровень логирования можно задать в файле `config.json`)
* Из файла `config.json` берутся следующие тестовые параметры:
    * логин/пароль менеджера (`manager_email`, `manager_password`)
    * данные о задаче (`task_title`, `task_description`, `hours`, `minutes`, `month`, `days`, `day_weeks`)
    * данные о компании (`company_name`, `company_type`)
    * опциональные атрибуты пользователя (`hobby`, `adres`, `name1`, `fathername1`, `cat`, `dog`, `parrot`, `cavy`, `hamster`, `phone`, `inn`, `gender`, `birthday`, `date_start`)
 
## Запуск и использование

Для запуска автотестов необходимо ввести команду **$ pytest** в *terminal*:
* Запустить все тесты: 
``` 
$ pytest test_user_api.py 
```
* Запустить определенный тест: 
``` 
$ pytest test_user_api.py::<TEST_NAME> 
```
* Запустить определенный тест-кейс: 
``` 
$ pytest test_case_<NUMBER>.py 
```

Ниже представлен пример запуска **test_case_1**:
```
$ pytest-3 pytest-3 test_case_1.py 
====================== test session starts ======================
platform linux -- Python 3.8.5, pytest-4.6.9, py-1.8.1, pluggy-0.13.0
rootdir: ~/test_users_api/user_test_python
collected 1 item                                                                                                                                                                                                                                    

test_case_1.py .

=====================  1 passed in 6.80 seconds ======================
```

Отрывок лога из `user.test.log` (уровень логирования `info`)
```
06-07 22:55,417 INFO         [test_case_1.py:33:test_case_1         ] ---------------Запуск test_case_1
06-07 22:55,417 INFO         [test_case_1.py:47:test_case_1         ] 1. Регистрация пользователя
06-07 22:55,418 INFO         [user_api.py:98:do_register         ] Вызов метода doRegister
06-07 22:55,418 INFO         [user_api.py:56:random_user_generator] Запуск получения данных рандомного пользователя
06-07 22:55,418 INFO         [user_api.py:60:random_user_generator] Установка соединения с https://randomuser.me/api
06-07 22:55,917 INFO         [user_api.py:26:valid_response      ] Проверка ответа от сервера
06-07 22:55,918 INFO         [user_api.py:29:valid_response      ] Status code = 200
06-07 22:55,919 INFO         [user_api.py:44:valid_response      ] Проверка ответа от сервера успешно выполнена
06-07 22:55,920 INFO         [user_api.py:72:random_user_generator] Получены данные рандомного пользователя: "email" : "wimke.broekmeulen@example.com", "name" : "whiteswan472", "password" : "dragoon"
06-07 22:55,921 INFO         [user_api.py:104:do_register         ] Установка соединения с http://users.bugred.ru:80/tasks/rest/doregister
06-07 22:55,225 INFO         [user_api.py:110:do_register         ] Отправлен запрос на регистрацию пользователя: "name" : "whiteswan472", "email" : "wimke.broekmeulen@example.com", "password" : "dragoon"
06-07 22:55,226 INFO         [user_api.py:26:valid_response      ] Проверка ответа от сервера
06-07 22:55,227 INFO         [user_api.py:29:valid_response      ] Status code = 200
06-07 22:55,228 INFO         [user_api.py:44:valid_response      ] Проверка ответа от сервера успешно выполнена
```
*Функциональные автотесты составлены согласно [документации](https://testbase.atlassian.net/wiki/spaces/USERS/overview?homepageId=1074221)*
