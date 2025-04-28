from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
import csv
from datetime import datetime
from io import StringIO

from .models import InventoryItem, CustomUser
from .forms import CustomUserCreationForm, InventoryItemForm, InventoryItemEditForm

def home(request):
    return render(request, 'home.html')

def aboutus(request):
    return render(request, 'aboutus.html')

@login_required
def index(request):
    # Check if this is a new user's first login
    is_new_user = request.session.get('is_new_user', False)
    
    sort_by = request.GET.get('sort_by', 'date_added')
    order = request.GET.get('order', 'asc')
    search_query = request.GET.get('search', '')
    
    # Filter items by the current user
    query = InventoryItem.objects.filter(user=request.user)
    
    if search_query:
        query = query.filter(
            Q(item_name__icontains=search_query) |
            Q(item_number__icontains=search_query) |
            Q(quantity__icontains=search_query) |
            Q(price__icontains=search_query)
        )
    
    # Apply sorting
    if sort_by == 'item_name':
        order_by = 'item_name' if order == 'asc' else '-item_name'
    elif sort_by == 'item_number':
        order_by = 'item_number' if order == 'asc' else '-item_number'
    elif sort_by == 'quantity':
        order_by = 'quantity' if order == 'asc' else '-quantity'
    elif sort_by == 'price':
        order_by = 'price' if order == 'asc' else '-price'
    else:
        order_by = 'date_added' if order == 'asc' else '-date_added'
    
    items = query.order_by(order_by)
    
    context = {
        'items': items,
        'mode': 'index',
        'sort_by': sort_by,
        'order': order,
        'search_query': search_query,
        'form': InventoryItemForm(),
        'is_new_user': is_new_user
    }
    
    # Clear the new user flag after first view
    if is_new_user:
        request.session['is_new_user'] = False
    
    return render(request, 'index.html', context)

