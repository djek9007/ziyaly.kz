from django import forms
from client_side_image_cropping import ClientsideCroppingWidget

from blog.models import Banner, Post, Tulga


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        exclude = ['create_date']
        widgets = {
            'image': ClientsideCroppingWidget(width=2000, height=590, preview_width=400, preview_height=118),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['create_date']
        widgets = {
            'image': ClientsideCroppingWidget(width=700, height=400, preview_width=260, preview_height=180),
        }

class TulgaForm(forms.ModelForm):
    class Meta:
        model = Tulga
        exclude = ['create_date']
        widgets = {
            'image': ClientsideCroppingWidget(width=360, height=480, preview_width=300, preview_height=400),
            'image_thumbnail': ClientsideCroppingWidget(width=72, height=72, preview_width=72, preview_height=72),
        }