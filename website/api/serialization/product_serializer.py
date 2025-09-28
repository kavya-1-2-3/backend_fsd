from rest_framework import serializers
from website.models import Product, Review
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields='__all__'
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # show username/email instead of id

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["user", "product", "created_at"]
