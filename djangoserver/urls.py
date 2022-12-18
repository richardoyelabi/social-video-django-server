"""djangoserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
)

urlpatterns = [
    #Admin
    path('admin/', admin.site.urls),

    #Account and auth
    path("account/", include("accounts.urls")),
    
    #Feed
    path("feed/", include("feeds.urls")),

    #Post
    path("post/", include("posts.urls")),
    
    #Chat
    path("chat/", include("chats.urls")),
    
    #Media
    path("media-upload/", include("media.urls")),
    
    #Video save
    path("video-save/", include("video_saves.urls")),

    #Subscription
    path("subscription/", include("subscriptions.urls")),
    
    #Video Purchase
    path("video-purchase/", include("video_purchases.urls")),
    
    #Special Request
    path("special-request/", include("special_requests.urls")),
    
    #Tip
    path("tip/", include("tips.urls")),
    
    #Notification
    path("notification/", include("notifications.urls")),
    
    #Transaction
    path("transaction/", include("transactions.urls")),
    
    #Id verification
    path("verification/", include("verifications.urls")),

    #Browsable API auth
    path("api-auth/", include("rest_framework.urls"),),

    #Schema
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/redoc/", SpectacularRedocView.as_view(
    url_name="schema"), name="redoc",),
    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(
    url_name="schema"), name="swagger-ui"),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
