from django.urls import path
from . import views

urlpatterns = [
    path('fund_wallet/', views.FundWalletView.as_view(), name='fund_wallet'),
    path('create_transfer_recipient/', views.CreateTransferRecipientView.as_view(), name='create_transfer_recipient'),
    path('transfer_funds/', views.TransferFundsView.as_view(), name='transfer_funds'),
]
