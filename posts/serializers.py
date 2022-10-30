from rest_framework import serializers

from django.contrib.auth import get_user_model

from posts.models import Post, Like, Comment
from accounts.serializers import UserPublicProfileSerializer
from media.models import Photo, Video
from media.serializers import PhotoSerializer, VideoSerializer

class LikeSerializer(serializers.ModelSerializer):
    """Serializer for LikeView"""
    account = UserPublicProfileSerializer(read_only=True)
    post = serializers.SlugRelatedField(slug_field="public_id", queryset=Post.objects.all())
    class Meta:
        model = Like
        fields = ["account", "post"]

class CommentSerializer(serializers.ModelSerializer):
    """Serializer for PostCommentView"""
    account = UserPublicProfileSerializer(read_only=True)
    post = serializers.SlugRelatedField(slug_field="public_id", queryset=Post.objects.all())
    class Meta:
        model = Comment
        fields = ["public_id", "account", "comment_text", "post", "time"]
        read_only_fields = ["public_id", "time"]

class CommentCreateSerializer(CommentSerializer):
    """Serializer for CommentCreateView"""
    account = serializers.SlugRelatedField(slug_field="public_id", queryset=get_user_model().objects.all())

class BasePostDetailSerializer(serializers.ModelSerializer):
    """Base serializer for RetrievePostView"""
    uploader = UserPublicProfileSerializer(read_only=True)
    media_item = serializers.FileField()
    class Meta:
        model = Post
        fields = ["public_id", "uploader", "post_type", "upload_time", "caption", "media_item", "likes_number", "comments_number"]
        read_only_fields = ["public_id", "upload_time", "likes_number", "comments_number"]

class PhotoPostDetailSerializer(BasePostDetailSerializer):
    """Serializer for photo posts"""
    media_item = PhotoSerializer(read_only=True)

class VideoPostDetailSerializer(BasePostDetailSerializer):
    """Serializer for video posts"""
    media_item = VideoSerializer(read_only=True)

class BasePostCreateSerializer(serializers.ModelSerializer):
    """Base serializer for CreatePostView"""
    uploader = serializers.SlugRelatedField(slug_field="public_id", queryset=get_user_model().objects.all())
    media_item = serializers.FileField()
    class Meta:
        model = Post
        fields = ["public_id", "uploader", "post_type", "upload_time", "caption", "media_item", "likes_number", "comments_number"]
        read_only_fields = ["public_id", "upload_time", "likes_number", "comments_number"]

class PhotoPostCreateSerializer(BasePostCreateSerializer):
    """Serializer for creating new photo posts"""

    media_item = PhotoSerializer()

    def create(self, validated_data):
        media_data = validated_data.pop("media_item")
        uploader = validated_data.pop("uploader")
        content_type = "post"

        media_data = {
            "uploader": uploader,
            "content_type": content_type,
            "media": media_data.get("media")
        }

        photo = Photo.objects.create(**media_data)
        
        post = Post.objects.create(media_item=photo, uploader=uploader, **validated_data)
        return post

class VideoPostCreateSerializer(BasePostCreateSerializer):
    """Serializer for creating new photo posts"""

    media_item = VideoSerializer()

    def create(self, validated_data):
        media_data = validated_data.pop("media")
        uploader = validated_data.pop("uploader")
        post_type = validated_data.get("post_type")

        #Determine (video) content type
        if post_type=="free_video":
            content_type = "free_post"
        elif post_type=="paid_video":
            content_type = "paid_post"

        media_data = {
            "uploader": uploader,
            "content_type": content_type,
            "media": media_data.get("media")
        }

        video = Video.objects.create(**media_data)
        
        post = Post.objects.create(media_item=video, uploader=uploader, **validated_data)
        return post