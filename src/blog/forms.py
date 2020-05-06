from django.forms import ModelForm
from blog.models import User, Post
from django import forms
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404


class SignUpForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['password'] != cleaned_data['password2']:
                raise forms.ValidationError('Password do not match! ')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        user.save()

        activation_code = user.activation_codes.create()
        activation_code.send_activation_code()
        return user


class RepeatEmailForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email',)

    def clean(self):
        cleaned_data = super().clean()
        user = get_object_or_404(User, email=cleaned_data['email'])
        act = user.activation_codes.all().last()

        if act.is_activated:
            raise Http404
        else:
            act.send_activation_code()
        return cleaned_data


class AdminPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'author', 'picture')


class PostForm(ModelForm):
    class Meta:
        Model = Post
        fields = ('title', 'text', 'author', 'picture')


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'author', 'category', 'picture')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.fields['author'].queryset = User.objects.filter(author_status=True)
