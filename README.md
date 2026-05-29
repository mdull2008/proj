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

Навыки в блоке `SKILL` хранятся в модели `Skill`. Их можно редактировать в
админке Django в разделе `Skills`; на главной странице они выводятся из базы.

Для production-сборки статики используйте:

```bash
python3 manage.py collectstatic
```