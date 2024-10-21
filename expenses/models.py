# expenses/models.py
from django.db import models
from django.core.exceptions import ValidationError

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} ({self.email}) {self.mobile_number}"

class Expense(models.Model):
    SPLIT_METHOD_CHOICES = [
        ('equal', 'Equal'),
        ('exact', 'Exact'),
        ('percentage', 'Percentage'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=10, choices=SPLIT_METHOD_CHOICES)
    split_details = models.JSONField()

    def __str__(self):
        return f"{self.user.name} - {self.total_amount}"

    def validate_split_details(self):
        if self.method == 'equal':
            # No additional validation needed for equal split
            pass
        elif self.method == 'exact':
            # Validate exact split details
            if not isinstance(self.split_details, dict):
                raise ValidationError("Split details for 'exact' method must be a dictionary.")
            total_split = sum(self.split_details.values())
            if total_split != self.total_amount:
                raise ValidationError("The total of exact splits must equal the total amount.")
        elif self.method == 'percentage':
            # Validate percentage split details
            if not isinstance(self.split_details, dict):
                raise ValidationError("Split details for 'percentage' method must be a dictionary.")
            total_percentage = sum(self.split_details.values())
            if total_percentage != 100:
                raise ValidationError("The total percentage must equal 100%.")
