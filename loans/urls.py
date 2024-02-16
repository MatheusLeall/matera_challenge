from django.urls import path
from loans.views import LoanListCreateView, PaymentListCreateView, RemainingBalanceView

urlpatterns = [
    path("emprestimos/", LoanListCreateView.as_view(), name="loan-list"),
    path("pagamentos/", PaymentListCreateView.as_view(), name="payment-list"),
    path("saldo-devedor/", RemainingBalanceView.as_view(), name="remaining-balance"),
]
