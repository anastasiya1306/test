from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView, IndexView

app_name = BlogConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('blogs/', BlogListView.as_view(), name='blog_list'),
    path('blog_detail/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/update/<int:pk>', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/delete/<int:pk>', BlogDeleteView.as_view(), name='blog_delete'),
]
