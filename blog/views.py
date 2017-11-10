import markdown
from django.db.models import Q
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

from .models import Post, Category, Tag
from comments.forms import CommentForm

# Create your views here.   ——定义视图函数


def search(request):
    """搜索功能视图函数"""

    '''获得用户提交的搜索关键词
    用户通过表单 get 方法提交的数据 Django 保存在 request.GET 里
    这是个类似于Py字典的对象，所以使用 get 方法从中取出键 q 对应的值，即用户的搜索关键词
    至于字典的键之所以叫 q 是因为模板的表单中搜索框 input 的 name 属性的值是 q '''
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        '''校验，如果用户没有输入搜索关键词而提交了表单
        就无需执行查询而在模板中渲染一个错误提示信息'''
        error_msg = '未输入关键词'
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    '''用户输入了搜索关键词就通过 filter 方法从数据库里过滤出符合条件的所有文章
    这里的过滤条件是 title__icontains=q，即 title 中包含（contains）关键字 q
    前缀 i 表示不区分大小写， icontains 是查询表达式（Field lookups）'''
    # Q 对象用于包装查询表达式，其作用是为了提供复杂的查询逻辑
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})


class IndexView(ListView):
    """主页的类视图
    类视图：因为 IndexView 类功能是从数据库中获取文章列表
    ListView 可以从数据库获取某个模型列表数据，所以继承 ListView
    属性：
        model：指定要获取的模型是 Post
        context_object_name：指定获取的模型列表数据保存的变量名，这个变量会被传递给模板
        template_name：指定要用这个视图渲染的模板
    """
    model = Post
    context_object_name = 'post_list'
    template_name = 'blog/index.html'

    # 指定 paginate_by 属性以开启分页功能，其值为每页文章数
    paginate_by = 3

    def get_context_data(self, **kwargs):
        """函数 render 的 context 参数将视图函数中的模板变量作为一个字典传递给模板
        例如 render(request, 'blog/index.html', context={'post_list': post_list})
        传递了一个 {'post_list': post_list} 字典给模板
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的
        所以复写该方法，以便插入一些自定义的模板变量"""
        # 首先获得父类生成的传递给模板的字典
        context = super().get_context_data(**kwargs)

        '''父类生成的字典中已有 paginator、page_obj、is_paginated 三个模板变量
        paginator 是 Paginator 的一个实例
        page_obj 是 Page 的一个实例
        is_paginated 是一个布尔变量，用于指示是否已分页
            例如如果规定每页10个数据，而本身只有5个数据，其实就用不着分页
            此时 is_paginated = False '''
        #  context 是一个字典，调用 get 方法从中取出某个键对应的值
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        '''将分页导航条的模板变量更新到 context 中
        pagination_data 方法返回的也是一个字典'''
        context.update(pagination_data)

        '''将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量渲染模板
        此时 context 字典中已有了显示分页导航条所需的数据'''
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，就不显示分页导航，因此返回一个空字典
            return {}

        # 当前页左/右的页码，初始为0
        left = []
        right = []

        # 标示第1页/最后1页后/前是否需要显示省略号
        left_has_more = False
        right_has_more = False

        '''标示是否需要显示第1页/末页的页码
        若当前页左边/右面的连续页码中已经含有第1页/末页的页码，此时无需再显示第1页/末页的页码
        其它情况下第1页/末页的页码始终需要显示
        初始值为 False'''
        first = False
        last = False

        # 获得当前用户请求的页码
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，如分了2页，就是[1, 2, 3]
        page_range = paginator.page_range

        if page_number == 1:
            '''如果用户请求第一页的数据，那么当前页左边不需要数据
            因此 left=[]（已默认为空）
            此时只要获取当前页右边的连续页码号
            比如页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]
            这里只获取了当前页码后连续两个页码，可以更改这个数字以获取更多页码'''
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                '''如果最右边的页码比最后一页的页码减去 1 还小
                说明最右边的页码和最后一页的页码之间还有其它页码
                因此需要显示省略号，通过 right_has_more 来指示'''
                right_has_more = True

            if right[-1] < total_pages:
                '''如果最右边的页码比最后一页的页码号小
                说明当前页右边的连续页码号中不包含最后一页的页码
                所以需要显示最后一页的页码号，通过 last 来指示'''
                last = True

        elif page_number == total_pages:
            '''如果用户请求最后1页的数据，当前页右边不需要数据，因此 right=[]（已默认为空），
            此时只要获取当前页左边的连续页码
            比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            这里只获取了当前页码后连续2个页码，更改这个数字以获取更多页码'''
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            '''如果最左边的页码比第2页页码还大
            说明最左边的页码和第1页的页码之间还有其它页码，因此需要显示省略号
            通过 left_has_more 来指示'''
            if left[0] > 2:
                left_has_more = True

            '''如果最左边的页码比第1页的页码大，说明当前页左边连续页码号中不包含第一页
            所以需要显示第一页的页码，通过 first 来指示'''
            if left[0] > 1:
                first = True

        else:
            '''用户请求的既不是最后1页，也不是第1页，则需要获取当前页左右两边的连续页码
            这里只获取了当前页码前后连续2个页码，更改这个数字以获取更多页码'''
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后1页及其前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第1页及其后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


