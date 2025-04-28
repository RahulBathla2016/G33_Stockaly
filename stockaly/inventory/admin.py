from django.contrib import admin
from .models import CustomUser, InventoryItem

admin.site.register(CustomUser)
admin.site.register(InventoryItem)