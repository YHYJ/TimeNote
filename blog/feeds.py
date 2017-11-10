from django.contrib.syndication.views import Feed

from .models import Post

# RSS功能相关代码


class AllPostsRssFeed(Feed):
    """生成规范化的XML文档以方便聚合器阅读"""

    # 显示在聚合器上的标题
    title = "时光笔记"

    # 通过聚合器跳转到网站的地址
    link = "/"

    # 显示在聚合器上的描述信息
    description = "我什么都没忘，但有些事只适合珍藏"

    # 需要显示的内容条目
    def items(self):
        return Post.objects.all()

    # 聚合器中显示的内容条目的标题
    def item_title(self, item):
        return "[%s] %s" % (item.category, item.title)

    # 聚合器显示的内容条目的描述
    def item_description(self, item):
        return item.body