class PostDetailView(DetailView):
    """详情页的类视图"""
    model = Post
    context_object_name = 'post'
    template_name = 'blog/detail.html'

    def get(self, request, *args, **kwargs):
        """覆写 get 方法，每当文章被访问一次，就将文章阅读量 +1
        get 方法返回的是一个 HttpResponse 实例
        只有当 get 方法被调用后，才有 self.object 属性
        其值为 Post 模型实例，即被访问的文章 post"""
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 文章阅读量 +1，self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        """对 post 的 body 值进行渲染"""
        post = super(PostDetailView, self).get_object(queryset=None)
        # 对md语法的拓展
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',  # 多种拓展
            'markdown.extensions.codehilite',  # 语法高亮拓展
            # 'markdown.extensions.toc',  # 自动生成目录拓展
            TocExtension(slugify=slugify)
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        """将 post、评论表单、post 下的评论列表传递给模板"""
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


class ArchivesView(ListView):
    """归档的类视图"""
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month
                                                               )


class CategoryView(ListView):
    """分类的类视图，因为属性和类 IndexView 一样，所以直接继承 IndexView """
    model = Post
    context_object_name = 'post_list'
    template_name = 'blog/index.html'

    def get_queryset(self):
        """获取指定分类下的文章列表数据：
        覆写了父类的 get_queryset 方法，该方法默认获取指定模型的全部列表数据"""
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(ListView):
    """标签的类视图"""
    model = Post
    context_object_name = 'post_list'
    template_name = 'blog/index.html'

    def get_queryset(self):
        """获取指定标签下的文章列表数据"""
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


# def index(request):
#     """主页视图
#     :param request: HTTP请求
#     :return: render: 根据参数构造HttpResponse
#     """
#     post_list = Post.objects.all().order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})


# def archives(request, year, month):
#     """归档视图
#     类似主页视图，但不再使用all()获取全部文章，而是使用filter根据条件筛选
#     Py 中类实例调用属性的方法通常是 created_time.year，但是由于这里作为函数的参数列表
#     所以 Django 要求把点替换成两个下划线，即 created_time__year 和 created_time__month
#     """
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month,).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})


# def category(request, pk):
#     """分类视图"""
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})


# def detail(request, pk):
#     """详情页视图
#     根据从URL捕获的文章id（即pk，这里pk和id等价）获取数据库中文章id为pk的记录，然后传递给模板
#     当传入的pk对应的Post在数据库中存在时，get_object_or_404方法返回对应的post，不存在则返回404
#     :param request:
#     :param pk:
#     :return:
#     """
#     post = get_object_or_404(Post, pk=pk)
#
#     # 调用模型方法ncrease_views() +1 阅读量
#     post.increase_views()
#
#     post.body = markdown.markdown(post.body,
#                                   extensions=[  # 对md语法的拓展
#                                       'markdown.extensions.extra',  # 多种拓展
#                                       'markdown.extensions.codehilite',  # 语法高亮拓展
#                                       'markdown.extensions.toc',    # 自动生成目录拓展
#                                   ])
#     form = CommentForm()
#     # 获取当前 post 下的所有评论
#     comment_list = post.comment_set.all()	 # post 和 comment 是一对多关系，这是该关系的查询方式
#
#     # 将文章、表单、文章的评论列表作为模板变量传给 detail.html 以渲染相应数据
#     context = {'post': post,
#                'form': form,
#                'comment_list': comment_list,
#                }
#
#     return render(request, 'blog/detail.html', context=context)
