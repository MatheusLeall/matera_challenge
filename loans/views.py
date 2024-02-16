from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
        return Payment.objects.filter(loan__client=self.request.user)


class RemainingBalanceView(generics.RetrieveAPIView):
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Checks if the loan belongs to the authenticated user
        if instance.client != request.user:
            return Response(
                {"error": "Você não tem permissão para acessar este recurso."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Calculates the remaining balance using the model method
        remaining_balance = instance.calculate_remaining_balance()

        serializer = self.get_serializer(instance)
        data = serializer.data
        data["remaining_balance"] = remaining_balance

        return Response(data)
