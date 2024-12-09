from django.urls import path, include

from participant import views


app_name = 'participant'

urlpatterns = [

    path('<slug:slug>/', views.participant_form, name='order'),
    path('<slug:slug>/success/', views.success_message, name='success_message'),
    path('send/<slug:slug>/', views.participant_send_file, name='send_file'),

]