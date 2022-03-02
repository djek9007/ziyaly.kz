from django import template

from blog.models import Category

register = template.Library()


@register.simple_tag(takes_context=True)
def show_category(context,):
        return  Category.objects.filter(published=True)

