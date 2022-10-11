from django.db import models
from django.conf import settings
from videos.models import Video

class Purchase(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    time_of_purchase = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer} purchased {self.video}"

class CancelledPurchase(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    time_of_cancellation = models.DateTimeField(auto_now_add=True)
    time_of_initial_purchase = models.DateTimeField()

    def __str__(self):
        return f"{self.buyer} cancelled their purchase of {self.video}"

class NullifiedPurchase(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    time_of_nullification = models.DateTimeField(auto_now_add=True)
    time_of_initial_purchase = models.DateTimeField()

    def __str__(self):
        return f"{self.buyer}'s purchase of {self.video} has been nullified"
