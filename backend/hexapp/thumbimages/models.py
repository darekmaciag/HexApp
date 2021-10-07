from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFill
import os
from uuid import uuid4
from django.core.validators import MaxValueValidator, MinValueValidator


def path_and_rename(instance, filename):
    upload_to = 'images'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class ThumbImage(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='thumbimages', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, default='')
    alt = models.CharField(max_length=100, blank=True, default='')
    image = models.ImageField(upload_to=path_and_rename, null=True, blank=True)
    image_small  = ImageSpecField(source='image', processors=[ResizeToFill(200, 200)], format='PNG', options={'quality': 70})
    image_medium = ImageSpecField(source='image', processors=[ResizeToFill(400, 400)], format='PNG', options={'quality': 70})

    class Meta:
        ordering = ['created']
        permissions = (
            ("hide_image", "Cant see image"),
            ("hide_image_medium", "Cant see medium image"),
            ("hide_image_link", "Cant see link"),
            )


class ImageLink(models.Model):
    owner = models.ForeignKey('auth.User', related_name='imagelinks', on_delete=models.CASCADE)
    image = models.ForeignKey(ThumbImage, related_name='links', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiry_time = models.IntegerField(default=30,validators=[MinValueValidator(30),MaxValueValidator(30000)])

    class Meta:
        ordering = ['created']
