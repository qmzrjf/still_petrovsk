from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, View, FormView, DetailView

from blog.models import User, ActivationCode, Post
from blog.forms import SignUpForm, RepeatEmailForm, PostForm


class SignUpView(CreateView):
    template_name = 'signup.html'
    queryset = User.objects.all()
    # fields = ('email', 'first_name', 'last_name', 'avatar',)
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
