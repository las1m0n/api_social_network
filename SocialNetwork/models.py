
from django.conf import settings
from django.db import models
from rest_framework.reverse import reverse as api_reverse
from django.contrib.auth.models import AbstractUser


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, null=True, blank=True)
    content = models.TextField(max_length=120, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)

    @property
    def owner(self):
        return self.user

    # def get_absolute_url(self):
    #     return reverse("api-social:post-view", kwargs={'pk': self.pk})

    def get_api_url(self, request=None):
        return api_reverse("api-social:post-read", kwargs={'pk': self.pk}, request=request)


