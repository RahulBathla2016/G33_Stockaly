from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    role = models.CharField(max_length=100, default="user")

    def __str__(self):
        return self.username

class InventoryItem(models.Model):
    item_name = models.CharField(max_length=100)
    item_number = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.FloatField()
    date_added = models.DateTimeField(default=timezone.now)
    last_changed = models.DateTimeField(null=True, blank=True)
    # Add user field to associate items with specific users
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='inventory_items', null=True)

    def __str__(self):
        return self.item_name
    
    def total_value(self):
        return self.quantity * self.price