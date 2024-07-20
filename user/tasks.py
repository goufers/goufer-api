from user.models import Booking
from celery import shared_task
from datetime import datetime
import time

@shared_task
def update_pro_gofers_availability_to_true_when_booking_end_time_expires():
    bookings = Booking.objects.all()
    for booking in bookings: 
        scheduled_date = datetime.strptime(booking.scheduled_date, '%Y-%m-%d').date()
        booking_end_time = time.strptime(booking.from_time, '%H:%M:%S')
        if datetime.now().date() > scheduled_date and time.time() > booking_end_time:
            booking.pro_gofer.is_available = True 
            booking.pro_gofer.save()
        
                
    
@shared_task     
def make_pro_gofers_unavailable_based_on_bookings_start_datetime():
    bookings = Booking.objects.all()
    for booking in bookings:
        if booking.status == 'accepted':
            scheduled_date = datetime.strptime(booking.scheduled_date, '%Y-%m-%d').date()
            booking_end_time = time.strptime(booking.from_time, '%H:%M:%S')
            if scheduled_date == datetime.now().date() and booking_end_time == time.time():
                booking.pro_gofer.is_available = False 
                booking.pro_gofer.save()
                
                

        
