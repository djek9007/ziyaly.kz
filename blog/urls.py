from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('<slug:category_slug>/', views.PostListView.as_view(), name='category'),
    path('<slug:category_slug>/<slug:slug>/', views.PostDetailView.as_view(), name='detail_post'),
    path('tulga/<slug:tulga_category_slug>/<slug:slug>/', views.TulgaDetailView.as_view(), name='detail_tulga'),




    path('', views.HomeView.as_view(), name='home'),
]
# +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)