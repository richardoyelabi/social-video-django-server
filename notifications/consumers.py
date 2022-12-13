from urllib import parse

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from rest_framework.authtoken.models import Token


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


class NotificationConsumer(AsyncJsonWebsocketConsumer, TokenAuth):

    async def connect(self):

        user = await self.get_user()

        if user is not None:

            await self.accept()

            await self.channel_layer.group_add(f"notification_{user.public_id}", self.channel_name)

            await self.set_connected(user, True)

    async def disconnect(self, code):

        user = await self.get_user()

        if user is not None:

            await self.set_connected(user, False)
            
            await self.channel_layer.group_discard(f"notification_{user.public_id}", self.channel_name)
        
        return await super().disconnect(code)

    async def site_notification(self, event):
        await self.send_json(event["content"])

    @database_sync_to_async
    def set_connected(self, user, value):
        user.connected = value
        user.save()