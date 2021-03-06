# currency_solution
API для получения разницы котировок валют по датам

## Поддерживаемые запросы

Список валют загружается с сайта ЦБ и записывается в базу данных Django один раз при проведении миграций: `python manage.py migrate`.

Запрос корневой страницы возвращает сохраненный список валют с сайта ЦБ. Для получения разницы котировок валюты между заданными датами используется запрос `/currency/*буквенный код валюты*/?start=*начальная дата*?end=*конечная дата*`. Ответ возвращается в формате JSON.

## Используемые технологии

В качестве основного инструмента используется Django Rest Framework, позволяющий достаточно быстро решить задачу с поддержкой хранения информации во внутренней БД, что позволяет уменьшить количество внешних запросов, а также обработки исключений и возможностью дальнейшего расширения функционала.

Для отправки и обработки внешних запросов используются библиотеки urllib и xmltodict, предоставляющие удобный интерфейс для парсинга и обработки XML-документов.