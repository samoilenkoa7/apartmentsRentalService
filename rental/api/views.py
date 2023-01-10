from django.db.models import Prefetch
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework import generics, status

from .permissions import check_object_permission
from .serializers import \
    ApartmentSerializer, AvailableTimeSerializer, ApartmentListViewSerializer, ReservationTimeSerializer

from booking.models import Apartment, ApartmentAvailableTime, UserReservation
from .services import get_token_validate_and_add_to_post_data, get_auth_token_from_header, get_user_from_auth_token, \
    increase_views_counter, validate_connection_of_available_time_to_post


class ApartmentModelAPIView(ModelViewSet):
    """Model view set for Apartment model"""
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer

    def list(self, request, *args, **kwargs):
        auth_token = get_auth_token_from_header(request)
        posts = Apartment.objects.all()\
            .prefetch_related('acc_pictures')\
            .prefetch_related(
            Prefetch('available_time', queryset=ApartmentAvailableTime.objects.all()
                     .exclude(pk__in=UserReservation.objects.all().values('time'))
                     )
        )
        if auth_token is not None:
            user = get_user_from_auth_token(auth_token)
            posts = posts.filter(user=user)
        posts_serialized = ApartmentListViewSerializer(posts, many=True)
        return Response(posts_serialized.data)

    def create(self, request, *args, **kwargs):
        new_post_data = get_token_validate_and_add_to_post_data(request)
        serialized_new_post = self.get_serializer(data=new_post_data)
        if serialized_new_post.is_valid(raise_exception=True):
            self.perform_create(serialized_new_post)
        return Response(serialized_new_post.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        post_to_delete = Apartment.objects.get(pk=pk)
        if check_object_permission(request, post_to_delete):
            post_to_delete.delete()
            return Response({f'Post {pk}': 'Deleted'})
        return PermissionError

    def retrieve(self, request, *args, **kwargs):
        pk = int(kwargs.get('pk', None))
        post = Apartment.objects.filter(pk=pk)
        full_post_data = post.prefetch_related(
            Prefetch('available_time',
                     queryset=ApartmentAvailableTime.objects.all()
                     .exclude(pk__in=UserReservation.objects.filter(apartment=post.first()).values('time'))
                     .only('time', 'id'))
        ).prefetch_related('acc_pictures').first()
        serialized_post = self.get_serializer(full_post_data)
        increase_views_counter(post)
        return Response(serialized_post.data)


class AvailableTimeCreateAPIView(generics.ListCreateAPIView):
    queryset = ApartmentAvailableTime.objects.all()
    serializer_class = AvailableTimeSerializer

    def create(self, request, *args, **kwargs):
        apartment = request.data.get('apartment', None)
        if apartment is not None:
            apartment_instance = Apartment.objects.get(pk=apartment)
            if check_object_permission(request, apartment_instance):
                return super().create(request, *args, **kwargs)
            raise PermissionError
        return ValidationError(detail='Field apartment is required', code=status.HTTP_400_BAD_REQUEST)


class ReservationTimeAPIModelViewSet(ModelViewSet):
    """Reservation model API view set"""
    queryset = UserReservation.objects.all()
    serializer_class = ReservationTimeSerializer

    def create(self, request, *args, **kwargs):
        new_reservation_data = get_token_validate_and_add_to_post_data(request)
        if validate_connection_of_available_time_to_post(
                new_reservation_data.get('time'), new_reservation_data.get('apartment')
        ):
            serialized_reservation_data = self.get_serializer(data=new_reservation_data)
            if serialized_reservation_data.is_valid():
                self.perform_create(serialized_reservation_data)
                return Response(serialized_reservation_data.data)
        else:
            return Response('This time is already booked', status=status.HTTP_409_CONFLICT)

    def destroy(self, request, *args, **kwargs):
        reservation_pk = kwargs.get('pk', None)
        reservation_instance = UserReservation.objects.get(pk=reservation_pk)
        if check_object_permission(request, reservation_instance):
            reservation_instance.delete()
            return Response({f'Post {reservation_pk}': 'Deleted'})
        return PermissionError
