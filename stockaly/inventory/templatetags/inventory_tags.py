from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def sum_inventory_value(items):
    """Calculate the total value of all inventory items"""
    total = 0
    for item in items:
        total += item.quantity * item.price
    return total

@register.filter
def low_stock_count(items):
    """Count items with low stock (less than 10)"""
    count = 0
    for item in items:
        if item.quantity < 10:
            count += 1
    return count

@register.filter
def recent_activity_count(items):
    """Count items with recent activity (added or changed in the last 7 days)"""
    count = 0
    one_week_ago = timezone.now() - timedelta(days=7)
    
    for item in items:
        if item.date_added >= one_week_ago or (item.last_changed and item.last_changed >= one_week_ago):
            count += 1
    
    return count
