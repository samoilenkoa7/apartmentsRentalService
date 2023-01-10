from rest_framework import serializers
from booking.models import Apartment, ApartmentPicture, ApartmentAvailableTime, UserReservation


class ApartmentPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentPicture
        fields = '__all__'


class AvailableTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentAvailableTime
        fields = "__all__"


class ApartmentListViewSerializer(serializers.ModelSerializer):
    """Was created to solve the problem with list-view"""
    acc_pictures = ApartmentPictureSerializer(many=True)
    available_time = AvailableTimeSerializer(many=True)

    class Meta:
        model = Apartment
        fields = ('pk', 'title', 'description', 'location', 'price',
                  'date', 'views', 'user', 'acc_pictures', 'available_time')


class ApartmentSerializer(serializers.ModelSerializer):
    """Apartment model serializer with relational tables"""
    def __init__(self, *args, **kwargs):
        """Init additional fields if it exists while creating new post"""
        self.Meta.fields = list(self.Meta.fields)
        data = kwargs.get('data', None)

        if data is not None:
            if data.get('available_time', None):
                ApartmentSerializer.available_time = AvailableTimeSerializer(many=True)
                self.Meta.fields.append('available_time')

            if data.get('acc_pictures', None):
                ApartmentSerializer.acc_pictures = ApartmentPictureSerializer(many=True)
                self.Meta.fields.append('acc_pictures')

        if args and args[0].available_time:
            ApartmentSerializer.available_time = AvailableTimeSerializer(many=True)
            self.Meta.fields.append('available_time')

        if args and args[0].acc_pictures:
            ApartmentSerializer.acc_pictures = ApartmentPictureSerializer(many=True)
            self.Meta.fields.append('acc_pictures')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Apartment
        fields = ('pk', 'title', 'description', 'location', 'price',
                  'date', 'views', 'user')


class ReservationTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReservation
        fields = ('id', 'user', 'apartment', 'time')
