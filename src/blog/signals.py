from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from blog.models import User, Post
import os

import shutil
from django.conf import settings


@receiver(pre_save, sender=User)
def pre_save_user_avatar(sender, instance, **kwargs):
    try:
        if instance.avatar not in (None, User.objects.get(id=instance.id).avatar):
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'avatar', str(instance.id)))
    except:
        pass


@receiver(post_save, sender=Post)
def save_file(sender, instance, created, **kwargs):
    if created:

        picture = str(instance.picture).split('/')[-1]
        source = os.path.join(settings.MEDIA_ROOT, 'post_picture', 'tmp', str(picture))
        destination = os.path.join(settings.MEDIA_ROOT, 'post_picture', str(instance.id), str(picture))
        os.mkdir(os.path.join(settings.MEDIA_ROOT, 'post_picture', str(instance.id)))
        shutil.copy(source, destination)

        picture_str = '/'.join(['post_picture', str(instance.id), picture])
        instance.picture = picture_str

        instance.save()
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'post_picture', 'tmp'))
