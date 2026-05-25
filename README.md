# Django portfolio site

Проект запускает загруженный HTML/CSS/изображения как Django-сайт.

## Быстрый старт

```bash
python3 -m pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

- Главная страница: <http://127.0.0.1:8000/>
- Админка Django: <http://127.0.0.1:8000/admin/>

Статика подключена из папки `DJANGO/`, поэтому загруженные `css`, `fonts` и `images`
используются на сайте через Django staticfiles.