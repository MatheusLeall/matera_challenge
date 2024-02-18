from django.urls import path

from loans.views import LoanListCreateView
from loans.views import PaymentListCreateView
from loans.views import RemainingBalanceView

urlpatterns = [
    path("loans/", LoanListCreateView.as_view(), name="loans"),
    path("payments/", PaymentListCreateView.as_view(), name="payments"),
    path(
        "remaining_balance/<uuid:id>/",
        RemainingBalanceView.as_view(),
        name="remaining-balance",
    ),
]
