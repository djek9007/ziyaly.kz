# forms.py
from django import forms
from django.core.exceptions import ValidationError

from .models import Participant, ParticipantSbornik
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.utils.translation import gettext_lazy as _
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django.utils.translation import gettext as _

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        exclude = ('status_form', 'conference')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Row(
                Column('full_name', css_class='form-group col-md-6'),
                Column('article_title', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('country', css_class='form-group col-md-6'),
                Column('city', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('workplace', css_class='form-group col-md-6'),
                Column('position', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('academic_degree', css_class='form-group col-md-6'),
                Column('academic_title', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('contact_phone', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('participation_form', css_class='form-group col-md-6'),
                Column('presentation_form', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('technical_requirements', css_class='form-group col-md-12'),
                css_class='form-row'
            ),
            Submit('submit', _('Қатысуға өтінім жіберу'), css_class='btn btn-info mb--45')
        )

def validate_file_size(value):
    limit = 20 * 1024 * 1024  # 20 MB
    if value.size > limit:
        raise ValidationError(_('Файл 20 МБ-тан аспауы керек.'))

def validate_file_extension(value):
    allowed_extensions = ['.pdf', '.doc', '.docx', '.odt', '.txt', '.zip', '.rar']
    file_extension = value.name.lower().split('.')[-1]
    if file_extension not in allowed_extensions:
        raise ValidationError(_('Тек PDF, DOC, DOCX, ODT, TXT, ZIP, RAR форматтарға рұқсат етіледі.'))

class ParticipantSbornikForm(forms.ModelForm):
    class Meta:
        model = ParticipantSbornik
        exclude = ('status_form', 'conference')

    file = forms.FileField(label=_('Файл'), validators=[validate_file_size, validate_file_extension])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(

            Row(
                Column('full_name', css_class='form-group col-md-6'),
                Column('article_title', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('country', css_class='form-group col-md-6'),
                Column('city', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('workplace', css_class='form-group col-md-6'),
                Column('position', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('academic_degree', css_class='form-group col-md-6'),
                Column('academic_title', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('contact_phone', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
                css_class='form-row'
            ),

            Row(
                Column('file', css_class='form-group col-md-12'),
                css_class='form-row'
            ),
            Submit('submit', _('Конференция жинағына материал жіберу'), css_class='btn btn-info mb--45')
        )


#     super().__init__(*args, **kwargs)
#     self.helper = FormHelper()
#     self.helper.form_method = 'post'
#     self.helper.layout = Layout(
#         Row(
#             Column('full_name', css_class='form-group col-md-6'),
#             Column('country', css_class='form-group col-md-6'),
#         ),
#         Row(
#             Column('city', css_class='form-group col-md-6'),
#             Column('workplace', css_class='form-group col-md-6'),
#         ),
#         Row(
#             Column('position', css_class='form-group col-md-6'),
#             Column('academic_degree', css_class='form-group col-md-6'),
#         ),
#         Row(
#             Column('academic_title', css_class='form-group col-md-6'),
#             Column('article_title', css_class='form-group col-md-6'),
#         ),
#         Row(
#             Column('email', css_class='form-group col-md-6'),
#             Column('contact_phone', css_class='form-group col-md-6'),
#         ),
#         Row(
#             Column('participation_form', css_class='form-group col-md-6'),
#             Column('presentation_form', css_class='form-group col-md-6'),
#         ),
#         Row(
#             Column('technical_requirements', css_class='form-group col-md-12'),
#         ),
#         Row(
#             Column('status_form', css_class='form-group col-md-6'),
#             Column('conference', css_class='form-group col-md-6'),
#         ),
#         Row(
#             Column('submit', css_class='form-group col-md-12'),
#         ),
#     )
#
#     self.helper.layout.append(Submit('submit', 'Submit'))