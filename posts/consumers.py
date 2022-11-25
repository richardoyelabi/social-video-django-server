from urllib import parse

from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from posts.models import Post, Like, Comment
from posts.serializers import LikeSerializer, CommentSerializer


# Returns user by validating Token
class TokenAuth(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_user(self):
        scope = self.scope
        try:
            # Parse the scope and gets the token
            query = parse.parse_qs(scope['query_string'].decode("utf-8"))['token'][0]
            if query:
                token = Token.objects.get(key=query)
                # Returns token user
                return token.user

        except Token.DoesNotExist:
            return None


class PostLikeCountConsumer(AsyncJsonWebsocketConsumer, TokenAuth):
    
    async def connect(self):
        """Connect and add channel to like_count_ group"""

        user = await self.get_user()

        if user is not None:

            await self.accept()

            post_id = self.scope["url_route"]["kwargs"]["post_id"]

            await self.channel_layer.group_add(f"like_count_{post_id}", self.channel_name)

    async def disconnect(self, code):
        """Clean up connection data"""

        post_id = self.scope["url_route"]["kwargs"]["post_id"]
        await self.channel_layer.group_discard(f"like_count_{post_id}", self.channel_name)
        return await super().disconnect(code)

    async def like_count_update(self, event):
        await self.send_json(event["content"])

    
class PostCommentCountConsumer(AsyncJsonWebsocketConsumer, TokenAuth):
    async def connect(self):
        """Connect and add channel to comment_count_ group"""

        user = await self.get_user()

        if user is not None:
            
            await self.accept()

            post_id = self.scope["url_route"]["kwargs"]["post_id"]

            await self.channel_layer.group_add(f"comment_count_{post_id}", self.channel_name)

    async def disconnect(self, code):
        """Clean up connection data"""

        post_id = self.scope["url_route"]["kwargs"]["post_id"]
        await self.channel_layer.group_discard(f"comment_count_{post_id}", self.channel_name)
        return await super().disconnect(code)

    async def comment_count_update(self, event):
        await self.send_json(event["content"])


class PostCommentConsumer(AsyncJsonWebsocketConsumer, TokenAuth):
    async def connect(self):
        """Connect and add channel to comments_ group"""

        user = await self.get_user()

        if user is not None:

            await self.accept()

            post_id = self.scope["url_route"]["kwargs"]["post_id"]

            await self.channel_layer.group_add(f"comments_{post_id}", self.channel_name)

    async def disconnect(self, code):
        """Clean up connection data"""

        post_id = self.scope["url_route"]["kwargs"]["post_id"]
        await self.channel_layer.group_discard(f"comments_{post_id}", self.channel_name)

        return await super().disconnect(code)

    async def comment_update(self, event):
        await self.send_json(event["content"])

