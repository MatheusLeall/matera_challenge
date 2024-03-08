import uuid

from datetime import date

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum


class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nominal_value = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    ip_address = models.GenericIPAddressField()
    request_date = models.DateField(auto_now_add=True)
    bank = models.CharField(max_length=255)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    iof_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def calculate_remaining_balance(self) -> float:
        total_payed = (
            Payment.objects.filter(loan=self).aggregate(Sum("payment_value"))[
                "payment_value__sum"
            ]
            or 0
        )
        days_passed = (date.today() - self.request_date).days
        accumulated_rates = (
            (self.interest_rate / 30) * days_passed * (self.nominal_value - total_payed)
        )
        iof_cost = self.iof_rate * self.nominal_value
        remaining_balance = (
            self.nominal_value + accumulated_rates + iof_cost - total_payed
        )
        return round(remaining_balance, 2)

    def __str__(self):
        return f"{self.client.username} - {self.id}"


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_date = models.DateField()
    payment_value = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)]
    )

    def __str__(self):
        return f"{self.loan.client.username} - {self.id}"
