from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, View, FormView, DetailView, ListView

from blog.models import User, ActivationCode, Post, Category
from blog.forms import SignUpForm, RepeatEmailForm, PostForm


class IndexView(ListView):
    queryset = Post.objects.all().select_related('author').order_by('-created')
    context_object_name = 'posts'
    template_name = 'index.html'
    paginate_by = 5
    model = Post

    # def get_context_data(self, **kwargs):
    #     context = super(IndexView, self).get_context_data(**kwargs)
    #     context['authors_name'] = User.objects.filter(author_status=True)
    #     return context


class SignUpView(CreateView):
    template_name = 'signup.html'
    queryset = User.objects.all()
    success_url = reverse_lazy('activation_code_sent')
    form_class = SignUpForm


class Activate(View):
    def get(self, request, activation_code):
        ac = get_object_or_404(
            ActivationCode.objects.select_related('user'),
            code=activation_code, is_activated=False,
        )

        if ac.is_expired:
            raise Http404

        ac.is_activated = True
        ac.save(update_fields=['is_activated'])

        user = ac.user
        user.is_active = True
        user.save(update_fields=['is_active'])
        return redirect('index')


class RepeatEmailView(FormView):
    template_name = 'repeat_email.html'
    success_url = reverse_lazy('activation_code_sent')
    form_class = RepeatEmailForm
    fields = ('email',)


class MyProfile(UpdateView):
    template_name = 'my_profile.html'
    queryset = User.objects.filter(is_active=True)
    fields = ('email', 'first_name', 'last_name', 'avatar')
    success_url = reverse_lazy('index')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(id=self.request.user.id)


class PostView(DetailView):
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all().select_related('author')


class AuthorSearchView(ListView):
    context_object_name = 'posts'
    template_name = 'author_search.html'
    paginate_by = 5
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.kwargs['pk'])


class CategorySearchView(ListView):
    context_object_name = 'posts'
    template_name = 'category_search.html'
    paginate_by = 5
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(category=self.kwargs['pk'])
