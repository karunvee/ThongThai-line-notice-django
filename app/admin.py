from django.contrib import admin
from .models import *


# Register your models here.
class LineNotifyAdmin(admin.ModelAdmin):
    search_fields = ['group_name', 'pk']
    list_display = (
        'token_access',
        'pk',
        'group_name',
        'buildingInfo',
                    )
    list_filter = ['buildingInfo']
admin.site.register(LineNotify, LineNotifyAdmin)

class BuildingAdmin(admin.ModelAdmin):
    search_fields = ['building_name', 'pk']
    list_display = (
        'building_name',
        'pk',
                    )
admin.site.register(Building, BuildingAdmin)

class FloorNumberAdmin(admin.ModelAdmin):
    search_fields = ['number']
    list_display = (
        'floor_name',
        'pk',
        'buildingInfo',
                    )
admin.site.register(FloorNumber, FloorNumberAdmin)

class LocationAdmin(admin.ModelAdmin):
    search_fields = ['number']
    list_display = (
        'location_name',
        'pk',
        'floorNumber',
                    )
admin.site.register(Location, LocationAdmin)

class StandardMessageAdmin(admin.ModelAdmin):
    search_fields = ['topic']
    list_display = (
        'topic',
        'pk',
        'description',
        'date_created',
                    )
admin.site.register(StandardMessage, StandardMessageAdmin)

class MessageAdmin(admin.ModelAdmin):
    search_fields = ['topic']
    list_display = (
        'topic',
        'pk',
        'location',
        'description',
                    )
    list_filter = ['location']
admin.site.register(Message, MessageAdmin)

class SubMessageAdmin(admin.ModelAdmin):
    search_fields = ['detail']
    list_display = (
        'message',
        'pk',
        'detail',
                    )
    list_filter = ['message']
admin.site.register(SubMessage, SubMessageAdmin)

class ContentSlideAdmin(admin.ModelAdmin):
    search_fields = ['content']
    list_display = (
        'content',
        'image',
        'date_created',
                    )
admin.site.register(ContentSlide, ContentSlideAdmin)

class ActivityRecordAdmin(admin.ModelAdmin):
    search_fields = ['reporter', 'assignee']
    list_display = (
        'message',
        'reporter',
        'assignee',
        'date_created',
        'date_done',
                    )
    list_filter = ['reporter', 'assignee', 'message__location__floorNumber__buildingInfo']
admin.site.register(ActivityRecord, ActivityRecordAdmin)