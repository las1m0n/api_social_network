from rest_framework import serializers

from SocialNetwork.models import Post


class PostSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'url',
            'pk',
            'user',
            'title',
            'content',
            'timestamp',
            'likes'
        ]
        read_only_fields = ['pk', 'user']

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)

    def validate_title(self, value):
        query = Post.objects.filter(title__iexact=value)
        if self.instance:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise serializers.ValidationError("This title has already been used")
        return value
