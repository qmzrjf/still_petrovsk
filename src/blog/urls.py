from django.urls import path
from blog.views import SignUpView, Activate

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('activate/<uuid:activation_code>/', Activate.as_view(), name='activate'),
]
