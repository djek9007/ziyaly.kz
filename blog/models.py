from django.db import models
from django.urls import reverse
from django.utils import timezone
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


# Create your models here.
# from sorl.thumbnail import ImageField, get_thumbnail


class Category(MPTTModel):
    """Модель категории"""
    name = models.CharField("Название категории", max_length=100)
    slug = models.SlugField("url", max_length=100, unique=True)
    parent = TreeForeignKey(
        'self',
        verbose_name="Родительская категория",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    published = models.BooleanField("отображать?", default=True)
    sort = models.PositiveIntegerField('порядок', default=0)
    icon = models.CharField('Иконка', max_length=50, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ('sort',)

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'category_slug': self.slug})




class Post(models.Model):
    """Модель постов"""
    title = models.CharField("Заголовок", max_length=250)
    text = models.TextField("Полный текст")
    description =  models.CharField("Краткое описание для поисковиков", max_length=250, default='')
    create_date = models.DateTimeField("дата создания", auto_now=True)
    slug = models.SlugField("url", max_length=100, unique=True)
    edit_date = models.DateTimeField(
        "дата редактирования",
        default=timezone.now,
        blank=True,
        null=True
    )
    published_date = models.DateTimeField(
        "дата публикации",
        default=timezone.now,
        blank=True,
        null=True
    )
    image = models.ImageField("главная фотография", upload_to="post/", null=True, blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name="Категория", on_delete=models.CASCADE
    )
    published = models.BooleanField("опубликовать?", default=True)
    sort = models.PositiveIntegerField('порядок', default=0)

    def __str__(self):
        return self.title
    # @property
    # def thumbnail(self):
    #     if self.image:
    #         return get_thumbnail(self.image, '730x509', quality=80)
    #     return None

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['sort', '-published_date', ]

    def get_absolute_url(self):
        return reverse('blog:detail_post', kwargs={'slug': self.slug})


class PhotoItem(models.Model):
    image = models.ImageField(upload_to='post/', verbose_name='Галерея', blank=True, null=True, unique=True)
    photo = models.ForeignKey(Post, related_name='photoitems', on_delete=models.CASCADE)

    # @property
    # def thumbnail(self):
    #     if self.image:
    #         return get_thumbnail(self.image, '730x509', quality=80)
    #     return None

    def __str__(self):
        return str(self.photo.id)
    class Meta:
        verbose_name = "Галерея постов"
        verbose_name_plural = "Галерея постов"