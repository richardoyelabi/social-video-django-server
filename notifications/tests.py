from django.test import TestCase


from notifications.models import Notification
from accounts.models import Account
from posts.models import Like, Comment
from subscriptions.models import Subscription
from video_purchases.models import Purchase
from chats.models import ChatMessage
from special_requests.models import SpecialRequest, MessagePurchase
from tips.models import Tip


receiver = Account.objects.get(username="testcreator1")


records = (
    Like.objects.get(account=2),
    Comment.objects.get(account=2),
    Subscription.objects.get(subscriber=2),
    Purchase.objects.get(buyer=2),
    ChatMessage.objects.get(public_id="22a4cbdc-802f-4f36-a99a-8280fa59e7b7"),
    SpecialRequest.objects.get(request_by=2),
    MessagePurchase.objects.get(buyer=2),
    Tip.objects.get(sender=2),
)

for record in records:
    Notification.notify(receiver=receiver, record=record)
