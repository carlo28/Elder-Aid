from django.db import models

from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

class Meeting(models.Model):
    location = models.CharField(max_length=120)
    participating_users = models.CharField(max_length=120)  #To be completed
    time = models.DateTimeField()
    activity = models.CharField(max_length=120)
    active = models.BooleanField()
    is_private = models.BooleanField()
# Create your models here.

def upload_location(instance, filename, *args, **kwargs):
    file_path = 'meeting/{creator_id}/{title}-{filename}'.format(
        creator_id = str(instance.creator.id), title=str(instance.title), filename = filename
    )
    return file_path

class MeetingPost(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    image = models.ImageField(upload_to=upload_location, null=False, blank=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)
    location = models.CharField(max_length=120)
    time = models.DateTimeField()
    activity = models.CharField(max_length=120)
    active = models.BooleanField(null=True, blank=True)
    is_private = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.title

@receiver(post_delete, sender=MeetingPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

def pre_save_meeting_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.creator.username + "-" + instance.title)

pre_save.connect(pre_save_meeting_post_receiver, sender=MeetingPost)
