from django.db import models
from django.conf import settings
from posts.models import Post
from .video_purchases_cut import cut as float_cut
from transactions.models import Transaction
from transactions.currency_convert import convert_currency

from decimal import Decimal


class Purchase(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_of_purchase = models.DateTimeField(auto_now_add=True)
    fee_currency = models.CharField(
        max_length=3, choices=Transaction.currency_choices, default="usd"
    )
    fee_amount = models.DecimalField(max_digits=100, decimal_places=50, default=0.00)

    def save(self, *args, **kwargs):
        # Get purchase fee
        video = self.video_post
        source_currency, self.fee_amount = (
            video.purchase_cost_currency,
            video.purchase_cost_amount,
        )

        cut = Decimal(float_cut)
        self.fee_amount = Decimal(self.fee_amount)

        # Convert fee_amount to destination currency if needed
        self.fee_amount = convert_currency(
            source=source_currency, target=self.fee_currency, amount=self.fee_amount
        )

        # Execute required transaction for purchase
        Transaction.objects.create(
            transaction_currency=self.fee_currency,
            amount_sent=self.fee_amount,
            sender=self.buyer,
            platform_fee=cut * self.fee_amount / 100,
            receiver=self.video_post.uploader,
            transaction_type="buy",
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.buyer} purchased {self.video_post}"


class CancelledPurchase(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_of_cancellation = models.DateTimeField(auto_now_add=True)
    time_of_initial_purchase = models.DateTimeField()
    fee_currency = models.CharField(
        max_length=3, choices=Transaction.currency_choices, default="usd"
    )
    fee_amount = models.DecimalField(max_digits=100, decimal_places=50, default=0.00)

    def __str__(self):
        return f"{self.buyer} cancelled their purchase of {self.video_post}"


class NullifiedPurchase(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_of_nullification = models.DateTimeField(auto_now_add=True)
    time_of_initial_purchase = models.DateTimeField()
    fee_currency = models.CharField(
        max_length=3, choices=Transaction.currency_choices, default="usd"
    )
    fee_amount = models.DecimalField(max_digits=100, decimal_places=50, default=0.00)

    def __str__(self):
        return f"{self.buyer}'s purchase of {self.video_post} has been nullified"
