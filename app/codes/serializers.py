from rest_framework import serializers

from codes.models import BrandCode


class BrandCodeInputSerializer(serializers.Serializer):
    """Serializer class for input data when creating codes for brand."""

    brand = serializers.CharField(max_length=100)
    count = serializers.IntegerField()
    discount_type = serializers.ChoiceField(
        choices=BrandCode.DiscountType.choices, default=BrandCode.DiscountType.AMOUNT
    )
    discount_value = serializers.DecimalField(max_digits=7, decimal_places=2)
    expiration_date = serializers.DateField(required=False)
    tags = serializers.CharField(required=False, max_length=100)


class BrandCodeSerializer(serializers.ModelSerializer):
    """Serializer class for response payload on code/s for brand."""

    code = serializers.StringRelatedField()

    class Meta:
        model = BrandCode
        fields = "__all__"
