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
✅ Сеть представляет собой группы Продавцов и Продуктов.

✅ Каждый Продавец и относится к одной из трех групп:
- Завод
- Розничная сеть
- Индивидуальный предприниматель\

И имеет уровень в иерархии, зависящий от длины цепочки поставок. Так, завод всегда имеет уровень 0, а следующее за ним звено цепи (покупатель) — 1.

✅ При изменении уровня Продавца (или смены им группы на "Завод"), изменяется уровень всех его покупателей.

✅ Каждый Продавец имеет одного поставщика и может иметь несколько Продуктов.

✅ Поставщика, размер задолженности перед ним, количество и описание Продуктов,
а также данные Продавца (за исключением даты создания) можно вносить и изменять в админ-панели.

✅ В группе продавцов для каждого объекта указана ссылка на поставщика, а также реализована возможность фильтрации по городам.

✅ На странице группы Продавцы функционал для обнуления задолженностей перед поставщиком у нескольких выбранных объектов.

#### API:
✅ По адресу `http://localhost/api/seller/` и `http://localhost/api/seller/<pk>` для _активных пользователей_ доступны все CRUD-операции
с моделью Продавца, кроме изменения размера задолженности перед поставщиком, это поле является неизменяемым.

✅ При помощи параметра _country_ осуществляется фильтрация по стране Продавца:\
`http://localhost/api/seller?country=Россия`.
