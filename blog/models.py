import markdown
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible    # Py2开发使用的装饰器

# Create your models here.  ——创建文章数据表


class Category(models.Model):
    """数据表：Category（分类）—— 数据列：name
    Django 要求模型必须继承 models.Model 类
    Category 只需要一个列 name 即可
    CharField 指定了列 name 的数据类型为字符型，最大长度为100
    Django 全部内置类型查看文档：
    https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
    """
    name = models.CharField(max_length=100, verbose_name='分类')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"


class Tag(models.Model):
    """数据表：Tag（标签）—— 数据列：name"""
    name = models.CharField(max_length=100, verbose_name='标签')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"


class Post(models.Model):
    """数据表：Post（文章）
       数据列：title —— 文章标题
              body —— 文章正文
              created_time —— 文章的创建时间
              modified_time —— 文章最后修改时间
              excerpt —— 文章摘要
              views —— 阅读量
            category —— 将 Category（分类）数据表与 Post（文章）数据表进行关联（一对多）
            tags —— 将 Tag（标签）数据表与 Post（文章）数据表进行关联（多对多）
            author —— 文章作者（一对多）
    """
    title = models.CharField(max_length=60, verbose_name='标题')

    # 使用字段TextField存储大段文本
    body = models.TextField(verbose_name='正文')

    '''文章摘要（可选）；
    默认情况下字段CharField要求必须存入数据，指定其参数blank=True即可允许空值'''
    excerpt = models.CharField(max_length=20, blank=True, verbose_name='摘要')

    # 使用字段DateTimeField存储时间
    created_time = models.DateTimeField(verbose_name='建立时间')
    modified_time = models.DateTimeField(verbose_name='最后修改时间')

    '''新增 views 字段记录阅读量：该类型值只能为0或正整数，初始化为0'''
    views = models.PositiveIntegerField(default=0, verbose_name='阅读量')

    '''规定一篇文章只能对应一个分类，但一个分类下可以有多篇文章，所以使用ForeignKey（一对多）的关联关系
    规定一篇文章可以有多个标签，一个标签下也可能有多篇文章，所以使用ManyToManyField（多对多）关联关系
    规定文章可以没有标签，因此为标签Tag指定blank=True'''
    category = models.ForeignKey(Category, verbose_name='分类')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')

    ''' User 从django.contrib.auth.models导入
    django.contrib.auth 是Django内置应用，专门处理网站用户的注册，登录等流程，User是其内置的用户模型
    通过ForeignKey一对多的将作者 User 和 Post 文章关联起来'''
    author = models.ForeignKey(User, verbose_name='作者')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """屏蔽域名，生成纯净的URL
        :return: reverse()
        参数1意为blog应用下的 name=detail 的函数
        由于 app_name = 'blog' 告诉了 Django urls.py 模块属于 blog 应用
        Django 能够顺利找到 blog 应用下 name 为 detail 的视图函数
        于是 reverse 函数会去解析这个视图函数对应的 URL
        这里 detail 对应的规则就是 post/(?P<pk>[0-9]+)/ 这个正则表达式
        而正则表达式部分会被后面传入的参数 pk 替换
        所以，如果 Post 的 id（或 pk，这里 pk 和 id 是等价的） 是 255 的话
        那么 get_absolute_url 函数返回的就是 /post/255/ ，这样 Post 就生成了自己的 URL
        """
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        """ increase_views 方法首先将自身对应的 views 字段值 +1
        然后将变化更新到数据库，使用 update_fields 参数指定只更新 views字段来提高效率"""
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        """如果没有填写文章摘要则自动生成，调用此方法前写的文章不生效"""
        if not self.excerpt:
            # 将 body 中的 Markdown 文本转为 HTML 文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 去掉 HTML 文本里的 HTML 标签，取前26个字符作为摘要
            self.excerpt = strip_tags(md.convert(self.body))[:2]
        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)

    class Meta:
        """ Django 允许在models.Model的子类里定义一个Meta内部类
        这个内部类通过指定一些属性来规定这个类该有的一些特性，例如 Post 的排序方式
        """
        ''' ordering 属性用来指定文章排序方式
        ['-created_time'] 指定按照文章发布时间排序，且负号表示逆序排列
        列表中可以用多个项：比如 ordering = ['-created_time', 'title']：
            那么首先依据 created_time 排序，如果 created_time 相同，则再依据 title 排序
            这样指定以后所有返回的文章列表都会自动按照 Meta 中指定的顺序排序'''
        verbose_name = "文章"
        verbose_name_plural = "文章"
        ordering = ['-created_time', 'title']
