from django.db import migrations


SKILLS = [
    {
        'title': 'Mobile Development (Kotlin)',
        'description_ru': 'Разработка нативных Android-приложений в Android Studio. Использование Jetpack Compose',
        'description_en': 'Developing native Android applications in Android Studio. Using Jetpack Compose',
        'icon_classes': 'fa fa-brands fa-android',
        'anchor': 'mobile-development-skill',
        'sort_order': 10,
    },
    {
        'title': 'C++ / ООP',
        'description_ru': 'Понимание объектно-ориентированного программирования, UML, паттернов проектирования',
        'description_en': 'Understanding object-oriented programming, UML, and design patterns',
        'icon_classes': 'fa fa-bars-progress',
        'anchor': 'cpp-oop-skill',
        'sort_order': 20,
    },
    {
        'title': 'Testing',
        'description_ru': 'Поддержка и тестирование программных модулей. Использование DevTools, pytest',
        'description_en': 'Support and testing of software modules. Using DevTools, pytest',
        'icon_classes': 'fa fa-user-secret',
        'anchor': 'testing-skill',
        'sort_order': 30,
    },
    {
        'title': 'Databases (SQL)',
        'description_ru': 'Проектирование реляционных баз данных. Работа с MySQL',
        'description_en': 'Relational database design. Working with MySQL',
        'icon_classes': 'fa fa-unlock-alt',
        'anchor': 'databases-sql-skill',
        'sort_order': 40,
    },
    {
        'title': 'Python',
        'description_ru': 'Написание скриптов, тестирование (pytest), работа с Django (создание веб-приложений).',
        'description_en': 'Writing scripts, testing (pytest), and working with Django (creating web applications).',
        'icon_classes': 'fa fa-regular fa-edit',
        'anchor': 'python-skill',
        'sort_order': 50,
    },
    {
        'title': 'Models and Databases',
        'description_ru': 'Создание моделей Django, миграций, таблиц базы данных и вывод данных через админку.',
        'description_en': 'Creating Django models, migrations, database tables, and managing content through the admin.',
        'icon_classes': 'fa fa-database',
        'anchor': 'models-database-skill',
        'sort_order': 60,
    },
]


def seed_skills(apps, schema_editor):
    Skill = apps.get_model('pages', 'Skill')
    for skill in SKILLS:
        Skill.objects.update_or_create(
            anchor=skill['anchor'],
            defaults=skill,
        )


def remove_seeded_skills(apps, schema_editor):
    Skill = apps.get_model('pages', 'Skill')
    Skill.objects.filter(anchor__in=[skill['anchor'] for skill in SKILLS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_skills, remove_seeded_skills),
    ]
