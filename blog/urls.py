from django.conf.urls import url

from . import views

# My creation   ——定义blog应用的url模式


app_name = 'blog'   # <URL模式命名空间>：告诉Django该urls.py模块属于blog应用
'''
一个复杂的 Django 项目可能不止这些URL模式，例如一些第三方应用中也可能有叫 index、detail 的URL模式
要把它们区分开来防止冲突需要通过 app_name 来指定命名空间
'''
urlpatterns = [  # 定义网址和视图函数的关系
    url(r'^$', views.IndexView.as_view(), name='index'),  # 绑定主页URL，参数1是网址，参数2是视图函数，参数3是处理函数的别名
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),    # 绑定详情页URL
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),

]
