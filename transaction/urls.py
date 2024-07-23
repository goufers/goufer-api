from . import views
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name='transaction/index.html')),
    path('fund_wallet/', views.FundWalletView.as_view(), name='fund_wallet'),
    path('create_transfer_recipient/', views.CreateTransferRecipientView.as_view(), name='create_transfer_recipient'),
    path('transfer_funds/', views.TransferFundsView.as_view(), name='transfer_funds'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list')
]
