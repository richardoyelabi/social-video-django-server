from django.urls import path
from feeds.profile_posts import ActiveSubPostFeedView, ExpiredSubPostFeedView, PurchasedPostFeedView, SavedPostFeedView
from feeds.creator_posts import NewCreatorPostFeedView, NewCreatorPremiumVideoFeedView, TopCreatorPremiumVideoFeedView


urlpatterns = [
    #Subscription posts
    path("active-sub-posts/", ActiveSubPostFeedView.as_view(), name="active_sub_post_feed"),
    path("expired-sub-posts/", ExpiredSubPostFeedView.as_view(), name="expired_sub_post_feed"),
    
    #Purchased posts
    path("purchased-posts/", PurchasedPostFeedView.as_view(), name="purchased_feed"),
    
    #Saved posts
    path("saved-posts/", SavedPostFeedView.as_view(), name="saved"),
    
    #Creator posts
    path("<uuid:creator_id>/all-posts/", NewCreatorPostFeedView.as_view(), name="creator_all_posts"),
    path("<uuid:creator_id>/all-premium-videos/", NewCreatorPremiumVideoFeedView.as_view(), name="creator_all_premium_videos"),
    path("<uuid:creator_id>/top-premium-videos/", TopCreatorPremiumVideoFeedView.as_view(), name="creator_top_premium_videos"),
]