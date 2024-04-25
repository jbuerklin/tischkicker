from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Debt(models.Model):
    receivers = models.ManyToManyField(User, related_name="debts_received")
    senders = models.ManyToManyField(User, related_name="debts_sent")
    amount = models.PositiveSmallIntegerField()
    date = models.DateField()
    note = models.TextField(blank=True)
    done = models.BooleanField(default=False)

    def save(self, *args, **kwargs) -> None:
        if not self.date:
            self.date = timezone.now().date()
        return super().save(*args, **kwargs)

    def get_senders(self):
        return ", ".join([sender.username for sender in self.senders.all()])

    def get_receivers(self):
        return ", ".join([receiver.username for receiver in self.receivers.all()])
