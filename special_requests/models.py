from django.db import models
from django.conf import settings
from chats.models import ChatMessage
from .special_requests_cut import cut as float_cut
from transactions.models import Transaction
from transactions.currency_convert import convert_currency

from decimal import Decimal


class SpecialRequest(models.Model):
    request_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_requests", null=True, on_delete=models.SET_NULL)
    request_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="received_requests", null=True, on_delete=models.SET_NULL)
    request = models.ForeignKey(ChatMessage, related_name="special_request", on_delete=models.CASCADE)
    created = models.DateTimeField()


class MessagePurchase(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    video_message = models.ForeignKey(ChatMessage, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    fee_currency = models.CharField(max_length=3, choices=Transaction.currency_choices, default="usd")
    fee_amount = models.DecimalField(max_digits=100, decimal_places=50, default=0.00)
    request = models.ForeignKey(SpecialRequest, related_name="purchases", null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):

        #Get purchase fee
        video = self.video_message
        source_currency, self.fee_amount = (video.purchase_cost_currency, video.purchase_cost_amount)

        cut = Decimal(float_cut)
        self.fee_amount = Decimal(self.fee_amount)

        #Convert fee_amount to destination currency if needed
        self.fee_amount = convert_currency(
            source=source_currency,
            target=self.fee_currency,
            amount=self.fee_amount
        )
        
        #Execute required transaction for purchase
        Transaction.objects.create(
            transaction_currency=self.fee_currency,
            amount_sent=self.fee_amount,
            sender=self.buyer,
            platform_fee=cut*self.fee_amount/100,
            receiver=self.video_message.user,
            transaction_type="request"
        )

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.buyer} unlocked the premium message {self.video_message}"