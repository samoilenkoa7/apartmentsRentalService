from django.contrib import admin
from .models import Apartment, ApartmentPicture, ApartmentAvailableTime, UserReservation


admin.site.register(Apartment)
admin.site.register(ApartmentPicture)
admin.site.register(ApartmentAvailableTime)
admin.site.register(UserReservation)
