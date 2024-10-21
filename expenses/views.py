# expenses/views.py
from rest_framework import generics
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Expense
from django.db import models
from .serializers import UserSerializer, ExpenseSerializer
import csv
from django.http import HttpResponse
from .utils import validate_input, is_valid_email

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        required_fields = ['email', 'mobile_number']
        is_valid, message = validate_input(required_fields, request.data)

        if not is_valid:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get('email')
        mobile_number = request.data.get('mobile_number')
        user = User.objects.filter(email=email, mobile_number=mobile_number).first()

        if user :
            return Response({'message': f"User logged in successfully, Hi {user.name}"}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_user_expenses(self, request, user_id):
        expenses = Expense.objects.filter(user=user_id)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id', None)
        if user_id:
            queryset = self.queryset.filter(user_id=user_id)
        else:
            queryset = self.queryset.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        

    @action(detail=False, methods=['get'], url_path='overall-expenses')
    def overall_expenses(self, request):
        # Retrieve overall expenses for all users
        overall_expenses = self.queryset.values('user__name').annotate(total_amount=models.Sum('total_amount'))
        return Response(overall_expenses)

    @action(detail=False, methods=['get'], url_path='download-balance-sheet')
    def download_balance_sheet(self, request):
        # Create a CSV response for the balance sheet
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'

        writer = csv.writer(response)
        writer.writerow(['User Name', 'Total Amount'])

        # Fetch overall expenses data
        overall_expenses = self.queryset.values('user__name').annotate(total_amount=models.Sum('total_amount'))

        for expense in overall_expenses:
            writer.writerow([expense['user__name'], expense['total_amount']])

        return response
