
from django.contrib import admin
from .models import Post, Category, Tag
from django.urls import reverse
from django.utils.html import format_html
from .adminforms import PostAdminForm
from .base_admin import BaseOwnerAdmin
# Register your models here.

@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count', 'owner')
    fields = ('name', 'status', 'is_nav')

    # 自定义展示字段
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义分类过滤器，只展示当前用户创建的分类"""

    title = '分类过滤器'
    parameter_name = 'owner_category'

    # 返回一个元组组成的列表，元组的第一个参数赋值给self.value用于进行条件过滤
    # 第二个参数用于在过滤器下展示，每个标签的名字
    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post)
class PostAdmin(BaseOwnerAdmin):
    # 让摘要以多行多列显示

    form = PostAdminForm
    iframe = """
    <iframe frameborder="1" border="1"
            marginwidth="0" marginheight="0"
            width=333 height=77
            src="http://music.163.com/outchain/player?type=2&id=1398258337&auto=1&height=66">
    </iframe>
    """
    list_display = (
        'title', 'category', 'status',
        'created_time', 'owner','operator',
        'music',
    )
    list_display_links = []
    filter_horizontal = ('tag',)
    # 注意这里不带引号。
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True

    # 字典的key 可以为 fields，classes，description
    fieldsets = (
        ('基础配置',{
            'description':'基础配置描述',
            'fields':(
                ('title', 'category'),
                'status',
            ),
        }),
        (('music'),{
            'fields':(
                'music',
            )
        }),

        (('内容'),{
            'fields':(
                'desc',
                'content',
            ),
        }),
        ('额外信息',{
            'classes':('collapse',),
            'fields':('tag',),
        }),
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id, ))
        )
    operator.short_description = '操作'

