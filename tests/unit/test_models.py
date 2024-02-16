from datetime import date

import pytest

from django.contrib.auth.models import User

from loans.models import Loan
from loans.models import Payment


@pytest.mark.django_db
class TestModels:
    TEST_IP_ADDRESS: str = "127.0.0.1"

    def test_should_create_loan(self):
        REMAINIG_BALANCE = 1000
        user = User.objects.create_user(username="testuser", password="testpass")

        loan = Loan.objects.create(
            nominal_value=REMAINIG_BALANCE,
            interest_rate=0.05,
            ip_address=self.TEST_IP_ADDRESS,
            request_date=date.today(),
            bank="Test Bank",
            client=user,
        )

        assert loan.id is not None
        assert loan.calculate_remaining_balance() == REMAINIG_BALANCE

    def test_payment_creation(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        loan = Loan.objects.create(
            nominal_value=25000,
            interest_rate=0.08,
            ip_address=self.TEST_IP_ADDRESS,
            request_date=date.today(),
            bank="Test Bank II",
            client=user,
        )

        payment = Payment.objects.create(
            loan=loan,
            payment_date=date.today(),
            payment_value=500,
        )

        assert payment.id is not None
