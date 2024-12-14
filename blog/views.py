from datetime import datetime

from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
# Create your views here.
from django.views import View
from django.db.models import Count
from .models import Category, Post, Banner, Tulga, Tulgasoz, CategoryTulga
from django.db.models import Q

class HomeView(View):
    def get_queryset(self):
        return Post.objects.filter(published=True)

    def get(self, request):
        banners = Banner.objects.filter(published=True)
        tulgalar = Tulga.objects.filter(published=True)[:3]

        naqylsoz = Tulgasoz.objects.filter(published=True, in_main=True).select_related('author')[:20]


        posts = self.get_queryset()[:6]


        context = {
            'post_list': posts,
            'banners':banners,
            'tulgalar':tulgalar,
            'naqylsoz': naqylsoz,
        }

        return render(request, 'blog/home.html', context)

class PostListView(View):
    def get_queryset(self):
        return Post.objects.filter(published=True).order_by('-published_date')

    def get(self, request, category_slug=None):
        # Получение всех категорий с количеством опубликованных постов
        categories = Category.objects.filter(published=True).annotate(posts_count=Count('post'))

        # Если передан slug категории, фильтруем по ней
        category = None
        posts = self.get_queryset()
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            posts = posts.filter(category=category)

        # Пагинация
        paginator = Paginator(posts, 4)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        # Получение последних постов для боковой панели
        recent_posts = Post.objects.filter(published=True).order_by('-published_date')[:5]

        context = {
            'post_list': posts,
            'category': category,
            'category_list': categories,
            'recent_posts': recent_posts,
        }

        return render(request, 'blog/blog_list.html', context)

class TulgaListView(View):
    """Вывод категории и вывод стати"""

    def get_queryset(self, search_query=None):
        queryset = Tulga.objects.filter(published=True)
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(text__icontains=search_query))
        return queryset

    def get(self, request, tulga_category_slug=None):
        search_query = request.GET.get('Search')  # Fetch search term from query params
        if tulga_category_slug:
            try:
                category = CategoryTulga.objects.get(slug=tulga_category_slug)
                posts = self.get_queryset(search_query).filter(category=category, category__published=True)
                title = category.name
            except CategoryTulga.DoesNotExist:
                raise Http404("Category does not exist.")
        else:
            category = None
            title = 'Қазақ елінің Ұлы тұлғалары'
            posts = self.get_queryset(search_query)

        category_tulga = CategoryTulga.objects.filter(published=True).annotate(post_count=Count('tulga'))
        paginator = Paginator(posts, 4)
        page = self.request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {
            'post_list': posts,
            'category': category,
            'title': title,
            'category_tulga': category_tulga,
            'search_query': search_query,  # Add search query to context
        }

        return render(request, 'blog/tulga_list.html', context)

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


