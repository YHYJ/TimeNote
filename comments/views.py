from django.shortcuts import render, get_object_or_404, redirect

from blog.models import Post
from .models import Comment
from .forms import CommentForm

# Create your views here.   ——定义comments应用的视图函数

"""
redirect ——对HTTP请求进行重定向：
    既可以接收一个 URL 作为参数，也可以接收一个模型的实例作为参数（例如这里的 post）
    如果接收一个模型的实例，那么这个模型必须实现了 get_absolute_url 方法
    这样 redirect 会根据 get_absolute_url 方法返回的 URL 值进行重定向。
"""


def post_comment(request, post_pk):
    """获取被评论的文章，后面需要将评论和文章进行关联"""
    post = get_object_or_404(Post, pk=post_pk)

    '''HTTP请求分 get 和 post
    一般用户通过表单提交数据都是通过 post 请求
    因此只当用户请求为 post 时才需处理表单数据'''
    if request.method == 'POST':
        '''用户提交的数据存在类字典对象 request.POST 中
        利用这些数据构造 CommentForm 的实例来生成Django表单：'''
        form = CommentForm(request.POST)

        if form.is_valid():
            '''form.is_valid() 方法使Django自动检测表单数据是否符合格式要求（是否填了所有表单字段且数据类型符合）
            commit=False作用是仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库'''
            comment = form.save(commit=False)

            # 将评论和被评论的文章进行关联
            comment.post = post

            # 调用模型实例的 save 方法将评论数据保存到数据库
            comment.save()

            '''重定向到 post 的详情页
            当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法
            然后重定向到 get_absolute_url 方法返回的 URL'''
            return redirect(post)

        else:
            '''检查到数据不合法，重新渲染详情页，并且渲染表单的错误
            因此传递三个模板变量给 detail.html：
                一个是文章 Post ，一个是评论列表 comment_list，一个是表单 form
            post.comment_set.all() 方法：
                这个方法有点类似于 Post.objects.all()
                其作用是获取这篇 post 下的的全部评论
                因为 Post 和 Comment 是 ForeignKey 关联的
                因此使用 post.comment_set.all() 反向查询全部评论
            '''
            comment_list = post.comment_set.all()
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'blog/detail.html', context=context)
    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页
    return redirect(post)
