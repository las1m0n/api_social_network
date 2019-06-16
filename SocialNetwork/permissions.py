from django.conf import settings

from rest_framework.permissions import BasePermission


class Check_API_KEY_Auth(BasePermission):
    def has_permission(self, request, view):
        api_key_secret = request.META.get('API_KEY')
        return api_key_secret == settings.API_KEY_SECRET
