from user.models import Booking
from celery import shared_task
from datetime import datetime


@shared_task
def update_pro_gofers_availability_to_true_when_booking_end_time_expires():
    current_time = datetime.now().time().strftime('%H:%M:%S')
    current_date = datetime.now().date()
    bookings = Booking.objects.filter(status='accepted', scheduled_date=current_date, to_time__lt=current_time,)
    for booking in bookings: 
        booking.pro_gofer.is_available = True 
        booking.pro_gofer.save()
       
            
        
                
    
@shared_task     
def make_pro_gofers_unavailable_based_on_bookings_start_datetime():
    bookings = Booking.objects.filter(status='accepted')
    for booking in bookings:
        scheduled_date = datetime.strptime(booking.scheduled_date, '%Y-%m-%d').date()
        booking_start_time = booking.from_time
        if scheduled_date == datetime.now().date() and booking_start_time == datetime.now().time().strftime('%H:%M:%S'):
            booking.pro_gofer.is_available = False 
            booking.pro_gofer.save()
                
                
                

        
