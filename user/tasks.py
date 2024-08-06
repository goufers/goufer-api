from user.models import Booking
from celery import shared_task
from datetime import datetime



@shared_task
def update_pro_gofers_availability_to_true_when_booking_end_time_expires():
    current_date = datetime.now().date().strftime('%Y-%m-%d')
    current_time = datetime.now().time().strftime('%H:%M:%S')
    bookings = Booking.objects.filter(status='accepted', scheduled_date=current_date, to_time__lt=current_time,)
    for booking in bookings: 
        booking.pro_gofer.is_available = True 
        booking.pro_gofer.save()
       
       
            
        
                
    
@shared_task     
def make_pro_gofers_unavailable_based_on_bookings_start_datetime():
    current_date = datetime.now().date().strftime('%Y-%m-%d')
    current_time = datetime.now().time().strftime('%H:%M:%S')
    bookings = Booking.objects.filter(status='accepted', scheduled_date=current_date, from_time=current_time)
    for booking in bookings:
        booking.pro_gofer.is_available = False 
        booking.pro_gofer.save()
            

            
                
                
                

        
