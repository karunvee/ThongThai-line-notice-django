from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('login/', login_user , name='login_user'),
    path('logout/', logout_user , name='logout_user'),
    path('line_notice/information/', get_line_information , name='get_line_information'),

    path('building/list/', get_building_list , name='get_building_list'),
    path('building/add/', add_building , name='add_building'),
    path('building/delete/', delete_building , name='delete_building'),
    path('building/update/', update_building , name='update_building'),

    path('floor/list/', get_floor_list , name='get_floor_list'),
    path('floor/add/', add_floor , name='add_floor'),
    path('floor/delete/', delete_floor , name='delete_floor'),
    path('floor/update/', update_floor , name='update_floor'),

    path('location/list/', get_location_list , name='get_location_list'),
    path('location/add/', add_location , name='add_location'),
    path('location/delete/', delete_location , name='delete_location'),
    path('location/update/', update_location , name='update_location'),

    path('message/list/', get_message_list , name='get_message_list'),
    path('message/add/', add_message , name='add_message'),
    path('message/update/', update_message , name='update_message'),
    path('message/delete/', delete_message , name='delete_message'),

    path('sub_message/add/', add_sub_message , name='add_sub_message'),
    path('sub_message/delete/', delete_sub_message , name='delete_sub_message'),

    path('content/list/', get_content_list , name='get_content_list'),
    path('content/add/', add_content , name='add_content'),
    path('content/delete/', delete_content , name='delete_content'),
    path('content/update/', update_content , name='update_content'),

    path('sending/message/', send_message , name='send_message'),
    path('complete/job/', complete_job , name='complete_job'),
    path('get/job/', get_job , name='get_job'),

    path('line/config/get/', get_line_notice_config , name='get_line_notice_config'),
    path('line/config/add/', add_line_notice_config , name='add_line_notice_config'),
    path('line/config/update/', update_line_notice_config , name='update_line_notice_config'),
    path('line/config/delete/', delete_line_notice_config , name='delete_line_notice_config'),
]

