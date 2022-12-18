from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.db import models

from media.validators import FileMimeValidator
from posts.models import Post, Like, Comment
from accounts.serializers import UserPublicProfileSerializer
from media.models import Photo, Video
from media.serializers import PhotoSerializer, VideoSerializer
from transactions.currency_convert import convert_currency


class ViewSerializer(serializers.ModelSerializer):
    """Serializer for PostViewView"""
    post = serializers.SlugRelatedField(slug_field="public_id", queryset=Post.objects.all())
    class Meta:
        model = Like
        fields = ["post"]


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
    """Serializer for free video posts"""
    media_item = VideoSerializer(read_only=True)


class PaidVideoPostDetailSerializer(VideoPostDetailSerializer):
    """Serializer for paid video posts"""
    usd_purchase_cost = serializers.SerializerMethodField()
    btc_purchase_cost = serializers.SerializerMethodField()

    def get_usd_purchase_cost(self, obj):
        return convert_currency(obj.purchase_cost_currency, "usd", obj.purchase_cost_amount)

    def get_btc_purchase_cost(self, obj):
        return convert_currency(obj.purchase_cost_currency, "btc", obj.purchase_cost_amount)
        
    class Meta:
        model = Post
        fields = ["public_id", "uploader", "post_type", "upload_time", "caption", "media_item", "likes_number", "comments_number", "usd_purchase_cost", "btc_purchase_cost"]
        read_only_fields = ["public_id", "upload_time", "likes_number", "comments_number"]


class PostListSerializer(serializers.ListSerializer):
    """Custom serializer for post list to implement custom to_representation for each item in list"""
    
    def to_representation(self, data):

        iterable = data.all() if isinstance(data, models.Manager) else data
        
        to_rep = []
        for item in iterable:
            to_rep += [self.get_to_rep(item)]
        return to_rep

    def get_to_rep(self, instance):

        if instance.post_type == "photo":
            return PhotoPostDetailSerializer(instance).to_representation(instance)

        elif instance.post_type == "free_video":
            return VideoPostDetailSerializer(instance).to_representation(instance)

        elif instance.post_type == "paid_video":
            return PaidVideoPostDetailSerializer(instance).to_representation(instance)


class PostDetailSerializer(serializers.ModelSerializer):
    """Common serializer for all post types"""

    class Meta:
        list_serializer_class = PostListSerializer
        model = Post
        fields = "__all__"


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

        media_data = {
            "uploader": uploader,
            "media": media_data.get("media")
        }

        photo = Photo.objects.create(**media_data)
        
        post = Post.objects.create(media_item=photo, uploader=uploader, **validated_data)
        return post


class VideoPostCreateSerializer(BasePostCreateSerializer):
    """Serializer for creating new free video posts"""

    media_item = VideoSerializer()

    def validate_media_item(self, value):
        validator = FileMimeValidator()
        validator(value.get("media"), api_call=True)
        return value

    def create(self, validated_data):
        media_data = validated_data.pop("media_item")
        uploader = validated_data.pop("uploader")
        post_type = validated_data.get("post_type")

        media_data = {
            "uploader": uploader,
            "media": media_data.get("media")
        }

        video = Video.objects.create(**media_data)
        
        post = Post.objects.create(media_item=video, uploader=uploader, **validated_data)
        return post


class PaidVideoPostCreateSerializer(VideoPostCreateSerializer):
    """Serializer for creating new premium video posts"""

    class Meta:
        model = Post
        fields = ["public_id", "uploader", "post_type", "upload_time", "caption", "media_item", "likes_number", "comments_number", "purchase_cost_currency", "purchase_cost_amount"]
        read_only_fields = ["public_id", "upload_time", "likes_number", "comments_number"]
