from django import forms
from django.db.models import Q

from .models import ApartmentAvailableTime, UserReservation


class CreateNewPostForm(forms.Form):
    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'postCreation'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'postCreation'
    }))
    price = forms.DecimalField(max_digits=5, widget=forms.NumberInput(attrs={
        'class': 'postCreation'
    }))
    location = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'postCreation'
    }))


class PostPictureForm(forms.Form):
    image_to_apartment = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'postCreation'
    }))


class NewReservationTimeForm(forms.ModelForm):
    time = forms.DateTimeField(label='Available time', widget=forms.TextInput(attrs={
        'type': 'datetime-local'
    }))

    class Meta:
        model = ApartmentAvailableTime
        fields = ('time', )


class ReservationCreateForm(forms.ModelForm):
    def __init__(self, apartment, *args, **kwargs):
        super(ReservationCreateForm, self).__init__(*args, **kwargs)
        self.fields['time'] = forms.ModelChoiceField(
            queryset=ApartmentAvailableTime.objects.filter(Q(apartment=apartment))
            .exclude(pk__in=UserReservation.objects.filter(apartment=apartment).values('time'))
        )

    class Meta:
        model = UserReservation
        fields = ('time',)
