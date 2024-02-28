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
def get_floor_list(request):
    try:
        query_data = BuildingQuerySerializer(data = request.query_params)

        if query_data.is_valid():
            floorList = FloorNumber.objects.filter(buildingInfo__pk = query_data.validated_data.get('building_id'))
            serializer = FloorNumberSerializer(instance=floorList, many=True)
            return Response({"detail": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Data format is invalid"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_floor(request):
    try:
        building_id = request.data.get('building_id')
        floor_name = request.data.get('floor_name')
        floor = FloorNumber.objects.create(
            buildingInfo = Building.objects.get(pk = building_id),
            floor_name = floor_name,
        )
        serializer = FloorNumberSerializer(instance=floor)
        return Response({"detail": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_floor(request):
    try:
        query_data = FloorQuerySerializer(data = request.query_params)

        if query_data.is_valid():
            pk = query_data.validated_data.get('floor_id')
            FloorNumber.objects.filter(pk = pk).delete()
            return Response({"detail": f"{pk} was deleted"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Data format is invalid"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_floor(request):
    try:
        floor_id = request.data.get('floor_id')
        floor_name = request.data.get('floor_name')
        building_id = request.data.get('building_id')

        FloorNumber.objects.filter(pk = floor_id).update(floor_name = floor_name, buildingInfo = Building.objects.get(pk = building_id))
        return Response({"detail": f"{floor_id} was updated"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)