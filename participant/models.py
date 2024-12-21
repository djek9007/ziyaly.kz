from django.db import models

# Create your models here.
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError



class Conference(models.Model):
    """Модель для конференции"""
    title = models.CharField(verbose_name=_('Конференция атауы'), max_length=255)
    slug = models.SlugField(verbose_name="URL", unique=True, max_length=50)
    start_date_order = models.DateTimeField(
        _('Өтінімді қабылдауды бастау күні'),
        default=timezone.now,

    )
    end_date_order = models.DateTimeField(
        _('Өтінімді қабылдауды аяқтау күні'),
        default=timezone.now,

    )
    start_date_journal = models.DateTimeField(
        _('Материалдарды қабылдауды бастау күні'),
        default=timezone.now,


    )
    end_date_journal = models.DateTimeField(
        _('Материалдарды қабылдауды аяқтау күні'),
        default=timezone.now,

    )
    published = models.BooleanField(_('Көрсету керек пе?'), default=True)



    class Meta:
        verbose_name = _('Конференция')
        verbose_name_plural = _('Конференциялар')

    def __str__(self):
        return self.title

class Participant(models.Model):
    """Модель заявки для участие в конференции"""
    full_name = models.CharField(verbose_name=_('Аты-жөніңіз'), max_length=255)
    country = models.CharField(verbose_name=_('Мемлекет'), max_length=100)
    city = models.CharField(verbose_name=_('Қала'), max_length=100)
    workplace = models.CharField(verbose_name=_('Жұмыс орныңыз'), max_length=255)
    position = models.CharField(verbose_name=_('Қызметіңіз'), max_length=100)
    academic_degree = models.CharField(verbose_name=_('Ғылыми дәреже'), max_length=100, blank=True, null=True)
    academic_title = models.CharField(verbose_name=_('Атағыңыз'), max_length=100, blank=True, null=True)
    article_title = models.CharField(verbose_name=_('Мақала атауы'), max_length=255)
    email = models.EmailField(verbose_name='Email')
    contact_phone = models.CharField(verbose_name=_('Телефон'), max_length=20, validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message=_('Телефон нөмірі "+999999999 " форматында болуы тиіс.')
            ),
        ])
    participation_form_choices = [
        ('online', _('Онлайн')),
        ('offline', _('Оффлайн')),
    ]
    participation_form = models.CharField(verbose_name=_('Қатысу түрі'), max_length=10,
                                          choices=participation_form_choices)
    presentation_form_choices = [
        ('video', _('Видео')),
        ('pdf', _('PDF')),
        ('slide', _('Презентация (powerpoint, google slides)')),
    ]
    presentation_form = models.CharField(verbose_name=_('Презентация формасы'), max_length=10,
                                         choices=presentation_form_choices)
    technical_requirements = models.TextField(verbose_name=_('Қажетті техникалық құралдар'), blank=True, null=True)
    check_form_choices = [
        ('new', _('Жаңа')),
        ('complement', _('Толықтыруды қажет етеді')),
        ('accepted', _('Қабылданды')),
        ('rejected', _('Қабылданбады')),

    ]
    status_form = models.CharField(verbose_name=_('Статусы'), max_length=20,
                                   choices=check_form_choices)
    conference = models.ForeignKey(Conference, verbose_name=_('Конференция'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Қатысуға өтінім')
        verbose_name_plural = _('Қатысуға өтінімдер')

    def __str__(self):
        return self.full_name

def validate_file_size(value):
    limit = 20 * 1024 * 1024  # 20 MB
    if value.size > limit:
        raise ValidationError(_('Файл 20 МБ-тан аспауы керек.'))

def validate_file_extension(value):
    allowed_extensions = ['pdf', 'doc', 'docx', 'odt', 'txt', 'zip', 'rar']  # Без точки
    file_extension = value.name.lower().split('.')[-1]
    if file_extension not in allowed_extensions:
        raise ValidationError(_('Тек PDF, DOC, DOCX, ODT, TXT, ZIP, RAR форматтарға рұқсат етіледі.'))

class ParticipantSbornik(models.Model):
    """Модель заявки для участие в конференции"""
    conference = models.ForeignKey(Conference, verbose_name='Конференция', on_delete=models.CASCADE)
    full_name = models.CharField(verbose_name=_('Аты-жөніңіз'), max_length=255)
    country = models.CharField(verbose_name=_('Мемлекет'), max_length=100)
    city = models.CharField(verbose_name=_('Қала'), max_length=100)
    workplace = models.CharField(verbose_name=_('Жұмыс орныңыз'), max_length=255)
    position = models.CharField(verbose_name=_('Қызметіңіз'), max_length=100)
    academic_degree = models.CharField(verbose_name=_('Ғылыми дәреже'), max_length=100, blank=True, null=True)
    academic_title = models.CharField(verbose_name=_('Атағыңыз'), max_length=100, blank=True, null=True)
    article_title = models.CharField(verbose_name=_('Мақала атауы'), max_length=255)
    email = models.EmailField(verbose_name='Email')
    contact_phone = models.CharField(verbose_name=_('Телефон'), max_length=20, validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message=_('Телефон нөмірі "+999999999 " форматында болуы тиіс.')
            ),
        ])
    check_form_choices = [
        ('new', _('Жаңа')),
        ('complement', _('Толықтыруды қажет етеді')),
        ('accepted', _('Қабылданды')),
        ('rejected', _('Қабылданбады')),

    ]
    file = models.FileField(verbose_name=_('Файл'), validators=[validate_file_size, validate_file_extension])
    status_form = models.CharField(verbose_name=_('Статусы'), max_length=20,
                                   choices=check_form_choices)


    class Meta:
        verbose_name = _('Жинаққа өтінім')
        verbose_name_plural = _('Жинаққа өтінімдер')

    def __str__(self):
        return self.full_name