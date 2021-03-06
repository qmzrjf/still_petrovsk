from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, CreateView, View, FormView, DetailView, ListView, DeleteView

from blog.models import User, ActivationCode, Post, Category, Tag, Comment
from blog.forms import SignUpForm, RepeatEmailForm, CreatePostForm, RequestCommentForm


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler403(request, exception):
    return render(request, '403.html', status=403)


def handler500(request):
    return render(request, '500.html', status=500)


class IndexView(ListView):
    queryset = Post.objects.all().select_related('author', 'category').order_by('-created')
    context_object_name = 'posts'
    template_name = 'index.html'
    paginate_by = 5
    model = Post


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
    queryset = Post.objects.all().select_related('author', 'category')

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        post = Post.objects.get(slug=self.kwargs['slug'])
        context['comments'] = Comment.objects.filter(post=post.id)
        return context


class AuthorSearchView(ListView):
    context_object_name = 'posts'
    template_name = 'author_search.html'
    paginate_by = 5
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.kwargs['pk']).select_related('author', 'category')


class CategorySearchView(ListView):
    context_object_name = 'posts'
    template_name = 'category_search.html'
    paginate_by = 5
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset()
        category = Category.objects.get(slug=self.kwargs['slug'])
        return queryset.filter(category=category.id).select_related('author', 'category')


class CreatePostView(UserPassesTestMixin, CreateView):
    template_name = 'create_post.html'
    queryset = User.objects.all()
    model = User
    success_url = reverse_lazy('index')
    form_class = CreatePostForm

    def test_func(self):
        return self.request.user.author_status

    def get_form_kwargs(self):
        kwargs = super(CreatePostView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PostChangeView(UserPassesTestMixin, UpdateView):
    template_name = 'post_change.html'
    queryset = Post.objects.all()
    fields = ('title', 'text', 'category')
    success_url = reverse_lazy('index')

    def test_func(self):
        post = Post.objects.get(id=self.kwargs['pk'])
        author_id = post.author.id
        return self.request.user.id == author_id


class NameSearchView (ListView):
    context_object_name = 'posts'
    template_name = 'name_search.html'
    paginate_by = 5
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        result_search = queryset.filter(title__icontains=search_query).select_related('author', 'category')
        if result_search:
            return result_search
        else:
            raise Http404


class TagListViews(ListView):
    context_object_name = 'posts'
    template_name = 'tag_list.html'
    paginate_by = 5
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset()
        tag = Tag.objects.get(slug=self.kwargs['slug'])
        return queryset.filter(tags=tag.id).select_related('author', 'category')

    def get_context_data(self, **kwargs):
        context = super(TagListViews, self).get_context_data(**kwargs)
        context['current_tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context


@login_required(login_url='login')
def comment_create_view(request, slug):

    post = get_object_or_404(Post, slug=slug)
    author = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        comment_form = RequestCommentForm(request.POST)

        if comment_form.is_valid():
            print('asdasd'*100)
            text = comment_form.cleaned_data['text']
            Comment.objects.create(post=post, author=author, text=text)
    else:
        comment_form = RequestCommentForm()

    return redirect('post_view', slug=slug)


class CommentDeleteView(UserPassesTestMixin, DeleteView):

    '''Костыль'''

    success_url = reverse_lazy('index')
    model = Comment


    def test_func(self):
        comment = Comment.objects.get(uuid_value=self.kwargs['pk'])
        author_id = comment.author.id
        return self.request.user.id == author_id
