from django.urls import path
from blog.views import SignUpView, Activate, RepeatEmailView, MyProfile, PostView, AuthorSearchView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('repeat/', RepeatEmailView.as_view(), name='repeat_email'),
    path('post/<int:pk>', PostView.as_view(), name='post_view'),
    path('profile/<int:pk>', MyProfile.as_view(), name='profile'),
    path('authorsearch/<int:pk>', AuthorSearchView.as_view(), name='author_search'),
    path('activate/<uuid:activation_code>/', Activate.as_view(), name='activate'),
]
