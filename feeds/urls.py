from django.urls import path
from feeds.profile_posts import ActiveSubPostFeedView, ExpiredSubPostFeedView, PurchasedPostFeedView, SavedPostFeedView


urlpatterns = [
    #Subscription posts
    path("active-sub-posts/", ActiveSubPostFeedView.as_view(), name="active_sub_post_feed"),
    path("expired-sub-posts/", ExpiredSubPostFeedView.as_view(), name="expired_sub_post_feed"),
    
    #Purchased posts
    path("purchased-posts/", PurchasedPostFeedView.as_view(), name="purchased_feed"),
    
    #Saved posts
    path("saved-posts/", SavedPostFeedView.as_view(), name="saved"),
]