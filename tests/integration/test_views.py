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


@pytest.fixture
def api_client():
    return APIRequestFactory()


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def token(user):
    return Token.objects.create(user=user)


@pytest.fixture
def loan(user):
    return Loan.objects.create(
        nominal_value=1000,
        interest_rate=0.05,
        ip_address="127.0.0.1",
        bank="Banco Teste",
        client=user,
    )


@pytest.mark.django_db
class TestLoanView:
    def test_should_return_401_unauthorized_when_credentials_is_not_provided(
        self, api_client, user
    ):
        # Arrange
        view = LoanListCreateView.as_view()
        url = reverse("loans")

        # Act
        request = api_client.post(url, data={"test": "data"}, format="json")
        response = view(request)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_return_201_created_when_create_loan(self, api_client, user, token):
        # Arrange
        view = LoanListCreateView.as_view()
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
        request = api_client.post(
            url, data, format="json", HTTP_AUTHORIZATION=f"Token {token.key}"
        )
        response = view(request)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert Loan.objects.count() == 1

    def test_should_return_200_ok_when_get_loan_information(
        self, api_client, user, token, loan
    ):
        # Arrange
        view = LoanListCreateView.as_view()
        url = reverse("loans")

        headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}

        # Act
        request = api_client.get(url, format="json", **headers)
        response = view(request, pk=loan.id)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1


@pytest.mark.django_db
class TestPaymentView:
    def test_should_return_401_unauthorized_when_credentials_is_not_provided(
        self, api_client, user, token
    ):
        # Arrange
        view = PaymentListCreateView.as_view()
        url = reverse("payments")

        # Act
        request = api_client.post(url, data={"test": "data"}, format="json")
        response = view(request)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_return_400_bad_request_when_payment_value_grather_than_remaining_balance(
        self, api_client, user, token, loan
    ):
        # Arrange
        view = PaymentListCreateView.as_view()
        url = reverse("payments")

        data = {
            "payment_date": date.today(),
            "payment_value": 2000,
            "loan": loan.pk,
        }

        # Act
        request = api_client.post(
            url, data, format="json", HTTP_AUTHORIZATION=f"Token {token.key}"
        )
        response = view(request)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_return_400_bad_request_if_payment_value_less_than_zero(
        self, api_client, user, token, loan
    ):
        # Arrange
        view = PaymentListCreateView.as_view()
        url = reverse("payments")

        data = {
            "payment_date": date.today(),
            "payment_value": -2000,
            "loan": loan.pk,
        }

        # Act
        request = api_client.post(
            url, data, format="json", HTTP_AUTHORIZATION=f"Token {token.key}"
        )
        response = view(request)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "payment_value": ["Ensure this value is greater than or equal to 0.0."]
        }

    def test_should_return_201_created_when_create_payment(
        self, api_client, user, token, loan
    ):
        # Arrange
        view = PaymentListCreateView.as_view()
        url = reverse("payments")

        data = {
            "payment_date": date.today(),
            "payment_value": 250,
            "loan": loan.pk,
        }

        # Act
        request = api_client.post(
            url, data, format="json", HTTP_AUTHORIZATION=f"Token {token.key}"
        )
        response = view(request)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert Payment.objects.count() == 1

    def test_should_return_200_ok_when_get_payment_information(
        self, api_client, user, token, loan
    ):
        # Arrange
        Payment.objects.create(payment_date=date.today(), payment_value=175, loan=loan)

        view = PaymentListCreateView.as_view()
        url = reverse("payments")

        headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}

        # Act
        request = api_client.get(url, format="json", **headers)
        response = view(request, pk=loan.id)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1


@pytest.mark.django_db
class TestRemainingBalanceView:
    def test_should_return_401_unauthorized_when_credentials_is_not_provided(
        self, api_client, user, token
    ):
        # Arrange
        view = PaymentListCreateView.as_view()
        url = reverse(
            "remaining-balance", kwargs={"id": "d253ed71-c8df-4e90-9247-6aa3c539987d"}
        )

        # Act
        request = api_client.post(url, format="json")
        response = view(request)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_return_403_forbidden_when_user_not_authorized(
        self, api_client, token, loan
    ):
        # Arrange
        loan = Loan.objects.create(
            nominal_value=1000,
            interest_rate=0.05,
            ip_address="127.0.0.1",
            bank="Banco Teste",
            client=User.objects.create_user(username="otheruser", password="otherpass"),
        )

        view = RemainingBalanceView.as_view()
        url = reverse("remaining-balance", kwargs={"id": loan.pk})

        headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}

        # Act
        request = api_client.get(url, format="json", **headers)
        response = view(request, id=loan.id)

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data == {
            "error": "You do not have permission to access the resource"
        }

    def test_should_return_200_ok_when_user_get_remaining_balance(
        self, api_client, user, token, loan
    ):
        # Arrange
        payment = Payment.objects.create(
            payment_date=date.today(), payment_value=175, loan=loan
        )

        view = RemainingBalanceView.as_view()
        url = reverse("remaining-balance", kwargs={"id": loan.pk})

        headers = {"HTTP_AUTHORIZATION": f"Token {token.key}"}

        # Act
        request = api_client.get(url, format="json", **headers)
        response = view(request, id=loan.id)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["remaining_balance"]
            == loan.nominal_value - payment.payment_value
        )
