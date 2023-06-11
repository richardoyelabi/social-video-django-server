from django.urls import path
from feeds.profile_posts import (
    ActiveSubPostFeedView,
    ExpiredSubPostFeedView,
    PurchasedPostFeedView,
    SavedPostFeedView,
)
from feeds.creator_posts import (
    NewCreatorPostFeedView,
    NewCreatorPremiumVideoFeedView,
    TopCreatorPremiumVideoFeedView,
)
from feeds.general_posts import (
    AllPostFeedView,
    TopVideoFeedView,
    TopPremiumVideoFeedView,
    NewPremiumVideoFeedView,
)
from feeds.creators import TopCreatorFeedView, SugCreatorFeedView


urlpatterns = [
    # Subscription posts
    path(
        "active-sub-posts/",
        ActiveSubPostFeedView.as_view(),
        name="active_sub_post_feed",
    ),
    path(
        "expired-sub-posts/",
        ExpiredSubPostFeedView.as_view(),
        name="expired_sub_post_feed",
    ),
    # Purchased posts
    path("purchased-posts/", PurchasedPostFeedView.as_view(), name="purchased_feed"),
    # Saved posts
    path("saved-posts/", SavedPostFeedView.as_view(), name="saved"),
    # Creator posts
    path(
        "<uuid:creator_id>/all-posts/",
        NewCreatorPostFeedView.as_view(),
        name="creator_all_posts",
    ),
    path(
        "<uuid:creator_id>/all-premium-videos/",
        NewCreatorPremiumVideoFeedView.as_view(),
        name="creator_all_premium_videos",
    ),
    path(
        "<uuid:creator_id>/top-premium-videos/",
        TopCreatorPremiumVideoFeedView.as_view(),
        name="creator_top_premium_videos",
    ),
    # General posts
    path("all-posts/", AllPostFeedView.as_view(), name="all_post_feed"),
    path("top-videos/", TopVideoFeedView.as_view(), name="top_video_feed"),
    path(
        "top-premium-videos/",
        TopPremiumVideoFeedView.as_view(),
        name="top_premium_video_feed",
    ),
    path(
        "new-premium-videos/",
        NewPremiumVideoFeedView.as_view(),
        name="new_premium_video_feed",
    ),
    # Creators
    path("top-creators/", TopCreatorFeedView.as_view(), name="top_creators"),
    path(
        "suggested-creators/", SugCreatorFeedView.as_view(), name="suggested_creators"
    ),
]
