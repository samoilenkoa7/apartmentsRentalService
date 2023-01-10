from .services import _get_user_id_from_headers


def check_object_permission(request, model_item):
    user = _get_user_id_from_headers(request)
    if user.is_staff or user.is_superuser:
        return True
    return user == model_item.user
