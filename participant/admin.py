from django.contrib import admin


from participant.models import Participant, Conference, ParticipantSbornik


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    # сверху админки показывает сохранить удалить
    list_display = ('id', 'title', 'slug')
    list_display_links = ('title',)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    icon_name = 'card_membership'


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    # сверху админки показывает сохранить удалить
    save_on_top = True
    # readonly_fields = ("slug",)
    icon_name = 'assignment_turned_in'
    list_filter = ('status_form', 'participation_form', 'presentation_form', 'conference')
    list_display = ('full_name', 'workplace', 'status_form')

@admin.register(ParticipantSbornik)
class ParticipantSbornikAdmin(admin.ModelAdmin):
    # сверху админки показывает сохранить удалить
    save_on_top = True
    # readonly_fields = ("slug",)
    icon_name = 'announcement'
    list_filter = ('conference', 'status_form',)
    list_display = ('full_name', 'article_title', 'contact_phone', 'file', 'status_form')