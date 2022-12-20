import uuid
from django.db import models
from tickets.models import Ticket

# Create your models here.


class Payment(models.Model):
    ID = models.UUIDField(default=uuid.uuid4, editable=False)
    payment_request_id = models.CharField(max_length=150)
    payment_id = models.CharField(max_length=150)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    response = models.TextField()
