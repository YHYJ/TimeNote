from haystack import indexes

from .models import Post

# 指定 django haystack 使用哪些数据建立索引以及如何存放索引
"""django haystack 规定，要相对某个 app 下的数据进行全文检索
就要在该 app 下创建一个 search_indexes.py 文件
然后创建一个 XXIndex 类（XX 为含有被检索数据的模型，如这里的 Post）
并且继承 SearchIndex 和 Indexable"""


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    """
        每个索引里面有且只有一个字段为 document=True
    这代表 django haystack 和搜索引擎将使用此字段的内容作为索引进行检索(primary field)
    如果使用一个字段设置了document=True，则一般约定此字段名为text
    这是在 SearchIndex 类里面一贯的命名，以防止后台混乱
        haystack 在 text 字段中提供了use_template=True
    这样就允许使用数据模板去建立搜索引擎索引的文件，就是说索引里面需要存放一些什么东西
    例如 Post 的 title 字段，这样就可以通过 title 内容来检索 Post 数据了
        数据模板的路径为 templates/search/indexes/youapp/\<model_name>_text.txt
    """
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
