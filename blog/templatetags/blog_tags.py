from django import template
from django.db.models.aggregates import Count
from ..models import Post, Category, Tag

# 自定义模板标签{% %} （{{ arguments }}是模板变量）

"""模板标签本质上是一个 Python 函数"""

# 实例化一个template.Library类
register = template.Library()


@register.simple_tag    # 使用装饰器注册该函数为模板标签
def get_recent_posts(num=6):
    """最新6篇文章模板标签"""
    return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def archives():
    """归档模板标签
    dates返回一个列表，其中元素为每一篇文章（Post）的创建时间，且是 Py 的 date 对象
    精确到月份，降序排列
    """
    return Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    """分类模板标签
    Count 计算分类下的文章数，参数为需要计数的模型的名称
    Category.objects.annotate 方法和 Category.objects.all 类似
        返回数据库中全部 Category 的记录
        同时通过 Count 方法统计返回的 Category 记录的集合中每条记录下的文章数
        Count 接受一个 和 Category 关联的模型参数名(post，通过 ForeignKey 关联)
        然后统计 Category 记录的集合中每条记录下与之关联的 Post 记录的行数，也就是文章数
        最后把这个值保存到 num_posts 属性中
    接着对结果集做了一个过滤，使用 filter 方法把 num_posts 的值小于 1 的分类过滤掉
    因为 num_posts 的值小于 1 表示该分类下没有文章，没有文章的分类不希望它在页面中显示"""
    # num_posts__gt=0 表示大于0(gt的功能)，大于等于是 gte
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tags():
    """标签云模板标签"""
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

