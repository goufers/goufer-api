from . import views
from django.urls import path, include

urlpatterns = [
    path('fund_wallet/', views.FundWalletView.as_view(), name='fund_wallet'),
    path('create_transfer_recipient/', views.CreateTransferRecipientView.as_view(), name='create_transfer_recipient'),
    path('transfer_funds/', views.TransferFundsView.as_view(), name='transfer_funds'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('schedules/', views.ScheduleListView.as_view(), name='schedule-list'),
    path('schedules/create/', views.ScheduleCreateView.as_view(), name='schedule-create'),
    path('bookings/', views.BookingListView.as_view(), name='booking-create'),
    path('bookings/create/', views.BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/update/', views.BookingUpdateView.as_view(), name='booking-update'),
    path('bookings/<int:pk>/cancel/', views.BookingCancelView.as_view(), name='booking-cancel'),
    path('bookings/accept/', views.BookingAcceptView.as_view(), name='booking-accept'),
    path('bookings/decline/', views.BookingDeclineView.as_view(), name='booking-decline'),
]
