from django.db import models
from django.conf import settings

class Supplier(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('food', 'Food & Beverages'),
        ('office', 'Office Supplies'),
        ('furniture', 'Furniture'),
        ('raw_materials', 'Raw Materials'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending Approval'),
        ('blacklisted', 'Blacklisted'),
    ]
    
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    website = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class SupplierProduct(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=100)
    product_code = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order_quantity = models.PositiveIntegerField(default=1)
    lead_time_days = models.PositiveIntegerField(default=7)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.product_name} ({self.supplier.name})"

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchase_orders')
    order_number = models.CharField(max_length=50, unique=True)
    order_date = models.DateField()
    expected_delivery_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_address = models.TextField()
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"PO-{self.order_number} - {self.supplier.name}"

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(SupplierProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.product.product_name} - {self.quantity} units"