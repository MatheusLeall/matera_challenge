from datetime import date

import pytest

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory

from loans.models import Loan
from loans.models import Payment
from loans.views import LoanListCreateView
from loans.views import PaymentListCreateView
from loans.views import RemainingBalanceView


@pytest.mark.django_db
class TestLoanView:
    def test_should_return_401_unauthorized_when_credentials_is_not_provided(self):
        # Arrange
        User.objects.create_user(username="testuser", password="testpass")

        view = LoanListCreateView.as_view()
        factory = APIRequestFactory()
        url = reverse("loans")

        # Act
        request = factory.post(url, data={"test": "data"}, format="json")
        response = view(request)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_return_201_created_when_create_loan(self):
        # Arrange
        user = User.objects.create_user(username="testuser", password="testpass")
        token = Token.objects.create(user=user)

        view = LoanListCreateView.as_view()
        factory = APIRequestFactory()
        url = reverse("loans")

        data = {
            "nominal_value": 1000,
            "interest_rate": 0.05,
            "ip_address": "127.0.0.1",
            "request_date": str(date.today()),
            "bank": "Test Bank",
            "client": user.pk,
        }

        # Act
        request = factory.post(
            url, data, format="json", HTTP_AUTHORIZATION=f"Token {token.key}"
        )
        response = view(request)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert Loan.objects.count() == 1

    def test_should_return_200_ok_when_get_loan_information(self):
        # Arrange
        user = User.objects.create_user(username="testuser", password="testpass")
        token = Token.objects.create(user=user)

        loan = Loan.objects.create(
            nominal_value=1000,
            interest_rate=0.05,
            ip_address="127.0.0.1",
            bank="Banco Teste",
            client=user,
        )

        view = LoanListCreateView.as_view()
        factory = APIRequestFactory()
        url = reverse("loans")

        headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}

        # Act
        request = factory.get(url, format="json", **headers)
        response = view(request, pk=loan.id)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1


@pytest.mark.django_db
class TestPaymentView:
    def test_should_return_401_unauthorized_when_credentials_is_not_provided(self):
        # Arrange
        User.objects.create_user(username="testuser", password="testpass")

        view = PaymentListCreateView.as_view()
        factory = APIRequestFactory()
        url = reverse("payments")

        # Act
        request = factory.post(url, data={"test": "data"}, format="json")
        response = view(request)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_return_201_created_when_create_payment(self):
        # Arrange
        user = User.objects.create_user(username="testuser", password="testpass")
        token = Token.objects.create(user=user)
        loan = Loan.objects.create(
            nominal_value=1000,
            interest_rate=0.05,
            ip_address="127.0.0.1",
            bank="Banco Teste",
            client=user,
        )

        view = PaymentListCreateView.as_view()
        factory = APIRequestFactory()
        url = reverse("payments")

        data = {
            "payment_date": date.today(),
            "payment_value": 250,
            "loan": loan.pk,
        }

        # Act
        request = factory.post(
            url, data, format="json", HTTP_AUTHORIZATION=f"Token {token.key}"
        )
        response = view(request)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert Payment.objects.count() == 1

    def test_should_return_200_ok_when_get_payment_information(self):
        # Arrange
        user = User.objects.create_user(username="testuser", password="testpass")
        token = Token.objects.create(user=user)

        loan = Loan.objects.create(
            nominal_value=1000,
            interest_rate=0.05,
            ip_address="127.0.0.1",
            bank="Banco Teste",
            client=user,
        )

        Payment.objects.create(payment_date=date.today(), payment_value=175, loan=loan)

        view = PaymentListCreateView.as_view()
        factory = APIRequestFactory()
        url = reverse("payments")

        headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}

        # Act
        request = factory.get(url, format="json", **headers)
        response = view(request, pk=loan.id)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1


@pytest.mark.django_db
class TestRemainingBalanceView:
    def test_should_return_401_unauthorized_when_credentials_is_not_provided(self):
        # Arrange
        User.objects.create_user(username="testuser", password="testpass")

        view = PaymentListCreateView.as_view()
        factory = APIRequestFactory()
        url = reverse(
            "remaining-balance", kwargs={"id": "d253ed71-c8df-4e90-9247-6aa3c539987d"}
        )

        # Act
        request = factory.post(url, format="json")
        response = view(request)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_return_403_forbidden_when_user_not_authorized(self):
        # Arrange
        user = User.objects.create_user(username="testuser", password="testpass")
        token = Token.objects.create(user=user)

        loan = Loan.objects.create(
            nominal_value=1000,
            interest_rate=0.05,
            ip_address="127.0.0.1",
            bank="Banco Teste",
            client=User.objects.create_user(username="otheruser", password="otherpass"),
        )

        view = RemainingBalanceView.as_view()
        factory = APIRequestFactory()
        url = reverse("remaining-balance", kwargs={"id": loan.pk})

        headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}

        # Act
        request = factory.get(url, format="json", **headers)
        response = view(request, id=loan.id)

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == {
            "error": "Você não tem permissão para acessar este recurso."
        }

    def test_should_return_200_ok_when_user_get_remaining_balance(self):
        # Arrange
        user = User.objects.create_user(username="testuser", password="testpass")
        token = Token.objects.create(user=user)

        loan = Loan.objects.create(
            nominal_value=1000,
            interest_rate=0.05,
            ip_address="127.0.0.1",
            bank="Banco Teste",
            client=user,
        )

        payment = Payment.objects.create(
            payment_date=date.today(), payment_value=175, loan=loan
        )

        view = RemainingBalanceView.as_view()
        factory = APIRequestFactory()
        url = reverse("remaining-balance", kwargs={"id": loan.pk})

        headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}

        # Act
        request = factory.get(url, format="json", **headers)
        response = view(request, id=loan.id)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["remaining_balance"]
            == loan.nominal_value - payment.payment_value
        )
