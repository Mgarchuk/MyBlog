from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post_Image(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.image.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.OneToOneField(Post_Image, on_delete=models.CASCADE, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Photo(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.text





