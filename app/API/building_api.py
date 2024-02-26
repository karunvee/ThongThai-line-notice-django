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
def get_building_list(request):
    try:
        buildingList = Building.objects.all()
        serializer = BuildingSerializer(instance=buildingList, many=True)
        return Response({"detail": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_building(request):
    try:
        building_name = request.data.get('building_name')
        building = Building.objects.create(
            building_name = building_name,
        )
        serializer = BuildingSerializer(instance=building)
        return Response({"detail": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_building(request):
    try:
        query_data = BuildingQuerySerializer(data = request.query_params)

        if query_data.is_valid():
            pk = query_data.validated_data.get('building_id')
            Building.objects.filter(pk = pk).delete()
            return Response({"detail": f"{pk} was deleted"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Data format is invalid"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_building(request):
    try:
        building_id = request.data.get('building_id')
        new_name = request.data.get('new_name')

        Building.objects.filter(pk = building_id).update(building_name = new_name)
        return Response({"detail": f"{building_id} was updated"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)