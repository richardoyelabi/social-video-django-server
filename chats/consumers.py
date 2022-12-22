from urllib import parse
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from chats.models import Thread, Inbox
from chats.serializers import \
    TextMessageDetailSerializer, TextMessageCreateSerializer, \
        PhotoMessageDetailSerializer, PhotoMessageCreateSerializer, \
            VideoMessageDetailSerializer, VideoMessageCreateSerializer, \
                PaidVideoMessageDetailSerializer, PaidVideoMessageCreateSerializer


channel_layer = get_channel_layer()

User = get_user_model()


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


# Determines users Online/Offline Activity
class OnlineOfflineConsumer(AsyncJsonWebsocketConsumer, TokenAuth):

    # Connects Websocket
    async def connect(self):
        # Accepts the connection
        await self.accept()
        # Get the request user
        user = await self.get_user()
        # If user is authenticated
        if user is not None:
            
            status = True

            # Update user Status to Online
            await self.update_user_status(user, status)

            #Broadcast user status
            await self.broadcast_user_status(user, status)

    async def disconnect(self, code):
        # Discard
        user = await self.get_user()
        if user is not None:

            status = False

            # Update user status to Offline
            await self.update_user_status(user, status)

            # Broadcast user status
            await self.broadcast_user_status(user, status)

        return await super().disconnect(code)

    async def user_update(self, event):
        await self.send_json(event)

    async def broadcast_user_status(self, user, status):
        public_id = user.public_id

        await self.channel_layer.group_send(
                f"status_{public_id}",
                {
                    "type": "status_update",
                    "content": {"online": status}
                }
            )

    @database_sync_to_async
    def update_user_status(self, user, status):
        user.online = status
        user.save()
        
        return user


#Watch an account's online/offline status
class WatchStatusConsumer(AsyncJsonWebsocketConsumer, TokenAuth):

    async def connect(self):
        await self.accept()
        user = await self.get_user()
        if user is not None:
            public_id = self.scope['url_route']['kwargs']['public_id']
            await self.channel_layer.group_add(f"status_{public_id}", self.channel_name)

    async def disconnect(self, code):
        public_id = self.scope['url_route']['kwargs']['public_id']
        await self.channel_layer.group_discard(f"status_{public_id}", self.channel_name)

        return await super().disconnect(code)

    async def status_update(self, event):
        await self.send_json(event["content"])


# User Inbox Consumer
class InboxConsumer(AsyncJsonWebsocketConsumer, TokenAuth):
    # Accepts connection
    async def connect(self):
        user = await self.get_user()
        await self.channel_layer.group_add(f"inbox_{user.public_id}", self.channel_name)
        await self.accept()

    # Disconnects
    async def disconnect(self, code):
        user = await self.get_user()
        await self.channel_layer.group_discard(f"inbox_{user.public_id}", self.channel_name)

        return await super().disconnect(code)

    # Send updated inbox data
    async def update_inbox(self, event):
        await self.send_json(event["content"])


class MessageConsumer(AsyncJsonWebsocketConsumer, TokenAuth):

    # Connects To Message Consumer
    async def connect(self):
        user = await self.get_user()
        if user is not None:
            second_user = self.scope['url_route']['kwargs']['public_id']
            thread = await self.get_thread(user, second_user)
            #await self.read_user_inbox(user, second_user)
            # Add to channel layer
            await self.channel_layer.group_add(f"thread_{thread.id}", self.channel_name)
            await self.accept()

    # Disconnects
    async def disconnect(self, code):
        user = await self.get_user()
        second_user = self.scope['url_route']['kwargs']['public_id']
        thread = await self.get_thread(user, second_user)
        await self.channel_layer.group_discard(f"thread_{thread.id}", self.channel_name)
        await self.accept()

        return await super().disconnect(code)

    # Receives message from socket
    async def receive_json(self, content, **kwargs):
        user = await self.get_user()
        second_user = self.scope['url_route']['kwargs']['public_id']
        thread = await self.get_thread(user, second_user)
        inboxes = await self.get_inbox(user, second_user)
        
        try:
            msg = await self.create_msg(user=user, other_user=second_user, thread=thread, content=content, inbox=inboxes)
        except ValueError as e:
            await self.send_json(
                {
                    "type": "error_message",
                    "message": "One or more of your parameters are invalid.",
                    "detail": e.args[0]
                }
            )
            return
        
        #await self.read_user_inbox(user, second_user)

        message_type = content.get("message_type")

        if message_type=="text":
            serializer = TextMessageDetailSerializer(msg)
        elif message_type=="photo":
            serializer = PhotoMessageDetailSerializer(msg)
        elif message_type=="free_video":
            serializer = VideoMessageDetailSerializer(msg)
        elif message_type=="paid_video":
            serializer = PaidVideoMessageDetailSerializer(msg)

        @database_sync_to_async
        def _get_data():
            return serializer.data

        data = await _get_data()

        #Make user and receiver serializabel (they're uuids)
        data["user"] = str(data["user"])
        data["receiver"] = str(data["receiver"])

        #Make media item public_ids serializable
        if not message_type=="text":
            data["media_item"]["public_id"] = str(data["media_item"]["public_id"])
            data["media_item"]["uploader"] = str(data["media_item"]["uploader"])

        await self.channel_layer.group_send(f'thread_{thread.id}',
                                            {
                                                'type': 'send_msg',
                                                'content': data
                                            })

        return super().receive_json(content, **kwargs)
        
    # Broadcast to channel layer
    async def send_msg(self, event):
        await self.send_json(event['content'])

    @database_sync_to_async
    def get_thread(self, user, other_user):
        return Thread.objects.get_or_new(user, other_user)[0]

    @database_sync_to_async
    def get_inbox(self, user, other_user):
        try:
            second_user = User.objects.get(public_id=other_user)
            user_inbox, created = Inbox.objects.get_or_create(user=user, second=second_user)
            other_user_inbox, created = Inbox.objects.get_or_create(user=second_user, second=user)
            return [user_inbox, other_user_inbox]
        except User.DoesNotExist:
            return []

    #Not being used
    @database_sync_to_async
    def read_user_inbox(self, user, other_user):
        second_user = User.objects.get(public_id=other_user)
        Inbox.objects.read_inbox(user, second_user)

    @database_sync_to_async
    def create_msg(self, user, other_user, content, thread, inbox):
        user_id = user.public_id
        second_user_id = other_user
        thread_id = thread.id

        data = {
            "thread": thread_id,
            "user": user_id,
            "receiver": second_user_id
        }

        data.update(content)

        message_type = content.get("message_type")

        if message_type=="text":
            serializer = TextMessageCreateSerializer(data=data)

        elif message_type=="photo":
            serializer = PhotoMessageCreateSerializer(data=data)

        elif message_type=="free_video":
            serializer = VideoMessageCreateSerializer(data=data)

        elif message_type=="paid_video":
            serializer = PaidVideoMessageCreateSerializer(data=data)

        else:
            raise ValueError("Invalid 'message_type' parameter.")

        if serializer.is_valid():
            new_message = serializer.save()

            for each in inbox:
                new_message.inbox.add(each)
                new_message.save()
            return new_message
        raise ValueError(serializer.errors)
