from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from rest_framework.reverse import reverse as api_reverse
from django.contrib.auth.models import AbstractUser

User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, null=True, blank=True)
    content = models.TextField(max_length=120, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user.username)

    @property
    def owner(self):
        return self.user

    # def get_absolute_url(self, request=None):
    #     return api_reverse("api-social:post-like", kwargs={'pk': self.pk}, request=request)

    def get_api_url(self, request=None):
        return api_reverse("api-social:post-read", kwargs={'pk': self.pk}, request=request)