@login_required
def add_item(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            # Save the form but don't commit to database yet
            item = form.save(commit=False)
            # Assign the current user to the item
            item.user = request.user
            # Now save to database
            item.save()
            messages.success(request, 'Item added successfully!')
            return redirect('index')
        else:
            messages.error(request, 'Error adding item. Please check the form.')
    
    return redirect('index')

@login_required
def view_item(request, id):
    # Only allow viewing items that belong to the current user
    item = get_object_or_404(InventoryItem, id=id, user=request.user)
    return render(request, 'view_item.html', {'item': item})

@login_required
def edit_item(request, id):
    # Only allow editing items that belong to the current user
    item = get_object_or_404(InventoryItem, id=id, user=request.user)
    
    if request.method == 'POST':
        form = InventoryItemEditForm(request.POST, instance=item)
        if form.is_valid():
            # Check if anything changed
            cleaned_data = form.cleaned_data
            if (cleaned_data['item_number'] == item.item_number and
                cleaned_data['item_name'] == item.item_name and
                cleaned_data['quantity'] == item.quantity and
                cleaned_data['price'] == item.price and
                cleaned_data['date_added'] == item.date_added):
                messages.info(request, 'Nothing has been changed')
            else:
                updated_item = form.save(commit=False)
                updated_item.last_changed = timezone.now()
                updated_item.save()
                messages.success(request, 'Item updated successfully!')
            
            return redirect('index')
        else:
            messages.error(request, 'Error updating item. Please check the form.')
    else:
        form = InventoryItemEditForm(instance=item)
    
    return render(request, 'index.html', {'item': item, 'mode': 'edit', 'form': form})

@login_required
def delete_item(request, id):
    # Only allow deleting items that belong to the current user
    item = get_object_or_404(InventoryItem, id=id, user=request.user)
    item.delete()
    messages.success(request, 'Item deleted successfully!')
    return redirect('index')

@login_required
def export_csv(request):
    # Only export items that belong to the current user
    items = InventoryItem.objects.filter(user=request.user)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date Added', 'Item Name', 'Item Number', 'Quantity', 'Price', 'Last Changed'])
    
    for item in items:
        date_added = item.date_added.strftime('%Y/%m/%d')
        last_changed = item.last_changed.strftime('%Y/%m/%d') if item.last_changed else ''
        writer.writerow([date_added, item.item_name, item.item_number, item.quantity, item.price, last_changed])
    
    return response

def role_required(request, role):
    if not request.user.is_authenticated or request.user.role != role:
        messages.error(request, "Unauthorized Access")
        return False
    return True

@login_required
def admin_dashboard(request):
    if not role_required(request, "admin"):
        return redirect('index')
    
    sort_by = request.GET.get('sort_by', 'date_added')
    order = request.GET.get('order', 'asc')
    search_query = request.GET.get('search', '')
    user_filter = request.GET.get('user_filter', 'all')
    
    # Get all users for the filter dropdown
    all_users = CustomUser.objects.all()
    
    # Base query - start with all items if admin
    query = InventoryItem.objects.all()
    
    # Filter by user if specified
    if user_filter != 'all':
        query = query.filter(user_id=user_filter)
    
    # Apply search filter if provided
    if search_query:
        query = query.filter(
            Q(item_name__icontains=search_query) |
            Q(item_number__icontains=search_query) |
            Q(quantity__icontains=search_query) |
            Q(price__icontains=search_query)
        )
    
    # Apply sorting
    if sort_by == 'item_name':
        order_by = 'item_name' if order == 'asc' else '-item_name'
    elif sort_by == 'item_number':
        order_by = 'item_number' if order == 'asc' else '-item_number'
    elif sort_by == 'quantity':
        order_by = 'quantity' if order == 'asc' else '-quantity'
    elif sort_by == 'price':
        order_by = 'price' if order == 'asc' else '-price'
    elif sort_by == 'user':
        order_by = 'user__username' if order == 'asc' else '-user__username'
    else:
        order_by = 'date_added' if order == 'asc' else '-date_added'
    
    items = query.order_by(order_by)
    user_count = CustomUser.objects.count()
    
    context = {
        'items': items,
        'mode': 'admin',
        'sort_by': sort_by,
        'order': order,
        'search_query': search_query,
        'user_filter': user_filter,
        'all_users': all_users,
        'user_count': user_count
    }
    
    return render(request, 'admin_dashboard.html', context)

# Admin view item function

# @login_required
# def admin_view_item(request, id):
#     if not role_required(request, "admin"):
#         return redirect('index')

#     item = get_object_or_404(InventoryItem, id=id)
#     return render(request, 'admin_view_item.html', {'item': item})


# Admin edit item function
@login_required
def admin_edit_item(request, id):
    if not role_required(request, "admin"):
        return redirect('index')

    item = get_object_or_404(InventoryItem, id=id)

    if request.method == 'POST':
        form = InventoryItemEditForm(request.POST, instance=item)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            if (cleaned_data['item_number'] == item.item_number and
                cleaned_data['item_name'] == item.item_name and
                cleaned_data['quantity'] == item.quantity and
                cleaned_data['price'] == item.price and
                cleaned_data['date_added'] == item.date_added):
                messages.info(request, 'Nothing has been changed')
            else:
                updated_item = form.save(commit=False)
                updated_item.last_changed = timezone.now()
                updated_item.save()
                messages.success(request, 'Item updated successfully!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Error updating item. Please check the form.')
    else:
        form = InventoryItemEditForm(instance=item)

    return render(request, 'admin_edit_item.html', {'form': form, 'item': item})



# Admin delete item function
@login_required
def admin_delete_item(request, id):
    if not role_required(request, "admin"):
        return redirect('index')
    
    item = get_object_or_404(InventoryItem, id=id)
    item.delete()
    messages.success(request, 'Item deleted successfully!')
    return redirect('admin_dashboard')

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "User registered successfully.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Check if this is a new user (created within the last 5 minutes)
            is_new_user = (timezone.now() - user.date_joined).total_seconds() < 300
            request.session['is_new_user'] = is_new_user
            
            if user.role == "admin":
                messages.success(request, "Admin logged in successfully.")
                return redirect('admin_dashboard')
            else:
                messages.success(request, "User logged in successfully.")
                return redirect('index')
        else:
            messages.error(request, "Invalid credentials.")
    
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "User Logged Out Successfully")
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

