# Django portfolio site

Проект запускает загруженный HTML/CSS/изображения как Django-сайт.

## Быстрый старт

```bash
python3 -m pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

- Главная страница: <http://127.0.0.1:8000/>
- Админка Django: <http://127.0.0.1:8000/admin/>

Статика подключена из папки `DJANGO/`, поэтому загруженные `css`, `fonts` и `images`
используются на сайте через Django staticfiles.

Для production-сборки статики используйте:

```bash
python3 manage.py collectstatic
```

## Telegram-бот для мастера маникюра

В проект добавлен отдельный бот `manicure_bot.py`. Он умеет:

- показывать прайс;
- принимать запись клиента по шагам;
- давать выбрать услугу, дату и время;
- сохранять заявки в Excel-таблицу `bookings.xlsx`;
- отправлять уведомление мастеру, если указан `MASTER_CHAT_ID`.

### Быстрый запуск

1. Установите зависимости:

```bash
python3 -m pip install -r requirements.txt
```

2. Создайте бота через Telegram-бота `@BotFather` и получите токен.

3. Запустите бота:

```bash
export TELEGRAM_BOT_TOKEN="ваш_токен_от_BotFather"
export MASTER_NAME="мастер маникюра Анна"
python3 manicure_bot.py
```

4. Чтобы бот отправлял мастеру новые заявки, сначала напишите своему боту команду:

```text
/myid
```

Скопируйте полученный chat ID и запустите бота так:

```bash
export TELEGRAM_BOT_TOKEN="ваш_токен_от_BotFather"
export MASTER_CHAT_ID="ваш_chat_id"
python3 manicure_bot.py
```

### Где хранятся записи

После первой заявки бот автоматически создаст файл `bookings.xlsx`.
Это обычная Excel-таблица с колонками:

- дата;
- время;
- услуга;
- цена;
- имя клиента;
- телефон;
- Telegram клиента;
- статус записи.

Файл `bookings.xlsx` не хранится в git и остается только у владельца бота.

Чтобы получить таблицу прямо в Telegram, мастер может написать боту:

```text
/excel
```

Команда доступна только владельцу, если при запуске указан `MASTER_CHAT_ID`.
Для публичной ссылки загрузите полученный `bookings.xlsx` в Google Drive или
Google Sheets и включите доступ "Все, у кого есть ссылка".

### Как поменять прайс

Откройте файл `manicure_bot.py` и измените блок `SERVICES`:

```python
SERVICES = {
    "gel": Service("gel", "Маникюр + гель-лак", "120 мин", 2500),
}
```

Можно менять название услуги, длительность и цену.

### Как поменять контакты

Контакты показаны в обработчике `menu:contacts` внутри файла `manicure_bot.py`.
Замените адрес, телефон и Telegram/Instagram на данные мастера.