import datetime

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login

from .models import Post, PostLikes, max_post_length
from .helpers import get_user_by_jwt


class PostCreateSerializer(serializers.Serializer):
    body = serializers.CharField(max_length=max_post_length, required=True)

    def create(self, validated_data):
        user = self.context['request'].user
        body = validated_data.get('body')
        post = Post(author=user, body=body, date_created=datetime.datetime.now())
        post.save()
        return post


class PostRetrieveSerializer(serializers.Serializer):
    author = serializers.CharField()
    date_created = serializers.DateTimeField()
    body = serializers.CharField(max_length=max_post_length)

    class Meta:
        model = Post
        fields = '__all__'


class LikePostSerializer(serializers.Serializer):

    def create(self, validated_data):
        user = self.context['request'].user
        check_like = PostLikes.objects.filter(user=user, post=validated_data.get('post'))
        if check_like.exists():
            return check_like.first()
        return PostLikes.objects.create(**validated_data, user=user, date_created=datetime.datetime.now())


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        user = get_user_by_jwt(validated_data.get('access'))
        update_last_login(None, user)
        return validated_data
