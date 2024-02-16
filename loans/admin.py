from django.contrib import admin

from loans.models import Loan
from loans.models import Payment


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nominal_value",
        "interest_rate",
        "ip_address",
        "request_date",
        "bank",
        "client",
    )
    search_fields = ("client__username", "id")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "loan", "payment_date", "payment_value")
    search_fields = ("loan__client__username", "id")
