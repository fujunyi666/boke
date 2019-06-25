from django.db import models
from django.contrib.auth.models import User
'''用户学习的主题'''
class Topic(models.Model):
    ''' 告诉 Django需要预留多大的空间'''
    id=models.AutoField('序号',primary_key=True)
    text=models.CharField('话题',max_length=200)
    '''记录日期和时间的数据。当用户创建新主题是，都会让Django将这个属性自动设置成当前的日期和时间'''
    date_added=models.DateTimeField('日期',auto_now_add=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户')

    class Meta:
        verbose_name_plural='话题'

    def __str__(self):
       '''返回模型的字符串表'''
       return self.text

class Entry(models.Model):
    '''学到的有关某个主题的具体知识'''
    '''外键'''
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)
    text=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)
    '''存储用于管理模型的额外信息'''
    class Meta:
        verbose_name_plural='笔记'

    def __str__(self):
        '''返回模型的字符串表示'''
        if len(self.text)>50:
          return self.text[:50]+"..."
        else :
            return self.text
