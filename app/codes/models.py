import uuid

from django.db import models


class Code(models.Model):
    """Model to store already generated code list."""

    code_value = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.code_value


class BrandCode(models.Model):
    """Model to store code list per brand."""

    class DiscountType(models.TextChoices):
        """Discount type enum values."""

        PERCENTAGE = "PERCENTAGE"
        AMOUNT = "AMOUNT"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.CharField(max_length=500)
    assigned_to = models.CharField(max_length=500, blank=True, null=True)
    code = models.ForeignKey(Code, on_delete=models.CASCADE)
    discount_type = models.CharField(max_length=50, choices=DiscountType.choices)
    discount_value = models.DecimalField(max_digits=7, decimal_places=2)
    expiration_date = models.DateField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_redeemed = models.BooleanField(default=False)
    redeemed_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.brand_ref} - {self.code}"


class CodeCursor(models.Model):
    """Model to find last pulled code from Code list."""

    brand = models.CharField(max_length=500)
    last_code = models.ForeignKey(Code, on_delete=models.CASCADE)
