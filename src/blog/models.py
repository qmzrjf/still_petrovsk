from uuid import uuid4
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from blog.tasks import send_activation_code_async
from pytils.translit import slugify


def avatar_path(instace, filename: str):
    ext = filename.split('.')[-1]
    f = str(uuid4())
    filename = f'{f}.{ext}'
    return '/'.join(['avatar', str(instace.id), filename])


def picture_path(instace, filename: str):
    ext = filename.split('.')[-1]
    f = str(uuid4())
    filename = f'{f}.{ext}'
    return '/'.join(['post_picture', 'tmp', filename])


class User(AbstractUser):
    avatar = models.ImageField(upload_to=avatar_path, null=True, blank=True, default=None)
    author_status = models.BooleanField(default=False)


class ActivationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activation_codes')
    created = models.DateTimeField(auto_now_add=True)
    code = models.UUIDField(default=uuid4, editable=False, unique=True)
    is_activated = models.BooleanField(default=False)

    @property
    def is_expired(self):
        now = datetime.now()
        diff = now - self.created
        return diff.days > 7

    def send_activation_code(self):
        send_activation_code_async.delay(self.user.email, self.code)


class Category(models.Model):
    category_name = models.CharField(max_length=25)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.category_name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Post(models.Model):
    picture = models.ImageField(upload_to=picture_path, null=True, blank=True, default=None)
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=50, unique=True)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    tags = models.ManyToManyField('Tag', related_name='tags')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}, {self.author}, {self.tags}, {self.created}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
