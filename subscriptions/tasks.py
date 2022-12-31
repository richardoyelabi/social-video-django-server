from celery import shared_task
from django.contrib.auth import get_user_model

from .models import SubscriptionTransaction, Subscription
from transactions.exceptions import TransactionInsufficientBalanceError

@shared_task
def process_sub_transaction(subscribed_to, subscriber):
    """Task to create subscription transaction."""

    Account = get_user_model()
    subscribed_to = Account.objects.get(id=subscribed_to)
    subscriber = Account.objects.get(id=subscriber)

    try:
        SubscriptionTransaction.objects.create(
            subscribed_to = subscribed_to,
            subscriber = subscriber
        )

    except TransactionInsufficientBalanceError:
        Subscription.objects.get(
            subscribed_to = subscribed_to,
            subscriber = subscriber
        ).delete()