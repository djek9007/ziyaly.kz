# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _


class Menu(MPTTModel):
    """Класс модели меню"""
    name = models.CharField(_('Атауы'), max_length=100)
    slug = models.CharField('URL', max_length=80, blank=True, null=True, unique=False)
    parent = TreeForeignKey(
        'self',
        verbose_name=_('Жоғары санаты'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    published = models.BooleanField(_('Көрсету керек пе?'), default=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Мәзір')
        verbose_name_plural = _('Мәзірлер')