from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'hours', views.HourViewSet)
router.register(r'days', views.DayViewSet)
router.register(r'schedules', views.ScheduleViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('fund_wallet/', views.FundWalletView.as_view(), name='fund_wallet'),
    path('create_transfer_recipient/', views.CreateTransferRecipientView.as_view(), name='create_transfer_recipient'),
    path('transfer_funds/', views.TransferFundsView.as_view(), name='transfer_funds'),
]
