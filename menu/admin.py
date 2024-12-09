# -*- coding: utf-8 -*-
from django.contrib import admin

from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from menu.models import Menu


@admin.register(Menu)
class MenuAdmin(DraggableMPTTAdmin):
    """Статичные страницы"""
    list_display = ('tree_actions', 'indented_title', 'slug', 'published',)
    list_display_links = ('indented_title',)
    list_editable = ('slug', 'published',)
    MPTT_ADMIN_LEVEL_INDENT = 20
    # list_filter = ("published", )
    # search_fields = ("name",)
    prepopulated_fields = {"slug": ("name", )}


    # сверху админки показывает сохранить удалить
    save_on_top = True
    # readonly_fields = ("slug",)
    icon_name = 'menu'