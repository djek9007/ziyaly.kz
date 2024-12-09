# -*- coding: utf-8 -*-
from django import template

from menu.models import Menu

register = template.Library()



@register.simple_tag()
def show_menu():
    return Menu.objects.filter(published=True)