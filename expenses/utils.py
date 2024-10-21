from rest_framework import status
from rest_framework.response import Response
import re

def validate_input(required_fields, data):
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"{field} is required"

    return True, "Valid"

def is_valid_email(email):
    
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None
