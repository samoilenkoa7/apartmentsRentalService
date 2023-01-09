from django.db import models
from django.urls import reverse_lazy

from django.contrib.auth import get_user_model

User = get_user_model()


class Apartment(models.Model):
    title = models.CharField('Item title', max_length=255)
    description = models.TextField('Item description')
    location = models.CharField('Location of Apartment', max_length=150)
    date = models.DateTimeField('Date added', auto_now_add=True)
    price = models.DecimalField('Price', decimal_places=2, max_digits=5)
    views = models.IntegerField('Post views count', default=0)
    user = models.ForeignKey(verbose_name='User', to=User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Apartment'
        verbose_name_plural = 'Apartments'
        ordering = ('-date', 'price')

    def get_booking_url(self):
        return reverse_lazy('reserve', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse_lazy('single-article', kwargs={'pk': self.pk})

    def delete_post(self):
        self.delete()

    def __str__(self):
        return f'Apartment with id: {self.pk} \n Title -{self.title}'


class ApartmentPicture(models.Model):
    image_to_apartment = models.ImageField('Image for post', upload_to='apps-pictures/%Y/%m/%d')
    pictures = models.ForeignKey(
        verbose_name='Pictures',
        to=Apartment,
        on_delete=models.CASCADE,
        related_name='acc_pictures'
    )

    def __str__(self):
        return self.image_to_apartment.url


class ApartmentAvailableTime(models.Model):
    time = models.DateTimeField('Available time')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Available time for {self.apartment.title} \n Time: {self.time}'


class UserReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    time = models.OneToOneField(ApartmentAvailableTime, on_delete=models.CASCADE)

    def __str__(self):
        return f'Reservation on user: {self.user} \n Time: {self.time.time} \n Apartment: {self.apartment.title}'
