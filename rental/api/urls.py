from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter


router_posts = DefaultRouter()
router_posts.register(r'posts', views.ApartmentModelAPIView, basename='post')

router_reservation_time = DefaultRouter()
router_reservation_time.register(r'reservation', views.ReservationTimeAPIModelViewSet, basename='reservation')

urlpatterns = [
    path('', include(router_posts.urls)),
    path('', include(router_reservation_time.urls)),
    path('time/list/', views.AvailableTimeCreateAPIView.as_view()),
    path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
