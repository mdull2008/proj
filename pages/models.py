from django.db import models


class Skill(models.Model):
    title = models.CharField(max_length=120)
    description_ru = models.TextField('description in Russian')
    description_en = models.TextField('description in English')
    icon_classes = models.CharField(
        max_length=120,
        default='fa fa-regular fa-edit',
        help_text='Font Awesome classes, for example: fa fa-brands fa-android',
    )
    anchor = models.SlugField(
        max_length=80,
        unique=True,
        help_text='HTML anchor used in links, for example: models-database-skill',
    )
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'title']

    def __str__(self):
        return self.title
