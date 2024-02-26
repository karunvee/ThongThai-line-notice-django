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
def get_content_list(request):
    try:
        contents = ContentSlide.objects.all()
        serializer = ContentSlideSerializer(instance=contents, many=True)
        return Response({"detail": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_content(request):
    try:
        content_name = request.data.get('content')
        image = request.data.get('image')
        content = ContentSlide.objects.create(
            content = content_name,
            image = image
        )
        serializer = ContentSlideSerializer(instance=content)
        return Response({"detail": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_content(request):
    try:
        content_id = request.data.get('content_id')
        new_content = request.data.get('new_content')
        image = request.data.get('image')

        content_obj = ContentSlide.objects.filter(pk = content_id).first()
        content_obj.content = new_content
        if image:
            content_obj.image = image
        print(content_obj)
        content_obj.save()
        return Response({"detail": f"{content_id} was updated"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_content(request):
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
    