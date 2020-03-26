from django.shortcuts import render,HttpResponse
from .models import Post,Category,Tag
from config.models import SideBar
from django.views.generic import ListView, DetailView
# Create your views here.


def post_list(request, category_id=None, tag_id=None):
    tag = None
    category= None

    if tag_id:
        p_list, tag = Post.get_by_tag(tag_id=tag_id)
    elif category_id:
        p_list, category = Post.get_by_category(category_id=category_id)
    else:
        p_list = Post.objects.filter(status=Post.STATUS_NORMAL)

    context = {
        'category':category,
        'tag':tag,
        'post_list':p_list,
        'sidebars':SideBar.get_all(),
        'categories':Category.objects.all(),
        'Tags':Tag.objects.all(),
        'latest_posts':Post.latest_posts(),
        'read_posts':Post.objects.filter(status=Post.STATUS_NORMAL).order_by('created_time')
    }

    return render(request, 'blog/index.html', context=context)


def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None

    context = {
        'post':post,
        'sidebars':SideBar.get_all(),
        'categories': Category.objects.all(),
        'Tags': Tag.objects.all(),
        'latest_posts': Post.latest_posts(),
        'read_posts': Post.objects.filter(status=Post.STATUS_NORMAL).order_by('created_time'),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/single.html', context=context)


def category(request, category_id):
    return HttpResponse(category_id)


def tag(request, tag_id):
    return HttpResponse(tag_id)


def About(request):
    context = {
        'name':'gly',
    }
    return render(request, 'blog/about.html', context=context)


def Contact(request):
    context = {
        'name':'gly',
    }
    return render(request, 'blog/contact.html', context=context)

