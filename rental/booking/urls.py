from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.create_new_post_view, name='create'),
    path('account/', views.account_view, name='account'),
    path('<int:pk>/', views.single_post_view, name='single-article'),
    path('', views.PostsMainListView.as_view(), name='all-posts'),
    path('delete/<int:pk>/', views.delete_post_from_account_view, name='delete-post'),
    path('reserver/<int:pk>/', views.create_reservation_view, name='reserve'),
    path('add-time/<int:pk>/', views.add_new_time_for_reservation_view, name='add-time')
]
