from django.urls import path
from blog.views import (SignUpView, Activate, RepeatEmailView, MyProfile, PostView,
                        AuthorSearchView, CategorySearchView, CreatePostView, PostChangeView,
                        NameSearchView, TagListViews)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('repeat/', RepeatEmailView.as_view(), name='repeat_email'),
    path('create/', CreatePostView.as_view(), name='create_post'),
    path('post/<slug:slug>', PostView.as_view(), name='post_view'),
    path('profile/<int:pk>', MyProfile.as_view(), name='profile'),
    path('postchange/<int:pk>', PostChangeView.as_view(), name='post_change'),
    path('authorsearch/<int:pk>', AuthorSearchView.as_view(), name='author_search'),
    path('postswithtag/<slug:slug>', TagListViews.as_view(), name='tag_search'),
    path('namesearch/', NameSearchView.as_view(), name='name_search'),
    path('categorysearch/<slug:slug>', CategorySearchView.as_view(), name='category_search'),
    path('activate/<uuid:activation_code>/', Activate.as_view(), name='activate'),
]
