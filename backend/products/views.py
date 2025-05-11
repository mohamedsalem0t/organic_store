from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Category, Product, Review, CartItem, Order, Payment
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    CartItemSerializer,
    OrderSerializer,
    PaymentSerializer,
    RegisterSerializer,
    LoginSerializer
)


# Model ViewSets
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


# Authentication Views
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User registered successfully",
                "user": {
                    "username": user.username,
                    "email": user.email
                },
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "user": {
                    "username": user.username,
                    "email": user.email
                },
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Order Processing View
@api_view(['POST'])
@permission_classes([AllowAny])
def place_order(request):
    data = request.data
    try:
        name = data.get('name')
        email = data.get('email')
        address = data.get('address')
        items = data.get('items')  # array of {id, quantity, price}

        if not all([name, email, address, items]):
            return Response(
                {'error': 'Missing fields'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create user (or fetch existing one)
        user, created = User.objects.get_or_create(
            username=email,
            defaults={'email': email}
        )

        # Calculate total
        total_price = sum(item['price'] * item['quantity'] for item in items)

        # Create order
        order = Order.objects.create(
            user=user,
            total_price=total_price,
            shipping_address=address
        )

        # Add cart items
        for item in items:
            product = Product.objects.get(id=item['id'])
            cart_item = CartItem.objects.create(
                user=user,
                product=product,
                quantity=item['quantity']
            )
            order.items.add(cart_item)

        # Create payment (simulated)
        Payment.objects.create(
            order=order,
            amount_paid=total_price,
            is_successful=True,
            payment_method='cash'
        )

        return Response(
            {'message': 'Order placed successfully ✅', 'order_id': order.id},
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )