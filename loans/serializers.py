from rest_framework import serializers

from loans.models import Loan
from loans.models import Payment


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class RemainingBalanceSerializer(serializers.ModelSerializer):
    remaining_balance = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ["id", "nominal_value", "request_date", "remaining_balance"]

    def get_remaining_balance(self, obj):
        return obj.calculate_remaining_balance()
