from datetime import datetime

from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views import View

from .models import Category, Post


class PostListView(View):
    """Вывод категории и вывод стати"""

    # запрос к базе по полю публикации на true и по дате на сегодня которые должны выводится
    def get_queryset(self):
        return Post.objects.filter(published=True)

    def get(self, request, category_slug=None, tag_slug=None):
        if category_slug is not None:
            posts = self.get_queryset().filter(category__slug=category_slug, category__published=True)
        else:
            posts = self.get_queryset()
        paginator = Paginator(posts, 4)
        page = self.request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)

        context = {
            'post_list': posts,
        }

        return render(request, 'blog/home.html', context)



class PostDetailView(View):
    """Полная статья одного статьи"""

    def get(self, request, **kwargs):

        post = get_object_or_404(Post, slug=kwargs.get("slug"))
        photoitems = post.photoitems.all()
        context = {
            'post': post,
            'photoitems': photoitems
        }
        return render(request, 'blog/detail.html', context)


