from django import forms
from .models import Comment

# form  ——评论表单


class CommentForm(forms.ModelForm):
    """Django 的表单类必须继承自 forms.Form 或者 forms.ModelForm 类
    如果表单对应有一个数据库模型（这里评论表单对应评论模型），那么使用 ModelForm 类会简单很多
    最简单的ModelForm版本只有一个内嵌的Meta类
    Meta类指示Django根据哪个模型创建表单以及表单中包含的字段
    model = Comment 根据模型Comment创建一个表单
    fields 指定该表单中显示的字段
    """
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']
