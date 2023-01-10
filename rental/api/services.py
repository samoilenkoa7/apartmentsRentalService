from django.db.models import F
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from booking.models import ApartmentAvailableTime, UserReservation


def get_user_from_auth_token(auth_token):
    user = Token.objects.get(key=auth_token).user
    if user:
        return user
    raise Token.DoesNotExist


def get_auth_token_from_header(request):
    auth_token = request.headers.get('Authorization', None)
    return auth_token


def _get_user_id_from_headers(request):
    auth_token = get_auth_token_from_header(request)
    user = get_user_from_auth_token(auth_token)
    return user


def get_token_validate_and_add_to_post_data(request) -> dict:
    auth_token = get_auth_token_from_header(request)
    if auth_token is not None:
        new_post = request.data.copy()
        user = get_user_from_auth_token(auth_token)
        user_id = user.id
        new_post['user'] = user_id
    else:
        raise ValidationError
    return new_post


def increase_views_counter(post):
    post = post.first()
    post.views = F('views') + 1
    post.save()


def validate_connection_of_available_time_to_post(reservation_instance_time_id, post_id):
    return {'id': int(reservation_instance_time_id)} in ApartmentAvailableTime.objects\
        .filter(apartment=post_id).values('id')\
        .exclude(pk__in=UserReservation.objects.filter(apartment=post_id).values('time'))


def check_user_permissions_for_object(request, model_item):
    user = _get_user_id_from_headers(request)
    if user.is_superuser or user.is_staff:
        return True
    return user == model_item.user

