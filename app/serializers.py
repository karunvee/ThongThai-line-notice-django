from rest_framework import serializers
from .models import *

class LineNotifySerializer(serializers.ModelSerializer):
    buildingInfo = serializers.StringRelatedField()
    class Meta(object):
        model = LineNotify
        fields = '__all__'

class BuildingSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Building
        fields = '__all__'

class FloorNumberSerializer(serializers.ModelSerializer):
    buildingInfo = serializers.StringRelatedField()
    class Meta(object):
        model = FloorNumber
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    floorNumber = serializers.StringRelatedField()
    class Meta(object):
        model = Location
        fields = '__all__'

class StandardMessageSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = StandardMessage
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Message
        fields = '__all__'

class SubMessageSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = SubMessage
        fields = ['id', 'detail']

class MessageWithSubSerializer(serializers.ModelSerializer):
    location = serializers.StringRelatedField()
    sub_message  = SubMessageSerializer(many=True, read_only=True)
    class Meta(object):
        model = Message
        fields = ['id', 'location', 'topic', 'description', 'sub_message']

class ContentSlideSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ContentSlide
        fields = '__all__'

class ActivityRecordSerializer(serializers.ModelSerializer):
    message = serializers.CharField()
    class Meta(object):
        model = ActivityRecord
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

class SubMessageQuerySerializer(serializers.Serializer):
    sub_message_id = serializers.CharField()