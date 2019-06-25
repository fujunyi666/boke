from django.contrib import admin
from index.models import Topic,Entry
#让Django通过管理网站管理我们的模型

admin.site.site_title='MyDjango 后台管理'
admin.site.site_header='MyDjango'
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['id','text','date_added','owner',]
    search_fields = ['id','text','date_added']
    ordering = ['id']


admin.site.register(Entry)
