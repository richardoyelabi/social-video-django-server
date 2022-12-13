from django.db import models
from django.conf import settings
from .tips_cut import cut
from transactions.models import Transaction
from chats.models import ChatMessage

from decimal import Decimal


class Tip(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="sent_tips")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="received_tips")
    created = models.DateTimeField()
    fee_currency = models.CharField(max_length=3, choices=Transaction.currency_choices, default="usd")
    fee_amount = models.DecimalField(max_digits=100, decimal_places=50, default=0.00)
    tip_message = models.ForeignKey(ChatMessage, null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):

        #Execute required transaction for purchase
        Transaction.objects.create(
            transaction_currency=self.fee_currency,
            amount_sent=Decimal(self.fee_amount),
            sender=self.sender,
            platform_fee=Decimal(cut*self.fee_amount/100),
            receiver=self.receiver,
            transaction_type="tip"
        )

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.sender} tipped {self.receiver} {self.fee_currency}{self.fee_amount}"
