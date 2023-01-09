from django.contrib import messages

from .forms import ReservationCreateForm, PostPictureForm, CreateNewPostForm, NewReservationTimeForm
from .models import Apartment, ApartmentPicture


def get_initial_values_and_reservation_form(request, pk: int) -> ReservationCreateForm:
    """Getting initial value for form and initialize it"""
    new_request_post = dict(request.POST)
    new_request_post['time'] = int(new_request_post['time'][0])
    form = ReservationCreateForm(data=new_request_post, apartment=Apartment.objects.get(pk=pk))
    return form


def get_request_data_and_save_reservation(form: ReservationCreateForm, request, pk: int):
    """Set user and apartment field to form instance and saving it"""
    new_reservation = form.save(commit=False)
    new_reservation.user = request.user
    new_reservation.apartment = Apartment.objects.get(pk=pk)
    new_reservation.save()


def delete_post_if_user_is_correct(request, pk: int) -> None:
    """Getting post that should be deleted and if user allows - do that"""
    post_to_delete = Apartment.objects.get(pk=pk)
    if request.user == post_to_delete.user:
        post_to_delete.delete()
    else:
        messages.error(request, "You are not authorized to delete this post!")


def initialize_form_for_pictures(request):
    """Initializes form to add pictures to the form """
    return PostPictureForm(
        data={
            key: value for key, value in request.POST.items()
            if key in ('csrfmiddlewaretoken', 'image_to_apartment')},
        files=request.FILES)


def create_new_apartments_post_and_save_to_db(form: CreateNewPostForm, form_pics: PostPictureForm, request):
    """Create new Apartment instance and saves it to db"""
    new_post = Apartment.objects.create(**form.cleaned_data, **{'user': request.user})
    new_post.save()
    new_post_picture = ApartmentPicture.objects.create(**form_pics.cleaned_data, **{'pictures': new_post})
    new_post_picture.save()


def connect_with_apartment_and_save_to_db(request, form: NewReservationTimeForm, pk: int):
    new_time = form.save(commit=False)
    new_time.apartment = Apartment.objects.get(pk=pk)
    new_time.save()
    messages.success(request, 'Time successfully added!')
