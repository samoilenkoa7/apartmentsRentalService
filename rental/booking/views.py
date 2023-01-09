from django.contrib import messages
from django.views import generic
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.utils.functional import SimpleLazyObject
from django.views.decorators.http import require_POST, require_http_methods
from django.db.models import F, QuerySet

from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

from .models import Apartment, ApartmentPicture
from .forms import CreateNewPostForm, PostPictureForm, ReservationCreateForm, NewReservationTimeForm
from .services import get_initial_values_and_reservation_form, get_request_data_and_save_reservation, \
    delete_post_if_user_is_correct, initialize_form_for_pictures, create_new_apartments_post_and_save_to_db, \
    connect_with_apartment_and_save_to_db

import logging


logger = logging.getLogger(__name__)


@require_POST
def create_new_post_view(request):
    if request.method == 'POST':
        form = CreateNewPostForm(request.POST)
        form_pics = initialize_form_for_pictures(request)
        if form.is_valid() and form_pics.is_valid():
            create_new_apartments_post_and_save_to_db(form, form_pics, request)
        else:
            logger.warning(f'"{form.errors}" occurred while creating new post')
            messages.error(request, "Provided data is not valid")
        return redirect('account')


def single_post_view(request, pk):
    post = ApartmentPicture.objects.select_related('pictures').get(pictures__pk=pk)
    views = post.pictures.views
    post.pictures.views = F('views') + 1
    create_new_post_form = ReservationCreateForm(apartment=Apartment.objects.get(pk=pk))
    context = {
        'post': post,
        'views': views,
        'form': create_new_post_form,
    }
    if request.user == post.pictures.user:
        create_new_available_time_form = NewReservationTimeForm()
        context['time_creation_form'] = create_new_available_time_form
    return render(request, template_name='booking/single-article.html', context=context)


@require_http_methods(["GET"])
@login_required()
def delete_post_from_account_view(request, pk):
    try:
        delete_post_if_user_is_correct(request, pk)
    finally:
        return redirect('account')


@login_required(login_url='login')
def account_view(request):
    form = CreateNewPostForm
    form_pics = PostPictureForm
    username = request.user.username
    posts = ApartmentPicture.objects.select_related('pictures').filter(pictures__user=request.user)
    posts = posts if len(posts) > 0 else 'You don\'t have posts yet'
    context = {
        'form': form,
        'form_pics': form_pics,
        'username': username,
        'posts': posts,
        'site': SimpleLazyObject(lambda: get_current_site(request)),
        'top_post_by_view': 'You don\'t have posts yet'
    }
    if isinstance(posts, QuerySet):
        top_post_by_view = posts.order_by('-pictures__views')[0]
        context['top_post_by_view'] = top_post_by_view
    return render(request, template_name='booking/account.html', context=context)


class PostsMainListView(generic.ListView):
    template_name = 'booking/list-view.html'
    context_object_name = 'posts'
    queryset = ApartmentPicture.objects.all().select_related('pictures')


@require_POST
@login_required()
def add_new_time_for_reservation_view(request, pk):
    form = NewReservationTimeForm(data=request.POST)
    if form.is_valid():
        connect_with_apartment_and_save_to_db(request, form, pk)
    else:
        logger.warning(f'"{form.errors}" occurred while creating new available time')
        messages.error(request, 'Some error occurred during adding time, please - try again later')
    utl_to_redirect = reverse_lazy('single-article', kwargs={'pk': pk})
    return redirect(utl_to_redirect)


@require_POST
@login_required()
def create_reservation_view(request, pk):
    if request.method == "POST":
        form = get_initial_values_and_reservation_form(request, pk)
        if form.is_valid():
            get_request_data_and_save_reservation(form, request, pk)
            messages.success(request, f'You have successfully booked this apartment for name {request.user.username}')
        else:
            logger.warning(f'{form.errors} occurred while reservation')
            messages.error(request, 'Not valid date... Try again later')
    url_to_redirect = reverse_lazy('single-article', kwargs={'pk': pk})
    return redirect(url_to_redirect)
