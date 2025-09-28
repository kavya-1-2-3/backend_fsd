from django import http
from django.http import JsonResponse, HttpResponseBadRequest
from website.api.serialization.product_serializer import ProductSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from website.models import Product
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


# GET all products
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def product_list(request):
    print("GET Product list API called")
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# POST to add new product  
@api_view(['POST'])
def product_add(request):
    print("POST Product add API called")
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUT to update product
@api_view(['PUT'])
def product_update(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    print(f"PUT Product update API called for id={id}")
    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DELETE product
@api_view(['DELETE'])
def product_delete(request, id): 
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    print(f"DELETE Product API called for id={id}")
    product.delete()
    return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    data = request.data.copy()
    data["product"] = product.id

    serializer = ReviewSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=request.user, product=product)  # attach logged-in user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

