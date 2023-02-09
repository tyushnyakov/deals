# DEALS
## Gems API

API обработки данных о покупках ювелирных украшений.

### Инструкция по запуску проекта

1. Клонировать проект
2. Перейти в корневую директорию проекта: 
~~~
cd deals
~~~
3. Запустить проект
~~~
docker-compose up --build
~~~
4. Для тестирования проекта открыть браузер по ссылке: [http:\\127.0.0.1:1337/swagger]()

API имеет два метода:
- GET - позволяет получить информацию со списком из 5 клиентов,
потративших наибольшую сумму за весь период
- POST - позволяет загружать файл в формате csv с данными о покупках клиентов.
