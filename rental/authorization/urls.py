from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='registration'),
    path('login/', views.login_user_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
