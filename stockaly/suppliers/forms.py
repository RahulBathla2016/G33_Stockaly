from django import forms
from .models import Supplier, SupplierProduct, PurchaseOrder, PurchaseOrderItem

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'company', 'email', 'phone', 'address', 'city', 'state', 
                  'zip_code', 'country', 'category', 'status', 'website', 'notes']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class SupplierProductForm(forms.ModelForm):
    class Meta:
        model = SupplierProduct
        fields = ['product_name', 'product_code', 'description', 'unit_price', 
                  'minimum_order_quantity', 'lead_time_days', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'order_number', 'order_date', 'expected_delivery_date', 
                  'status', 'total_amount', 'shipping_address', 'notes']
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_delivery_date': forms.DateInput(attrs={'type': 'date'}),
            'shipping_address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class PurchaseOrderItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = ['product', 'quantity', 'unit_price']