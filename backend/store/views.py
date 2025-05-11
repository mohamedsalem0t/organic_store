from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def search_products(request):
    try:
        query = request.GET.get('q', '')
        logger.info(f"Search query received: {query}")
        
        if not query or len(query.strip()) < 2:
            logger.info("Query too short or empty, returning empty results")
            return Response([], status=status.HTTP_200_OK)
        
        # Search in both name and description
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        ).distinct()[:10]  # Limit to 10 results
        
        logger.info(f"Found {products.count()} products matching query")
        
        if not products.exists():
            logger.info("No products found")
            return Response([], status=status.HTTP_200_OK)
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error in search_products: {str(e)}")
        return Response(
            {"detail": "An error occurred while searching"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'detail': 'Username and password are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'message': 'Login successful!'
        })
    else:
        return Response(
            {'detail': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        ) 