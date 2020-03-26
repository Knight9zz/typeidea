from django.contrib import admin
# 抽象出author基类

class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1. 用来补充model的owner
    2. 用来过滤query—_set只显示当前作者相关的信息
    """

    exclude = ('owner',)

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request,obj, form, change)