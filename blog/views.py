from datetime import datetime

from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
# Create your views here.
from django.views import View

from .models import Category, Post, Banner, Tulga, Tulgasoz


class HomeView(View):
    def get_queryset(self):
        return Post.objects.filter(published=True)

    def get(self, request):
        banners = Banner.objects.filter(published=True)
        tulgalar = Tulga.objects.filter(published=True)[:3]

        naqylsoz = Tulgasoz.objects.filter(published=True, in_main=True).select_related('author')[:20]


        posts = self.get_queryset()[:3]


        context = {
            'post_list': posts,
            'banners':banners,
            'tulgalar':tulgalar,
            'naqylsoz': naqylsoz,
        }

        return render(request, 'blog/home.html', context)

class PostListView(View):
    """Вывод категории и вывод стати"""

    # запрос к базе по полю публикации на true и по дате на сегодня которые должны выводится
    def get_queryset(self):
        return Post.objects.filter(published=True)

    def get(self, request, category_slug=None, tag_slug=None):
        # category = Category.objects.get(slug=category_slug)
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
            # 'category': category,
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
        return render(request, 'blog/blog_detail.html', context)


class TulgaDetailView(View):
    """Полная статья одного статьи"""

    def get(self, request, **kwargs):

        post = get_object_or_404(Tulga, slug=kwargs.get("slug"))
        photoitems = post.photoitemstulga.all()
        tulga_tulgasoz = post.tulga_tulgasoz.all()
        context = {
            'post': post,
            'photoitems': photoitems,
            'tulga_tulgasoz': tulga_tulgasoz
        }
        return render(request, 'blog/tulga_detail.html', context)
        
class ESearchView(View):
    template_name = 'search_list.html'

    def get(self, request, *args, **kwargs):
        context={}
        context['form'] = ContactForm()

        question = request.GET.get('q')

        if question is not None:

            search_articles = Post.objects.filter(title__istartswith=question) | Post.objects.filter(text__icontains=question)

            # формируем строку URL, которая будет содержать последний запрос
            # Это важно для корректной работы пагинации
            context['last_question'] = '?q=%s' % question

            current_page = Paginator(search_articles, 5)

            page = request.GET.get('page')
            try:
                context['post_list'] = current_page.page(page)
            except PageNotAnInteger:
                context['post_list'] = current_page.page(1)
            except EmptyPage:
                context['post_list'] = current_page.page(current_page.num_pages)

        return render(request, template_name=self.template_name, context=context)


