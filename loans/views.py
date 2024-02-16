from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from loans.models import Loan
from loans.models import Payment
from loans.serializers import LoanSerializer
from loans.serializers import PaymentSerializer


class LoanListCreateView(generics.ListCreateAPIView):
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    def get_queryset(self):
        return Loan.objects.filter(client=self.request.user)


class PaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(loan__cliente=self.request.user)


class RemainingBalanceView(generics.RetrieveAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        loan = Loan.objects.filter(client=self.request.user, id=self.kwargs["pk"])
        return loan
