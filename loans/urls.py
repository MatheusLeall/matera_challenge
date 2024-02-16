from django.urls import path

from loans.views import LoanListCreateView
from loans.views import PaymentListCreateView
from loans.views import RemainingBalanceView

urlpatterns = [
    path("loans/", LoanListCreateView.as_view(), name="loan-list"),
    path("payments/", PaymentListCreateView.as_view(), name="payment-list"),
    path("remainig_balance/", RemainingBalanceView.as_view(), name="remaining-balance"),
]