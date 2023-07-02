import time

from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from ratelimit.decorators import ratelimit

from app.forms import CommitForm
from app.models import Link
from helpers import get_page_list


class IndexView(generic.TemplateView):
    template_name = 'app/index.html'

class SearchView(generic.ListView):
    model = Link
    template_name = 'app/search.html'
    context_object_name = 'link_list'
    paginate_by = 10
    q = ''       # 搜索词
    duration = 0 # 耗时
    record_count = 0

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator, page)
        context['page_list'] = page_list
        context['q'] = self.q
        context['duration'] = round(self.duration,6)
        context['record_count'] = self.record_count
        return context

    def get_queryset(self):
        start = time.time()
        self.q = self.request.GET.get("q", "")
        search_list = Link.objects.get_search_list(self.q)
        # 如搜索为空，则放假数据
        if len(search_list) <= 0:
            search_list = Link.objects.get_fake_list()
        end = time.time()
        self.duration = end - start
        self.record_count = len(search_list)
        return search_list

class DetailView(generic.DetailView):
    model = Link
    template_name = 'app/detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.increase_hot_count()
        return obj

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        recommend_list = Link.objects.get_recommend_list()
        context['recommend_list'] = recommend_list
        return context

class CommitView(generic.CreateView):

    model = Link
    form_class = CommitForm
    template_name = 'app/commit.html'

    # @ratelimit(key='ip', rate='2/m')
    def post(self, request, *args, **kwargs):
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            messages.warning(self.request, "操作太频繁了，请1分钟后再试")
            return render(request, 'app/commit.html', {'form': CommitForm()})
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "提交成功! 等待管理员审核。")
        return reverse('app:commit')

class DemoView(generic.TemplateView):
    template_name = 'app/demo.html'