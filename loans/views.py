from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from loans.models import Loan
from loans.models import Payment
from loans.serializers import LoanSerializer
from loans.serializers import PaymentSerializer


class LoanListCreateView(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class RemainingBalanceView(generics.RetrieveAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        loan = Loan.objects.get(client=self.request.user, id=self.kwargs["pk"])
        return loan
