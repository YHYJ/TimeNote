from django.db import models

# Create your models here.  ——创建comments应用的数据表


class Comment(models.Model):
    """数据表：Comment（评论）
       数据列：name —— 评论者名
              email —— 邮箱
              url —— 个人网址
              text —— 评论内容
              created_time —— 评论时间    auto_now_add=True 参数自动填充当前时间
            post —— 将 Post（文章）数据表与 Comment（评论）数据表进行关联（一对多）
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]
