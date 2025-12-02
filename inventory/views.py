from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item
from .forms import ItemForm

@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            # Set status to PENDING for non-staff users
            if not request.user.is_staff:
                item.status = 'PENDING'
            item.save()
            
            if item.status == 'PENDING':
                messages.info(request, f"{item.name} has been submitted for approval.")
            else:
                messages.success(request, f"{item.name} has been listed successfully!")
            return redirect('my_items')
    else:
        form = ItemForm()
    
    return render(request, 'inventory/add_item.html', {'form': form, 'title': 'List a New Item'})

@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id, owner=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            # Reset to PENDING if edited by non-staff? Optional, but safer.
            # For now, let's keep existing status or maybe reset if critical fields change.
            # Simplicity: Don't reset status on edit for now, or maybe we should?
            # Let's keep it simple: if you edit it, it stays as is unless we decide otherwise.
            # Actually, to prevent abuse, maybe we should reset to PENDING?
            # Let's stick to the user request: "admin must accept a user input items before accepting it"
            # This implies new items.
            item.save()
            messages.success(request, f"{item.name} has been updated!")
            return redirect('my_items')
    else:
        form = ItemForm(instance=item)
    
    return render(request, 'inventory/add_item.html', {'form': form, 'title': f'Edit {item.name}'})

@login_required
def my_items(request):
    items = Item.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'inventory/my_items.html', {'items': items})

@login_required
def pending_items(request):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
    
    items = Item.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'inventory/pending_items.html', {'items': items})

@login_required
def approve_item(request, item_id):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('home')
        
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        print(f"Approving item: {item.name} (ID: {item.id})")
        item.status = 'AVAILABLE'
        item.save()
        messages.success(request, f"{item.name} has been approved and is now available!")
        return redirect('pending_items')
    
    return redirect('pending_items')
