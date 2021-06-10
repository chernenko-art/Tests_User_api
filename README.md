# Тестирование API [users.bugred.ru](http://users.bugred.ru/)

 ## Описание

 Функциональное тестирование API [users.bugred.ru](http://users.bugred.ru/) включает в себя:

* Автотесты **`Python`** - [*user_test_python*](https://github.com/chernenko-art/tests_user_api/tree/master/user_test_python)
* Коллекцию **`Postman`** - [*user_test_postman*](https://github.com/chernenko-art/tests_user_api/tree/master/user_test_postman)
### Подробности использования указаны в `REDME.md` соответствующего раздела.

*Функциональные автотесты составлены согласно [документации.](https://testbase.atlassian.net/wiki/spaces/USERS/overview?homepageId=1074221)*

## **Выявленные баги**
* Метод `deleteAvatar`:
    * реализован посредством отправки `POST` запроса вместо `DELETE` (противоречит `REST`)
* Метод `UpdateTask`:
    * реализован посредством отправки `POST` запроса вместо `PUT` (противоречит `REST`)
* Методы `CreateUser`, `CreateUserWithTask`:
    * не содержат поле `password`, что делает невозможной авторизацию пользователя в системе
* Метод `UserOneField`:
    * при успешном выполнении возвращает значение `"type" = "error"` в теле ответа
* Метод `delUser`:
    * при успешном выполнении возвращает массив `array(1)` в теле ответа вместо `json`
* Методы `AddTaskInCron`, `delTask`:
    * нельзя передать `json` при отправке `POST` запроса (работает только передача параметров посредством `from-data`)
* Метод `doLogin`:
    * при авторизации менеджера нельзя передать `json` в `POST` запросе (работает только передача параметров посредством `from-data`), однако при авторизации простого пользователя  передать `json` можно
* Метод `CreateCompany`:
    * при совпадении поля `company_name` с ранее созданной компанией не выдает ошибку, возвращает `'type' == 'success'` в теле ответа
* Метод `FullUpdateUser`:
    * при выполнении запроса на обновление всех полей пользователя, не обновляются поля `"hobby", "task", "companies"` (происходит затирание полей)
* При возникновени ошибки любого из методов, кроме `MagicSearch`, в заголовке ответа возвращается `"status code" = "200", ok` 
### Дополнительно
В `user_test_python` реализована запись логов в файл user_tests.log (уровень логов можно изменить в файле конфигурации `congig.json` -> log -> level).

В случае ошибки запуска тестов из дирректории user_test_python, воспользуйтесь командой  *`pip install -r requirements.txt`* в `terminal`.
