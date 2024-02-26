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
def get_location_list(request):
    try:
        query_data = FloorQuerySerializer(data = request.query_params)

        if query_data.is_valid():
            locationList = Location.objects.filter(floorNumber__pk = query_data.validated_data.get('floor_id'))
            serializer = LocationSerializer(instance=locationList, many=True)
            return Response({"detail": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Data format is invalid"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_location(request):
    try:
        floor_id = request.data.get('floor_id')
        location_name = request.data.get('location_name')
        location = Location.objects.create(
            floorNumber = FloorNumber.objects.get(pk = floor_id),
            location_name = location_name,
        )
        serializer = LocationSerializer(instance=location)
        return Response({"detail": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_location(request):
    try:
        query_data = LocationQuerySerializer(data = request.query_params)

        if query_data.is_valid():
            pk = query_data.validated_data.get('location_id')
            Location.objects.filter(pk = pk).delete()
            return Response({"detail": f"{pk} was deleted"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Data format is invalid"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_location(request):
    try:
        location_id = request.data.get('location_id')
        new_name = request.data.get('new_name')
        floor_id = request.data.get('floor_id')

        Location.objects.filter(pk = location_id).update(location_name = new_name, floorNumber = FloorNumber.objects.get(pk = floor_id))
        return Response({"detail": f"{location_id} was updated"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)