from rest_framework import serializers
from .models import *

class LineNotifySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = LineNotify
        fields = '__all__'

class BuildingSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Building
        fields = '__all__'

class FloorNumberSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = FloorNumber
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Location
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Message
        fields = '__all__'

class ContentSlideSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ContentSlide
        fields = '__all__'

class AcitivityRecordSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = AcitivityRecord
        fields = '__all__'

class LineConfigQuerySerializer(serializers.Serializer):
    config_id = serializers.CharField()

class BuildingQuerySerializer(serializers.Serializer):
    building_id = serializers.CharField()

class FloorQuerySerializer(serializers.Serializer):
    floor_id = serializers.CharField()

class LocationQuerySerializer(serializers.Serializer):
    location_id = serializers.CharField()

class MessageQuerySerializer(serializers.Serializer):
    message_id = serializers.CharField()