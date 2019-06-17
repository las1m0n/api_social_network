from rest_framework import generics, mixins
from SocialNetwork.models import Post
from .serializers import PostSerializer
from django.db.models import Q
from .permissions import IsOwnerOrReadOnly


class PostView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Post.objects.all()

    def get_object(self):
        pk = self.kwargs.get('pk')
        return Post.objects.get(pk=pk)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class PostAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = PostSerializer

    def get_queryset(self):
        qs = Post.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(title__icontains=query) | Q(content__icontains=query))
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}
