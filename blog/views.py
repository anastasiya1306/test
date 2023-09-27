from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, TemplateView

from blog.forms import BlogForm
from blog.models import Blog
from main.models import Subscription


class IndexView(TemplateView):
    extra_context = {
        'title': 'Главная страница'
    }
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['blog_list'] = Blog.objects.filter(is_publication=True).order_by('?')[:3]
        return context_data


class BlogListView(ListView):
    model = Blog
    extra_context = {
        'title': 'Статьи'
    }
    template_name = 'blog_list.html'

    def get_queryset(self):

        user = self.request.user
        subscription_blogs_id = Subscription.objects.filter(user=user, status=True).values_list('blog__id', flat=True)
        unsubscription_blogs = Blog.objects.filter(is_publication=True).exclude(id__in=subscription_blogs_id).exclude(user=user)

        return unsubscription_blogs


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
        return super().form_valid(form)


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = context_data['object']
        return context_data

    def get_object(self, **kwargs):
        views = super().get_object(**kwargs)
        views.count_views += 1
        views.save()
        return views


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')

    def get_success_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.object.slug})


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
