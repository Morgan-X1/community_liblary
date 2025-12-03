from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from inventory.models import Item, Category
from loans.forms import ReservationForm
from loans.services import create_reservation, is_item_available
from users.models import User
from loans.models import Reservation

def landing_page(request):
    return render(request, 'core/landing.html')

def catalog(request):
    category_id = request.GET.get('category')
    if category_id:
        items = Item.objects.filter(category_id=category_id, status='AVAILABLE')
    else:
        items = Item.objects.filter(status='AVAILABLE')
    
    from datetime import date
    today = date.today()
    
    # Check availability for each item
    # Note: For a large catalog, this should be optimized with annotations/subqueries
    for item in items:
        item.is_booked = Reservation.objects.filter(
            item=item,
            start_date__lte=today,
            end_date__gte=today,
            status__in=['PENDING', 'ACTIVE']
        ).exists()

    categories = Category.objects.all()
    return render(request, 'inventory/catalog.html', {
        'items': items,
        'categories': categories,
        'current_category': int(category_id) if category_id else None
    })

from datetime import date

def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    
    # Check if currently on loan
    today = date.today()
    current_reservation = Reservation.objects.filter(
        item=item,
        start_date__lte=today,
        end_date__gte=today,
        status__in=['PENDING', 'ACTIVE']
    ).first()
    
    return render(request, 'inventory/item_detail.html', {
        'item': item,
        'current_reservation': current_reservation
    })

@login_required
def reserve_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            try:
                create_reservation(request.user, item, start_date, end_date)
                messages.success(request, f"Reservation created for {item.name}!")
                return redirect('dashboard')
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = ReservationForm()
    
    return render(request, 'loans/reserve_item.html', {
        'form': form,
        'item': item
    })

@login_required
def dashboard(request):
    reservations = request.user.reservations.all().order_by('-created_at')
    return render(request, 'users/dashboard.html', {'reservations': reservations})

@login_required(login_url='admin_login')
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Please log in with an administrator account.")
        return redirect('admin_login')
    
    # Gather stats
    total_users = User.objects.count()
    total_items = Item.objects.count()
    pending_items_count = Item.objects.filter(status='PENDING').count()
    active_loans = Reservation.objects.filter(status='ACTIVE').count()
    
    context = {
        'total_users': total_users,
        'total_items': total_items,
        'pending_items_count': pending_items_count,
        'active_loans': active_loans,
    }
    return render(request, 'core/admin_dashboard.html', context)

def create_admin_user(request):
    # SECURITY: This is a temporary workaround for Render's paid shell.
    # It should be removed after use.
    if request.user.is_authenticated and request.user.is_superuser:
        return HttpResponse("Admin already exists and you are logged in.")

    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Check if any superuser exists to prevent abuse
    if User.objects.filter(is_superuser=True).exists():
        return HttpResponse("A superuser already exists. Login with that account.")

    try:
        # Create a default superuser
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        return HttpResponse("Superuser 'admin' created! Password is 'admin123'. Please login and change it immediately.")
    except Exception as e:
        return HttpResponse(f"Error creating superuser: {str(e)}")
