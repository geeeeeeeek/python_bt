from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('search', views.SearchView.as_view(), name='search'),
    path('detail/<int:pk>', views.DetailView.as_view(), name='detail'),
    path('commit', views.CommitView.as_view(), name='commit'),
    path('demo', views.DemoView.as_view(), name='demo'),
]