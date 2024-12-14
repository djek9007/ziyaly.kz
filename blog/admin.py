from django.contrib import admin
from django import forms


from .forms import BannerForm, PostForm, TulgaForm
from .models import Category, Post, PhotoItem, Banner, Tulga, PhotoItemTulga, CategoryTulga, Tulgasoz
from tinymce.widgets import TinyMCE
from django.contrib import admin

from client_side_image_cropping import DcsicAdminMixin
class ActionPublish(admin.ModelAdmin):
    """Action для публикации и снятия с публикации"""

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        rows_updated = queryset.update(published=False)
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    def publish(self, request, queryset):
        """Опубликовать"""
        rows_updated = queryset.update(published=True)
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change',)


class BannerAdmin(DcsicAdminMixin, admin.ModelAdmin):
    form = BannerForm
    list_display = ('title', 'published', 'created_date')
    search_fields = ('title', 'description')
    list_filter = ('published', 'created_date')

admin.site.register(Banner, BannerAdmin)

@admin.register(Category)
class CategoryAdmin(ActionPublish):
    """Статичные страницы"""
    list_display = ("name", "published",'slug', "id")
    list_editable = ("published", )
    list_filter = ("published", )
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name", )}

    actions = ['unpublish', 'publish']
    # сверху админки показывает сохранить удалить
    save_on_top = True
    # readonly_fields = ("slug",)

class PostAdminForm(forms.ModelForm):
    """Виджет редактора ckeditor"""
    form = PostForm

    class Meta:
        model = Post
        fields = '__all__'

class PhotoItemInline(admin.TabularInline):
    model = PhotoItem

class PhotoItemTulgaInline(admin.TabularInline):
    model = PhotoItemTulga

class TulgasozInline(admin.TabularInline):
    model = Tulgasoz


@admin.register(Post)
class PostAdmin(DcsicAdminMixin, ActionPublish):
    """Статичные страницы"""
    list_display = ("title", 'category',"published",'slug', "id",  )
    list_editable = ("published", )
    list_filter = ("published", "published_date",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title", )}
    form = PostForm
    actions = ['unpublish', 'publish']
    list_per_page = 50 #разделение записи

    inlines = [PhotoItemInline]
    # сверху админки показывает сохранить удалить
    save_on_top = True
    readonly_fields = ("edit_date",)

@admin.register(Tulga)
class TulgaAdmin(DcsicAdminMixin, ActionPublish):
    """Статичные страницы"""
    list_display = ("name", "published",'slug', "id",  )
    list_editable = ("published", )
    list_filter = ("published", "category",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name", )}
    form = TulgaForm
    actions = ['unpublish', 'publish']
    list_per_page = 50 #разделение записи

    inlines = [PhotoItemTulgaInline]
    # сверху админки показывает сохранить удалить
    save_on_top = True
    readonly_fields = ("edit_date",)
@admin.register(CategoryTulga)
class CategoryAdmin(ActionPublish):
    """Статичные страницы"""
    list_display = ("name", "published",'slug', "id")
    list_editable = ("published", )
    list_filter = ("published", )
    search_fields = ("name",)

    actions = ['unpublish', 'publish']
    # сверху админки показывает сохранить удалить
    save_on_top = True
    # readonly_fields = ("slug",)

@admin.register(Tulgasoz)
class TulgaSozAdmin(DcsicAdminMixin, ActionPublish):
    """Статичные страницы"""
    list_display = ("author", "text", "published", 'slug', "id", "in_main")
    list_editable = ("published", "in_main")
    list_filter = ("published", "author",)
    search_fields = ("author__name",)  # Предполагается, что author имеет поле name

    form = TulgaForm
    actions = ['unpublish', 'publish']
    list_per_page = 50  # Разделение записи
    save_on_top = True

    # Используйте это, чтобы предварительно заполнить слаг на основе других полей
    prepopulated_fields = {"slug": ("author",)}  # Это поле будет заполняться на основе текстового поля

