# expenses/urls.py

from django.urls import path
from .views import UserViewSet, ExpenseViewSet, UserRegistrationView, UserLoginView

urlpatterns = [
    path('users/register/', UserRegistrationView.as_view(), name='user-register'),
    path('users/login/', UserLoginView.as_view(), name='user-login'),
    path('users/', UserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
    path('expenses/', ExpenseViewSet.as_view({'post': 'create', 'get': 'list'}), name='expense-list'),
    path('expenses/user/<int:user_id>/', ExpenseViewSet.as_view({'get': 'get_user_expenses'}), name='user-expenses'),
    path('expenses/download-balance-sheet/', ExpenseViewSet.as_view({'get': 'download_balance_sheet'}), name='download-balance-sheet'),
]
