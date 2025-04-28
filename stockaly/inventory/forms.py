from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, InventoryItem

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['item_name', 'item_number', 'quantity', 'price']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'item_number': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
        }
        
    # Exclude user field from the form as it will be set in the view

class InventoryItemEditForm(forms.ModelForm):
    date_added = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date'}
    ))
    
    class Meta:
        model = InventoryItem
        fields = ['date_added', 'item_name', 'item_number', 'quantity', 'price']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'item_number': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'id': 'edit_quantity'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01', 'id': 'edit_price'}),
        }
        
    # Exclude user field from the form as it will be preserved in the view
