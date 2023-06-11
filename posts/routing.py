from django.urls import path

from posts.consumers import (
    PostLikeCountConsumer,
    PostCommentCountConsumer,
    PostCommentConsumer,
)

websocket_urlpatterns = [
    path(
        "<uuid:post_id>/like-count/",
        PostLikeCountConsumer.as_asgi(),
        name="post_like_count",
    ),
    path(
        "<uuid:post_id>/comment-count/",
        PostCommentCountConsumer.as_asgi(),
        name="post_comment_count",
    ),
    path("<uuid:post_id>/comments/", PostCommentConsumer.as_asgi(), name="comments"),
]
