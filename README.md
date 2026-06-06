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
- сохранять заявки в `bot_bookings.json`;
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