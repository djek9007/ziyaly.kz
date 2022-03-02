from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.forms import CheckboxSelectMultiple, models
from django.utils.safestring import mark_safe

from .models import Category, Post, PhotoItem


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
    text = forms.CharField(required=False, label="Контент страницы", widget=CKEditorUploadingWidget())
    # category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=True, widget=forms.CheckboxSelectMultiple, label='Категория')

    class Meta:
        model = Post
        fields = '__all__'

class PhotoItemInline(admin.TabularInline):
    model = PhotoItem



@admin.register(Post)
class PostAdmin(ActionPublish):
    """Статичные страницы"""
    list_display = ("title", "published",'slug', "id", 'name_category', 'sort',)
    list_editable = ("published", 'sort',)
    list_filter = ("published",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title", )}
    form = PostAdminForm
    actions = ['unpublish', 'publish']
    list_per_page = 50 #разделение записи
    filter_horizontal  = ('category',)
    inlines = [PhotoItemInline]
    # сверху админки показывает сохранить удалить
    save_on_top = True
    # readonly_fields = ("image",)