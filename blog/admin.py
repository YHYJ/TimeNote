from django.contrib import admin

from .models import Post, Category, Tag

# Register your models here.    ——注册手动创建的模型，创建并注册站点管理类


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'excerpt', 'created_time', 'modified_time', 'category', 'views', 'author']
    list_per_page = 10  # 每页显示数量
    actions_on_bottom = True    # 底部增加操作选项
    search_fields = ['title']   # 搜索框
    # 编辑页字段显示顺序
    # fields = ['title', 'author', 'body', 'category', 'created_time', 'modified_time', 'tags', 'excerpt', 'views']
    # 字段分组
    fieldsets = (
        ('必填', {'fields': ('title', 'author', 'body', 'category', 'created_time', 'modified_time')}),
        ('选填', {'fields': ('tags', 'excerpt', 'views')}),
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    list_per_page = 10
    actions_on_bottom = True


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    list_per_page = 10
    actions_on_bottom = True


class SearchAdmin(admin.ModelAdmin):
    """搜索框"""
    search_fields = ['name']


# 注册新添加的 PostAdmin 
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
# admin.site.register(SearchAdmin)
