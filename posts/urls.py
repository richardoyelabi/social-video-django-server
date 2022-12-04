from django.urls import path
from posts.views import PostViewView, PostLikeView, PostCommentView, CommentView, CommentCreateView, PostView, CreatePostView, PostVideoStreamView

urlpatterns = [

    #Views
    path("<uuid:post_id>/views/", PostViewView.as_view(), name="post_views"),

    #Likes
    path("<uuid:post_id>/likes/", PostLikeView.as_view(), name="post_likes"),
    
    #Comments
    path("comment/<uuid:comment_id>/", CommentView.as_view(), name="single_post_comment"),
    path("<uuid:post_id>/comments/", PostCommentView.as_view(), name="post_comments"),
    path("<uuid:post_id>/comments/new/", CommentCreateView.as_view(), name="new_comment"),
    
    #Video stream
    path("<uuid:post_id>/video-stream/<uuid:video_id>/", PostVideoStreamView.as_view(), name="post_video_stream"),
    
    #Post
    path("<uuid:post_id>/", PostView.as_view(), name="post"),
    path("new-post/", CreatePostView.as_view(), name="new_post"),
]