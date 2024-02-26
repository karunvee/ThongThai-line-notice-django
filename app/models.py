from django.db import models
from django.utils import timezone


# Create your models here.
class LineNotify(models.Model):
    group_name = models.CharField(max_length=20)
    token_access = models.CharField(max_length=43)

    def __str__(self):
        return self.token_access

class Building(models.Model):
    building_name = models.CharField(max_length=20)
    def __str__(self):
        return self.building_name

class FloorNumber(models.Model):
    floor_name = models.CharField(max_length=100)
    buildingInfo = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return "%s, %s" % (self.buildingInfo.building_name, self.floor_name)

class Location(models.Model):
    location_name = models.CharField(max_length=80)
    floorNumber = models.ForeignKey(FloorNumber, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return "%s, %s" % (self.floorNumber, self.location_name)


class Message(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    topic = models.CharField(max_length = 100)    
    description = models.TextField()

    def __str__(self):
        return self.topic

class AcitivityRecord(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)
    assignee = models.CharField(max_length = 30, blank = True)    
    reporter = models.CharField(max_length = 30)    
    date_created = models.DateTimeField(default=timezone.now)
    date_done = models.DateTimeField(blank = True)

    def __str__(self):
        return self.message.topic

class ContentSlide(models.Model):
    content = models.CharField(max_length = 60)
    image = models.ImageField(upload_to='images/')  # 'upload_to' defines the upload directory
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.pk}.{self.content}"