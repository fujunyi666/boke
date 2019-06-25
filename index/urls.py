from django.conf.urls import url
from . import views
app_name = 'index'
urlpatterns=[
    # 主页
    url(r'^$',views.index,name='index'),
    #显示所有主题
    url(r'^topics/$',views.topics,name='topics'),
    #特定主题的页面
    # /(?P<topic_id>\d+)/ )与包含在两个斜杠内的整数匹配，并将这个整数存储在一个名为topic_id时掺中。
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    # 用于添加新主题的网页
    url(r'^new_topic/$', views.new_topic, name='new_topic'),
    # 用于添加新条目的页面
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
    # 用于编辑条目的页面
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
    url(r'^del_topic/$',views.del_topic,name='del_topic'),
    url(r'^del_entry/$',views.del_entry,name='del_entry'),
    url(r'^edit_topic/(?P<topic_id>\d+)/$', views.edit_topic, name='edit_topic'),
]