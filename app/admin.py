from django.contrib import admin
from .models import *


# Register your models here.
class LineNotifyAdmin(admin.ModelAdmin):
    list_display = (
        'token_access',
        'pk',
        'group_name',
                    )
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

class ContentSlideAdmin(admin.ModelAdmin):
    search_fields = ['content']
    list_display = (
        'content',
        'image',
        'date_created',
                    )
admin.site.register(ContentSlide, ContentSlideAdmin)

class AcitivityRecordAdmin(admin.ModelAdmin):
    search_fields = ['reporter', 'assignee']
    list_display = (
        'message',
        'reporter',
        'assignee',
        'date_created',
        'date_done',
                    )
    list_filter = ['reporter', 'assignee']
admin.site.register(AcitivityRecord, AcitivityRecordAdmin)