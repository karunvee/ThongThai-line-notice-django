from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from .API.building_api import *
from .API.floor_api import *
from .API.location_api import *
from .API.content_api import *
from .API.message_api import *

from django.contrib.auth import authenticate

import pytz
from datetime import datetime
import requests

from linebot import LineBotApi
from linebot.models import FlexSendMessage
from linebot.exceptions import LineBotApiError

# Create your views here.
@api_view(['POST'])
def login_user(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        if(authenticate(username=username, password=password)):
            user = authenticate(username=username, password=password)
            token, create = Token.objects.get_or_create(user=user)
            return Response({"detail": "success", "token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Username or password is incorrect."}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({"detail": f"Failure, data as provided is incorrect. Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        token_key = request.headers.get('Authorization').split(' ')[1]
        print("token_key")
        print(token_key)

        if not token_key:
            return Response({"detail": "Token not provided (%s)" % token_key}, status=status.HTTP_400_BAD_REQUEST)
        token = get_object_or_404(Token, key=token_key)
        token.delete()
        return Response({"detail": "You were logged out."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_line_information(request):
    try:
        lineInfo = LineNotify.objects.all()
        serializer = LineNotifySerializer(instance=lineInfo, many=True)
        return Response({"detail": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_message(request):
    try:
        message_id = request.data.get('message_id')
        reporter = request.data.get('reporter')

        message = get_object_or_404(Message, pk= message_id)
        message_notify(message, reporter)

        activity = ActivityRecord.objects.create(
            message = message,
            reporter = reporter,
        )
        serializer = ActivityRecordSerializer(instance=activity)
        return Response({"detail": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def message_notify(message, reporter):
    line_group = LineNotify.objects.all()

    for line_index in line_group:
        LINE_NOTIFY_ACCESS_TOKEN = line_index.token_access

        # URL to send a message to LINE Notify
        LINE_NOTIFY_API_URL = "https://notify-api.line.me/api/notify"

        # Message to send (can be an empty string)
        now = datetime.now(pytz.timezone('Asia/Bangkok'))
        message = f"\n เรื่อง :  {message.topic} \n รายละเอียด :  {message.description}"
        message = message + f"\n สถานที่ :  {message.location.floorNumber.buildingInfo.building_name}, {message.location.floorNumber.floor_name}, {message.location.location_name}"
        message = message + f"\n ผู้แจ้ง : {reporter}"

        headers = {
            # "Content-Type": "multipart/form-data",
            "Authorization": f"Bearer {LINE_NOTIFY_ACCESS_TOKEN}"
        }

        data = {
            "message": message
        }

        # Send a message to the LINE Notify service
        response = requests.post(LINE_NOTIFY_API_URL, headers=headers, data=data)



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_line_notice_config(request):
    try:
        lines = LineNotify.objects.all()
        serializer = LineNotifySerializer(instance=lines, many=True)
        return Response({"detail": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_line_notice_config(request):
    try:
        group_name = request.data.get('group_name')
        token_access = request.data.get('token_access')

        line = LineNotify.objects.create(
            group_name = group_name,
            token_access = token_access
        )
        serializer = LineNotifySerializer(instance=line)
        return Response({"detail": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_line_notice_config(request):
    try:
        config_id = request.data.get('config_id')
        group_name = request.data.get('group_name')
        token_access = request.data.get('token_access')

        line = LineNotify.objects.filter(pk = config_id)
        line.update(
            group_name = group_name,
            token_access = token_access
        )
        serializer = LineNotifySerializer(instance=line, many=True)
        return Response({"detail": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_line_notice_config(request):
    try:
        query_data = LineConfigQuerySerializer(data = request.query_params)

        if query_data.is_valid():
            pk = query_data.validated_data.get('config_id')
            LineNotify.objects.filter(pk = pk).delete()
            return Response({"detail": f"{pk} was deleted"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Data format is invalid"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_job(request):
    try:
        query_data = BuildingQuerySerializer(data = request.query_params)

        if query_data.is_valid():
            pk = query_data.validated_data.get('building_id')
            current_job = ActivityRecord.objects.filter(message__location__floorNumber__buildingInfo__pk = pk).first()

            serializer = ActivityRecordSerializer(instance=current_job)
            return Response({"detail": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Data format is invalid"}, status=status.HTTP_400_BAD_REQUEST)    
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def complete_job(request):
    try:
        activity_id = request.data.get('activity_id')
        assignee = request.data.get('assignee')
        date_done = timezone.now

        activity = ActivityRecord.objects.filter(pk = activity_id)
        if not activity.exists():
            return Response({"detail": "not found"}, status=status.HTTP_404_NOT_FOUND)

        activity.update(
            assignee = assignee,
            date_done = date_done,
        )

        return Response({"detail": "success"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_authentication(request):
    try:
        return Response({"detail": "Token is valid"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": f"Failure, data as provided is incorrect. Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)