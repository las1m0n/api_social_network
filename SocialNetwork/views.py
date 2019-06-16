from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import Check_API_KEY_Auth


class ExampleView(APIView):
    permission_classes = (Check_API_KEY_Auth,)

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)
