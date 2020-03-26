from django.views.generic import ListView, DetailView
from .models import Post
from config.models import SideBar
from .models import Post, Category, Tag
from django.shortcuts import get_object_or_404
from django.db.models import Q
from config.models import Link

class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all(),
            'Tags': Tag.objects.all(),
            'latest_posts': Post.latest_posts(),
            'read_posts': Post.objects.filter(status=Post.STATUS_NORMAL).order_by('created_time'),
            'Links': Link.objects.filter(status=Link.STATUS_NORMAL),
        })
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/index.html'



class CategoryView(IndexView):

    def get_queryset(self):
        """
        queryset 用于定义基础的数据集和model二选一
        get_queryset:如果定义了queryset会直接返回queryset
        这里在父类的数据集上根据条件进一步筛选
        :return:
        这里当点击某个分类时，会过滤出当前分类下的博文
        """
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):


    def get_queryset(self):
        """重写queryset，根据tag_id过滤"""
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        # 注意这里是双下划线
        return queryset.filter(tag__id=tag_id)



class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/single.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'


class SearchView(IndexView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'keyword':self.request.GET.get('keyword'),
            'result':'ok',
        })
        return context


    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))






