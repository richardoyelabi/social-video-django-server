from django.db import models
from django.conf import settings
from media.models import Video
from .video_purchases_cut import cut
from transactions.models import Transaction

from decimal import Decimal

class Purchase(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    time_of_purchase = models.DateTimeField(auto_now_add=True)
    fee_currency = models.CharField(max_length=3, choices=Transaction.currency_choices, default="usd")
    fee_amount = models.DecimalField(max_digits=100, decimal_places=50, default=0.00)

    def save(self, *args, **kwargs):

        #Get purchase fee
        video = self.video
        self.fee_currency, self.fee_amount = (video.purchase_cost_currency, video.purchase_cost_amount)
        
        #Execute required transaction for purchase
        Transaction.objects.create(
            transaction_currency=self.fee_currency,
            amount_sent=self.fee_amount,
            sender=self.buyer,
            platform_fee=Decimal(cut*self.fee_amount/100),
            receiver=self.video.uploader,
            transaction_type="subscribe"
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.buyer} purchased {self.video}"

class CancelledPurchase(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    time_of_cancellation = models.DateTimeField(auto_now_add=True)
    time_of_initial_purchase = models.DateTimeField()
    fee_currency = models.CharField(max_length=3, choices=Transaction.currency_choices, default="usd")
    fee_amount = models.DecimalField(max_digits=100, decimal_places=50, default=0.00)

    def __str__(self):
        return f"{self.buyer} cancelled their purchase of {self.video}"

class NullifiedPurchase(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    time_of_nullification = models.DateTimeField(auto_now_add=True)
    time_of_initial_purchase = models.DateTimeField()
    fee_currency = models.CharField(max_length=3, choices=Transaction.currency_choices, default="usd")
    fee_amount = models.DecimalField(max_digits=100, decimal_places=50, default=0.00)

    def __str__(self):
        return f"{self.buyer}'s purchase of {self.video} has been nullified"
