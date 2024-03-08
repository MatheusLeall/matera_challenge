from rest_framework import serializers

from loans.models import Loan
from loans.models import Payment


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        exclude = ["id"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation = {"results": representation}

        return representation


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["loan", "payment_date", "payment_value"]

    def validate_payment_value(self, value):
        loan_id = self.initial_data.get("loan")
        if not loan_id:
            raise serializers.ValidationError("Loan is required.")

        try:
            loan = Loan.objects.get(pk=loan_id)
        except Loan.DoesNotExist:
            raise serializers.ValidationError("Loan does not exist.")

        remaining_balance = loan.calculate_remaining_balance()

        if value > remaining_balance:
            raise serializers.ValidationError(
                "Payment amount greater than remaining balance."
            )

        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation = {"results": representation}

        return representation


class RemainingBalanceSerializer(serializers.ModelSerializer):
    remaining_balance = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ["id", "nominal_value", "request_date", "remaining_balance"]

    def get_remaining_balance(self, obj):
        return obj.calculate_remaining_balance()
