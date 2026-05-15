from django.urls import path
from .views import RegisterView, LoginView, UserProfilView

urlpatterns=[
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/',UserProfilView.as_view(), name='profile'),
]