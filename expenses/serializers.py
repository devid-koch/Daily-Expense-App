# expenses/serializers.py
from rest_framework import serializers
from .models import User as UserModel, Expense

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'name', 'mobile_number']

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'user', 'total_amount', 'method', 'split_details']

    def validate(self, data):
        expense = Expense(**data)
        expense.validate_split_details()
        return data

