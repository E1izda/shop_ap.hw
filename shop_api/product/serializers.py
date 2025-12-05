from rest_framework import serializers
from .models import Category, Product, Review
from django.db.models import Avg, Count
from rest_framework.exceptions import ValidationError

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)\
    
    def validate(self, attrs):
        request = self.context.get('request')
        if request is None:
            raise serializers.ValidationError("Request не передан в сериализатор.")

        from common.validators import validate_user_age
        validate_user_age(request.user)

        return attrs

    class Meta:
        model = Product
        fields = '__all__'


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=2, max_length=250)


    class Meta:
        model = Product
        fields = '__all__'


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=2, max_length=250)

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, min_length=5)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Product does not exist!')
        return product_id

class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=2, max_length=250)
    description = serializers.CharField(required=False, default='No description')
    price = serializers.FloatField(min_value=1)
    category_id = serializers.IntegerField()

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category does not exist!')
        return category_id

    
