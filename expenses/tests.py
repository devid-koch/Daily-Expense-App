from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

class ExpenseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
    response = self.client.post('/api/users/', {
        'email': 'testuser@example.com',
        'name': 'Test User',
        'mobile': '1234567890'
    }, format='json')
    
    print(response.data)  # Add this line for debugging
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_add_equal_expense(self):
        response = self.client.post('/api/expenses/', {
            'description': 'Dinner',
            'amount': 1000,
            'split_method': 'equal',
            'participants': [
                {'user': self.user.id, 'amount_owed': 500},
                {'user': self.user.id, 'amount_owed': 500}
            ]
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_percentage_expense_validation(self):
    response = self.client.post('/api/expenses/', {
        'description': 'Party Expense',
        'amount': 1000.00,
        'split_method': 'percentage',
        'participants': [
            {'user': 1, 'percentage': 50},
            {'user': 2, 'percentage': 25},
            {'user': 3, 'percentage': 25}
        ]
    }, format='json')
    
    print(response.data)  # Add this line for debugging
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Update this based on the actual response structure
    self.assertIn('non_field_errors', response.data)  # Check if key exists first
    self.assertIn('The total percentage split must add up to 100%', response.data['non_field_errors'])

