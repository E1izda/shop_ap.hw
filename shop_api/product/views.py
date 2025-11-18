from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer, CategoryValidateSerializer,
    ProductSerializer, ProductValidateSerializer,
    ReviewSerializer, ReviewValidateSerializer
)


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        category = Category.objects.create(
            name=serializer.validated_data.get('name')
        )

        return Response(CategorySerializer(category).data,
                        status=status.HTTP_201_CREATED)


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        category = self.get_object()
        category.name = serializer.validated_data.get('name')
        category.save()

        return Response(CategorySerializer(category).data,
                        status=status.HTTP_200_OK)



class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            product = Product.objects.create(
                title=serializer.validated_data.get('title'),
                description=serializer.validated_data.get('description'),
                price=serializer.validated_data.get('price'),
                category_id=serializer.validated_data.get('category_id'),
            )

        return Response(ProductSerializer(product).data,
                        status=status.HTTP_201_CREATED)


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        product = self.get_object()

        with transaction.atomic():
            product.title = serializer.validated_data.get('title')
            product.description = serializer.validated_data.get('description')
            product.price = serializer.validated_data.get('price')
            product.category_id = serializer.validated_data.get('category_id')
            product.save()

        return Response(ProductSerializer(product).data,
                        status=status.HTTP_200_OK)



class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            review = Review.objects.create(
                text=serializer.validated_data.get('text'),
                stars=serializer.validated_data.get('stars'),
                product_id=serializer.validated_data.get('product_id'),
            )

        return Response(ReviewSerializer(review).data,
                        status=status.HTTP_201_CREATED)


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        review = self.get_object()

        with transaction.atomic():
            review.text = serializer.validated_data.get('text')
            review.stars = serializer.validated_data.get('stars')
            review.product_id = serializer.validated_data.get('product_id')
            review.save()

        return Response(ReviewSerializer(review).data,
                        status=status.HTTP_200_OK)
