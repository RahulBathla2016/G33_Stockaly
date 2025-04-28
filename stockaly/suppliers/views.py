from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.http import HttpResponse
import csv
from datetime import datetime

from .models import Supplier, SupplierProduct, PurchaseOrder, PurchaseOrderItem
from .forms import SupplierForm, SupplierProductForm, PurchaseOrderForm, PurchaseOrderItemForm

@login_required
def supplier_dashboard(request):
    total_suppliers = Supplier.objects.count()
    active_suppliers = Supplier.objects.filter(status='active').count()
    total_products = SupplierProduct.objects.count()
    pending_orders = PurchaseOrder.objects.filter(status__in=['draft', 'submitted']).count()
    
    recent_suppliers = Supplier.objects.order_by('-date_added')[:5]
    recent_orders = PurchaseOrder.objects.order_by('-created_at')[:5]
    
    # Get supplier categories distribution
    categories = Supplier.objects.values('category').annotate(count=Count('id')).order_by('-count')
    
    context = {
        'total_suppliers': total_suppliers,
        'active_suppliers': active_suppliers,
        'total_products': total_products,
        'pending_orders': pending_orders,
        'recent_suppliers': recent_suppliers,
        'recent_orders': recent_orders,
        'categories': categories,
    }
    
    return render(request, 'suppliers/dashboard.html', context)

@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by('name')
    
    # Handle search
    search_query = request.GET.get('search', '')
    if search_query:
        suppliers = suppliers.filter(name__icontains=search_query) | suppliers.filter(company__icontains=search_query)
    
    # Handle filtering
    status_filter = request.GET.get('status', '')
    if status_filter:
        suppliers = suppliers.filter(status=status_filter)
        
    category_filter = request.GET.get('category', '')
    if category_filter:
        suppliers = suppliers.filter(category=category_filter)
    
    context = {
        'suppliers': suppliers,
        'search_query': search_query,
        'status_filter': status_filter,
        'category_filter': category_filter,
    }
    
    return render(request, 'suppliers/supplier_list.html', context)

@login_required
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier added successfully!')
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    
    return render(request, 'suppliers/supplier_form.html', {'form': form, 'title': 'Add Supplier'})

@login_required
def edit_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier updated successfully!')
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    
    return render(request, 'suppliers/supplier_form.html', {'form': form, 'title': 'Edit Supplier'})

@login_required
def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, 'Supplier deleted successfully!')
        return redirect('supplier_list')
    
    return render(request, 'suppliers/confirm_delete.html', {'supplier': supplier})

@login_required
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    products = supplier.products.all()
    purchase_orders = supplier.purchase_orders.all().order_by('-order_date')
    
    context = {
        'supplier': supplier,
        'products': products,
        'purchase_orders': purchase_orders,
    }
    
    return render(request, 'suppliers/supplier_detail.html', context)

@login_required
def add_supplier_product(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    
    if request.method == 'POST':
        form = SupplierProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.supplier = supplier
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('supplier_detail', pk=supplier.id)
    else:
        form = SupplierProductForm()
    
    return render(request, 'suppliers/product_form.html', {
        'form': form, 
        'title': f'Add Product for {supplier.name}',
        'supplier': supplier
    })

@login_required
def edit_supplier_product(request, pk):
    product = get_object_or_404(SupplierProduct, pk=pk)
    
    if request.method == 'POST':
        form = SupplierProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('supplier_detail', pk=product.supplier.id)
    else:
        form = SupplierProductForm(instance=product)
    
    return render(request, 'suppliers/product_form.html', {
        'form': form, 
        'title': f'Edit Product',
        'supplier': product.supplier
    })

@login_required
def delete_supplier_product(request, pk):
    product = get_object_or_404(SupplierProduct, pk=pk)
    supplier_id = product.supplier.id
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('supplier_detail', pk=supplier_id)
    
    return render(request, 'suppliers/confirm_delete_product.html', {'product': product})

@login_required
def purchase_order_list(request):
    orders = PurchaseOrder.objects.all().order_by('-order_date')
    
    # Handle search
    search_query = request.GET.get('search', '')
    if search_query:
        orders = orders.filter(order_number__icontains=search_query) | orders.filter(supplier__name__icontains=search_query)
    
    # Handle filtering
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    context = {
        'orders': orders,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    
    return render(request, 'suppliers/purchase_order_list.html', context)

@login_required
def add_purchase_order(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            messages.success(request, 'Purchase order created successfully!')
            return redirect('purchase_order_detail', pk=order.id)
    else:
        form = PurchaseOrderForm()
    
    return render(request, 'suppliers/purchase_order_form.html', {'form': form, 'title': 'Create Purchase Order'})

@login_required
def edit_purchase_order(request, pk):
    order = get_object_or_404(PurchaseOrder, pk=pk)
    
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Purchase order updated successfully!')
            return redirect('purchase_order_detail', pk=order.id)
    else:
        form = PurchaseOrderForm(instance=order)
    
    return render(request, 'suppliers/purchase_order_form.html', {'form': form, 'title': 'Edit Purchase Order'})

@login_required
def delete_purchase_order(request, pk):
    order = get_object_or_404(PurchaseOrder, pk=pk)
    
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Purchase order deleted successfully!')
        return redirect('purchase_order_list')
    
    return render(request, 'suppliers/confirm_delete_order.html', {'order': order})

@login_required
def purchase_order_detail(request, pk):
    order = get_object_or_404(PurchaseOrder, pk=pk)
    items = order.items.all()
    
    context = {
        'order': order,
        'items': items,
    }
    
    return render(request, 'suppliers/purchase_order_detail.html', context)

@login_required
def add_order_item(request, order_id):
    order = get_object_or_404(PurchaseOrder, pk=order_id)
    
    if request.method == 'POST':
        form = PurchaseOrderItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.purchase_order = order
            item.total_price = item.quantity * item.unit_price
            item.save()
            
            # Update order total
            order.total_amount = order.items.aggregate(total=Sum('total_price'))['total'] or 0
            order.save()
            
            messages.success(request, 'Item added to purchase order!')
            return redirect('purchase_order_detail', pk=order.id)
    else:
        # Only show products from the order's supplier
        form = PurchaseOrderItemForm()
        form.fields['product'].queryset = SupplierProduct.objects.filter(supplier=order.supplier)
    
    return render(request, 'suppliers/order_item_form.html', {
        'form': form, 
        'title': 'Add Item to Purchase Order',
        'order': order
    })

@login_required
def export_suppliers_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="suppliers_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Company', 'Email', 'Phone', 'Address', 'City', 'State', 'Zip', 'Country', 'Category', 'Status', 'Website'])
    
    suppliers = Supplier.objects.all().values_list(
        'name', 'company', 'email', 'phone', 'address', 'city', 'state', 'zip_code', 'country', 'category', 'status', 'website'
    )
    
    for supplier in suppliers:
        writer.writerow(supplier)
    
    return response