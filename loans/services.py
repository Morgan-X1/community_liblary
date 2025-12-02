from django.db.models import Q
from .models import Reservation

def is_item_available(item, start_date, end_date):
    """
    Check if an item is available for a given date range.
    Returns True if available, False otherwise.
    """
    overlapping_reservations = Reservation.objects.filter(
        item=item,
        status__in=['PENDING', 'ACTIVE'],
    ).filter(
        Q(start_date__lte=end_date) & Q(end_date__gte=start_date)
    )
    
    return not overlapping_reservations.exists()

def create_reservation(user, item, start_date, end_date):
    """
    Create a reservation if the item is available.
    Raises ValueError if item is not available.
    """
    if not is_item_available(item, start_date, end_date):
        raise ValueError("Item is not available for the selected dates.")
    
    reservation = Reservation.objects.create(
        user=user,
        item=item,
        start_date=start_date,
        end_date=end_date,
        status='PENDING'
    )
    return reservation
