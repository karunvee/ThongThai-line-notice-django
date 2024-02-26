from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ..models import *
from ..serializers import *

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_message_list(request):
    try:
        messages = Message.objects.all()
        serializer = MessageSerializer(instance=messages, many=True)
        return Response({"detail": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_message(request):
    try:
        location = Location.objects.get(pk = request.data.get('location_id'))
        topic = request.data.get('topic')
        description = request.data.get('description')
        message = Message.objects.create(
            location = location,
            topic = topic,
            description = description
        )
        serializer = MessageSerializer(instance=message)
        return Response({"detail": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_message(request):
    try:
        query_data = MessageQuerySerializer(data = request.query_params)

        if query_data.is_valid():
            pk = query_data.validated_data.get('message_id')
            Message.objects.filter(pk = pk).delete()
            return Response({"detail": f"{pk} was deleted"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Data format is invalid"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_message(request):
    try:
        message_id = request.data.get('message_id')
        location_id = request.data.get('location_id')
        new_topic = request.data.get('topic')
        new_description = request.data.get('description')

        location = Location.objects.filter(pk = location_id)
        Message.objects.filter(pk = message_id).update(location = location, topic = new_topic, description = new_description)
        return Response({"detail": f"{message_id} was updated"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    