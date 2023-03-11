# Онлайн платформа торговой сети электроники
Веб-приложение с API интерфейсом, админ-панелью и базой данных.
___


### Стек 📚
- Python 3.10
- Django 4.1.7
- DRF 3.14.0
- PostgreSQL 14.6
- Docker
___
### Запуск 🚀
1) Клонируйте репозиторий
`git clone https://github.com/Alstacon/net_shop.git`.
2) Смените имя файла с `.env.example` на `.env` и заполните его валидными значениями.
3) Запустите докер-контейнер `docker-compose up --build -d`.


___
### Функционал 🪛
#### Админ-панель:
✅ Сеть представляет собой группы Продавцов и Продуктов.\
<br>
✅ В группе продавцов для каждого объекта указана ссылка на поставщика, а также реализована возможность фильтрации по городам.\
<br>
✅ Добавлен функционал для обнуления задолженностей перед поставщиком у выбранных объектов.

#### API:

✅ По адресу `http://localhost/api/seller/` и `http://localhost/api/seller/<pk>` для активных пользователей доступны все CRUD-операции
с моделью поставщика, кроме изменения размера задолженности перед поставщиком, это поле является неизменяемым.\
<br>
✅ При помощи параметра _country_ осуществляется фильтрация по стране Продавца:\
`http://localhost/api/seller?country=Россия`
<br>
