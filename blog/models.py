
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from dynamic_filenames import FilePattern
from tinymce.models import HTMLField
from django.core.files.storage import default_storage
from django.utils.text import slugify
from django.core.exceptions import ValidationError

page_file_item = FilePattern(
    filename_pattern='{app_label:.25}/{model_name:.30}/{uuid:base32}{ext}'
)
class Banner(models.Model):
    """Баннер для главной страницы"""
    title = models.CharField(_('Тақырыбы'), max_length=250)
    title_slug = models.CharField(_('Сілтеме тақырыбы'), max_length=250, default='Толығырақ')
    slug = models.CharField("url", max_length=250, blank=True, null=True)
    description = models.CharField(verbose_name=_('Қысқаша мағлұмат'), blank=True, null=True, max_length=255)
    image = models.ImageField(_('Негізгі фотосурет'), upload_to=page_file_item, help_text=_('Фото көлемі 2000x590'))
    created_date = models.DateTimeField(_('Құрылған күні'), auto_now_add=True)
    edit_date = models.DateTimeField(_('Өңдеу күні'), default=timezone.now, blank=True, null=True)
    title_show = models.BooleanField(_('Тақырыбын көрсету керек пе?'), default=True)
    description_show = models.BooleanField(_('Қысқаша мағлұматты көрсету керек пе?'), default=True)
    published = models.BooleanField(_('Көрсету керек пе?'), default=True)

    class Meta:
        verbose_name = _('Баннер')
        verbose_name_plural = _('Баннерлер')

    def __str__(self):
        return self.title








class Category(models.Model):
    """Модель категории"""
    name = models.CharField(_("Атауы"), max_length=100)
    slug = models.SlugField("url", max_length=100, unique=True)
    published = models.BooleanField(_("Көрсету?"), default=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пост санаты'
        verbose_name_plural = 'Посттар санаты'


    def get_absolute_url(self):
        return reverse('blog:category_post', kwargs={'category_slug': self.slug})




class Post(models.Model):
    """Модель постов"""
    category = models.ForeignKey(
        Category,
        verbose_name="Категория", on_delete=models.CASCADE
    )
    title = models.CharField(_("Атауы"), max_length=250)
    slug = models.SlugField("url", max_length=100, unique=True)
    text = HTMLField(verbose_name=_("Мазмұны"))
    description =  models.CharField(_("Іздеу жүйелеріне арналған қысқаша сипаттама"), max_length=250, default='')
    create_date = models.DateTimeField(_("Құрылған күні"), auto_now=True)

    edit_date = models.DateTimeField(
        _("Өңдеу күні"),
        default=timezone.now,
        blank=True,
        null=True
    )
    published_date = models.DateTimeField(
        _("Жарияланған күні"),
        default=timezone.now,
        blank=True,
        null=True
    )
    image = models.ImageField(_("Басты фото"), upload_to=page_file_item, help_text=_('Фото көлемі 360x280'), blank=True, null=True)

    published = models.BooleanField(_("Көрсету?"), default=True)

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посттар"
        ordering = [ '-published_date', ]

    def get_absolute_url(self):
        return reverse('blog:detail_post', kwargs={'category_slug': self.category.slug,'slug': self.slug})


class PhotoItem(models.Model):
    image = models.ImageField(upload_to=page_file_item, verbose_name=_('Галерея'), blank=True, null=True, unique=True)
    photo = models.ForeignKey(Post, related_name='photoitems', on_delete=models.CASCADE)

    # @property
    # def thumbnail(self):
    #     if self.image:
    #         return get_thumbnail(self.image, '730x509', quality=80)
    #     return None

    def __str__(self):
        return str(self.photo.id)
    class Meta:
        verbose_name = _("Пост галереясы")
        verbose_name_plural = _("Посттар галереясы")

class CategoryTulga(models.Model):
    """Модель категории"""
    name = models.CharField(_("Атауы"), max_length=100)
    slug = models.SlugField("url", max_length=100, unique=True)
    published = models.BooleanField(_("Көрсету?"), default=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тұлға санаты'
        verbose_name_plural = 'Тұлғалар санаты'

    def get_absolute_url(self):
        return reverse('blog:category_tulga', kwargs={'tulga_category_slug': self.slug})

class Tulga(models.Model):
    """Модель постов"""
    category = models.ForeignKey(
        CategoryTulga,
        verbose_name="Тұлға санаты", on_delete=models.CASCADE
    )
    name = models.CharField(_("Аты жөні"), max_length=250)
    slug = models.SlugField("url", max_length=100, unique=True)

    text = HTMLField(verbose_name=_("Мазмұны"))
    description =  models.CharField(_("Іздеу жүйелеріне арналған қысқаша сипаттама"), max_length=250, default='')
    create_date = models.DateTimeField(_("Құрылған күні"), auto_now=True)

    edit_date = models.DateTimeField(
        _("Өңдеу күні"),
        default=timezone.now,
        blank=True,
        null=True
    )
    published_date = models.DateTimeField(
        _("Жарияланған күні"),
        default=timezone.now,
        blank=True,
        null=True
    )
    image = models.ImageField(_("Тұлғаның фотосы"), upload_to=page_file_item, help_text=_('Фото көлемі 400x400'), blank=True, null=True)
    image_thumbnail = models.ImageField(_("Тұлғаның қысқаша фотосы"), upload_to=page_file_item, help_text=_('Фото көлемі 72x72'),
                              blank=True, null=True)

    published = models.BooleanField(_("Көрсету?"), default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:detail_tulga', kwargs={'tulga_category_slug': self.category.slug,'slug': self.slug})

    def has_thumbnail(self):
        return self.image_thumbnail and default_storage.exists(self.image_thumbnail.name)


    class Meta:
        verbose_name = "Ұлы тұлға"
        verbose_name_plural = "Ұлы тұлғалар"
        ordering = [ '-published_date', ]



class PhotoItemTulga(models.Model):
    image = models.ImageField(upload_to=page_file_item, verbose_name=_('Галерея'), blank=True, null=True, unique=True)
    photo = models.ForeignKey(Tulga, related_name='photoitemstulga', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Тұлға галереясы")
        verbose_name_plural = _("Тұлға галереясы")


class Tulgasoz(models.Model):
    """Модель категории"""
    author = models.ForeignKey(Tulga, verbose_name=_("Ұлы тұлға"), on_delete=models.CASCADE, related_name='tulga_tulgasoz')
    text = HTMLField(verbose_name=_("Нақыл сөз"))
    slug = models.SlugField("url", max_length=100, unique=True)
    published = models.BooleanField(_("Көрсету?"), default=True)
    in_main = models.BooleanField(_('Басты бетте көрсету керек пе?'), default=False)


    def __str__(self):
        return self.author.name

    def save(self, *args, **kwargs):
        base_slug = slugify(self.author.slug[:10])
        text_slug = slugify(self.text[:30])
        new_slug = f"{base_slug}-{text_slug}"

        # Позволяем текущему слагу оставаться в силе, если он совпадает
        if self.pk:  # Мы редактируем существующий экземпляр
            existing_instance = Tulgasoz.objects.get(pk=self.pk)
            if existing_instance.slug == new_slug:
                self.slug = new_slug
                super().save(*args, **kwargs)
                return

        # Иначе, обеспечиваем уникальность
        count = 1
        unique_slug = new_slug
        while Tulgasoz.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{new_slug}-{count}"
            count += 1

        self.slug = unique_slug
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Ұлы тұлғаның нақыл сөзі'
        verbose_name_plural = 'Тұлғалардың нақыл сөздері'