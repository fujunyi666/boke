from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseNotFound


def index(request):
    return render(request, 'index/index.html')


@login_required(login_url='/users/login1.html')
def topics(request):
    '''显示所有的主题'''
    # 查询数据库--请求提供Topic对象，并按属性date_add对他们进行排序
    # 让Django只从数据库中获取owner属性作为当前用户的Topic对象
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'index/topics.html', context)


@login_required(login_url='/users/login1.html')
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    # 按照date_added进行排序
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'index/topic.html', context)


@login_required(login_url='/users/login1.html')
def new_topic(request):
    if request.method != 'POST':

        form = TopicForm()
    else:

        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('index:topics'))
    context = {'form': form}
    return render(request, 'index/new_topic.html', context)


@login_required(login_url='/users/login1.html')
def new_entry(request, topic_id):
    '''在特定主题中添加新条目'''
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':

        form = EntryForm()

    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # 让Django创建一个新的条目对象，并将其存储在new_entry中，False是不将其保存到数据库中
            new_entry = form.save(commit=False)
            # 我们将new_entry的属性topic设置成在这个函数开头从数据库中获取的主题
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('index:topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'index/new_entry.html', context)


@login_required(login_url='/users/login1.html')
def edit_entry(request, entry_id):
    '''编辑既有条目'''
    # 获取用户要修改的条目对象，以及与该条目相关联的主题
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    # instance = entry表示用既有条目中的信息去填充它
    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单

        form = EntryForm(instance=entry)
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index:topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'index/edit_entry.html', context)


@login_required(login_url='/users/login1.html')
def del_topic(request, topic_id):
    try:
        topic = Topic.objects.get(id=topic_id)
        # 删除该记录
        topic.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url='/users/login1.html')
def del_entry(request, entry_id):
    try:
        entry = Topic.objects.get(id=entry_id)
        # 删除该记录
        entry.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url='/users/login1.html')
def edit_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = TopicForm(instance=topic)

    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index:topics'))

    context = {'topic': topic, 'form': form}
    return render(request, 'index/edit_topic.html', context)
