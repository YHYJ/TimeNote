from django.conf.urls import url

from . import views

# My creation   ——定义评论应用的url模式


app_name = 'comments'
urlpatterns = [
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name='post_comment'),
]
