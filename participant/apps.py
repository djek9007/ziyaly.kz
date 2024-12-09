from django.apps import AppConfig


class ParticipantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'participant'
    verbose_name='Конференция'
    verbose_name_plural='Конференциялар'
