from django.urls import path
from posts.views import PostLikeView, PostCommentView, CommentView, CommentCreateView, PostView, CreatePostView

urlpatterns = [
    path("<uuid:post_id>/likes/", PostLikeView.as_view(), name="post_likes"),
    path("<uuid:post_id>/comments/", PostCommentView.as_view(), name="post_comments"),
    path("<uuid:post_id>/comments/new/", CommentCreateView.as_view(), name="new_comment"),
    path("<uuid:post_id>/", PostView.as_view(), name="post"),
    path("comment/<uuid:comment_id>/", CommentView.as_view(), name="single_post_comment"),
    path("new-post/", CreatePostView.as_view(), name="new_post"),
]