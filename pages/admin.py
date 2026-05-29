from django.contrib import admin

from .models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('title', 'anchor', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
    search_fields = ('title', 'description_ru', 'description_en')
    prepopulated_fields = {'anchor': ('title',)}
